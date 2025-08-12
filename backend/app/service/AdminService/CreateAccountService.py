from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select , insert
from app.models.Users import User
from app.models.Roles import Role, RoleEnum
from app.models.UserRole import user_roles  # Import bảng trung gian dạng Table
from app.schemas.AccountSchema.AccountRegisterSchema import AccountRegisterSchema, MessegeRegister
from app.Utils.HashPassword import hash_password

async def CreateAccountAdmin( account : AccountRegisterSchema, db: AsyncSession, role_name: RoleEnum = RoleEnum.ADMIN):
    """
    Dịch vụ tạo tài khoản quản trị viên
    """
    query_email = select(User).where(User.email == account.email)
    query_phone = select(User).where(User.phone == account.phone)
    query_accountname = select(User).where(User.accountname == account.accountname)
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
        raise HTTPException(status_code=400, detail="Account name already exists")
    # Mã hóa mật khẩu
    password = hash_password(account.password)
    # Tạo người dùng mới
    new_user = User(
        name=account.name,
        surname=account.surname,
        accountname=account.accountname,
        email=account.email,
        phone=account.phone,
        password=password,  # Lưu mật khẩu đã mã hóa
        status=User.StatusUserEnum.ACTIVE  # Mặc định trạng thái là ACTIVE
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
            raise HTTPException(status_code=400, detail="Role does not exist")

        # Gán vai trò cho người dùng thông qua bảng user_roles
        await db.execute(
            insert(user_roles).values(user_id=new_user.id, role_id=role.id)
        )

        await db.commit()  # Commit các thay đổi

    except Exception as e:
        await db.rollback()  # Rollback nếu có lỗi xảy ra
        raise HTTPException(status_code=500, detail=str(e))
    return MessegeRegister(message="Account created successfully", accountname=new_user.accountname)
