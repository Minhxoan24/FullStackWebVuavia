import React from "react";
import "./ConfirmModal.css";

const ConfirmPurchaseModal = ({ show, onConfirm, onClose }) => {
    if (!show) return null;

    const handleBackdropClick = (e) => {
        if (e.target === e.currentTarget) onClose();
    };

    return (
        <div className="modal-backdrop-custom" onClick={handleBackdropClick}>
            <div className="modal-dialog modal-lg modal-dialog-centered">
                <div className="modal-content custom-modal">
                    <div className="confirm-body text-center py-4">
                        <div className="warning-icon mx-auto mb-3">!</div>
                        <h5 className="mb-4 fw-semibold text-secondary-emphasis">
                            Bạn chắc chắn muốn mua sản phẩm này
                        </h5>
                        <div className="d-flex gap-3 justify-content-center">
                            <button className="btn btn-primary px-4 fw-semibold" onClick={onConfirm}>
                                ĐỒNG Ý
                            </button>
                            <button className="btn btn-danger px-4 fw-semibold" onClick={onClose}>
                                HỦY BỎ
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConfirmPurchaseModal;
