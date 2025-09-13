import React, { useState, useEffect } from "react";
import "./HomePage.css";
import Logo from "../../Assets/Logo/Logo.jsx";
import { NavLink } from "react-router-dom";
import ProductCard from "../../Components/Card/ProductCard.jsx";
import { getAllProductswithcategory } from "../../Services/ApiTypeProduct.jsx";

const HomePage = () => {
    // Danh sách bài viết sidebar
    const latestPosts = [
        {
            id: 1,
            title: "Hướng Dẫn Cài Proxy Cho Telegram Miễn Phí - Truy Cập Nhanh, Bỏ Chặn Dễ Dàng",
            image: Logo.share1,
            navlink: "/proxy-tutorial",
        },
        {
            id: 2,
            title: "Các tips và chiến lược để tối ưu hóa việc đăng bài Facebook theo khung giờ.",
            image: Logo.share2,
            navlink: "/tips",
        },
        {
            id: 3,
            title: "Mẹo để sử dụng Facebook Lead Ads thu thập thông tin khách hàng tiềm năng",
            image: Logo.share3,
            navlink: "tip-create-ads",
        },
        {
            id: 4,
            title: "Mẹo tạo quảng cáo story trên facebook hiệu quả và thu hút người xem",
            image: Logo.share4,
            navlink: "/tip-use-face",
        },
    ];

    const [dataTypeProduct, setDataTypeProduct] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getAllProductswithcategory();
                setDataTypeProduct(data);
                console.log("Sản phẩm đã tải:", data);
            } catch (error) {
                console.error("Lỗi khi tải sản phẩm:", error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="homepage">
            <div className="container">
                {/* Banner và sidebar */}
                <div className="row g-2 mb-4">
                    <div className="col-md-8">
                        <div className="banner-image">
                            <img
                                src={Logo.Banner}
                                alt="Vuavia Banner"
                                className="img-fluid rounded shadow"
                            />
                        </div>
                    </div>

                    <div className="col-md-4">
                        <div className="sidebar-container shadow-sm rounded">
                            <div className="sidebar-header d-flex align-items-center">
                                <span className="dropdown-icon">▼</span>
                                <span className="sidebar-title ms-2">CHIA SẺ MỚI NHẤT !</span>
                            </div>
                            <div className="sidebar-posts">
                                {latestPosts.map((post) => (
                                    <div key={post.id} className="post-item d-flex mb-2">
                                        <div className="post-thumbnail me-2">
                                            <img
                                                src={post.image}
                                                alt={post.title}
                                                className="rounded"
                                            />
                                        </div>
                                        <div className="post-info">
                                            <h6 className="post-title mb-0">
                                                <NavLink to={post.navlink}>{post.title}</NavLink>
                                            </h6>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Danh mục sản phẩm */}
                <div className="ContainerProduct">
                    {dataTypeProduct.map((category) => (
                        <div key={category.id} className="mb-5">
                            <h4 className="category-title fw-bold" style={{ textAlign: "left" }}>
                                {category.name}
                            </h4>
                            <hr style={{ border: "2px solid #F39C12", width: "100%", marginLeft: 0 }} />
                            <div className="row row-cols-1 row-cols-md-4 g-3 mt-2 px-2">
                                {category.type_products.map((product) => (
                                    <div key={product.id} className="col">
                                        <ProductCard product={product} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default HomePage;