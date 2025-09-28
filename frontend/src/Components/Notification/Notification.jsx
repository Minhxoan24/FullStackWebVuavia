import React, { useEffect } from "react";
import { FaCheckCircle, FaExclamationTriangle, FaTimes } from "react-icons/fa";
import "./Notification.css";

const Notification = ({ type, message, onClose, duration = 0 }) => {
    useEffect(() => {
        if (duration > 0 && onClose) {
            const timer = setTimeout(() => {
                onClose();
            }, duration);
            return () => clearTimeout(timer);
        }
    }, [duration, onClose]);

    const getIcon = () => {
        switch (type) {
            case "success":
                return <FaCheckCircle className="notification-icon success" />;
            case "error":
            case "danger":
                return <FaExclamationTriangle className="notification-icon error" />;
            default:
                return <FaExclamationTriangle className="notification-icon" />;
        }
    };

    const getTitle = () => {
        switch (type) {
            case "success":
                return "Thành công";
            case "error":
            case "danger":
                return "Lỗi";
            default:
                return "Thông báo";
        }
    };

    return (
        <div className="notification-overlay">
            <div className="notification-modal">
                <div className="notification-header">
                    {getIcon()}
                    <h5 className="notification-title">{getTitle()}</h5>
                    <button className="notification-close" onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>
                <div className="notification-body">
                    <p className="notification-message">{message}</p>
                </div>
                <div className="notification-footer">
                    <button className="btn btn-primary" onClick={onClose}>
                        Đóng
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Notification;
