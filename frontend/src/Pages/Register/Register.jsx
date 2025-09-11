import React, { useState, useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { AuthContext } from "../../Context/AuthContext";

const Register = () => {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();
  const [form, setForm] = useState({
    accountname: "",
    password: "",
    email: "",
    surname: "",
    name: "",
    phone: "",
  });

  const handleChange = (e) =>
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (
      !form.accountname ||
      !form.password ||
      !form.email ||
      !form.surname ||
      !form.name ||
      !form.phone
    ) {
      alert("Vui lòng nhập đầy đủ thông tin");
      return;
    }
    try {
      await register({
        name: form.name,
        surname: form.surname,
        accountname: form.accountname,
        email: form.email,
        password: form.password,
        phone: form.phone,
      });
      alert("Đăng ký thành công");
      navigate("/"); // hoặc /login nếu không auto-login
    } catch (err) {
      alert(err.response?.data?.detail || err.message || "Đăng ký thất bại");
    }
  };

  return (
    <>
      <div className="register-page">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-md-6 col-lg-5">
              <div className="register-form-container bg-white rounded-4 shadow-lg p-5">
                <h2 className="text-center fw-bold mb-4 text-uppercase">
                  ĐĂNG KÝ
                </h2>

                <form
                  className="register-form"
                  onSubmit={handleSubmit}
                >
                  {/* Tên tài khoản */}
                  <div className="mb-3">
                    <label className="form-label fw-semibold text-dark">
                      Tên tài khoản *
                    </label>
                    <input
                      type="text"
                      name="accountname"
                      value={form.accountname}
                      onChange={handleChange}
                      required
                      className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                      placeholder="Nhập tên tài khoản"
                      style={{ backgroundColor: "#f8f9fa" }}
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
                      value={form.email}
                      onChange={handleChange}
                      required
                      className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                      placeholder="Nhập địa chỉ email"
                      style={{ backgroundColor: "#f8f9fa" }}
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
                      value={form.password}
                      onChange={handleChange}
                      required
                      className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                      placeholder="Nhập mật khẩu"
                      style={{ backgroundColor: "#f8f9fa" }}
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
                          value={form.surname}
                          onChange={handleChange}
                          required
                          className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                          placeholder="Nhập họ"
                          style={{ backgroundColor: "#f8f9fa" }}
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
                          value={form.name}
                          onChange={handleChange}
                          required
                          className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                          placeholder="Nhập tên"
                          style={{ backgroundColor: "#f8f9fa" }}
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
                      value={form.phone}
                      onChange={handleChange}
                      required
                      className="form-control form-control-lg bg-light border-0 rounded-3 px-3"
                      placeholder="Nhập số điện thoại"
                      style={{ backgroundColor: "#f8f9fa" }}
                    />
                  </div>

                  {/* Điều khoản */}
                  <div className="mb-4">
                    <p className="text-muted small">
                      Dữ liệu cá nhân của bạn sẽ được sử dụng để hỗ trợ trải nghiệm
                      của bạn trên toàn bộ trang web này, để quản lý quyền truy cập
                      vào tài khoản của bạn và cho các mục đích khác được mô tả
                      trong chính sách riêng tư của chúng tôi.
                    </p>
                  </div>

                  {/* Nút đăng ký */}
                  <button
                    type="submit"
                    className="btn btn-lg w-100 fw-bold rounded-3 text-white"
                    style={{
                      backgroundColor: "#ff6b35",
                      borderColor: "#ff6b35",
                      padding: "12px",
                    }}
                  >
                    ĐĂNG KÝ
                  </button>

                  {/* Link đăng nhập */}
                  <div className="text-center mt-4">
                    <p className="text-muted mb-0">
                      Đã có tài khoản?{" "}
                      <NavLink
                        to="/login"
                        className="text-decoration-none"
                        style={{ color: "#ff6b35" }}
                      >
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
};

export default Register;