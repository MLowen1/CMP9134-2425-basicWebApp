import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  // Set the base URL for your backend API
  // Make sure this matches where your Flask backend is running
  baseURL: 'http://localhost:5000/api', // Adjust port if your backend runs elsewhere
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: Add an interceptor to include the auth token in requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optional: Add an interceptor to handle 401 Unauthorized responses (e.g., redirect to login)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized access, e.g., clear token and redirect
      localStorage.removeItem('token');
      // You might want to use window.location.href = '/login'; or trigger a logout state change
      console.error("Unauthorized access - 401");
      // Avoid infinite loops by not redirecting automatically here if the context itself causes it
    }
    return Promise.reject(error);
  }
);


export default api;
