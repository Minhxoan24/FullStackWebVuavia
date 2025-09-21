import React from "react";
import "./ConfirmModal.css";
import { Modal } from "react-bootstrap";

const ConfirmPurchaseModal = ({ show, onConfirm, onClose }) => {
    if (!show) return null;



    return (
        <Modal
            show={show}
            onHide={onClose}
            centered
            backdrop
            backdropClassName="custom-backdrop"   // nền xám nhẹ
            dialogClassName="confirm-modal"
        >
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
        </Modal>
    );
};
export default ConfirmPurchaseModal;
