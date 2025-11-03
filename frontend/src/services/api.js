import axios from 'axios';

// const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://backend:8000/api';
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictionService = {
  getRegions: () => api.get('/regions'),
  predictRegion: (regionId) => api.get(`/predict/${regionId}`),
  predictAllRegions: (regionId) => api.get(`/predict-all/${regionId}`),
};

export default api;
