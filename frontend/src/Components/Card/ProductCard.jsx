import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./ProductCard.css";
import Button from "../Buttons/ButtonBuy.jsx";

const ProductCard = ({ product }) => {
    let descriptionData = {};
    try {
        descriptionData = product.description
            ? JSON.parse(product.description)
            : {};
    } catch (e) {
        console.error("Description parse error:", e);
    }

    return (
        <div className="card product-card shadow-sm h-100">
            {/* Ảnh sản phẩm */}
            <img
                src={product?.image}
                className="card-img-top product-image"
                alt={product?.name || "Product"}
            />

            {/* Nội dung */}
            <div className="card-body text-center">
                <h5 className="card-title fw-bold mb-2">{product?.name}</h5>

                <p className="text-success small mb-2">
                    Còn sẵn: <b>{product?.quantity ?? 0}</b> sản phẩm
                </p>

                {/* Giá */}
                <div className="mb-3">
                    <span className="text-muted text-decoration-line-through me-2">
                        {(product?.price * 1.2).toLocaleString("vi-VN")} ₫
                    </span>
                    <span className="text-danger fw-bold fs-5">
                        {product?.price?.toLocaleString("vi-VN") || 0} ₫
                    </span>
                </div>

                {/* Hover mô tả */}
                <div className="card-hover">
                    <ul className="text-start small">
                        {Object.entries(descriptionData).map(([key, value]) => (
                            <li key={key}>
                                <strong>{key}:</strong> {value}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Button */}
                <Button
                    text="MUA TÀI KHOẢN"
                    onClick={() => alert("Chức năng đang được phát triển!")}
                />
            </div>
        </div>
    );
};

export default ProductCard;