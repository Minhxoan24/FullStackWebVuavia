import { AuthContext } from '../../Context/AuthContext';
import './ChangeInformationAccount.css';
import Button from '../../Components/Buttons/ButtonBuy';

const ChangeInformationAccount = () => {
    return (
        <div className="change-info-container">
            <div className="text-content">
                <form>
                    <div className='nameinformation'>
                        <div>
                            <label>Họ</label>
                            <input type="text" defaultValue={AuthContext.user.surename} />
                        </div>
                        <div>
                            <label>Tên</label>
                            <input type="text" defaultValue={AuthContext.user.name} />
                        </div>
                    </div>
                    <div>
                        <label>Tên Hiển Thị</label>
                        <input type="text" defaultValue={AuthContext.user.surname + " " + AuthContext.user.name} />
                    </div>
                    <div>
                        <label>Địa Chỉ Email</label>
                        <input type="email" defaultValue={AuthContext.user.email} />
                    </div>
                    <h3>Thay đổi mật khẩu</h3>
                    <div>
                        <label>Mật Khẩu Hiện Tại</label>
                        <input type="password" placeholder='Nhập mật khẩu hiện tại' />
                    </div>
                    <div>
                        <label>Mật Khẩu Mới</label>
                        <input type="password" placeholder='Nhập mật khẩu mới' />
                    </div>
                    <div>
                        <label>Xác Nhận Mật Khẩu Mới</label>
                        <input type="password" placeholder='Xác nhận mật khẩu mới' />
                    </div>
                </form>
                <Button className='save-changes-button'>Lưu Thay Đổi</Button>

            </div>
        </div>

    );
}
export default ChangeInformationAccount;