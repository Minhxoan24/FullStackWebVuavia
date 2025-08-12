import React from "react";

import './Login.css';
import { useState } from "react";
import { NavLink } from "react-router-dom";

const Login = () => {
    const [FormState, setFormState] = useState({
     



    });
    return (
        <>

            <div className="login-page">
                <div className="container">
                    <div className="row justify-content-center">
                        <div className="col-md-6 col-lg-5">
                            <div className="login-form-container bg-white rounded-4 shadow-lg p-5">
                                <h2 className="text-center fw-bold mb-4 text-uppercase">ĐĂNG NHẬP</h2>

                                <form className="login-form">
                                    {/* Tên tài khoản hoặc địa chỉ email */}
                                    <div className="mb-3">
                                        <label className="form-label fw-semibold text-dark">
                                            Tên tài khoản hoặc địa chỉ email *
                                        </label>
                                        <input
                                            type="text"
                                            name="accountname"
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="Nhập tài khoản hoặc email"
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
                                            className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                            placeholder="••••••••"
                                            style={{ backgroundColor: '#f8f9fa' }}
                                        />
                                    </div>

                                    {/* Ghi nhớ mật khẩu */}
                                    <div className="form-check mb-4">
                                        <input
                                            className="form-check-input"
                                            type="checkbox"
                                            name="rememberMe"
                                            id="rememberPassword"
                                        />
                                        <label className="form-check-label text-dark" htmlFor="rememberPassword">
                                            Ghi nhớ mật khẩu
                                        </label>
                                    </div>

                                    {/* Nút đăng nhập */}
                                    <button
                                        type="submit"
                                        className="btn btn-lg w-100 fw-bold rounded-3 mb-3 text-white"
                                        style={{
                                            backgroundColor: '#ff6b35',
                                            borderColor: '#ff6b35',
                                            padding: '12px'
                                        }}
                                    >
                                        ĐĂNG NHẬP
                                    </button>

                                    {/* Quên mật khẩu */}
                                    <div className="text-center mb-4">
                                        <a href="#" className="text-decoration-none text-muted">
                                            Quên mật khẩu?
                                        </a>
                                    </div>

                                    {/* Link đăng ký */}
                                    <div className="text-center">
                                        <p className="text-muted mb-0">
                                            Chưa có tài khoản? {' '}
                                            <NavLink to="/register" className="text-decoration-none" style={{ color: '#ff6b35' }}>
                                                Đăng ký ngay
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

export default Login;