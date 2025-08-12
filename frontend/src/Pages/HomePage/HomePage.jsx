import React from 'react';
import './HomePage.css';
import Logo from '../../Assets/Logo/Logo.jsx';
import { NavLink } from 'react-router-dom';

const HomePage = () => {
    const latestPosts = [
        {
            id: 1,
            title: "Hướng Dẫn Cài Proxy Cho Telegram Miễn Phí - Truy Cập Nhanh, Bỏ Chặn Dễ Dàng",
            image: Logo.share1,
            navlink: "/proxy-tutorial"

        },
        {
            id: 2,
            title: "Các tips và chiến lược để tối ưu hóa việc đăng bài Facebook theo khung giờ.",
            image: Logo.share2,
            navlink: "/tips"
        },
        {
            id: 3,
            title: "Mẹo để sử dụng Facebook Lead Ads thu thập thông tin khách hàng tiềm năng",
            image: Logo.share3,
            navlink: "tip-create-ads"
        },
        {
            id: 4,
            title: "Mẹo tạo quảng cáo story trên facebook hiệu quả và thu hút người xem",
            image: Logo.share4,
            navlink: "/tip-use-face"
        }
    ];

    return (
        <div className="homepage">
            <div className="container">
                <div className="row g-2">
                    {/* Banner bên trái */}
                    <div className="col-md-8">
                        <div className="banner-image">
                            <img src={Logo.Banner} alt="Vuavia Banner" className="img-fluid" />
                        </div>
                    </div>

                    {/* Sidebar bên phải */}
                    <div className="col-md-4">
                        <div className="sidebar-container">
                            <div className="sidebar-header">
                                <span className="dropdown-icon">▼</span>
                                <span className="sidebar-title">CHIA SẺ MỚI NHẤT !</span>
                            </div>
                            <div className="sidebar-posts">
                                {latestPosts.map((post) => (
                                    <div key={post.id} className="post-item">
                                        <div className="post-thumbnail">
                                            <img src={post.image} alt={post.title} />
                                        </div>
                                        <div className="post-info">
                                            <h3 className="post-title">
                                                <NavLink to={post.navlink}>{post.title}</NavLink>
                                            </h3>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;