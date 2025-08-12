import React from "react";

// import './Register.css';
import { NavLink } from "react-router-dom";
import { useState } from "react";


const Register = () => {
    const [FormRegister, setFormRegister] = useState({
        accountname: '',
        password: '',
        email: '',
        surname: '',
        name: '',
        phone: '',
    })
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormRegister(preFormregister => ({
            ...preFormregister,
            [name]: value
        }));
    };
    const handleSubmitRegister = (e) => {
        e.preventDefault();
        console.log("Form submitted:", FormRegister);
        console.error("DEBUG - Form Data:", JSON.stringify(FormRegister, null, 2));
        console.warn("DEBUG - Form submitted at:", new Date().toISOString());


    };

    return (
        <>

            <div className="register-page">
                <div className="container">
                    <div className="row justify-content-center">
                        <div className="col-md-6 col-lg-5">
                            <div className="register-form-container bg-white rounded-4 shadow-lg p-5">
                                <h2 className="text-center fw-bold mb-4 text-uppercase">ĐĂNG KÝ</h2>

                                <form className="register-form" onSubmit={handleSubmitRegister}>
                                    {/* Tên tài khoản */}
                                    <div className="mb-3">
                                        <label className="form-label fw-semibold text-dark">
                                            Tên tài khoản *
                                        </label>
                                        <input
                                            type="text"
                                            name="accountname"
                                            value={FormRegister.accountname}
                                            onChange={handleChange}
                                            required
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="Nhập tên tài khoản"
                                            style={{ backgroundColor: '#f8f9fa' }}
                                        />
                                    </div>

                                    {/* Địa chỉ email */}
                                    <div className="mb-3">
                                        <label className="form-label fw-semibold text-dark">
                                            Địa chỉ email *
                                        </label>
                                        <input
                                            type="email"
                                            name="email"
                                            value={FormRegister.email}
                                            onChange={handleChange}
                                            required
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="Nhập địa chỉ email"
                                            style={{ backgroundColor: '#f8f9fa' }}
                                        />
                                    </div>

                                    {/* Mật khẩu */}
                                    <div className="mb-3">
                                        <label className="form-label fw-semibold text-dark">
                                            Mật khẩu *
                                        </label>
                                        <input
                                            type="password"
                                            name="password"
                                            value={FormRegister.password}
                                            onChange={handleChange}
                                            required
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="Nhập mật khẩu"
                                            style={{ backgroundColor: '#f8f9fa' }}
                                        />
                                    </div>

                                    {/* Họ và Tên */}
                                    <div className="row">
                                        <div className="col-6">
                                            <div className="mb-3">
                                                <label className="form-label fw-semibold text-dark">
                                                    Họ *
                                                </label>
                                                <input
                                                    type="text"
                                                    name="surname"

                                                    value={FormRegister.surname}
                                                    onChange={handleChange}
                                                    required
                                                    className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                                    placeholder="Nhập họ"
                                                    style={{ backgroundColor: '#f8f9fa' }}
                                                />
                                            </div>
                                        </div>
                                        <div className="col-6">
                                            <div className="mb-3">
                                                <label className="form-label fw-semibold text-dark">
                                                    Tên *
                                                </label>
                                                <input
                                                    type="text"
                                                    name="name"
                                                    value={FormRegister.name}
                                                    onChange={handleChange}
                                                    required
                                                    className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                                    placeholder="Nhập tên"
                                                    style={{ backgroundColor: '#f8f9fa' }}
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* Số điện thoại */}
                                    <div className="mb-4">
                                        <label className="form-label fw-semibold text-dark">
                                            Số điện thoại *
                                        </label>
                                        <input
                                            type="tel"
                                            name="phone"
                                            value={FormRegister.phone}
                                            onChange={handleChange}
                                            required
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="Nhập số điện thoại"
                                            style={{ backgroundColor: '#f8f9fa' }}
                                        />
                                    </div>

                                    {/* Điều khoản */}
                                    <div className="mb-4">
                                        <p className="text-muted small">
                                            Dữ liệu cá nhân của bạn sẽ được sử dụng để hỗ trợ trải nghiệm của bạn trên
                                            toàn bộ trang web này, để quản lý quyền truy cập vào tài khoản của bạn và
                                            cho các mục đích khác được mô tả trong chính sách riêng tư của chúng tôi.
                                        </p>
                                    </div>

                                    {/* Nút đăng ký */}
                                    <button
                                        type="submit"
                                        className="btn btn-lg w-100 fw-bold rounded-3 text-white"
                                        style={{
                                            backgroundColor: '#ff6b35',
                                            borderColor: '#ff6b35',
                                            padding: '12px'
                                        }}



                                    >
                                        ĐĂNG KÝ
                                    </button>

                                    {/* Link đăng nhập */}
                                    <div className="text-center mt-4">
                                        <p className="text-muted mb-0">
                                            Đã có tài khoản? {' '}
                                            <NavLink to="/login" className="text-decoration-none" style={{ color: '#ff6b35' }}>
                                                Đăng nhập ngay
                                            </NavLink>
                                        </p>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Register;