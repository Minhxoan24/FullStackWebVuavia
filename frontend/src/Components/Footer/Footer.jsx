import React from 'react';
import { NavLink } from 'react-router-dom'; // nếu bạn đã dùng React Router
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css'; // optional: nếu bạn muốn custom thêm
import Logo from '../../Assets/Logo/Logo';

const Footer = () => {
    return (
        <footer className="bg-dark text-light pt-5 pb-4">
            <div className="container text-md-left">
                <div className="row">

                    {/* Cột 1: Thông tin và logo */}
                    <div className="col-md-5 col-lg-5 col-xl-5 mx-auto mb-4">
                        <div className="d-flex align-items-center mb-3">
                            <img src={Logo.ImgLogo} alt="Logo" width="200" height="70" />
                            <h5 className="ms-2 text-warning">vuavia</h5>
                        </div>
                        <p><strong>HỆ THỐNG CUNG CẤP TÀI NGUYÊN QUẢNG CÁO</strong></p>
                        <p><strong>Địa chỉ:</strong> Số 66 Nguyên Xá, Minh Khai, Từ Liêm, Hà Nội</p>
                        <p><strong>Email:</strong> cskhvuavia@gmail.com</p>
                        <p><strong>Website:</strong> <a className="text-warning" href="https://vuavia.vn">https://vuavia.vn</a></p>
                        <p><strong>Hỗ trợ:</strong> 8h00 – 23h00 tất cả các ngày</p>
                        <p className="text-warning fst-italic">Chúng tôi không chịu trách nhiệm cho hành vi sử dụng sai mục đích.</p>
                        <div className="d-flex mt-3 gap-2">
                            <img src="/images/bank.png" alt="Bank" height="30" />
                            <img src="/images/bitcoin.png" alt="Bitcoin" height="30" />
                            <img src="/images/mastercard.png" alt="MasterCard" height="30" />
                            <img src="/images/visa.png" alt="Visa" height="30" />
                        </div>
                    </div>

                    {/* Cột 2: Hướng dẫn */}
                    <div className="col-md-3 col-lg-3 col-xl-3 mx-auto mb-4">
                        <h6 className="text-uppercase fw-bold text-warning">Hướng dẫn</h6>
                        <ul className="list-unstyled">
                            <li><NavLink to="/huong-dan-dang-ky" className="text-light">Đăng ký tài khoản</NavLink></li>
                            <li><NavLink to="/huong-dan-mua-hang" className="text-light">Mua hàng</NavLink></li>
                            <li><NavLink to="/huong-dan-thanh-toan" className="text-light">Thanh toán</NavLink></li>
                            <li><NavLink to="/huong-dan-nap-tien" className="text-light">Nạp tiền</NavLink></li>
                            <li><NavLink to="/huong-dan-thay-doi" className="text-light">Thay đổi thông tin</NavLink></li>
                            <li><NavLink to="/huong-dan-tim-tai-khoan" className="text-light">Tìm tài khoản</NavLink></li>
                        </ul>
                    </div>

                    {/* Cột 3: Chính sách */}
                    <div className="col-md-3 col-lg-3 col-xl-3 mx-auto mb-4">
                        <h6 className="text-uppercase fw-bold text-warning">Chính sách</h6>
                        <ul className="list-unstyled">
                            <li><NavLink to="/chinh-sach-thu-mua" className="text-light">Thu mua</NavLink></li>
                            <li><NavLink to="/chinh-sach-hoan-tien" className="text-light">Hoàn tiền</NavLink></li>
                            <li><NavLink to="/chinh-sach-bao-mat" className="text-light">Bảo mật</NavLink></li>
                            <li><NavLink to="/chinh-sach-bao-hanh" className="text-light">Bảo hành</NavLink></li>
                            <li><NavLink to="/dieu-khoan" className="text-light">Điều khoản sử dụng</NavLink></li>
                            <li><NavLink to="/chinh-sach-du-lieu" className="text-light">Chính sách dữ liệu</NavLink></li>
                        </ul>
                    </div>

                </div>
            </div>
        </footer>
    );
};

export default Footer;