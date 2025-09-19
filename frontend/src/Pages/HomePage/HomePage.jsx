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

    const [dataCategories, setDataCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                const data = await getAllProductswithcategory();
                setDataCategories(data);
                console.log("Danh mục và sản phẩm đã tải:", data);
            } catch (error) {
                console.error("Lỗi khi tải sản phẩm:", error);
                setError("Không thể tải dữ liệu. Vui lòng thử lại sau.");
            } finally {
                setLoading(false);
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

                {/* Content + Product */}
                <div className="content-section container">
                    {loading ? (
                        <div className="text-center py-5">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Đang tải...</span>
                            </div>
                            <p className="mt-2">Đang tải sản phẩm...</p>
                        </div>
                    ) : error ? (
                        <div className="alert alert-danger text-center" role="alert">
                            {error}
                        </div>
                    ) : dataCategories && dataCategories.length > 0 ? (
                        dataCategories.map((category) => (
                            <div key={category.id} className="category-section mb-5">
                                {/* Tiêu đề danh mục với số lượng sản phẩm */}
                                <h2 className="category-title fw-bold text-left mb-3">
                                    {category.name}
                                    {/* <span className="badge bg-primary ms-2">
                                        {category.type_products?.length || 0} sản phẩm
                                    </span> */}
                                </h2>
                                <hr style={{ border: "2px solid #F39C12", width: "100%", margin: "0 auto 30px auto" }} />

                                {/* Danh sách sản phẩm trong danh mục */}
                                <div className="row row-cols-1 row-cols-md-4 g-3">
                                    {category.type_products && category.type_products.length > 0 ? (
                                        category.type_products.map((product) => (
                                            <div key={product.id} className="col d-flex justify-content-center">
                                                <ProductCard product={product} />
                                            </div>
                                        ))
                                    ) : (
                                        <div className="col-12 text-center">
                                            <p className="text-muted">Không có sản phẩm nào trong danh mục này.</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="col-12 text-center py-5">
                            <p className="text-muted">Không có danh mục nào.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default HomePage;