import axios from 'axios';
import { BASE_URL } from './BaseURL';
// Create axios instance
const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

//  Request interceptor ( chặn yêu cầu )
apiClient.interceptors.request.use(
  (config) => {
    // Thêm token vào header nếu có
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
// Response interceptor ( chặn phản hồi )
apiClient.interceptors.response.use(
  (response) => {
    // Xử lý phản hồi thành công
    return response;
  },
  (error) => {
    // Xử lý lỗi
    if (error.response && error.response.status === 401) {
        // Xử lý trường hợp token hết hạn hoặc không hợp lệ
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    } 
    return Promise.reject(error);
  }
);
