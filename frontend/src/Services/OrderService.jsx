import apiClient from "./ApiService";

const CreateOrder = async (orderData) => {
    const order = {
        type_product_id: orderData.type_product_id,
        quantity: orderData.quantity,
        // voucher_id: orderData.voucher_id || null,
    }
    try {
        const response = await apiClient.post("/orders/checkout", order);
        return response.data;
    } catch (error) {
        console.error("Error creating order:", error);
        throw error;
    }
};

export default CreateOrder;