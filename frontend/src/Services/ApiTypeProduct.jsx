import apiClient from "./ApiService";
const getAllProductswithcategory = async () => {
    try {
        const res = await apiClient.get("/type-product/list-TypeProduct-with-Category");  // Thay đổi endpoint
        return res.data;
    } catch (error) {
        console.error("Error fetching products:", error);
        throw error;
    }
}
const getAllTypeProducts = async () => {
    try {
        const res = await apiClient.get("/type-product/list");
        return res.data;
    } catch (error) {
        console.error("Error fetching all type products:", error);
        throw error;
    }
}
const getAllTypeProductByIdCategory = async (id) => {
    try {
        const res = await apiClient.get(`/type-product/list-by-category/${id}`);
        return res.data;
    }
    catch (error) {
        console.error("Error fetching type products by category ID:", error);
        throw error;
    }
}
const getTypeProductById = async (id) => {
    try {
        const res = await apiClient.get(`/type-product/Detail/${id}`);
        return res.data;
    } catch (error) {
        console.error("Error fetching type product by ID:", error);
        throw error;
    }
}
const postTypeProduct = async (productData) => {
    try {
        const res = await apiClient.post("/type-product/create", productData);
        return res.data;
    } catch (error) {
        console.error("Error creating type product:", error);
        throw error;
    }
}
const putTypeProduct = async (id, productData) => {
    try {
        const res = await apiClient.put(`/type-product/update/${id}`, productData);
        return res.data;
    } catch (error) {
        console.error("Error updating type product:", error);
        throw error;
    }
}
const deleteTypeProduct = async (id) => {
    try {
        const res = await apiClient.delete(`/type-product/delete/${id}`);
        return res.data;
    } catch (error) {
        console.error("Error deleting type product:", error);
        throw error;
    }
}
const getListtypeproductByCateGory = async (id_category) => {
    try {
        const res = await apiClient.get(`/type-product/list-TypeProduct/${id_category}`);
        return res.data;
    } catch (error) {
        console.error("Error fetching type products by category:", error);
        throw error;
    }
}

export { getAllProductswithcategory, getAllTypeProducts, getAllTypeProductByIdCategory, getTypeProductById, postTypeProduct, putTypeProduct, deleteTypeProduct, getListtypeproductByCateGory };
