
import { AuthContext } from '../../Context/AuthContext';
import LogoOverView from '../../Assets/Logo/Logo';
import './OverView.css';
const OverView = () => {
    return (
        <div className="overview-container">
            <div className="logo">
                <img src={LogoOverView} alt="Logo OverView" />
            </div>
            <div className="text-content">
                <h5>Vua Via xin kính chào {AuthContext.user.surename + " " + AuthContext.user.name}. </h5>
                <h6>Đây là trang tổng quan của Vuavia.VN</h6>
                <p>Tại đây quý khách có thể xem lịch sử giao dịch, kiểm tra số dư, kiểm tra các đơn đặt hàng của quý khách một cách nhanh chóng! </p>
                <p>Chúc quý khách hàng {AuthContext.user.surename + " " + AuthContext.user.name} luôn gặp nhiều may mắn trong công việc, và có nhiều sức khỏe. Thay mặt đội ngũ QTV Vuavia cảm ơn {AuthContext.user.surename + " " + AuthContext.user.name} đã tin tưởng và sử dụng dịch vụ của chúng tôi</p>
            </div>

        </div>
    );
};

export default OverView;