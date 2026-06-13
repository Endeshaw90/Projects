import axios from "axios";

const axiosClient = axios.create({
  baseURL: "http://localhost:8080", 
});

axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  console.log(`[REQUEST] ${config.method?.toUpperCase()} ${config.url}`, config.data || "");
  return config;
});

axiosClient.interceptors.response.use(
  (response) => {
    console.log(`[RESPONSE] ${response.status} ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error(`[ERROR] ${error.response?.status} ${error.config?.url}`, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default axiosClient;

