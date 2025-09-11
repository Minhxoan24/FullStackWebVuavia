from fastapi import HTTPException, Depends
from app.core.auth import get_current_user
from app.models.Users import User
from app.models.Roles import RoleEnum

def require_admin_role(current_user: User = Depends(get_current_user)) -> User:
    """Kiểm tra user có role ADMIN không"""
    try:
        # Lấy roles của user
        user_roles = [role.name for role in current_user.roles] if current_user.roles else []
        
        # Kiểm tra có role ADMIN không (chỉ có USER và ADMIN)
        if RoleEnum.ADMIN not in user_roles:
            raise HTTPException(
                status_code=403, 
                detail="Access denied. Admin privileges required."
            )
        
        return current_user
        
    except AttributeError:
        # Trường hợp roles không load được
        raise HTTPException(
            status_code=500,
            detail="Error checking user permissions"
        )
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Unable to verify admin privileges."
        )

# Alias để dễ sử dụng trong các endpoint
def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Lấy admin user hiện tại - alias cho require_admin_role"""
    return require_admin_role(current_user)

def require_user_role(current_user: User = Depends(get_current_user)) -> User:
    """Kiểm tra user có role USER không (chỉ để hoàn thiện, thực tế ít dùng)"""
    try:
        user_roles = [role.name for role in current_user.roles] if current_user.roles else []
        
        if RoleEnum.USER not in user_roles and RoleEnum.ADMIN not in user_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Valid user role required."
            )
        
        return current_user
        
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Unable to verify user privileges."
        )