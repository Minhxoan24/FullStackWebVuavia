from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware để log các request"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Tính thời gian xử lý
        process_time = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {response.status_code} - Time: {process_time:.4f}s")
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware để giới hạn số request (đơn giản)"""
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Cleanup old entries
        self.clients = {
            ip: requests for ip, requests in self.clients.items()
            if any(req_time > current_time - self.period for req_time in requests)
        }
        
        # Check rate limit
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        # Remove old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if req_time > current_time - self.period
        ]
        
        if len(self.clients[client_ip]) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )
        
        # Add current request
        self.clients[client_ip].append(current_time)
        
        response = await call_next(request)
        return response

def setup_cors(app):
    """Cấu hình CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React dev server
            "http://127.0.0.1:3000",
            "https://vuavia.vn",      # Production domain
            "https://www.vuavia.vn"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_middlewares(app):
    """Setup tất cả middleware"""
    # CORS
    setup_cors(app)
    
    # Logging
    app.add_middleware(LoggingMiddleware)
    
    # Rate limiting (có thể bật/tắt)
    # app.add_middleware(RateLimitMiddleware, calls=100, period=60)

async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
