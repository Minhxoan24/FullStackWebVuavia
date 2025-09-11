import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";
import Path from "../../Routes/Paths.jsx";

const ListItemNavbar = [
    { name: "Home", path: Path.HOME },
    { name: "Acc VIỆT", path: Path.ACC_VIET },
    { name: "Acc NGOẠI", path: Path.ACC_NGOAI },
    { name: "Acc XMDT", path: Path.ACC_XMDT },
    { name: "Acc 902", path: Path.ACC_902 },
    { name: "ZALO", path: Path.ZALO },
    { name: "CLONE", path: Path.CLONE },
    { name: "MAIL OUTLOOK", path: Path.OUTLOOK },
    { name: "SWITTER", path: Path.SWITTER },
    { name: "THỦ THUẬT", path: Path.THU_THUAT },
    { name: "Acc SPAM", path: Path.ACC_SPAM },
];

const Navbar = () => {
    return (
        <div className="navbar">
            {ListItemNavbar.map((i) => (    // Duyệt qua từng phần tử trong mảng ListItemNavbar
                <NavLink
                    key={i.path} // Sử dụng path làm key để đảm bảo duy nhất
                    to={i.path} // Đường dẫn đến trang tương ứng
                    className={({ isActive }) =>
                        `navbar-link ${isActive ? "active" : ""}`
                    }
                >
                    {i.name}
                </NavLink>
            ))}
        </div>
    );
};

export default Navbar;
