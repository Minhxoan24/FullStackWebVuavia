from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, insert
from app.models.Users import User, StatusUserEnum
from app.models.Roles import Role, RoleEnum
from app.models.UserRole import user_roles  
from app.schemas.AccountSchema.AccountRegisterSchema import  CreateUserRegisterSchema , MessegeRegisterSchema
from app.Utils.HashPassword import hash_password

async def RegisterAccountService(new_account: CreateUserRegisterSchema, db: AsyncSession, role_name: RoleEnum = RoleEnum.USER):
    """
    Dịch vụ đăng ký tài khoản người dùng mới
    """
    # Kiểm tra trùng lặp email, phone, accountname
    query_email = select(User).where(User.email == new_account.email)
    query_phone = select(User).where(User.phone == new_account.phone)
    query_accountname = select(User).where(User.accountname == new_account.accountname)

    result_email = await db.execute(query_email)
    result_phone = await db.execute(query_phone)
    result_accountname = await db.execute(query_accountname)
    
    user_email = result_email.scalar_one_or_none()
    user_phone = result_phone.scalar_one_or_none()
    user_accountname = result_accountname.scalar_one_or_none()

    if user_email is not None:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    if user_phone is not None:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    if user_accountname is not None:
        raise HTTPException(status_code=400, detail="Accountname already exists")

    # Mã hóa mật khẩu
    password = hash_password(new_account.password)

    # Tạo người dùng mới
    new_user = User(
        name=new_account.name,
        surname=new_account.surname,
        accountname=new_account.accountname,
        email=new_account.email,
        phone=new_account.phone,
        password=password,  # Lưu mật khẩu đã mã hóa
        status=StatusUserEnum.ACTIVE  # Mặc định trạng thái là ACTIVE
    )

    try:
        # Thêm người dùng mới vào session
        db.add(new_user)
        await db.flush()  # Lưu tạm để lấy ID của user

        # Kiểm tra vai trò tồn tại
        query = select(Role).where(Role.name == role_name)
        result = await db.execute(query)
        role = result.scalars().first()
        if not role:
            await db.rollback()  # Rollback nếu vai trò không tồn tại
            raise HTTPException(status_code=400, detail="Role not found")

        # Gán vai trò cho người dùng thông qua bảng user_roles
        await db.execute(
            insert(user_roles).values(user_id=new_user.id , role_id=role.id)
        )

        await db.commit()  # Commit các thay đổi
        await db.refresh(new_user)  # Lấy dữ liệu mới nhất từ database
        return MessegeRegisterSchema(message="User registered successfully")
    except HTTPException as httpex:
        
        raise httpex  
    except Exception as e:
        await db.rollback()  # Rollback nếu có lỗi
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
  