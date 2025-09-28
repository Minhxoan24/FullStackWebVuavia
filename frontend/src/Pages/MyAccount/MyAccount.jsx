import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import "./MyAccount.css";
import { AuthContext } from "../../Context/AuthContext";
import { updateProfile, changePassword } from "../../Services/ApiUserService";
import { Form, Button, Row, Col, Spinner } from "react-bootstrap";
import { FaUser, FaEnvelope, FaPhone, FaLock, FaKey, FaCheckCircle } from "react-icons/fa";
import Notification from "../../Components/Notification/Notification";
import ChangePasswordModal from "../../Components/ChangePasswordModal/ChangePasswordModal";
import AvatarDisplay from "../../Components/AvtDisplay/AvtDisplay";  // Thêm import

const EMAIL_RGX = /^\S+@\S+\.\S+$/;
const PHONE_RGX = /^[0-9()+\-.\s]{9,20}$/;

const MyAccount = () => {
    const { user, refreshUser } = useContext(AuthContext);

    const [form, setForm] = useState({
        firstName: user?.name || "",
        lastName: user?.surname || "",
        accountName: user?.accountname || "",
        email: user?.email || "",
        phone: user?.phone || "",
    });

    const [errors, setErrors] = useState({});
    const [saving, setSaving] = useState(false);
    const [alert, setAlert] = useState({ type: "", msg: "" }); // 'success' | 'danger' | ''
    const [showPasswordModal, setShowPasswordModal] = useState(false);

    const onChange = (e) =>
        setForm((s) => ({ ...s, [e.target.name]: e.target.value }));

    const clearAlert = () => setAlert({ type: "", msg: "" });

    const validate = () => {
        const err = {};
        if (!form.firstName.trim()) err.firstName = "Vui lòng nhập Tên.";
        if (!form.lastName.trim()) err.lastName = "Vui lòng nhập Họ.";
        if (!form.accountName.trim()) err.accountName = "Vui lòng nhập Tên tài khoản.";
        if (!EMAIL_RGX.test(form.email.trim())) err.email = "Email không hợp lệ.";
        if (!PHONE_RGX.test(form.phone.trim())) err.phone = "Số điện thoại không hợp lệ.";

        setErrors(err);
        return Object.keys(err).length === 0;
    };

    const validatePassword = (passwordData) => {
        const err = {};
        if (!passwordData.currentPassword) err.currentPassword = "Nhập mật khẩu hiện tại.";
        if (!passwordData.newPassword) err.newPassword = "Nhập mật khẩu mới.";
        if (!passwordData.confirmPassword) err.confirmPassword = "Xác nhận mật khẩu mới.";
        if (passwordData.newPassword && passwordData.newPassword.length < 8)
            err.newPassword = "Mật khẩu mới tối thiểu 8 ký tự.";
        if (
            passwordData.currentPassword &&
            passwordData.newPassword &&
            passwordData.currentPassword === passwordData.newPassword
        )
            err.newPassword = "Mật khẩu mới phải khác mật khẩu hiện tại.";
        if (
            passwordData.newPassword &&
            passwordData.confirmPassword &&
            passwordData.newPassword !== passwordData.confirmPassword
        )
            err.confirmPassword = "Xác nhận mật khẩu phải giống mật khẩu mới.";
        return err;
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        clearAlert();
        if (!validate()) return;

        setSaving(true);
        try {
            await updateProfile({
                name: form.firstName.trim(),
                surname: form.lastName.trim(),
                phone: form.phone.trim(),
            });

            await refreshUser?.();

            setAlert({ type: "success", msg: "Cập nhật thành công!" });
        } catch (error) {
            console.error("Update error:", error);
            setAlert({
                type: "danger",
                msg: error?.message || "Có lỗi xảy ra khi lưu thay đổi.",
            });
        } finally {
            setSaving(false);
        }
    };

    const onChangePassword = async (pwdForm) => {
        const pwErr = validatePassword(pwdForm);
        if (Object.keys(pwErr).length > 0) {
            setErrors(pwErr);
            return;
        }
        setSaving(true);
        try {
            await changePassword({
                currentPassword: pwdForm.currentPassword,
                newPassword: pwdForm.newPassword,
                confirmPassword: pwdForm.confirmPassword,
            });
            setShowPasswordModal(false);
            setTimeout(() => {
                setAlert({ type: "success", msg: "Mật khẩu đã được thay đổi thành công!" });
            }, 250);
        } catch (error) {
            console.error("Change password error:", error);
            setAlert({
                type: "danger",
                msg: error?.message || "Có lỗi xảy ra khi đổi mật khẩu.",
            });
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="account-wrap py-4">
            <div className="container">
                <div className="account-card p-4 p-md-5 mx-auto">
                    {/* Alerts */}
                    {!!alert.type && alert.type === "success" && alert.msg.includes("mật khẩu") && (
                        <Notification type="success" message={alert.msg} onClose={clearAlert} />
                    )}
                    {!!alert.type && alert.type === "success" && !alert.msg.includes("mật khẩu") && (
                        <div className="alert alert-success d-flex align-items-center mb-4" role="alert">
                            <FaCheckCircle className="me-2" />
                            {alert.msg}
                        </div>
                    )}
                    {!!alert.type && alert.type === "danger" && (
                        <Notification type="danger" message={alert.msg} onClose={clearAlert} />
                    )}

                    {/* Form */}
                    {/* Thêm AvatarDisplay ở đầu form */}
                    <div className="text-center mb-4">
                        <AvatarDisplay
                            avatarUrl={user?.avatar || "https://res.cloudinary.com/dkwvlimht/image/upload/v1758401193/bc439871417621836a0eeea768d60944_fvui3e.jpg"}
                            onAvatarUpdated={refreshUser}  // Refresh user sau upload để cập nhật avatar
                        />
                    </div>
                    <Form onSubmit={onSubmit} noValidate>
                        <Row className="g-4">
                            <Col md={6}>
                                <Form.Group>
                                    <Form.Label className="required">
                                        <FaUser className="me-2" />
                                        Tên
                                    </Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="firstName"
                                        value={form.firstName}
                                        onChange={onChange}
                                        isInvalid={!!errors.firstName}
                                        className="form-control-elevated"
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.firstName}
                                    </Form.Control.Feedback>
                                </Form.Group>
                            </Col>

                            <Col md={6}>
                                <Form.Group>
                                    <Form.Label className="required">
                                        <FaUser className="me-2" />
                                        Họ
                                    </Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="lastName"
                                        value={form.lastName}
                                        onChange={onChange}
                                        isInvalid={!!errors.lastName}
                                        className="form-control-elevated"
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.lastName}
                                    </Form.Control.Feedback>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label className="required">
                                        <FaUser className="me-2" />
                                        Tên Tài khoản
                                    </Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="accountName"
                                        value={form.accountName}

                                        isInvalid={!!errors.accountName}
                                        className="form-control-elevated"
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.accountName}
                                    </Form.Control.Feedback>
                                    <Form.Text className="fst-italic mt-1">
                                        Tên này sẽ hiển thị trong trang Tài khoản và phần Đánh giá Tài khoản
                                    </Form.Text>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label className="required">
                                        <FaEnvelope className="me-2" />
                                        Địa chỉ email
                                    </Form.Label>
                                </Form.Group>
                                <Form.Control
                                    type="email"
                                    name="email"
                                    value={form.email}

                                    isInvalid={!!errors.email}
                                    className="form-control-elevated"
                                    required
                                />
                                <Form.Control.Feedback type="invalid">
                                    {errors.email}
                                </Form.Control.Feedback>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label className="required">
                                        <FaPhone className="me-2" />
                                        Số điện thoại
                                    </Form.Label>
                                    <Form.Control
                                        type="tel"
                                        name="phone"
                                        value={form.phone}
                                        onChange={onChange}
                                        isInvalid={!!errors.phone}
                                        className="form-control-elevated"
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.phone}
                                    </Form.Control.Feedback>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <hr className="my-4" />
                                <div className="d-flex justify-content-between align-items-center password-section">
                                    <div className="section-title text-uppercase fw-semibold">
                                        <FaLock className="me-2" />
                                        Thay đổi mật khẩu
                                    </div>
                                    <div className="d-flex gap-2">

                                        <Button
                                            variant="outline-primary"
                                            onClick={() => setShowPasswordModal(true)}
                                            className="btn-change-password"
                                        >
                                            <FaKey className="me-2" />
                                            Đổi mật khẩu
                                        </Button>
                                    </div>
                                </div>
                            </Col>

                            <Col xs={12}>
                                <Button type="submit" className="btn-save px-4 fw-semibold" disabled={saving}>
                                    {saving ? (
                                        <>
                                            <Spinner animation="border" size="sm" className="me-2" />
                                            Đang lưu...
                                        </>
                                    ) : (
                                        "Lưu thay đổi"
                                    )}
                                </Button>
                            </Col>
                        </Row>
                    </Form>

                    {/* Modal đổi mật khẩu */}
                    <ChangePasswordModal
                        show={showPasswordModal}
                        onHide={() => setShowPasswordModal(false)}
                        onSubmit={onChangePassword}
                        loading={saving}
                        errors={errors}
                        onErrorsChange={setErrors}
                    />
                </div>
            </div>
        </div>
    );
};

export default MyAccount;
