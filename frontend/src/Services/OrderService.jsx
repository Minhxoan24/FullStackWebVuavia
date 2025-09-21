import apiClient from "./ApiService";

const CreateOrder = async (orderData) => {
    // Validation cơ bản
    if (!orderData.type_product_id || !orderData.quantity || orderData.quantity <= 0) {
        throw new Error("Dữ liệu đơn hàng không hợp lệ: thiếu type_product_id hoặc quantity không hợp lệ.");
    }
    if (orderData.discount_amount < 0) {
        throw new Error("Giảm giá không thể âm.");
    }

    const order = {
        type_product_id: orderData.type_product_id,
        quantity: orderData.quantity,
        discount_amount: orderData.discount_amount || 0  // Mặc định 0 nếu không có
    };

    try {
        const response = await apiClient.post("/orders/checkout", order);
        return response.data;
    } catch (error) {
        console.error("Lỗi tạo đơn hàng:", error);
        // Thêm xử lý lỗi chi tiết
        if (error.response) {
            throw new Error(`Lỗi server: ${error.response.status} - ${error.response.data.message || 'Không xác định'}`);
        } else {
            throw new Error("Lỗi kết nối mạng.");
        }
    }
};

export default CreateOrder;