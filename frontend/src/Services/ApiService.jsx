import axios from 'axios';
import { BASE_URL } from './BaseURL';  // import để lấy URL cơ sở của API

// Create axios instance
const apiClient = axios.create({   //  api default  will have BaseURL , header
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor to add token to headers
apiClient.interceptors.request.use((config) => { //config la tất cả thông tin của  request
  const token = localStorage.getItem('access_token'); // lấy token từ localStorage
  // nếu có token thì gắn vào header
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
},
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use((response) => response,
  async (error) => {
    const originalRequest = error.config; // Lưu request ban đầu để gọi lại nếu cần thiết , 

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // tránh lặp vô hạn

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const res = await axios.post(`${BASE_URL}/Account/refresh`, {  // Nếu backend có endpoint này
            token: refreshToken,
          });


          // Lưu token mới
          localStorage.setItem('access_token', res.data.access_token);
          localStorage.setItem('refresh_token', res.data.refresh_token);

          // Gắn lại token mới
          apiClient.defaults.headers.Authorization = `Bearer ${res.data.access_token}`;

          originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`; // Gắn token mới vào request ban đầu config = originalRequest

          // Gọi lại request ban đầu
          return apiClient(originalRequest);
        }
      }
      catch (refreshError) {
        // Refresh token cũng hết hạn => logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }

    return Promise.reject(error);
  }
);
export default apiClient;