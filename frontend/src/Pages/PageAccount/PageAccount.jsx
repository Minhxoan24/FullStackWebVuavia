import React from 'react';
import { Link } from 'react-router-dom';  // Để link đến các trang khác
import './PageAccount.css';  // Import CSS riêng

const PageAccount = () => {
    return (
        <div className="my-account-container">
            {/* Sidebar bên trái */}
            <aside className="sidebar">
                <h2>Menu Tài Khoản</h2>
                <ul className="sidebar-menu">
                    <li><Link to="/account" className="sidebar-link">Trang Tài Khoản</Link></li>
                    <li><Link to="/orders" className="sidebar-link active">Đơn Hàng Của Tôi</Link></li>
                    <li><Link to="/profile" className="sidebar-link">Tài Khoản</Link></li>
                    <li><Link to="/deposit" className="sidebar-link">Nạp Tiền</Link></li>
                    <li><Link to="/transactions" className="sidebar-link">Lịch Sử Giao Dịch</Link></li>
                    <li><Link to="/logout" className="sidebar-link">Đăng Xuất</Link></li>
                </ul>
            </aside>

            {/* Nội dung chính bên phải */}
            <main className="main-content">
                <h1>Trang Đơn Hàng</h1>
                <p>Đây là nơi hiển thị danh sách đơn hàng của bạn.</p>

                {/* Ví dụ nội dung đơn hàng (bạn tự thêm data từ API) */}
                <div className="orders-list">
                    <div className="order-item">
                        <h3>Đơn hàng #12345</h3>
                        <p>Trạng thái: Đang xử lý</p>
                        <p>Tổng tiền: 500.000 đ</p>
                    </div>
                    <div className="order-item">
                        <h3>Đơn hàng #12346</h3>
                        <p>Trạng thái: Hoàn thành</p>
                        <p>Tổng tiền: 300.000 đ</p>
                    </div>
                    {/* Thêm nhiều item từ API */}
                </div>
            </main>
        </div>
    );
};

export default PageAccount;