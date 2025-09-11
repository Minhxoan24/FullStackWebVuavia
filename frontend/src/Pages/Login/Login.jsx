import React, { useState, useContext } from "react";
import { NavLink } from "react-router-dom";

import { AuthContext } from "../../Context/AuthContext";
import "./Login.css";

const Login = () => {
    const { login } = useContext(AuthContext);
    const [formState, setFormState] = useState({
        accountname: "",
        password: "",
        rememberMe: false,
    });

    // Cập nhật state khi input thay đổi
    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormState({
            ...formState,
            [name]: type === "checkbox" ? checked : value,
        });
    };

    // Xử lý submit form
    const handleSubmit = async (e) => {

        e.preventDefault();
        if (!formState.accountname || !formState.password) {
            alert("Vui lòng nhập đầy đủ thông tin");
            return;
        }


        try {
            const data = await login(formState);
            alert("Login successful!");
            console.log("Login successful:", data);
            // Redirect to homepage or dashboard
        } catch (error) {
            console.error("Login failed:", error);
            alert("Login failed:" + (error.response?.data?.message || error.message));
        }
    };

    return (
        <div className="login-page">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-6 col-lg-5">
                        <div className="login-form-container bg-white rounded-4 shadow-lg p-5">
                            <h2 className="text-center fw-bold mb-4 text-uppercase">ĐĂNG NHẬP</h2>

                            <form className="login-form" autoComplete="on" onSubmit={handleSubmit}>
                                {/* Tên tài khoản hoặc địa chỉ email */}
                                <div className="mb-3">
                                    <label className="form-label fw-semibold text-dark">
                                        Tên tài khoản hoặc địa chỉ email *
                                    </label>
                                    <input
                                        type="text"
                                        name="accountname"
                                        autoComplete="accountname"
                                        value={formState.accountname}
                                        onChange={handleChange}
                                        className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                        placeholder="Nhập tên tài khoản hoặc email nhé "
                                    />
                                </div>

                                {/* Mật khẩu */}
                                <div className="mb-3">
                                    <label className="form-label fw-semibold text-dark">Mật khẩu *</label>
                                    <input
                                        type="password"
                                        name="password"
                                        autoComplete="current-password"
                                        value={formState.password}
                                        onChange={handleChange}
                                        className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                                        placeholder="••••••••"
                                    />
                                </div>

                                {/* Ghi nhớ mật khẩu */}
                                <div className="form-check mb-4">
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        name="rememberMe"
                                        id="rememberPassword"
                                        checked={formState.rememberMe}
                                        onChange={handleChange}
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
                                        backgroundColor: "#ff6b35",
                                        borderColor: "#ff6b35",
                                        padding: "12px",
                                    }}
                                >
                                    ĐĂNG NHẬP
                                </button>

                                {/* Quên mật khẩu */}
                                <div className="text-center mb-4">
                                    <a href="/forgot-password" className="text-decoration-none text-muted">
                                        Quên mật khẩu?
                                    </a>
                                </div>

                                {/* Link đăng ký */}
                                <div className="text-center">
                                    <p className="text-muted mb-0">
                                        Chưa có tài khoản?{" "}
                                        <NavLink
                                            to="/register"
                                            className="text-decoration-none"
                                            style={{ color: "#ff6b35" }}
                                        >
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
    );
};

export default Login;
