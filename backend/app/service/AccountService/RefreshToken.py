from fastapi import HTTPException, Depends
from app.core.JWT import create_access_token, verify_refresh_token

async def create_new_access_token(refresh_token: str):
    try:

        # Verify the refresh token
        user = verify_refresh_token(refresh_token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # Create a new access token
        access_token = create_access_token(user_id=user)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        