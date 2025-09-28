import apiClient from "./ApiService";

const getProfile = async () => {
    try {
        const res = await apiClient.get("/Account/information");
        return res.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};

const updateProfile = async (data) => {
    try {
        const res = await apiClient.put("Account/update", data);
        return res.data;
    } catch (error) {
        console.error("Error updating profile:", error);
        throw error;
    }
};

const changePassword = async (data) => {
    try {
        const res = await apiClient.put("Account/change-password", data);
        return res.data;
    } catch (error) {
        console.error("Error changing password:", error);
        throw error;
    }
};

const GetTransactionHistory = async () => {
    try {
        const res = await apiClient.get("/transaction-history/my-transactions");
        return res.data;
    } catch (error) {
        console.error("Error fetching transaction history:", error);
        throw error;
    }
};

const getMyVoucher = async () => {
    try {
        const res = await apiClient.get("/voucher/my-vouchers");
        return res.data;
    } catch (error) {
        console.error("Error fetching my vouchers:", error);
        throw error;
    }
};

const getMyOrder = async () => {
    try {
        const res = await apiClient.get("/orders/my-orders");
        return res.data;
    } catch (error) {
        console.error("Error fetching my orders:", error);
        throw error;
    }
};

const getMyOrderDetail = async (order_detail_Id) => {
    try {
        const res = await apiClient.get(`/orders/order/orderDetail/${order_detail_Id}`);
        return res.data;
    } catch (error) {
        console.error("Error fetching my order details:", error);
        throw error;
    }
};

// ===== FORGOT PASSWORD FUNCTIONS =====
const requestPasswordResetOTP = async (email) => {
    try {
        const res = await apiClient.post("/Account/forgot-password/request-otp", { email });
        return res.data;
    } catch (error) {
        console.error("Error requesting password reset OTP:", error);
        throw error;
    }
};

const verifyPasswordResetOTP = async (email, otp) => {
    try {
        const res = await apiClient.post("/Account/forgot-password/verify-otp", { email, otp });
        return res.data;
    } catch (error) {
        console.error("Error verifying password reset OTP:", error);
        throw error;
    }
};

const resetPasswordWithOTP = async (email, otp, new_password) => {
    try {
        const res = await apiClient.post("/Account/forgot-password/reset", { 
            email, 
            otp, 
            new_password 
        });
        return res.data;
    } catch (error) {
        console.error("Error resetting password:", error);
        throw error;
    }
};

const uploadAvatar = async (formData) => {  // Sửa tham số từ file thành formData
    try {
        const res = await apiClient.post("/Account/avatar", formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return res.data; // assume {status, message}
    } catch (error) {
        console.error("Error uploading avatar:", error);
        throw error;
    }
};

export { 
    getProfile, 
    updateProfile, 
    changePassword, 
    uploadAvatar,
    GetTransactionHistory, 
    getMyVoucher, 
    getMyOrder, 
    getMyOrderDetail,
    // Forgot password exports
    requestPasswordResetOTP,
    verifyPasswordResetOTP,
    resetPasswordWithOTP
};
