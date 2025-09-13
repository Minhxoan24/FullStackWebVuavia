import apiClient from "./ApiService";
const getProfile = async () => {
    try {
        const res = await apiClient.get("/Account/information"); // Sửa lại đường dẫn cho đúng với backend
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


const TransactionHistory = async () => {
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
        const res = await apiClient.get("/order/my-orders");
        return res.data;
    } catch (error) {
        console.error("Error fetching my orders:", error);
        throw error;
    }
};
const getMyOrderDetail = async (orderId) => {
    try {
        const res = await apiClient.get(`/order/orderDetail/${orderId}`);
        return res.data;
    } catch (error) {
        console.error("Error fetching my order details:", error);
        throw error;
    }
};



export { getProfile, updateProfile, changePassword, TransactionHistory, getMyVoucher, getMyOrder, getMyOrderDetail };
