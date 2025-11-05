import axios from 'axios';

const stage = 'production';

const API_BASE_URL = stage === 'local' ? 'http://localhost:8000/api' : '/api';

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
