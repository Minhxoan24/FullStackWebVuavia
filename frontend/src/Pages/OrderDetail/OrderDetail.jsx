// src/Pages/OrderDetail/OrderDetail.jsx
import React, { useEffect, useMemo, useState } from "react";
import { Spinner } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { getMyOrderDetail } from "../../Services/ApiUserService.jsx";
import "./OrderDetail.css";

// ===== Helpers =====
const fmtDateTime = (iso) => {
    try {
        const d = new Date(iso);
        const date = d.toLocaleDateString("vi-VN", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        });
        const time = d
            .toLocaleTimeString("vi-VN", { hour12: false })
            .replace(/\.\d+$/, "");
        return `${date} ${time}`;
    } catch {
        return "-";
    }
};
const fmtMoney = (n) =>
    (Number(n) || 0).toLocaleString("vi-VN", { maximumFractionDigits: 0 }) +
    " đ";

// map trạng thái -> badge
const statusBadge = (s) => {
    if (!s) return { text: "Không rõ", cls: "bg-secondary" };
    const x = String(s).toLowerCase();
    if (["done", "completed", "đã hoàn thành", "success"].includes(x))
        return { text: "Đã hoàn thành", cls: "bg-success" };
    if (["pending", "đang xử lý", "processing"].includes(x))
        return { text: "Đang xử lý", cls: "bg-warning text-dark" };
    if (["canceled", "cancelled", "đã hủy"].includes(x))
        return { text: "Đã hủy", cls: "bg-danger" };
    return { text: s, cls: "bg-secondary" };
};

const OrderDetail = ({ orderDetailId }) => {  // Thêm prop orderDetailId
    const { orderId } = useParams();
    const id = orderDetailId || (orderId ? Number(orderId) : null);  // Ưu tiên prop, fallback useParams

    const [detail, setDetail] = useState(null);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState("");

    useEffect(() => {
        const fetchOrderDetail = async () => {
            setLoading(true);
            setErr("");
            try {
                const data = await getMyOrderDetail(id);
                setDetail(data);
            } catch (e) {
                const msg =
                    e?.response?.data?.detail ||
                    e?.message ||
                    "Không thể tải chi tiết đơn hàng";
                setErr(msg);
                setDetail(null);
            } finally {
                setLoading(false);
            }
        };

        if (id && !Number.isNaN(id)) fetchOrderDetail();
        else setErr("ID chi tiết đơn hàng không hợp lệ");
    }, [id]);

    // dữ liệu hiển thị “hóa đơn” (phần trên)
    const productLine = useMemo(() => {
        if (!detail) return { name: "-", qty: 0, price: 0 };
        return {
            name: detail?.type_product_name || `Sản phẩm #${detail?.type_product_id}`,
            qty: detail?.quantity ?? 0,
            price: detail?.total_amount ?? 0,
        };
    }, [detail]);

    // ===== Copy helpers =====
    const copyToClipboard = async (text) => {
        try {
            await navigator.clipboard.writeText(text);
        } catch {
            // fallback
            const ta = document.createElement("textarea");
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
        }
    };

    const handleCopyRow = (acc) => {
        // giống ảnh: "email|password"
        const content = `${acc?.login_name || ""}|${acc?.password || ""}`;
        copyToClipboard(content);
    };

    const handleCopyAll = () => {
        if (!detail?.accounts_info?.length) return;
        const all = detail.accounts_info
            .map((a) => `${a?.login_name || ""}|${a?.password || ""}`)
            .join("\n");
        copyToClipboard(all);
    };

    // ===== Render =====
    if (loading) {
        return (
            <div className="d-flex align-items-center gap-2 p-3">
                <Spinner animation="border" size="sm" />
                <span>Đang tải đơn hàng…</span>
            </div>
        );
    }

    if (err) {
        return (
            <div className="container py-4">
                <div className="alert alert-danger" role="alert">
                    <h4 className="alert-heading">Lỗi!</h4>
                    <p className="mb-3">{err}</p>
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

    if (!detail) {
        return (
            <div className="container py-4">
                <div className="alert alert-warning" role="alert">
                    <h4 className="alert-heading">Không tìm thấy đơn hàng</h4>
                    <p className="mb-3">Không có dữ liệu chi tiết cho đơn hàng này.</p>
                </div>
            </div>
        );
    }

    const badge = statusBadge(detail?.status);

    return (
        <div className="container py-4 order-detail-page">
            {/* ===== Header đơn hàng ===== */}
            <div className="order-header card border-0 shadow-sm mb-4">
                <div className="card-body d-flex flex-wrap justify-content-between align-items-center btn btn-warning">
                    <div className="lh-sm ">
                        <div className="small text-muted">
                            Đơn hàng{" "}
                            <span className="fw-semibold">#{detail?.order_id ?? detail?.id}</span>{" "}
                            đã được đặt lúc
                        </div>
                        <div className="fw-semibold">{fmtDateTime(detail?.time)}</div>
                    </div>
                    {/* <span className={`badge px-3 py-2 fs-7 ${badge.cls}`}>
                        {badge.text}
                    </span> */}
                </div>
            </div>

            {/* ===== Chi tiết đơn hàng (hóa đơn) ===== */}
            <div className="summary card border-0 shadow-sm mb-4">
                <div className="card-header bg-white border-0 pt-3 pb-0">
                    <h5 className="card-title fw-bold mb-3">Chi tiết đơn hàng</h5>
                </div>
                <div className="card-body pt-0">
                    <div className="table-responsive">
                        <table className="table align-middle mb-0">
                            <thead className="table-light">
                                <tr>
                                    <th className="text-uppercase small text-muted">Tài khoản</th>
                                    <th className="text-end text-uppercase small text-muted">
                                        Tổng
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>
                                        {productLine.name} × {productLine.qty}
                                    </td>
                                    <td className="text-end">{fmtMoney(productLine.price)}</td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <th className="text-muted">Tổng số phụ:</th>
                                    <td className="text-end">{fmtMoney(productLine.price)}</td>
                                </tr>
                                <tr>
                                    <th className="text-muted">Tổng cộng:</th>
                                    <td className="text-end fw-bold text-success">
                                        {fmtMoney(productLine.price)}
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            </div>

            {/* ===== Danh sách tài khoản ===== */}
            <div className="accounts card border-0 shadow-sm mb-4">
                <div className="card-header bg-white border-0 d-flex justify-content-between align-items-center">
                    <h5 className="fw-bold mb-0">Tài khoản</h5>
                    <button className="btn btn-danger btn-copy-all" onClick={handleCopyAll}>
                        Sao chép toàn bộ
                    </button>
                </div>

                <div className="card-body pt-0">
                    <div className="table-responsive">
                        <table className="table table-bordered align-middle mb-0">
                            <thead className="table-light">
                                <tr>
                                    <th className="text-uppercase small text-muted">Tài khoản</th>
                                    <th className="text-uppercase small text-muted">
                                        Thông tin đăng nhập
                                    </th>
                                    <th style={{ width: 140 }} />
                                </tr>
                            </thead>
                            <tbody>
                                {detail?.accounts_info?.length ? (
                                    detail.accounts_info.map((acc, idx) => (
                                        <tr key={acc?.id ?? idx}>
                                            <td>{productLine.name}</td>
                                            <td className="login-cell">
                                                <span className="mono">
                                                    {acc?.login_name}
                                                    {"|"}
                                                    {acc?.password}
                                                </span>
                                            </td>
                                            <td className="text-end">
                                                <button
                                                    className="btn btn-danger btn-copy"
                                                    onClick={() => handleCopyRow(acc)}
                                                >
                                                    SAO CHÉP
                                                </button>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={3} className="text-center text-muted py-4">
                                            Không có tài khoản nào.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* ===== Địa chỉ thanh toán ===== */}
            <div className="billing card border-0 shadow-sm">
                <div className="card-header bg-white border-0">
                    <h5 className="fw-bold mb-0">Địa chỉ thanh toán</h5>
                </div>
                <div className="card-body pt-0">
                    <p className="mb-1 text-muted">N/A</p>
                    <p className="mb-0">{detail?.billing_email || detail?.email}</p>
                </div>
            </div>
        </div>
    );
};

export default OrderDetail;
