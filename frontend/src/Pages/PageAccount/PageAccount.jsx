import React, { useState, useContext } from "react";
import { Container, Row, Col, Card, ListGroup } from "react-bootstrap";
import { AuthContext } from '../../Context/AuthContext';
import './PageAccount.css';


import MyAccount from '../../Pages/MyAccount/MyAccount.jsx';
import MyOrders from '../../Pages/MyOrder/MyOrder.jsx';

import TransactionHistory from '../../Pages/TransactionHistory/TransactionHistory.jsx';
import ReCharge from '../../Pages/ReCharge/ReCharge.jsx';
import OverView from '../../Pages/OverView/OverView.jsx';
import MyVoucher from "../MyVoucher/MyVoucher.jsx";
import HomePage from "../HomePage/HomePage.jsx";



const PageAccount = () => {
    const { user, logout } = useContext(AuthContext);
    const [activePage, setActivePage] = useState("OverView");

    // map tên page với component
    const renderContent = () => {
        switch (activePage) {
            case "OverView": return <OverView />;
            case "MyOrders": return <MyOrders />;
            case "TransactionHistory": return <TransactionHistory />;
            case "ReCharge": return <ReCharge />;
            case "MyAccount": return <MyAccount />;
            case "promotions": return <MyVoucher />;
            case "logout": logout(); return <HomePage />;
            default: return <OverView />;

        }

    };

    return (
        <Container className="my-4">
            <Row>
                {/* Sidebar */}
                <Col md={3}>
                    <div className="shadow-sm p-3 text-center">
                        <img
                            src={user.avatar || "https://via.placeholder.com/100"}
                            alt="Avatar"
                            className="rounded-circle"
                            style={{ width: "100px", height: "100px" }}
                        />
                        <h6 className="mt-3 mb-0">{user.surname + ' ' + user.name}</h6>
                        <small className="text-muted">{user.email}</small>

                        <ListGroup className="mt-4 account-sidebar" variant="flush">
                            <ListGroup.Item
                                action
                                active={activePage === "OverView"}
                                onClick={() => setActivePage("OverView")}
                            >
                                <i className="bi bi-speedometer2"></i> Trang tổng quan
                            </ListGroup.Item>
                            <ListGroup.Item
                                action
                                active={activePage === "MyOrders"}
                                onClick={() => setActivePage("MyOrders")}
                            >
                                <i className="bi bi-receipt"></i> Đơn hàng của bạn
                            </ListGroup.Item>
                            <ListGroup.Item
                                action
                                active={activePage === "TransactionHistory"}
                                onClick={() => setActivePage("TransactionHistory")}
                            >
                                <i className="bi bi-clock-history"></i> Lịch sử giao dịch
                            </ListGroup.Item>
                            <ListGroup.Item
                                action
                                active={activePage === "ReCharge"}
                                onClick={() => setActivePage("ReCharge")}
                            >
                                <i className="bi bi-wallet2"></i> Nạp tiền
                            </ListGroup.Item>
                            <ListGroup.Item
                                action
                                active={activePage === "MyAccount"}
                                onClick={() => setActivePage("MyAccount")}
                            >
                                <i className="bi bi-person-lines-fill"></i> Thay đổi thông tin tài khoản
                            </ListGroup.Item>
                            <ListGroup.Item
                                action
                                active={activePage === "promotions"}
                                onClick={() => setActivePage("promotions")}
                            >
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
                        <Card.Body>
                            {renderContent()}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default PageAccount;
