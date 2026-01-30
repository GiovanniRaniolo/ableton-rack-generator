import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';
console.log("🔌 API Client Initialized. Target:", API_BASE_URL);

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  /**
   * List all available devices from the backend
   */
  getDevices: async () => {
    const response = await client.get('/devices');
    return response.data;
  },

  /**
   * Generate an ADG rack from a natural language prompt
   * @param {string} prompt - The description of the rack
   * @returns {Promise<{ filename: string, download_url: string, devices: string[] }>}
   */
  generateRack: async (prompt) => {
    const response = await client.post('/generate', { prompt });
    return response.data;
  },

  /**
   * Download a generated ADG file
   * @param {string} filename - The name of the file to download
   */
  downloadRack: (filename) => {
    window.location.href = `${API_BASE_URL}/download/${filename}`;
  },
};

export default api;
