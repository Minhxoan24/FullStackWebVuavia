import React, { useState, useEffect, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
    requestPasswordResetOTP,
    verifyPasswordResetOTP,
    resetPasswordWithOTP,
} from "../../Services/ApiUserService";
import "./ForgotPassword.css";
import Modal from "../../Components/Modal/Modal";

/* ---------- OtpInput: 6-box OTP with paste & focus handling ---------- */
const OtpInput = ({ length = 6, value = "", onChange, disabled, autoFocus = false }) => {
    const inputsRef = useRef([]);
    const [digits, setDigits] = useState(Array(length).fill(""));

    useEffect(() => {
        // sync from parent if needed
        if (value && value.length === length) {
            setDigits(value.split(""));
        }
    }, [value, length]);

    // auto focus first input when requested
    useEffect(() => {
        if (autoFocus) {
            // small delay to ensure inputs mounted
            const t = setTimeout(() => {
                if (inputsRef.current && inputsRef.current[0]) inputsRef.current[0].focus();
            }, 50);
            return () => clearTimeout(t);
        }
    }, [autoFocus]);

    const focusIndex = (i) => {
        if (inputsRef.current[i]) inputsRef.current[i].focus();
    };

    const handleChange = (i, v) => {
        const cleaned = v.replace(/\D/g, "");
        if (!cleaned) {
            const next = [...digits];
            next[i] = "";
            setDigits(next);
            onChange?.(next.join(""));
            return;
        }
        const next = [...digits];
        next[i] = cleaned[0];
        // distribute remaining paste across following boxes
        let ci = i + 1;
        for (let k = 1; k < cleaned.length && ci < length; k++, ci++) {
            next[ci] = cleaned[k];
        }
        setDigits(next);
        onChange?.(next.join(""));
        // move focus to next empty or the last
        const nextEmpty = next.findIndex((d, idx) => d === "" && idx > i);
        focusIndex(nextEmpty !== -1 ? nextEmpty : Math.min(length - 1, i + cleaned.length));
    };

    const handleKeyDown = (i, e) => {
        if (e.key === "Backspace") {
            e.preventDefault();
            const next = [...digits];
            if (next[i]) {
                next[i] = "";
                setDigits(next);
                onChange?.(next.join(""));
                return;
            }
            const prevIndex = Math.max(0, i - 1);
            next[prevIndex] = "";
            setDigits(next);
            onChange?.(next.join(""));
            focusIndex(prevIndex);
        } else if (e.key === "ArrowLeft") {
            e.preventDefault();
            focusIndex(Math.max(0, i - 1));
        } else if (e.key === "ArrowRight") {
            e.preventDefault();
            focusIndex(Math.min(length - 1, i + 1));
        }
    };

    const handleFocus = (i, e) => {
        e.target.select();
    };

    return (
        <div className="otp-wrapper" role="group" aria-label="Nhập mã OTP gồm 6 chữ số">
            {Array.from({ length }).map((_, i) => (
                <input
                    key={i}
                    type="text"
                    inputMode="numeric"
                    pattern="[0-9]*"
                    maxLength={1}
                    className="otp-box"
                    value={digits[i]}
                    onChange={(e) => handleChange(i, e.target.value)}
                    onKeyDown={(e) => handleKeyDown(i, e)}
                    onFocus={(e) => handleFocus(i, e)}
                    disabled={disabled}
                    ref={(el) => (inputsRef.current[i] = el)}
                    aria-label={`Ký tự OTP thứ ${i + 1}`}
                />
            ))}
        </div>
    );
};

/* ---------- Password field with show/hide ---------- */
const PasswordField = ({ label, value, onChange, placeholder, minLength = 6, id }) => {
    const [show, setShow] = useState(false);
    const [caps, setCaps] = useState(false);

    return (
        <div className="mb-4">
            <label className="form-label fw-semibold">
                <i className="fas fa-lock me-2" />
                {label}
            </label>
            <div className="password-field">
                <input
                    id={id}
                    type={show ? "text" : "password"}
                    className="form-control form-control-lg"
                    value={value}
                    onChange={onChange}
                    onKeyUp={(e) => setCaps(e.getModifierState && e.getModifierState("CapsLock"))}
                    placeholder={placeholder}
                    minLength={minLength}
                    required
                />
                <button
                    type="button"
                    className="toggle-visibility"
                    onClick={() => setShow((s) => !s)}
                    aria-label={show ? "Ẩn mật khẩu" : "Hiển thị mật khẩu"}
                >
                    <i className={`fas ${show ? "fa-eye-slash" : "fa-eye"}`} />
                </button>
            </div>
            {caps && <div className="form-text text-warning">Bạn đang bật Caps Lock</div>}
        </div>
    );
};

const ForgotPassword = () => {
    const [step, setStep] = useState(1); // 1: request, 2: verify, 3: reset, 4: success
    const [email, setEmail] = useState("");
    const [otp, setOtp] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [countdown, setCountdown] = useState(0); // seconds
    // New modal state
    const [modal, setModal] = useState({ visible: false, title: '', message: '', type: 'info', onConfirm: null, showConfirm: true, confirmText: 'OK' });
    const navigate = useNavigate();

    // Helper to normalize API error detail (supports {code, message} or string)
    const extractErrorDetail = (err) => {
        // Prefer the HTTP detail field; fall back to message or error.message
        let det = err?.response?.data?.detail ?? err?.response?.data?.message ?? err?.message ?? 'Lỗi không xác định';

        // If it's an object, prefer its message property
        if (det && typeof det === 'object') {
            det = det.message ?? JSON.stringify(det);
        }

        if (typeof det !== 'string') det = String(det);

        // Map common English/backend messages to Vietnamese (regex-based)
        const translations = [
            { pattern: /Internal Server Error/i, replace: 'Lỗi máy chủ nội bộ. Vui lòng thử lại.' },
            { pattern: /Định dạng email không hợp lệ|Invalid email format/i, replace: 'Định dạng email không hợp lệ.' },
            { pattern: /Email already exists/i, replace: 'Email đã tồn tại.' },
            { pattern: /Phone number already exists/i, replace: 'Số điện thoại đã tồn tại.' },
            { pattern: /No changes detected/i, replace: 'Không có thay đổi nào.' },
            { pattern: /Password must be at least (\d+) characters/i, replace: (m, p1) => `Mật khẩu phải có ít nhất ${p1} ký tự.` },
            { pattern: /Password must be at most (\d+) characters/i, replace: (m, p1) => `Mật khẩu tối đa ${p1} ký tự.` },
            { pattern: /OTP has expired|OTP expired|Mã OTP đã hết hạn|Mã OTP đã hết hạn hoặc không tồn tại/i, replace: 'Mã OTP đã hết hạn hoặc không tồn tại.' },
            { pattern: /Maximum OTP attempts reached|Đã vượt quá số lần thử tối đa/i, replace: 'Đã vượt quá số lần thử tối đa. Vui lòng yêu cầu mã mới.' },
            { pattern: /Invalid OTP|Mã OTP không đúng/i, replace: 'Mã OTP không đúng.' },
            { pattern: /Daily OTP limit exceeded/i, replace: 'Đã đạt giới hạn gửi mã trong ngày. Vui lòng thử lại vào ngày mai.' },
            { pattern: /Email not found|User not found|No user/i, replace: 'Không tìm thấy tài khoản với email này.' },
            { pattern: /Password reset processed|Password has been reset successfully/i, replace: 'Đặt lại mật khẩu thành công.' }
        ];

        for (const t of translations) {
            if (t.pattern.test(det)) {
                try {
                    return det.replace(t.pattern, typeof t.replace === 'function' ? t.replace : t.replace);
                } catch (_) {
                    return typeof t.replace === 'function' ? t.replace(null) : t.replace;
                }
            }
        }

        // If no translation matched, return the original detail string
        return det;
    };

    const closeModal = () => setModal((m) => ({ ...m, visible: false, onConfirm: null }));

    // show modal helper
    const showModal = ({ title, message, type = 'info', onConfirm = null, showConfirm = true, confirmText = 'OK' }) => {
        setModal({ visible: true, title, message, type, onConfirm, showConfirm, confirmText });
    };

    // countdown
    useEffect(() => {
        let t;
        if (countdown > 0) {
            t = setTimeout(() => setCountdown((s) => s - 1), 1000);
        }
        return () => clearTimeout(t);
    }, [countdown]);

    const formatTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

    const handleRequestOtp = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");
        try {
            const res = await requestPasswordResetOTP(email);
            const msg = res?.message || "Đã gửi OTP đến email của bạn.";
            setMessage(msg);
            // show confirmation modal
            showModal({
                title: 'Yêu cầu mã OTP',
                message: msg,
                type: 'success',
                showConfirm: true,
                confirmText: 'OK',
                onConfirm: () => {
                    closeModal();
                    setStep(2);
                }
            });
            setCountdown(180);
            setOtp("");
        } catch (err) {
            const errMsg = extractErrorDetail(err) || "Có lỗi xảy ra. Vui lòng thử lại.";
            setError(errMsg);
            showModal({ title: 'Lỗi', message: errMsg, type: 'error', showConfirm: false });
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");
        try {
            const res = await verifyPasswordResetOTP(email, otp);
            const msg = res?.message || "OTP hợp lệ. Vui lòng đặt mật khẩu mới.";
            // Show modal that requires user confirmation before proceeding to set new password
            showModal({
                title: 'OTP chính xác',
                message: msg,
                type: 'success',
                showConfirm: true,
                confirmText: 'Tiếp tục',
                onConfirm: () => {
                    closeModal();
                    setStep(3);
                }
            });
        } catch (err) {
            const errMsg = extractErrorDetail(err) || "OTP không hợp lệ hoặc đã hết hạn.";
            setError(errMsg);
            showModal({ title: 'Lỗi xác minh OTP', message: errMsg, type: 'error', showConfirm: false });
        } finally {
            setLoading(false);
        }
    };

    const handleResendOtp = async () => {
        if (countdown > 0) return;
        setLoading(true);
        setError("");
        try {
            await requestPasswordResetOTP(email);
            const msg = "Đã gửi lại OTP mới đến email của bạn.";
            showModal({ title: 'Gửi lại mã', message: msg, type: 'success', showConfirm: true, confirmText: 'OK', onConfirm: () => closeModal() });
            setCountdown(180);
            setOtp("");
        } catch (err) {
            const errMsg = extractErrorDetail(err) || "Không thể gửi lại OTP. Vui lòng thử lại sau.";
            setError(errMsg);
            showModal({ title: 'Lỗi', message: errMsg, type: 'error', showConfirm: false });
        } finally {
            setLoading(false);
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");

        if (newPassword !== confirmPassword) {
            const errMsg = "Mật khẩu xác nhận không khớp.";
            setError(errMsg);
            showModal({ title: 'Lỗi', message: errMsg, type: 'error', showConfirm: false });
            setLoading(false);
            return;
        }
        if (newPassword.length < 6) {
            const errMsg = "Mật khẩu phải có ít nhất 6 ký tự.";
            setError(errMsg);
            showModal({ title: 'Lỗi', message: errMsg, type: 'error', showConfirm: false });
            setLoading(false);
            return;
        }

        try {
            const res = await resetPasswordWithOTP(email, otp, newPassword);
            const msg = res?.message || "Đặt lại mật khẩu thành công!";
            // On success show success modal and redirect to home with state to show login
            showModal({
                title: 'Hoàn tất',
                message: msg,
                type: 'success',
                showConfirm: true,
                confirmText: 'Đến trang chính',
                onConfirm: () => {
                    closeModal();
                    // redirect to home and pass state to indicate login should be shown
                    navigate('/', { state: { showLogin: true } });
                }
            });
            setStep(4);
        } catch (err) {
            const errMsg = extractErrorDetail(err) || "Có lỗi xảy ra khi đặt lại mật khẩu.";
            setError(errMsg);
            showModal({ title: 'Lỗi', message: errMsg, type: 'error', showConfirm: false });
        } finally {
            setLoading(false);
        }
    };

    const passwordStrength = (() => {
        const v = newPassword;
        let score = 0;
        if (v.length >= 8) score++;
        if (/[A-Z]/.test(v)) score++;
        if (/[a-z]/.test(v)) score++;
        if (/\d/.test(v)) score++;
        if (/[^A-Za-z0-9]/.test(v)) score++;
        return Math.min(score, 4); // 0..4
    })();

    return (
        <div className="forgot-password-page container py-5">
            <div className="row justify-content-center">
                <div className="col-lg-6 col-md-8">
                    <div className="fp-card shadow-lg rounded-4">
                        <div className="fp-card__body p-4 p-md-5">

                            {/* Header */}
                            <div className="text-center mb-4">
                                <h2 className="fw-bold brand-title">Quên mật khẩu</h2>
                                <div className="step-indicator mt-3">
                                    {[1, 2, 3].map((n) => (
                                        <span key={n} className={`step ${step >= n ? "active" : ""}`}>
                                            <span className="step__number">{n}</span>
                                        </span>
                                    ))}
                                </div>
                            </div>

                            {/* Alerts */}
                            {message && (
                                <div className="alert alert-success fade show d-flex align-items-center">
                                    <i className="fas fa-check-circle me-2" />
                                    <span>{message}</span>
                                </div>
                            )}
                            {error && (
                                <div className="alert alert-danger fade show d-flex align-items-center">
                                    <i className="fas fa-exclamation-triangle me-2" />
                                    <span>{error}</span>
                                </div>
                            )}

                            {/* Step 1 */}
                            {step === 1 && (
                                <form onSubmit={handleRequestOtp} className="animate-in">
                                    <div className="mb-4">
                                        <label className="form-label fw-semibold">
                                            <i className="fas fa-envelope me-2" />
                                            Địa chỉ Email
                                        </label>
                                        <div className="input-with-icon">
                                            <i className="fas fa-at" />
                                            <input
                                                type="email"
                                                className="form-control form-control-lg"
                                                value={email}
                                                onChange={(e) => setEmail(e.target.value)}
                                                placeholder="Nhập địa chỉ email của bạn"
                                                required
                                            />
                                        </div>
                                        <div className="form-text">
                                            Chúng tôi sẽ gửi mã OTP đến email này để xác minh danh tính.
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        className="btn btn-lg w-100 text-white fw-bold accent-btn"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" />
                                                Đang gửi...
                                            </>
                                        ) : (
                                            <>
                                                <i className="fas fa-paper-plane me-2" />
                                                Gửi mã OTP
                                            </>
                                        )}
                                    </button>
                                </form>
                            )}

                            {/* Step 2 */}
                            {step === 2 && (
                                <form onSubmit={handleVerifyOtp} className="animate-in">
                                    <div className="mb-4">
                                        <label className="form-label fw-semibold d-flex align-items-center justify-content-between">
                                            <span>
                                                <i className="fas fa-key me-2" />
                                                Mã OTP
                                            </span>
                                            <span className="otp-hint">
                                                Gửi tới <strong>{email}</strong>
                                            </span>
                                        </label>

                                        <OtpInput
                                            length={6}
                                            value={otp}
                                            onChange={setOtp}
                                            disabled={loading}
                                            autoFocus
                                        />

                                        {/* Timer ring + resend */}
                                        <div className="d-flex align-items-center justify-content-between mt-3">
                                            <div className="timer">
                                                <span className="timer-ring">
                                                    <svg width="28" height="28" viewBox="0 0 36 36" className="circular">
                                                        <path
                                                            className="bg"
                                                            d="M18 2.0845
                                 a 15.9155 15.9155 0 0 1 0 31.831
                                 a 15.9155 15.9155 0 0 1 0 -31.831"
                                                        />
                                                        <path
                                                            className="progress"
                                                            style={{
                                                                strokeDasharray: `${Math.max(
                                                                    0,
                                                                    (countdown / 180) * 100
                                                                )}, 100`,
                                                            }}
                                                            d="M18 2.0845
                                 a 15.9155 15.9155 0 0 1 0 31.831
                                 a 15.9155 15.9155 0 0 1 0 -31.831"
                                                        />
                                                    </svg>
                                                </span>
                                                <span className="timer-text">
                                                    {countdown > 0 ? `Hết hạn sau ${formatTime(countdown)}` : "OTP đã hết hạn"}
                                                </span>
                                            </div>

                                            <button
                                                type="button"
                                                className="btn btn-sm btn-outline-secondary rounded-pill px-3"
                                                onClick={handleResendOtp}
                                                disabled={countdown > 0 || loading}
                                            >
                                                <i className="fas fa-redo me-2" />
                                                {countdown > 0 ? "Chờ..." : "Gửi lại mã"}
                                            </button>
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        className="btn btn-lg w-100 text-white fw-bold accent-btn mb-2"
                                        disabled={loading || otp.replace(/\D/g, "").length !== 6}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" />
                                                Đang xác minh...
                                            </>
                                        ) : (
                                            <>
                                                <i className="fas fa-shield-alt me-2" />
                                                Xác minh OTP
                                            </>
                                        )}
                                    </button>

                                    <div className="text-center small text-muted">
                                        Lưu ý: Mã OTP chỉ có hiệu lực trong 03 phút.
                                    </div>
                                </form>
                            )}

                            {/* Step 3 */}
                            {step === 3 && (
                                <form onSubmit={handleResetPassword} className="animate-in">
                                    <PasswordField
                                        id="new-pass"
                                        label="Mật khẩu mới"
                                        value={newPassword}
                                        onChange={(e) => setNewPassword(e.target.value)}
                                        placeholder="Nhập mật khẩu mới"
                                        minLength={6}
                                    />

                                    {/* Strength meter */}
                                    <div className="strength-meter mb-4" aria-hidden="true">
                                        <div className={`bar ${passwordStrength >= 1 ? "on" : ""}`} />
                                        <div className={`bar ${passwordStrength >= 2 ? "on" : ""}`} />
                                        <div className={`bar ${passwordStrength >= 3 ? "on" : ""}`} />
                                        <div className={`bar ${passwordStrength >= 4 ? "on" : ""}`} />
                                    </div>

                                    <PasswordField
                                        id="confirm-pass"
                                        label="Xác nhận mật khẩu"
                                        value={confirmPassword}
                                        onChange={(e) => setConfirmPassword(e.target.value)}
                                        placeholder="Nhập lại mật khẩu mới"
                                        minLength={6}
                                    />

                                    <button
                                        type="submit"
                                        className="btn btn-lg w-100 text-white fw-bold accent-btn"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2" />
                                                Đang cập nhật...
                                            </>
                                        ) : (
                                            <>
                                                <i className="fas fa-save me-2" />
                                                Đặt lại mật khẩu
                                            </>
                                        )}
                                    </button>
                                </form>
                            )}

                            {/* Step 4 */}
                            {step === 4 && (
                                <div className="text-center animate-in">
                                    <div className="mb-4 success-anim">
                                        <i className="fas fa-check-circle fa-5x text-success mb-3" />
                                        <h4 className="text-success mb-3">🎉 Hoàn tất!</h4>
                                        <p className="lead">Mật khẩu của bạn đã được đặt lại thành công.</p>
                                        <p className="text-muted">Bạn có thể đăng nhập bằng mật khẩu mới ngay bây giờ.</p>
                                    </div>
                                    <button
                                        className="btn btn-lg text-white fw-bold accent-btn"
                                        onClick={() => navigate("/login")}
                                    >
                                        <i className="fas fa-sign-in-alt me-2" />
                                        Đăng nhập ngay
                                    </button>
                                </div>
                            )}

                            {/* Back link */}
                            {step < 4 && (
                                <div className="text-center mt-4">
                                    <Link to="/login" className="text-decoration-none back-link">
                                        <i className="fas fa-arrow-left me-2" />
                                        Quay lại đăng nhập
                                    </Link>
                                </div>
                            )}

                            {/* Modal */}
                            <Modal
                                visible={modal.visible}
                                title={modal.title}
                                message={modal.message}
                                type={modal.type}
                                showConfirm={modal.showConfirm}
                                confirmText={modal.confirmText}
                                onClose={closeModal}
                                onConfirm={() => {
                                    if (typeof modal.onConfirm === 'function') modal.onConfirm();
                                    else closeModal();
                                }}
                            />

                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
