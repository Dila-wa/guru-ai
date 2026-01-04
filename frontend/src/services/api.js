import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export const askQuestion = async (grade, subject, question) => {
  try {
    const response = await api.post('/api/v1/ask', {
      grade,
      subject,
      question,
    });
    return response.data;
  } catch (error) {
    console.error('Question API call failed:', error);
    throw error;
  }
};

export const getStatus = async () => {
  try {
    const response = await api.get('/api/v1/status');
    return response.data;
  } catch (error) {
    console.error('Status check failed:', error);
    throw error;
  }
};

export default api;
