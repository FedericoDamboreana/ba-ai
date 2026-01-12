import api from './api';

export const generationApi = {
  generate: async (itemId) => {
    const response = await api.post(`/items/${itemId}/generate`);
    return response.data;
  },

  regenerate: async (itemId, feedback) => {
    const response = await api.post(`/items/${itemId}/regenerate`, { feedback });
    return response.data;
  },

  export: async (itemId) => {
    const response = await api.get(`/items/${itemId}/export`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default generationApi;
