import apiClient from "./ApiService";

const login = async (data) => {
  // Chuyển đổi username thành accountname để match với backend
  const loginData = {
    accountname: data.accountname,
    password: data.password
  };
  const res = await apiClient.post("/Account/login", loginData);
  return res.data;
};

const register = async (data) => {
  const res = await apiClient.post("/Account/register", data);
  return res.data;
};

const logout = async () => {
  try {
    await apiClient.post("/Account/logout");
  } catch (e) {
    // ignore if endpoint not present
  }
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  delete apiClient.defaults.headers.common['Authorization'];
};

export default { login, register, logout  };
