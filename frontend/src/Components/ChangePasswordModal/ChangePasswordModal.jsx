import React, { useState } from "react";
import { Form, Button, Row, Col, InputGroup, Spinner } from "react-bootstrap";
import { FaLock, FaEye, FaEyeSlash, FaTimes } from "react-icons/fa";
import "./ChangePasswordModal.css";

const ChangePasswordModal = ({ show, onHide, onSubmit, loading, errors, onErrorsChange }) => {
    const [form, setForm] = useState({
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
    });

    const [showPasswords, setShowPasswords] = useState({
        current: false,
        new: false,
        confirm: false,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (onErrorsChange && errors[name]) {
            onErrorsChange(prev => ({ ...prev, [name]: "" }));
        }
    };

    const toggleShowPassword = (field) => {
        setShowPasswords(prev => ({ ...prev, [field]: !prev[field] }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await onSubmit(form);
    };

    const handleClose = () => {
        setForm({
            currentPassword: "",
            newPassword: "",
            confirmPassword: "",
        });
        setShowPasswords({
            current: false,
            new: false,
            confirm: false,
        });
        onHide();
    };

    if (!show) return null;

    return (
        <div className="change-password-overlay">
            <div className="change-password-modal">
                <div className="change-password-header">
                    <div className="change-password-title">
                        <FaLock className="title-icon" />
                        <h3>Thay đổi mật khẩu</h3>
                    </div>
                    <button className="close-button" onClick={handleClose}>
                        <FaTimes />
                    </button>
                </div>

                <div className="change-password-body">
                    <Form onSubmit={handleSubmit}>
                        <Row className="g-4">
                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label>Mật khẩu hiện tại</Form.Label>
                                    <InputGroup>
                                        <Form.Control
                                            type={showPasswords.current ? "text" : "password"}
                                            name="currentPassword"
                                            value={form.currentPassword}
                                            onChange={handleChange}
                                            isInvalid={!!errors.currentPassword}
                                            placeholder="Nhập mật khẩu hiện tại"
                                            className="password-input"
                                        />
                                        <Button
                                            variant="outline-secondary"
                                            size="sm"
                                            onClick={() => toggleShowPassword('current')}
                                            className="password-toggle"
                                        >
                                            {showPasswords.current ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                        <Form.Control.Feedback type="invalid">
                                            {errors.currentPassword}
                                        </Form.Control.Feedback>
                                    </InputGroup>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label>Mật khẩu mới</Form.Label>
                                    <InputGroup>
                                        <Form.Control
                                            type={showPasswords.new ? "text" : "password"}
                                            name="newPassword"
                                            value={form.newPassword}
                                            onChange={handleChange}
                                            isInvalid={!!errors.newPassword}
                                            placeholder="Nhập mật khẩu mới (tối thiểu 8 ký tự)"
                                            className="password-input"
                                        />
                                        <Button
                                            variant="outline-secondary"
                                            size="sm"
                                            onClick={() => toggleShowPassword('new')}
                                            className="password-toggle"
                                        >
                                            {showPasswords.new ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                        <Form.Control.Feedback type="invalid">
                                            {errors.newPassword}
                                        </Form.Control.Feedback>
                                    </InputGroup>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label>Xác nhận mật khẩu mới</Form.Label>
                                    <InputGroup>
                                        <Form.Control
                                            type={showPasswords.confirm ? "text" : "password"}
                                            name="confirmPassword"
                                            value={form.confirmPassword}
                                            onChange={handleChange}
                                            isInvalid={!!errors.confirmPassword}
                                            placeholder="Xác nhận mật khẩu mới"
                                            className="password-input"
                                        />
                                        <Button
                                            variant="outline-secondary"
                                            size="sm"
                                            onClick={() => toggleShowPassword('confirm')}
                                            className="password-toggle"
                                        >
                                            {showPasswords.confirm ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                        <Form.Control.Feedback type="invalid">
                                            {errors.confirmPassword}
                                        </Form.Control.Feedback>
                                    </InputGroup>
                                </Form.Group>
                            </Col>
                        </Row>
                    </Form>
                </div>

                <div className="change-password-footer">
                    <Button
                        variant="secondary"
                        onClick={handleClose}
                        className="cancel-button"
                        disabled={loading}
                    >
                        Hủy
                    </Button>
                    <Button
                        type="submit"
                        variant="primary"
                        onClick={handleSubmit}
                        className="submit-button"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <Spinner animation="border" size="sm" className="me-2" />
                                Đang lưu...
                            </>
                        ) : (
                            "Đổi mật khẩu"
                        )}
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default ChangePasswordModal;
