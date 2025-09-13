
import { AuthContext } from '../../Context/AuthContext';
import Logo from '../../Assets/Logo/Logo.jsx';
import './OverView.css';
import { useContext } from 'react';

const OverView = () => {
    const { user } = useContext(AuthContext);
    return (
        <div className="overview-container">
            <div className="logo">
                <img src={Logo.LogoOverView} alt="Logo OverView" />
            </div>
            <div className="text-content">
                <h5>Vua Via xin kính chào <strong>{user.surname + " " + user.name}</strong>.</h5> <br />
                <h6>Đây là trang tổng quan của Vuavia.VN</h6><br />
                <p><i> Tại đây quý khách có thể xem lịch sử giao dịch, kiểm tra số dư, kiểm tra các đơn đặt hàng của quý khách một cách nhanh chóng! </i></p>
                <p><i> Chúc quý khách hàng <strong>{user.surname + " " + user.name}</strong> luôn gặp nhiều may mắn trong công việc, và có nhiều sức khỏe. Thay mặt đội ngũ QTV Vuavia cảm ơn <strong>{user.surname + " " + user.name}</strong> đã tin tưởng và sử dụng dịch vụ của chúng tôi</i></p>
            </div>

        </div>
    );
};

export default OverView; 