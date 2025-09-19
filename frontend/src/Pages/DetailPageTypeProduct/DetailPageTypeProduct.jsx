// src/Pages/TypeProductDetail/TypeProductDetail.jsx
import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import SpecList from "../../Components/Product/SpecList";
import QuantityInput from "../../Components/Product/QuantityInput";
import Button from "../../Components/Buttons/ButtonBuy";
import { getTypeProductById, getinfortypeproduct } from "../../Services/ApiTypeProduct";
import CreateOrder from "../../Services/OrderService";

const TypeProductDetail = () => {
    const { id } = useParams();

    const [product, setProduct] = useState(null);
    const [infor, setinfor] = useState(null);
    const [qty, setQty] = useState(1);
    const [activeTab, setActiveTab] = useState("desc");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProduct = async () => {
            setLoading(true);
            setError(null);

            try {
                console.log("Fetching product with ID:", id);

                // SỬAẠ: Thêm id parameter
                const data = await getTypeProductById(id);
                console.log("Product data:", data);
                setProduct(data);

                // Fetch information (có thể không có - handle 404 gracefully)
                try {
                    const infor = await getinfortypeproduct(id);
                    console.log("Infor data:", infor);
                    setinfor(infor);
                } catch (inforError) {
                    console.warn("No additional information found for product:", id);
                    setinfor(null);
                }

            } catch (error) {
                console.error("Failed to fetch product:", error);
                setError(error.message || "Có lỗi xảy ra khi tải sản phẩm");
            } finally {
                setLoading(false);
            }
        };

        if (id) {
            fetchProduct();
        }
    }, [id]);

    // Thêm xử lý loading
    if (loading) {
        return (
            <div className="container py-4">
                <div className="text-center">
                    <div className="spinner-border" role="status">
                        <span className="visually-hidden">Đang tải...</span>
                    </div>
                    <p className="mt-2">Đang tải thông tin sản phẩm...</p>
                </div>
            </div>
        );
    }

    // Thêm xử lý error
    if (error) {
        return (
            <div className="container py-4">
                <div className="alert alert-danger" role="alert">
                    <h4 className="alert-heading">Lỗi!</h4>
                    <p>{error}</p>
                    <button
                        className="btn btn-outline-danger"
                        onClick={() => window.location.reload()}
                    >
                        Thử lại
                    </button>
                </div>
            </div>
        );
    }

    // Kiểm tra xem có sản phẩm không
    if (!product) {
        return (
            <div className="container py-4">
                <div className="alert alert-warning" role="alert">
                    Không tìm thấy sản phẩm với ID: {id}
                </div>
            </div>
        );
    }

    // SỬAẠ: Xử lý description từ API response (string JSON)
    let descriptionData = {};
    if (product?.description) {
        try {
            // Backend trả về description dưới dạng string JSON
            descriptionData = typeof product.description === 'string'
                ? JSON.parse(product.description)
                : product.description;
        } catch (e) {
            console.error("Error parsing description:", e);
            descriptionData = {};
        }
    }

    // Xử lý describe data từ backend (JSONB dict) - có thể null
    const describe = infor?.describe || {};

    // Hàm format giá
    const formatPrice = (price) => {
        return new Intl.NumberFormat('vi-VN').format(price);
    };

    // Hàm xử lý mua hàng
    const handleBuy = async (e) => {
        e.preventDefault();
        const orderData = {
            type_product_id: product.id,
            quantity: qty,
        }
        console.log("Order data:", orderData);
        try {
            const result = await CreateOrder(orderData);
            console.log("Order created successfully:", result);
        } catch (error) {
            console.error("Error creating order:", error);
        }
    };

    return (
        <div className="container py-4">
            {/* breadcrumb đơn giản */}
            <nav className="mb-3 small text-muted">
                <span>TRANG CHỦ</span> / <span>SHOP</span>
            </nav>

            {/* ===== HÀNG CHI TIẾT SẢN PHẨM ===== */}
            <div className="row g-4">
                {/* Ảnh */}
                <div className="col-lg-6">
                    <div className="p-3 border rounded-3 bg-white h-100 d-flex align-items-center justify-content-center">
                        <img
                            src={product.image}
                            alt={product.name}
                            className="img-fluid"
                            style={{ maxHeight: 480, objectFit: "contain" }}
                        />
                    </div>
                </div>

                {/* Thông tin */}
                <div className="col-lg-6">
                    <h3 className="fw-bold">{product.name}</h3>
                    <div className="text-success fw-semibold mb-2">
                        Còn sẵn: {product.quantity ?? 0} sản phẩm
                    </div>

                    {/* Giá */}
                    <div className="d-flex align-items-baseline gap-3 mb-3">
                        <span className="fs-3 fw-bold text-danger">
                            {formatPrice(product.price)} đ
                        </span>
                    </div>




                    {/* Thông số kỹ thuật từ product.description */}
                    <SpecList specs={descriptionData} />
                    {/* Số lượng + mua */}
                    <div className="d-flex align-items-center gap-3 my-3">
                        <QuantityInput
                            value={qty}
                            min={1}
                            max={product.quantity ?? 1}
                            onChange={setQty}
                        />

                    </div>


                    {/* Mã sản phẩm */}
                    <div className="mt-3 mb-3 small text-muted">
                        <div>Mã: HMT{String(product.id).padStart(2, "0")}</div>
                    </div>
                    <Button text="MUA TÀI KHOẢN" onClick={handleBuy} />
                </div>
            </div>

            {/* ===== HỘP MÔ TẢ Ở DƯỚI CHI TIẾT ===== */}
            <div className="mt-5">
                {/* Tabs (Bootstrap) */}
                <ul className="nav nav-tabs">
                    <li className="nav-item">
                        <button
                            className={`nav-link ${activeTab === "desc" ? "active" : ""}`}
                            onClick={() => setActiveTab("desc")}
                            type="button"
                        >
                            Mô tả
                        </button>
                    </li>
                    <li className="nav-item">
                        <button
                            className={`nav-link ${activeTab === "review" ? "active" : ""}`}
                            onClick={() => setActiveTab("review")}
                            type="button"
                        >
                            Đánh giá (0)
                        </button>
                    </li>
                </ul>

                {/* Nội dung tab */}
                <div className="border border-top-0 rounded-bottom p-4 bg-white">
                    {activeTab === "desc" && (
                        <div>
                            <h4 className="fw-bold mb-4 text-primary">
                                Thông tin chi tiết sản phẩm
                            </h4>
                            {describe && Object.keys(describe).length > 0 ? (
                                <div style={{ lineHeight: 1.7 }}>
                                    {/* Hiển thị nội dung từ describe object với styling tốt hơn */}
                                    {Object.entries(describe).map(([key, value], index) => (
                                        <div key={key} className="mb-4">
                                            <h5 className="fw-bold text-dark mb-3" style={{ color: '#2c3e50' }}>
                                                {index + 1}. {key}
                                            </h5>
                                            <div
                                                className="text-muted"
                                                style={{
                                                    whiteSpace: "pre-line",
                                                    marginLeft: "1rem",
                                                    fontSize: "0.95rem",
                                                    lineHeight: "1.8"
                                                }}
                                                dangerouslySetInnerHTML={{
                                                    __html: typeof value === 'string' ? value.replace(/\n/g, '<br/>') : JSON.stringify(value)
                                                }}
                                            />
                                            {index < Object.keys(describe).length - 1 && (
                                                <hr className="my-4" style={{ borderColor: '#ecf0f1' }} />
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-muted text-center py-4">
                                    <p className="fst-italic mb-2">
                                        Chưa có mô tả chi tiết cho sản phẩm này.
                                    </p>
                                    {!infor && (
                                        <small className="text-warning">
                                            * Thông tin bổ sung chưa được cập nhật trong hệ thống
                                        </small>
                                    )}
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === "review" && (
                        <div className="text-muted text-center py-4">
                            <p className="fst-italic mb-2">
                                Chưa có đánh giá nào. Hãy là người đầu tiên đánh giá sản phẩm này!
                            </p>
                            {/* TODO: chèn form/DS đánh giá tại đây */}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default TypeProductDetail;
