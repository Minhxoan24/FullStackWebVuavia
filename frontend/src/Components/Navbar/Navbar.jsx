import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

const ListItemNavbar = [
    { name: "Home", path: "/" },
    { name: "Acc VIỆT", path: "/mua-via-viet" },
    { name: "Acc NGOẠI", path: "/mua-via-ngoai" },
    { name: "Acc XMDT", path: "/mua-via-xmdt" },
    { name: "Acc 902", path: "/mua-via-902" },
    { name: "ZALO", path: "/mua-via-zalo" },
    { name: "CLONE", path: "/mua-via-clone" },
    { name: "MAIL OUTLOOK", path: "/mua-via-outlook" },
    { name: "SWITTER", path: "/mua-via-switter" },
    { name: "THỦ THUẬT", path: "/mua-via-thuthuat" },
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
