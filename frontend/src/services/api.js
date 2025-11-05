import axios from 'axios';

const API_BASE_URL =
  process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictionService = {
  getRegions: () => api.get('/regions'),
  predictRegion: (regionId) => api.get(`/predict/${regionId}`),
  predictAllRegions: () => api.get(`/predict-all/`),
};

export default api;
