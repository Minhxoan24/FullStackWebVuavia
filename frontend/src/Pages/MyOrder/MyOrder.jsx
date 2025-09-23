// MyOrder.jsx
import React, { useEffect, useMemo, useState } from "react";
import { Button, Spinner } from "react-bootstrap";
import { getMyOrder } from "../../Services/ApiUserService.jsx";
import { useNavigate } from "react-router-dom";

// Helpers
const fmtDate = (iso) => {
    try {
        const d = new Date(iso);
        return d.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
    } catch {
        return "-";
    }
};
const fmtMoney = (n) =>
    (Number(n) || 0).toLocaleString("vi-VN", { maximumFractionDigits: 0 }) + " đ";
const statusLabel = (s) => {
    const map = {
        COMPLETED: "Đã hoàn thành",
        PAID: "Đã thanh toán",
        PENDING: "Đang xử lý",
        CANCELED: "Đã hủy",
        string: "Đã hoàn thành",
    };
    return map[s] ?? s ?? "-";
};

const MyOrder = ({ onViewOrder }) => {  // Thêm prop onViewOrder
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const onViewOrderHandler = (id) => {  // Đổi tên hàm
        if (onViewOrder) {
            onViewOrder(id);  // Gọi callback từ parent
        } else {
            navigate(`/order-detail/${id}`);  // Fallback nếu không có callback
        }
    };

    useEffect(() => {
        (async () => {
            setLoading(true);
            setError("");
            try {
                // API: [{ order_id, time, quantity, total_amount, order_detail_id, status }]
                const data = await getMyOrder();
                setOrders(Array.isArray(data) ? data : []);
            } catch {
                setError("Failed to fetch orders");
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    const hasData = useMemo(() => (orders?.length ?? 0) > 0, [orders]);

    if (loading) {
        return (
            <div className="d-flex align-items-center gap-2 p-3">
                <Spinner animation="border" size="sm" />
                <span>Đang tải đơn hàng…</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container py-4">
                <div className="alert alert-danger" role="alert">
                    <h4 className="alert-heading">Lỗi!</h4>
                    <p className="mb-3">{error}</p>
                    <button className="btn btn-outline-danger" onClick={() => window.location.reload()}>
                        Thử lại
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="my-order-page container py-4">
            <p className="lead fst-italic mb-2">Kính gửi Quý khách hàng,</p>
            <p className="text-secondary mb-4">
                Để duy trì hiệu suất và bảo mật hệ thống, chúng tôi sẽ tiến hành
                <span className="fw-semibold text-danger"> xóa các dữ liệu đã lưu trữ quá 1 tháng</span>.
                Để tránh mất mát dữ liệu quan trọng, vui lòng sao lưu dữ liệu.
            </p>

            {!hasData ? (
                <div className="text-muted">Chưa có đơn hàng nào.</div>
            ) : (
                <div className="order-table-wrapper">
                    <table className="table align-middle order-table">
                        <thead>
                            <tr>
                                <th className="text-uppercase small fw-bold text-secondary">ĐƠN HÀNG</th>
                                <th className="text-uppercase small fw-bold text-secondary">NGÀY</th>
                                <th className="text-uppercase small fw-bold text-secondary">TÌNH TRẠNG</th>
                                <th className="text-uppercase small fw-bold text-secondary">TỔNG</th>
                                <th className="text-uppercase small fw-bold text-secondary text-end">CÁC THAO TÁC</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map((o) => {
                                const id = o.order_id;
                                const date = fmtDate(o.time);
                                const qty = Number(o.quantity) || 0;
                                const money = fmtMoney(o.total_amount);
                                const stt = statusLabel(o.status);
                                const detailId = o.order_detail_id;

                                return (
                                    <tr key={id}>
                                        <td className="fw-semibold">#{id}</td>
                                        <td>{date}</td>
                                        <td className="text-secondary">{stt}</td>
                                        <td>
                                            <span className="fw-bold">{money}</span>{" "}
                                            <span className="text-secondary small">cho {qty} mục</span>
                                        </td>
                                        <td className="text-end">
                                            <Button
                                                variant="warning"
                                                className="px-3 fw-bold text-white"
                                                onClick={() => onViewOrderHandler(detailId)}  // Sử dụng handler mới
                                                disabled={!detailId}
                                            >
                                                XEM
                                            </Button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default MyOrder;
