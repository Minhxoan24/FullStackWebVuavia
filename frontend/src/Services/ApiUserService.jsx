import apiClient from "./ApiService";
const getProfile = async () => {
    try {
        const res = await apiClient.get("/account/information");
        return res.data;
    } catch (error) {
        console.error("Error fetching profile:", error);
        throw error;
    }
};

const updateProfile = async (data) => {
    try {
        const res = await apiClient.put("/account/information", data);
        return res.data;
    } catch (error) {
        console.error("Error updating profile:", error);
        throw error;
    }
};

const changePassword = async (data) => {
    try {
        const res = await apiClient.put("/account/change-password", data);
        return res.data;
    } catch (error) {
        console.error("Error changing password:", error);
        throw error;
    }
};
export { getProfile, updateProfile, changePassword };
