import React, { useEffect, useMemo, useState } from "react";
import { Spinner } from "react-bootstrap";
import "./TransactionHistory.css";
// Nếu bạn đã có service, đổi tên dưới đây cho khớp:
import { GetTransactionHistory } from "../../Services/ApiUserService.jsx";

const fmtDateTime = (iso) => {
    try {
        const d = new Date(iso);
        const date = d.toLocaleDateString("vi-VN", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
        });
        const time = d
            .toLocaleTimeString("vi-VN", { hour12: false })
            .replace(/\.\d+$/, ""); // bỏ mili giây nếu có
        return `${date} ${time}`;
    } catch {
        return "-";
    }
};

const fmtMoneySigned = (n) => {
    const x = Number(n) || 0;
    const sign = x > 0 ? "+" : x < 0 ? "-" : "";
    const abs = Math.abs(x).toLocaleString("vi-VN", { maximumFractionDigits: 0 });
    return `${sign}${abs}`;
};

const amountClass = (n) => (n > 0 ? "amount-positive" : n < 0 ? "amount-negative" : "");

const TransactionHistory = () => {
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState("");

    useEffect(() => {
        (async () => {
            setLoading(true);
            setErr("");
            try {
                const data = await GetTransactionHistory(); // ← thay bằng API thực của bạn
                setRows(Array.isArray(data) ? data : []);
            } catch (e) {
                setErr("Không tải được lịch sử giao dịch.");
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    const hasData = useMemo(() => (rows?.length ?? 0) > 0, [rows]);

    return (
        <div className="container py-4">
            {/* Header bar */}
            <div className="history-title d-flex align-items-center px-3 py-2 mb-3">
                <span className="me-2">↩</span>
                <strong>Lịch sử giao dịch</strong>
            </div>

            {loading && (
                <div className="d-flex align-items-center gap-2">
                    <Spinner animation="border" size="sm" />
                    <span>Đang tải…</span>
                </div>
            )}

            {err && !loading && <div className="alert alert-danger">{err}</div>}

            {!loading && !err && !hasData && (
                <div className="text-muted">Chưa có giao dịch nào.</div>
            )}

            {!loading && !err && hasData && (
                <div className="tx-table-wrapper">
                    <table className="table align-middle tx-table">
                        <thead>
                            <tr>
                                <th className="small text-secondary">#</th>
                                <th className="small text-secondary">SỐ TIỀN</th>
                                <th className="small text-secondary">NỘI DUNG</th>
                                <th className="small text-secondary">THỜI GIAN</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows.map((r) => (
                                <tr key={r.id}>
                                    <td className="text-secondary">#{r.id}</td>
                                    <td className={`fw-bold ${amountClass(r.amount)}`}>
                                        {fmtMoneySigned(r.amount)}
                                    </td>
                                    <td className="tx-desc">
                                        {r.description}
                                        {r.order_id ? (
                                            <>
                                                {" "}
                                                - <span className="tx-link">Đơn hàng #{r.order_id}</span>
                                            </>
                                        ) : null}
                                    </td>
                                    <td className="text-secondary">{fmtDateTime(r.created_at)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
export default TransactionHistory;