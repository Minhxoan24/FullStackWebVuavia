import React from 'react';
import Logo from '../../Assets/Logo/Logo';
import { FiSearch } from 'react-icons/fi';
import './Header.css';
import ModalLogin from '../Modal/ModalLogin/ModalLogin';
import { useState } from 'react';

import { useNavigate } from 'react-router-dom';
const Header = () => {

    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();
    const handleClickLogo = () => {
        navigate('/');
    }
    const handleLoginClick = () => {
        setShowModal(true);
    };
    const handleCloseModal = () => {
        setShowModal(false);
    };
    return (
        <>
            <header className="header">
                <div className="logo-container">
                    <img src={Logo.ImgLogo} alt="VUA Logo" className="logo" onClick={handleClickLogo} />
                </div>
                <div className="search-container">
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Tìm sản phẩm"
                    />
                    <FiSearch className="search-icon" />
                </div>
                <div className="auth-container">
                    <span className="auth-text" onClick={handleLoginClick}>Đăng nhập / Đăng ký</span>
                </div>
                <div className="balance-container">
                    <button className="balance-button">SỐ DƯ: 0 đ</button>
                </div>
            </header>
            {/* // xử lý modal đăng nhập */}
            <ModalLogin show={showModal} handleClose={handleCloseModal} />
        </>
    );
};

export default Header;
