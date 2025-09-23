import React, { useState, useContext, useMemo, useEffect } from "react";
import { Container, Row, Col, Card, ListGroup } from "react-bootstrap";
import { AuthContext } from "../../Context/AuthContext";
import "./PageAccount.css";

import MyAccount from "../../Pages/MyAccount/MyAccount.jsx";
import MyOrders from "../../Pages/MyOrder/MyOrder.jsx";
import TransactionHistory from "../../Pages/TransactionHistory/TransactionHistory.jsx";
import ReCharge from "../../Pages/ReCharge/ReCharge.jsx";
import OverView from "../../Pages/OverView/OverView.jsx";
import MyVoucher from "../MyVoucher/MyVoucher.jsx";
import HomePage from "../HomePage/HomePage.jsx";
import OrderDetail from "../OrderDetail/OrderDetail.jsx";

const PAGE_META = {
    OverView: { title: "TRANG TỔNG QUAN", subtitle: "TRANG TỔNG QUAN" },
    MyOrders: { title: "ĐƠN HÀNG CỦA BẠN", subtitle: "ĐƠN HÀNG CỦA BẠN" },
    TransactionHistory: { title: "LỊCH SỬ GIAO DỊCH", subtitle: "LỊCH SỬ GIAO DỊCH" },
    ReCharge: { title: "NẠP TIỀN", subtitle: "NẠP TIỀN" },
    MyAccount: { title: "THAY ĐỔI THÔNG TIN TÀI KHOẢN", subtitle: "THÔNG TIN TÀI KHOẢN" },
    promotions: { title: "KHUYẾN MÃI CỦA BẠN", subtitle: "KHUYẾN MÃI" },
};

const PageAccount = () => {
    const { user, logout } = useContext(AuthContext);
    const [activePage, setActivePage] = useState("OverView");
    const [orderDetailId, setOrderDetailId] = useState(null);  // Thêm state cho ID chi tiết

    const meta = useMemo(() => PAGE_META[activePage] ?? PAGE_META.OverView, [activePage]);

    useEffect(() => {
        document.title = `${meta.subtitle} · Vuavia`;
    }, [meta]);

    const renderContent = () => {
        switch (activePage) {
            case "OverView": return <OverView />;
            case "MyOrders": return <MyOrders onViewOrder={(id) => { setOrderDetailId(id); setActivePage("OrderDetail"); }} />;  // Truyền callback
            case "OrderDetail": return <OrderDetail orderDetailId={orderDetailId} />;  // Thêm case mới
            case "TransactionHistory": return <TransactionHistory />;
            case "ReCharge": return <ReCharge />;
            case "MyAccount": return <MyAccount />;
            case "promotions": return <MyVoucher />;
            case "logout": logout(); return <HomePage />;
            default: return <OverView />;
        }
    };

    return (
        <div>
            {/* HEADER — giống ảnh: nền xám, viền đen, title + subtitle */}
            <div className="page-header">
                <h1 className="page-title">{meta.title}</h1>
                <p className="page-subtitle">{meta.subtitle}</p>
            </div>

            <Container className="my-4">
                <Row>
                    {/* Sidebar */}
                    <Col md={3}>
                        <div className="shadow-sm p-3 text-center">
                            <img
                                src={
                                    (user?.avatar) ||
                                    "https://res.cloudinary.com/dkwvlimht/image/upload/v1758401193/bc439871417621836a0eeea768d60944_fvui3e.jpg"
                                }
                                alt="Avatar"
                                className="rounded-circle"
                                style={{ width: "100px", height: "100px" }}
                            />
                            <h6 className="mt-3 mb-0">
                                {(user?.surname ? user.surname + " " : "") + (user?.name || "User")}
                            </h6>
                            <small className="text-muted">{user?.email || "email@example.com"}</small>

                            <ListGroup className="mt-4 account-sidebar" variant="flush">
                                <ListGroup.Item action active={activePage === "OverView"} onClick={() => setActivePage("OverView")}>
                                    <i className="bi bi-speedometer2"></i> Trang tổng quan
                                </ListGroup.Item>
                                <ListGroup.Item action active={activePage === "MyOrders"} onClick={() => setActivePage("MyOrders")}>
                                    <i className="bi bi-receipt"></i> Đơn hàng của bạn
                                </ListGroup.Item>
                                <ListGroup.Item
                                    action
                                    active={activePage === "TransactionHistory"}
                                    onClick={() => setActivePage("TransactionHistory")}
                                >
                                    <i className="bi bi-clock-history"></i> Lịch sử giao dịch
                                </ListGroup.Item>
                                <ListGroup.Item action active={activePage === "ReCharge"} onClick={() => setActivePage("ReCharge")}>
                                    <i className="bi bi-wallet2"></i> Nạp tiền
                                </ListGroup.Item>
                                <ListGroup.Item action active={activePage === "MyAccount"} onClick={() => setActivePage("MyAccount")}>
                                    <i className="bi bi-person-lines-fill"></i> Thay đổi thông tin tài khoản
                                </ListGroup.Item>
                                <ListGroup.Item action active={activePage === "promotions"} onClick={() => setActivePage("promotions")}>
                                    <i className="bi bi-gift"></i> Khuyến mãi của bạn
                                </ListGroup.Item>
                                <ListGroup.Item action onClick={() => setActivePage("logout")}>
                                    <i className="bi bi-box-arrow-right"></i> Đăng xuất
                                </ListGroup.Item>
                            </ListGroup>
                        </div>
                    </Col>

                    {/* Main content */}
                    <Col md={9}>
                        <Card className="shadow-sm p-3 border-0">
                            <Card.Body>{renderContent()}</Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default PageAccount;
