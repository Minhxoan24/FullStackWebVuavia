import React, { useState, useContext } from "react";
import { AuthContext } from "../../../Context/AuthContext"; // đường dẫn tuỳ vị trí file
import './ModalLogin.css';

import { useNavigate } from 'react-router-dom';
const ModalLogin = ({ show, handleClose }) => {
    const { login } = useContext(AuthContext);
    const [formModalLogin, setFormModalLogin] = useState({
        accountname: "",
        password: "",
    });





    const navigate = useNavigate();
    // if show = True thì !show = false mà false thì bỏ qua . nếu show = false thì !show = true . điều kiện đúng trả về null 
    if (!show) return null;


    const handleRegisterClick = () => {
        handleClose(); // đóng modal
        navigate('/register'); // chuyển sang trang đăng ký
    };

    const handleBackdropClick = (e) => {
        if (e.target === e.currentTarget) {
            handleClose();
        }
    };
    const handleSubmitLogin = async (e) => {
        e.preventDefault(); // Ngăn chặn hành vi mặc định của form (tải lại trang)
        // Gọi API đăng nhập ở đây
        if (!formModalLogin.accountname || !formModalLogin.password) {
            alert("Vui lòng nhập đầy đủ thông tin");
            return;
        }
        try {
            const data = await login(formModalLogin);
            alert("Login successful!");
            setFormModalLogin({
                accountname: "",
                password: "",
            });
            handleClose(); // Đóng modal sau khi đăng nhập thành công
            navigate('/'); // Chuyển hướng sang trang chủ (hoặc trang bạn muốn)
        } catch (error) {
            console.error("Login failed:", error);
            alert("Login failed:" + (error.response?.data?.message || error.message));
        }
    };



    return (
        <>
            {/* Modal Backdrop */}
            <div className="modal-backdrop-custom" onClick={handleBackdropClick}>{/* Modal Backdrop sử dụng để làm mờ phần còn lại của trang */}
                <div className="modal-dialog modal-lg modal-dialog-centered"> {/* Modal dialog phần hộp thoại chính bên trong modal để bao bọc content   modal-lg : size modal  */}
                    <div className="modal-content border-0 rounded-4 overflow-hidden shadow-lg">
                        <div className="modal-body p-0">
                            <div className="row g-0">
                                {/* Left Side - Gradient */}
                                <div className="col-md-5 modal-left-gradient d-flex flex-column justify-content-center align-items-center text-white p-5">
                                    <div className="text-center">
                                        <h2 className="fw-bold mb-3 display-6">ĐĂNG KÝ</h2>
                                        <p className="mb-4 fs-6">Bạn chưa có tài khoản, đăng ký ngay!</p>
                                        <button className="btn btn-outline-light btn-lg px-4 py-2 rounded-2 fw-semibold border-2" onClick={handleRegisterClick}>
                                            ĐĂNG KÝ TÀI KHOẢN MỚI
                                        </button>
                                    </div>
                                </div>

                                {/* Right Side - Login Form */}
                                <div className="col-md-7 bg-white p-5 position-relative">
                                    {/* Close Button */}
                                    <button
                                        type="button"
                                        className="btn-close position-absolute top-0 end-0 m-3"
                                        onClick={handleClose}
                                    ></button>

                                    <div className="login-form-container">
                                        <h3 className="fw-bold mb-4 text-dark">ĐĂNG NHẬP</h3>

                                        <form onSubmit={handleSubmitLogin}>
                                            {/* Username/Email Input */}
                                            <div className="mb-3">
                                                <label className="form-label fw-semibold text-dark mb-2">
                                                    Tên tài khoản *
                                                </label>
                                                <input
                                                    type="text"
                                                    className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                                    placeholder="Nhập tên tài khoản !"

                                                    style={{ backgroundColor: '#f8f9fa' }}
                                                    name="accountname"
                                                    autoComplete="accountname"
                                                    value={formModalLogin.accountname}
                                                    onChange={(e) => setFormModalLogin({ ...formModalLogin, accountname: e.target.value })}
                                                />
                                            </div>

                                            {/* Password Input */}
                                            <div className="mb-3">
                                                <label className="form-label fw-semibold text-dark mb-2">
                                                    Mật khẩu *
                                                </label>
                                                <input
                                                    type="password"
                                                    className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                                    placeholder="••••••••"
                                                    style={{ backgroundColor: '#f8f9fa' }}
                                                    name="password"
                                                    autoComplete="current-password"
                                                    value={formModalLogin.password}
                                                    onChange={(e) => setFormModalLogin({ ...formModalLogin, password: e.target.value })}
                                                />
                                            </div>

                                            {/* Remember Password Checkbox */}
                                            <div className="form-check mb-3">
                                                <input
                                                    className="form-check-input"
                                                    type="checkbox"
                                                    id="rememberPassword"
                                                />
                                                <label className="form-check-label text-dark" htmlFor="rememberPassword">
                                                    Ghi nhớ mật khẩu
                                                </label>
                                            </div>

                                            {/* Login Button */}
                                            <button
                                                type="submit"
                                                className="btn btn-warning btn-lg w-100 fw-bold rounded-3 mb-3 text-white"

                                                style={{
                                                    backgroundColor: '#ff6b35',
                                                    borderColor: '#ff6b35',
                                                    padding: '12px'

                                                }}
                                            >
                                                ĐĂNG NHẬP
                                            </button>

                                            {/* Forgot Password Link */}
                                            <div className="text-center mb-4">
                                                <a href="/forgot-password" className="text-decoration-none text-muted">
                                                    Quên mật khẩu?
                                                </a>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Social Login Footer */}
                        <div className="modal-footer bg-white border-0 pt-0 pb-4">
                            <div className="container-fluid">
                                <div className="row g-2">
                                    <div className="col-6">
                                        <button
                                            type="button"
                                            className="btn btn-primary w-100 fw-semibold rounded-pill d-flex align-items-center justify-content-center"
                                            style={{
                                                backgroundColor: '#4267B2',
                                                borderColor: '#4267B2',
                                                padding: '10px 15px'
                                            }}
                                        >
                                            <i className="fab fa-facebook-f me-2"></i>
                                            ĐĂNG NHẬP BẰNG FACEBOOK
                                        </button>
                                    </div>
                                    <div className="col-6">
                                        <button
                                            type="button"
                                            className="btn btn-danger w-100 fw-semibold rounded-pill d-flex align-items-center justify-content-center"
                                            style={{
                                                backgroundColor: '#db4437',
                                                borderColor: '#db4437',
                                                padding: '10px 15px'
                                            }}
                                        >
                                            <i className="fab fa-google me-2"></i>
                                            ĐĂNG NHẬP BẰNG GOOGLE
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ModalLogin;