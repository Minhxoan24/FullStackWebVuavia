import React, { useEffect, useRef, useState, useContext, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../../Context/AuthContext";
import "./ModalLogin.css";

const ModalLogin = ({ show, handleClose }) => {
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const [form, setForm] = useState({
        accountname: localStorage.getItem("remember_accountname") || "",
        password: "",
        remember: !!localStorage.getItem("remember_accountname"),
    });
    const [submitting, setSubmitting] = useState(false);
    const [errMsg, setErrMsg] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const dialogRef = useRef(null);
    const firstFieldRef = useRef(null);

    useEffect(() => {
        if (!show) return;
        const prevOverflow = document.body.style.overflow;
        document.body.style.overflow = "hidden";
        firstFieldRef.current?.focus();

        const onKey = (e) => {
            if (e.key === "Escape") handleClose();
            if (e.key === "Tab" && dialogRef.current) {
                const focusables = dialogRef.current.querySelectorAll(
                    'a[href],button:not([disabled]),textarea,input,select,[tabindex]:not([tabindex="-1"])'
                );
                if (!focusables.length) return;
                const first = focusables[0];
                const last = focusables[focusables.length - 1];
                if (e.shiftKey && document.activeElement === first) {
                    e.preventDefault(); last.focus();
                } else if (!e.shiftKey && document.activeElement === last) {
                    e.preventDefault(); first.focus();
                }
            }
        };
        document.addEventListener("keydown", onKey);
        return () => {
            document.body.style.overflow = prevOverflow;
            document.removeEventListener("keydown", onKey);
        };
    }, [show, handleClose]);

    const onBackdropClick = (e) => {
        if (e.target === e.currentTarget) handleClose();
    };

    const onChange = (e) => {
        const { name, value, type, checked } = e.target;
        setForm((s) => ({ ...s, [name]: type === "checkbox" ? checked : value }));
        setErrMsg("");
    };

    const rememberAccountname = useCallback((remember, accountname) => {
        if (remember && accountname) localStorage.setItem("remember_accountname", accountname);
        else localStorage.removeItem("remember_accountname");
    }, []);

    const handleRegisterClick = () => {
        handleClose();
        navigate("/register");
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrMsg("");
        if (!form.accountname?.trim() || !form.password) {
            setErrMsg("Vui lòng nhập đầy đủ thông tin.");
            return;
        }
        setSubmitting(true);
        try {
            await login({ accountname: form.accountname.trim(), password: form.password });
            rememberAccountname(form.remember, form.accountname.trim());
            setForm((s) => ({ ...s, password: "" }));
            handleClose();
            navigate("/");
        } catch (error) {
            const msg = error?.response?.data?.message || error?.message || "Đăng nhập thất bại.";
            setErrMsg(msg);
        } finally {
            setSubmitting(false);
        }
    };

    if (!show) return null;

    return (
        <div className="modal-backdrop-custom" onClick={onBackdropClick}>
            <div
                className="modal-dialog modal-lg modal-dialog-centered"
                role="dialog"
                aria-modal="true"
                aria-labelledby="loginTitle"
                ref={dialogRef}
            >
                <div className="modal-content custom-modal">
                    <div className="modal-body p-0">
                        <div className="row g-0">
                            {/* LEFT SIDE */}
                            <div className="col-md-6 left-pane d-flex flex-column justify-content-center align-items-center text-white">
                                <div className="left-inner text-center">
                                    <h2 className="left-title">ĐĂNG KÍ</h2>
                                    <p className="left-sub">Bạn chưa có tài khoản, đăng kí ngay!</p>
                                    <button
                                        type="button"
                                        className="btn btn-left-outline"
                                        onClick={handleRegisterClick}
                                    >
                                        ĐĂNG KÍ TÀI KHOẢN MỚI
                                    </button>
                                </div>
                            </div>

                            {/* RIGHT SIDE */}
                            <div className="col-md-6 right-pane position-relative">
                                <button
                                    type="button"
                                    className="btn-close position-absolute top-0 end-0 m-3 close-white"
                                    onClick={handleClose}
                                    aria-label="Đóng"
                                />
                                <div className="right-inner">
                                    <h3 className="right-title" id="loginTitle">ĐĂNG NHẬP</h3>

                                    {errMsg && <div className="alert alert-danger py-2">{errMsg}</div>}

                                    <form onSubmit={handleSubmit} noValidate>
                                        {/* Username or email */}
                                        <div className="mb-3">
                                            <label className="form-label fw-semibold text-dark mb-2" htmlFor="accountname">
                                                Tên tài khoản hoặc địa chỉ email *
                                            </label>
                                            <input
                                                id="accountname"
                                                name="accountname"
                                                type="text"
                                                className="form-control input-soft"
                                                placeholder="Nhập tên tài khoản"
                                                autoComplete="username"
                                                value={form.accountname}
                                                onChange={onChange}
                                                ref={firstFieldRef}
                                                required
                                            />
                                        </div>

                                        {/* Password + Eye */}
                                        <div className="mb-3">
                                            <label className="form-label fw-semibold text-dark mb-2" htmlFor="password">
                                                Mật khẩu *
                                            </label>
                                            <div className="position-relative">
                                                <input
                                                    id="password"
                                                    name="password"
                                                    type={showPassword ? "text" : "password"}
                                                    className="form-control input-soft pe-5"
                                                    placeholder="••••••••"
                                                    autoComplete="current-password"
                                                    value={form.password}
                                                    onChange={onChange}
                                                    required
                                                />
                                                <button
                                                    type="button"
                                                    className="btn btn-sm btn-link pw-toggle"
                                                    aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
                                                    title={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
                                                    onClick={() => setShowPassword(s => !s)}
                                                >
                                                    {showPassword ? (
                                                        // Eye-off icon
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                                            viewBox="0 0 24 24" fill="none">
                                                            <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"
                                                                stroke="currentColor" strokeWidth="2" />
                                                            <path d="M14.12 9.88a3 3 0 1 1-4.24 4.24"
                                                                stroke="currentColor" strokeWidth="2" />
                                                            <path d="M3 3l18 18" stroke="currentColor" strokeWidth="2" />
                                                        </svg>
                                                    ) : (
                                                        // Eye icon
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                                                            viewBox="0 0 24 24" fill="none">
                                                            <path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"
                                                                stroke="currentColor" strokeWidth="2" />
                                                            <circle cx="12" cy="12" r="3"
                                                                stroke="currentColor" strokeWidth="2" />
                                                        </svg>
                                                    )}
                                                </button>
                                            </div>
                                        </div>

                                        {/* Remember */}
                                        <div className="form-check mb-3">
                                            <input
                                                className="form-check-input"
                                                type="checkbox"
                                                id="remember"
                                                name="remember"
                                                checked={form.remember}
                                                onChange={onChange}
                                            />
                                            <label className="form-check-label text-dark" htmlFor="remember">
                                                Ghi nhớ mật khẩu
                                            </label>
                                        </div>

                                        {/* Submit */}
                                        <button
                                            type="submit"
                                            className="btn btn-login-outline w-100"
                                            disabled={submitting}
                                        >
                                            {submitting ? "ĐANG ĐĂNG NHẬP..." : "ĐĂNG NHẬP"}
                                        </button>

                                        {/* Forgot */}
                                        <div className="text-start mt-3">
                                            <a href="/forgot-password" className="link-forgot">
                                                Quên mật khẩu?
                                            </a>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* SOCIAL BAR */}
                    <div className="social-bar">
                        <div className="row g-2 social-wrap">
                            <div className="col-md-6">
                                <button type="button" className="btn social social-fb w-100">
                                    <i className="fab fa-facebook-f me-2"></i>
                                    <span className="social-text">ĐĂNG NHẬP BẰNG FACEBOOK</span>
                                </button>
                            </div>
                            <div className="col-md-6">
                                <button type="button" className="btn social social-gg w-100">
                                    <i className="fab fa-google me-2"></i>
                                    <span className="social-text">ĐĂNG NHẬP BẰNG GOOGLE</span>
                                </button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default ModalLogin;