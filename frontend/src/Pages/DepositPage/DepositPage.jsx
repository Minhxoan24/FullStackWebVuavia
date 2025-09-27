import './DepositPage.css';
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../Context/AuthContext';
import ApiDeposit from '../../Services/ApiDeposit'; // Thêm checkDepositStatus

const DepositPage = () => {
    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    // Danh sách mệnh giá (có thể fetch từ API nếu cần)
    const [options] = useState([
        { id: 1, price: 10000 },
        { id: 2, price: 20000 },
        { id: 3, price: 30000 },
        { id: 4, price: 50000 },
        { id: 5, price: 100000 },
        { id: 6, price: 200000 },
        { id: 7, price: 500000 },
    ]);

    const [selectedId, setSelectedId] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [depositInfo, setDepositInfo] = useState(null); // Khi có -> hiển thị màn QR

    const selected = options.find(o => o.id === selectedId);
    const method = 'Chuyển khoản ngân hàng';
    const username = user?.accountname || 'Chưa đăng nhập';

    const formatVND = (n) =>
        new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(n);

    const handlePay = async () => {
        if (!selected) return;
        try {
            setLoading(true);
            setError('');
            const data = await ApiDeposit.createDeposit({ amount: selected.price });
            // data cần trả về: { qr_code_url, transaction_code, bank_info: {account, name, bank} }
            setDepositInfo(data);
            // Option: scroll đến QR
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 0);
        } catch (e) {
            setError(e?.message || 'Có lỗi xảy ra, vui lòng thử lại.');
        } finally {
            setLoading(false);
        }
    };

    const resetToChoose = () => {
        setDepositInfo(null);
        setLoading(false);
        setError('');
    };

    return (
        <>
            {/* HEADER – thanh màu cam trên cùng */}
            <div className="topup-hero  py-4 mb-4">
                <div className="container">
                    <div className="topup-hero__inner">
                        <span className="topup-hero__title">Nạp tiền</span>
                    </div>
                </div>
            </div>

            <div className="container py-4 topup-page">
                {/* Nếu chưa tạo giao dịch -> hiển thị 2 cột */}
                {!depositInfo ? (
                    <div className="row g-4">
                        {/* LEFT: Chọn mệnh giá */}
                        <div className="col-lg-5">
                            <div className="card shadow-sm h-100">
                                <div className="card-header bg-white border-0 pt-3 pb-0">
                                    <h5 className="mb-3 fw-semibold">QR Pay</h5>
                                    <div className="text-muted small">Chọn mệnh giá</div>
                                </div>
                                <div className="card-body">
                                    <div className="list-group list-group-flush">
                                        {options.map(opt => {
                                            const active = selectedId === opt.id;
                                            return (
                                                <label
                                                    key={opt.id}
                                                    className={
                                                        'list-group-item d-flex align-items-center justify-content-between pointer ' +
                                                        (active ? 'list-group-item-action active-like' : 'list-group-item-action')
                                                    }
                                                    onClick={() => setSelectedId(opt.id)}
                                                >
                                                    <div className="d-flex align-items-center gap-3">
                                                        <input
                                                            type="radio"
                                                            className="form-check-input m-0"
                                                            name="price"
                                                            checked={active}
                                                            onChange={() => setSelectedId(opt.id)}
                                                            onClick={(e) => e.stopPropagation()}
                                                        />
                                                        <span className="fw-500">{formatVND(opt.price)}</span>
                                                    </div>
                                                </label>
                                            );
                                        })}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* RIGHT: Chi tiết + nút xử lý */}
                        <div className="col-lg-7">
                            <div className="card shadow-sm h-100">
                                <div className="card-header bg-white border-0 pt-3">
                                    <h5 className="mb-0 fw-semibold">Chi tiết giao dịch</h5>
                                </div>
                                <div className="card-body">
                                    <div className="d-flex justify-content-between py-2 border-bottom">
                                        <span className="text-muted">Sản phẩm được chọn</span>
                                        <span className="fw-semibold">
                                            {selected ? formatVND(selected.price) : 'Chưa chọn'}
                                        </span>
                                    </div>
                                    <div className="d-flex justify-content-between py-2 border-bottom">
                                        <span className="text-muted">Phương thức thanh toán</span>
                                        <span className="fw-semibold">{method}</span>
                                    </div>
                                    <div className="d-flex justify-content-between py-2">
                                        <span className="text-muted">Tên tài khoản</span>
                                        <span className="fw-semibold">{username}</span>
                                    </div>

                                    <button
                                        className="btn btn-danger w-100 mt-3 py-2 fw-semibold"
                                        disabled={!selected || loading}
                                        onClick={handlePay}
                                    >
                                        {loading ? 'Đang xử lý...' : 'Xử lý thanh toán'}
                                    </button>

                                    {!selected && (
                                        <div className="form-text mt-2">
                                            Hãy chọn một mệnh giá để tiếp tục.
                                        </div>
                                    )}
                                    {error && <p className="text-danger mt-2">{error}</p>}
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    // ĐÃ TẠO GIAO DỊCH: hiển thị màn QR full-width
                    <div className="row">
                        <div className="col-12">
                            <div className="card shadow-sm">
                                <div className="card-body text-center qr-wrap">
                                    <h6 className="qr-title">
                                        Quét mã QR dưới đây bằng ứng dụng Internet Banking để thanh toán
                                    </h6>

                                    <img
                                        className="qr-img"
                                        src={depositInfo.qr_code_url}
                                        alt="QR Code"
                                    />

                                    <div className="qr-note text-muted">
                                        Lưu ý: Mã QR này sẽ hết hạn sau 24 giờ kể từ lúc tạo
                                    </div>

                                    <div className="qr-order text-muted">
                                        Số hoá đơn: <span>{depositInfo.transaction_code}</span>
                                    </div>

                                    <div className="qr-tip text-muted">
                                        Sau khi thanh toán, nhấp vào nút bên dưới
                                    </div>

                                    <button
                                        className="btn btn-lg qr-done-btn"
                                        onClick={async () => {
                                            try {
                                                const statusData = await ApiDeposit.checkDepositStatus(depositInfo.transaction_code);
                                                if (statusData.status === 'COMPLETED') {
                                                    alert('Thanh toán thành công!');
                                                    navigate('/'); // Hoặc '/deposit/success'
                                                } else {
                                                    alert('Chưa nhận được thanh toán. Vui lòng thử lại sau.');
                                                }
                                            } catch (e) {
                                                alert('Lỗi kiểm tra trạng thái. Vui lòng thử lại.');
                                            }
                                        }}
                                    >
                                        Tôi đã hoàn tất thanh toán trên App
                                    </button>

                                    <button className="btn btn-link mt-2" onClick={resetToChoose}>
                                        ← Chọn lại mệnh giá
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
};

export default DepositPage;
