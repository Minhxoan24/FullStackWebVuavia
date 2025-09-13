


import React, { useState, useContext, useEffect } from 'react';
import Logo from '../../Assets/Logo/Logo';
import { FiSearch } from 'react-icons/fi';
import './Header.css';
import ModalLogin from '../Modal/ModalLogin/ModalLogin';
import { AuthContext } from '../../Context/AuthContext';
import { useNavigate, Link, NavLink } from 'react-router-dom';
import DefaultAvt from '../../Assets/Logo/Logo';


const Header = () => {
    const [showModal, setShowModal] = useState(false);
    const { user, logout } = useContext(AuthContext);
    const [balance, setBalance] = useState(0);
    const navigate = useNavigate();

    const handleClickLogo = () => {
        navigate('/');
    };
    const handleClickMyOrders = () => {
        navigate('/my-orders');
    };
    const handleClickPageAccount = () => {
        navigate('/account');
    };
    const handleClickRecharge = () => {

    };
    const handleClickTransactionHistory = () => {

    };
    const handleClickAccount = () => {
        navigate('/account');
    };
    const handleClickLogout = () => {
        navigate('/');
        logout();
    };

    const handleLoginClick = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    useEffect(() => {
        if (user?.balance) {
            setBalance(user.balance);
        } else {
            setBalance(0);
        }
    }, [user]);

    return (
        <div class Name='header-container'>
            <header className="header">
                {/* Logo */}
                <div className="logo-container">
                    <img
                        src={Logo.ImgLogo}
                        alt="VUA Logo"
                        className="logo"
                        onClick={handleClickLogo}
                    />
                </div>

                {/* Search */}
                <div className="search-container">
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Tìm sản phẩm"
                    />
                    <FiSearch className="search-icon" />
                </div>

                {/* Auth */}
                <div className="auth-container">
                    {!user ? (
                        <>
                            <span onClick={handleLoginClick}> Đăng nhập / Đăng Ký </span>

                        </>
                    ) : (
                        <div className="user-menu dropdown ">
                            <div className="user-info">
                                <img
                                    src={user.avatar || DefaultAvt}
                                    alt="avatar"
                                    className="avatar"
                                />
                                <span>{user.surname + " " + user.name}</span>
                                <div className="dropdown">
                                    <ul className="dropdown-menu">

                                        <li><Link className="dropdown-item" onClick={handleClickPageAccount} to="/account">Trang Tài Khoản</Link></li>
                                        <li><Link className="dropdown-item" onClick={handleClickMyOrders} to="/my-orders">Đơn Hàng Của Tôi</Link></li>
                                        <li><Link className="dropdown-item" onClick={handleClickAccount} to="/account"> Tài Khoản </Link></li>
                                        <li><Link className="dropdown-item" onClick={handleClickRecharge} to="/recharge"> Nạp Tiền </Link></li>
                                        <li><Link className="dropdown-item" onClick={handleClickTransactionHistory} to="/transaction-history">Lịch Sử Giao Dịch</Link></li>
                                        <li><Link className="dropdown-item" onClick={handleClickLogout} to="/">Đăng Xuất</Link></li>

                                    </ul>
                                </div>

                            </div>

                            <div className="balance-container">
                                <button className="balance-button">
                                    SỐ DƯ: {balance} đ
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </header>

            {/* Modal Login */}
            <ModalLogin show={showModal} handleClose={handleCloseModal} />
        </div>
    );
};

export default Header;