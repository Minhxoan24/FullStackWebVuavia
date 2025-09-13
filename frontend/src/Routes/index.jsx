import React from 'react';
import { Routes, Route } from 'react-router-dom'; /* Routes là component bao bọc chứa các Route. Nó dùng để tổ chức và quản lý các tuyến đường trong ứng dụng.
Route định nghĩa một đường dẫn (URL) cụ thể và component sẽ hiển thị khi người dùng truy cập đường dẫn đó. */
import HomePage from '../Pages/HomePage/HomePage.jsx';
import AccViet from '../Pages/AccViet/AccViet.jsx';
import ThuThuat from '../Pages/ThuThuat/ThuThuat.jsx';
import Switter from '../Pages/Switter/Switter.jsx';
import AccNgoai from '../Pages/AccNgoai/AccNgoai.jsx';
import Acc902 from '../Pages/Acc902/Acc902.jsx';
import AccSpam from '../Pages/AccSpam/AccSpam.jsx';
import Clone from '../Pages/Clone/Clone.jsx';
import MailOutLook from '../Pages/MailOutLook/MailOutLook.jsx';
import AccXmdt from '../Pages/AccXmdt/AccXmdt.jsx';
import Zalo from '../Pages/Zalo/Zalo.jsx';
import Path from './Paths.jsx';
import MainLayout from '../Layouts/MainLayout.jsx';
import Register from '../Pages/Register/Register.jsx';
import Login from '../Pages/Login/Login.jsx';
import TIPS from '../Pages/ShareNew/Tips/Tips.jsx';
import TipCreateADS from '../Pages/ShareNew/TipCreateADS/TipCreateADS.jsx';
import TipUseface from '../Pages/ShareNew/TipUseFace/TipUseFace.jsx';
import ProxyTutorial from '../Pages/ShareNew/ProxyTutorial/ProxyTutorial.jsx';

import MyAccount from '../Pages/MyAccount/MyAccount.jsx';
import MyOrders from '../Pages/MyOrder/MyOrder.jsx';
import OrderDetail from '../Pages/OrderDetail/OrderDetail.jsx';
import TransactionHistory from '../Pages/TransactionHistory/TransactionHistory.jsx';
import ReCharge from '../Pages/ReCharge/ReCharge.jsx';
import OverView from '../Pages/OverView/OverView.jsx';
import PageAccount from '../Pages/PageAccount/PageAccount.jsx';

const AppRoutes = () => {
    return (
        <Routes>
            <Route element={<MainLayout />}>
                <Route path={Path.HOME} element={<HomePage />} />
                <Route path={Path.ACC_VIET} element={<AccViet />} />
                <Route path={Path.ACC_NGOAI} element={<AccNgoai />} />
                <Route path={Path.ACC_XMDT} element={<AccXmdt />} />
                <Route path={Path.ACC_902} element={<Acc902 />} />
                <Route path={Path.ZALO} element={<Zalo />} />
                <Route path={Path.CLONE} element={<Clone />} />
                <Route path={Path.OUTLOOK} element={<MailOutLook />} />
                <Route path={Path.SWITTER} element={<Switter />} />
                <Route path={Path.THU_THUAT} element={<ThuThuat />} />
                <Route path={Path.ACC_SPAM} element={<AccSpam />} />
                <Route path={Path.REGISTER} element={<Register />} />
                <Route path={Path.LOGIN} element={<Login />} />
                <Route path={Path.TIPS} element={<TIPS />} />
                <Route path={Path.TIP_USE_FACE} element={<TipUseface />} />
                <Route path={Path.TIP_CREATE_ADS} element={<TipCreateADS />} />
                <Route path={Path.PROXY_TUTORIAL} element={<ProxyTutorial />} />
                <Route path={Path.MY_ACCOUNT} element={<MyAccount />} />
                <Route path={Path.MY_ORDERS} element={<MyOrders />} />
                <Route path={Path.TRANSACTION_HISTORY} element={<TransactionHistory />} />
                <Route path={Path.RECHARGE} element={<ReCharge />} />
                <Route path={Path.OVERVIEW} element={<OverView />} />
                <Route path={Path.ORDER_DETAIL} element={<OrderDetail />} />
                <Route path={Path.PAGE_ACCOUNT} element={<PageAccount />} />
            </Route>

        </Routes>

    );
}
export default AppRoutes;