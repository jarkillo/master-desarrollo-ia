/**
 * API client configuration
 */
import axios from 'axios';
import i18n from '../i18n/config';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging and i18n headers
apiClient.interceptors.request.use(
  (config) => {
    // Add Accept-Language header based on current i18n language
    const currentLanguage = i18n.language || 'es';
    config.headers['Accept-Language'] = currentLanguage;

    console.log(`[API] ${config.method?.toUpperCase()} ${config.url} (lang: ${currentLanguage})`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.status);
    return response;
  },
  (error) => {
    console.error('[API] Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
