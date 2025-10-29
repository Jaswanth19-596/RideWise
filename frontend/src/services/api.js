import axios from 'axios';

const API_BASE_URL =
  process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictionService = {
  getCurrentTime: () => api.get('/current-time'),
  getRegions: () => api.get('/regions'),
  predictRegion: (regionId) => api.get(`/predict/${regionId}`),
  predictAllRegions: () => api.get('/predict-all'),
};

export default api;
