import React from "react";

export default function PriceBlock({ price }) {
    const fmt = (v) =>
        (v ?? 0).toLocaleString("vi-VN", { maximumFractionDigits: 0 }) + " ₫";

    return (
        <div className="mb-3">
            <div className="fs-3 fw-bold text-dark">{fmt(price)}</div>
        </div>
    );
}
