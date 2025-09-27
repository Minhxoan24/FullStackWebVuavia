from fastapi import APIRouter

# Deprecated: endpoints moved under /Account/forgot-password
router = APIRouter(prefix="/forgot-password", tags=["ForgotPassword"])  # kept for backward compatibility, no routes
