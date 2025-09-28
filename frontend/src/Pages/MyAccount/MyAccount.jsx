import React, { useState, useContext } from "react";
import "./MyAccount.css";
import { AuthContext } from "../../Context/AuthContext";
import { updateProfile, changePassword } from "../../Services/ApiUserService";
import { Form, Button, Row, Col, Alert, Spinner, InputGroup } from "react-bootstrap";
import { FaUser, FaEnvelope, FaPhone, FaLock, FaCheckCircle, FaEye, FaEyeSlash } from "react-icons/fa";

const EMAIL_RGX = /^\S+@\S+\.\S+$/;
const PHONE_RGX = /^[0-9()+\-.\s]{9,20}$/;

const MyAccount = () => {
    const { user } = useContext(AuthContext);

    const [form, setForm] = useState({
        firstName: user?.name || "",
        lastName: user?.surname || "",
        accountName: user?.accountname || "",
        email: user?.email || "",
        phone: user?.phone || "",
        currentPassword: "",
        newPassword: "",
        confirmPassword: "",
    });

    const [errors, setErrors] = useState({});
    const [saving, setSaving] = useState(false);
    const [alert, setAlert] = useState({ type: "", msg: "" }); // 'success' | 'danger' | ''
    const [showPasswords, setShowPasswords] = useState({
        current: false,
        new: false,
        confirm: false,
    });

    const onChange = (e) =>
        setForm((s) => ({ ...s, [e.target.name]: e.target.value }));

    const validate = () => {
        const err = {};
        if (!form.firstName.trim()) err.firstName = "Vui lòng nhập Tên.";
        if (!form.lastName.trim()) err.lastName = "Vui lòng nhập Họ.";
        if (!form.accountName.trim()) err.accountName = "Vui lòng nhập Tên tài khoản.";
        if (!EMAIL_RGX.test(form.email.trim())) err.email = "Email không hợp lệ.";
        if (!PHONE_RGX.test(form.phone.trim())) err.phone = "Số điện thoại không hợp lệ.";

        // Nếu bất kỳ ô mật khẩu nào được nhập → kiểm tra đủ bộ và khớp
        const anyPw = form.currentPassword || form.newPassword || form.confirmPassword;
        if (anyPw) {
            if (!form.currentPassword) err.currentPassword = "Nhập mật khẩu hiện tại.";
            if (!form.newPassword) err.newPassword = "Nhập mật khẩu mới.";
            if (!form.confirmPassword) err.confirmPassword = "Xác nhận mật khẩu mới.";
            if (form.newPassword && form.newPassword.length < 6)
                err.newPassword = "Mật khẩu mới tối thiểu 6 ký tự.";
            if (form.newPassword && form.confirmPassword && form.newPassword !== form.confirmPassword)
                err.confirmPassword = "Xác nhận mật khẩu mới không khớp.";
        }

        setErrors(err);
        return Object.keys(err).length === 0;
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        setAlert({ type: "", msg: "" });

        if (!validate()) return;

        setSaving(true);
        try {
            // 1) Cập nhật hồ sơ cơ bản (đúng theo payload bạn đang dùng)
            await updateProfile({
                name: form.firstName.trim(),
                surname: form.lastName.trim(),
                phone: form.phone.trim(),
            });

            // 2) Nếu nhập mật khẩu → gọi đổi mật khẩu
            if (form.currentPassword && form.newPassword && form.confirmPassword) {
                await changePassword({
                    currentPassword: form.currentPassword,
                    newPassword: form.newPassword,
                    confirmPassword: form.confirmPassword, // giữ theo API bạn đang gọi
                });
                // dọn trường mật khẩu sau khi đổi
                setForm((s) => ({
                    ...s,
                    currentPassword: "",
                    newPassword: "",
                    confirmPassword: "",
                }));
            }

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

    const toggleShowPassword = (field) => {
        setShowPasswords((prev) => ({ ...prev, [field]: !prev[field] }));
    };

    return (
        <div className="account-wrap py-4">
            <div className="container">
                <div className="account-card p-4 p-md-5 mx-auto">
                    {!!alert.type && (
                        <Alert variant={alert.type} className="mb-4">
                            {alert.type === "success" && <FaCheckCircle className="me-2" />}
                            {alert.msg}
                        </Alert>
                    )}

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
                                        onChange={onChange}
                                        isInvalid={!!errors.accountName}
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
                                    <Form.Control
                                        type="email"
                                        name="email"
                                        value={form.email}
                                        onChange={onChange}
                                        isInvalid={!!errors.email}
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.email}
                                    </Form.Control.Feedback>
                                </Form.Group>
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
                                        required
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        {errors.phone}
                                    </Form.Control.Feedback>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <hr className="my-4" />
                                <div className="section-title text-uppercase fw-semibold text-muted">
                                    <FaLock className="me-2" />
                                    Thay đổi mật khẩu
                                </div>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label>
                                        Mật khẩu hiện tại <span className="text-muted">(bỏ trống nếu không đổi)</span>
                                    </Form.Label>
                                    <InputGroup>
                                        <Form.Control
                                            type={showPasswords.current ? "text" : "password"}
                                            name="currentPassword"
                                            value={form.currentPassword}
                                            onChange={onChange}
                                            isInvalid={!!errors.currentPassword}
                                        />
                                        <Button variant="outline-secondary" size="sm" onClick={() => toggleShowPassword('current')}>
                                            {showPasswords.current ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                    </InputGroup>
                                    <Form.Control.Feedback type="invalid">
                                        {errors.currentPassword}
                                    </Form.Control.Feedback>
                                </Form.Group>
                            </Col>

                            <Col xs={12}>
                                <Form.Group>
                                    <Form.Label>
                                        Mật khẩu mới <span className="text-muted">(bỏ trống nếu không đổi)</span>
                                    </Form.Label>
                                    <InputGroup>
                                        <Form.Control
                                            type={showPasswords.new ? "text" : "password"}
                                            name="newPassword"
                                            value={form.newPassword}
                                            onChange={onChange}
                                            isInvalid={!!errors.newPassword}
                                        />
                                        <Button variant="outline-secondary" size="sm" onClick={() => toggleShowPassword('new')}>
                                            {showPasswords.new ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                    </InputGroup>
                                    <Form.Control.Feedback type="invalid">
                                        {errors.newPassword}
                                    </Form.Control.Feedback>
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
                                            onChange={onChange}
                                            isInvalid={!!errors.confirmPassword}
                                        />
                                        <Button variant="outline-secondary" size="sm" onClick={() => toggleShowPassword('confirm')}>
                                            {showPasswords.confirm ? <FaEyeSlash /> : <FaEye />}
                                        </Button>
                                    </InputGroup>
                                    <Form.Control.Feedback type="invalid">
                                        {errors.confirmPassword}
                                    </Form.Control.Feedback>
                                </Form.Group>
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
                </div>
            </div>
        </div>
    );
};

export default MyAccount;
