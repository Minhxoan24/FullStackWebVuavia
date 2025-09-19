// src/Components/Product/ProductCard.jsx
import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./ProductCard.css";
import Button from "../Buttons/ButtonBuy.jsx";
import ModalPurchaseTypeProduct from "../Modal/ModalPurchase/ModalPurchase.jsx";
import { useNavigate } from "react-router-dom";

const ProductCard = ({ product }) => {
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);

    const handleBuyClick = (e) => {
        // Ngăn click lan lên card (không điều hướng)
        e.stopPropagation();
        setShowModal(true);
    };

    const handleCloseModal = () => setShowModal(false);

    const handleViewDetails = () => {
        navigate(`/detail-type-product/${product?.id}`);
    };

    // ---- Parse description linh hoạt (string hoặc object) ----
    let descriptionData = {};
    if (product?.description) {
        if (typeof product.description === "string") {
            try {
                descriptionData = JSON.parse(product.description);
            } catch (e) {
                console.error("Description parse error:", e);
                descriptionData = {};
            }
        } else if (typeof product.description === "object") {
            descriptionData = product.description;
        }
    }

    // ---- Helper format giá ----
    const formatPrice = (n) =>
        (Number(n) || 0).toLocaleString("vi-VN", { maximumFractionDigits: 0 });

    const isOutOfStock = (product?.quantity ?? 0) <= 0;

    return (
        <>
            <div
                className="card product-card shadow-sm h-100"
                onClick={handleViewDetails}
                role="button"
            >
                {/* Ảnh sản phẩm */}
                <img
                    src={product?.image}
                    className="card-img-top product-image"
                    alt={product?.name || "Product"}
                    onError={(e) => {
                        e.currentTarget.src =
                            "https://via.placeholder.com/600x600?text=No+Image";
                    }}
                />

                {/* Nội dung */}
                <div className="card-body text-center">
                    <h5 className="card-title fw-bold mb-2">
                        {product?.name ?? "Sản phẩm"}
                    </h5>

                    {/* <p className="text-success small mb-2">
                        Còn sẵn: <b>{product?.quantity ?? 0}</b> sản phẩm
                    </p> */}

                    {/* Giá */}
                    <div className="mb-3">
                        <span className="text-danger fw-bold fs-5">
                            {formatPrice(product?.price)} ₫
                        </span>
                    </div>

                    {/* Hover mô tả (nếu có) */}
                    {descriptionData && Object.keys(descriptionData).length > 0 && (
                        <div className="card-hover">
                            <ul className="text-start small mb-3">
                                {Object.entries(descriptionData).map(([key, value]) => (
                                    <li key={key}>
                                        <strong>{key}:</strong>{" "}
                                        {typeof value === "object" ? JSON.stringify(value) : value}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Button Mua — chặn bubble để không điều hướng */}
                    <Button
                        text={isOutOfStock ? "HẾT HÀNG" : "MUA TÀI KHOẢN"}
                        onClick={handleBuyClick}
                        disabled={isOutOfStock}
                    />
                </div>
            </div>

            {/* Modal Purchase */}
            <ModalPurchaseTypeProduct
                show={showModal}
                onClose={handleCloseModal}
                id={product?.id}
            />
        </>
    );
};

export default ProductCard;
