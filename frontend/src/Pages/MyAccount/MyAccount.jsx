import { AuthContext } from '../../Context/AuthContext';

import React, { useState, useContext, useEffect } from 'react';
const MyAccount = () => {
    const { user } = useContext(AuthContext);
    return (
        <div>
            <h1>Thông tin tài khoản</h1>
            <p>Họ tên: {user.name}</p>
            <p>Email: {user.email}</p>
        </div>
    )
};
export default MyAccount;