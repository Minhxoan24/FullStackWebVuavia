import apiClient from "./ApiService";

const createDeposit = async (depositData) => {
    try {
        const res = await apiClient.post("/deposit/create", depositData);
        return res.data;
    } catch (error) {
        console.error("Error creating deposit:", error);
        throw error;
    }
};

const checkDepositStatus = async (transactionCode) => {
    try {
        const res = await apiClient.get(`/deposit/status/${transactionCode}`);
        return res.data;
    } catch (error) {
        console.error("Error checking deposit status:", error);
        throw error;
    }
};

export default { createDeposit, checkDepositStatus };


