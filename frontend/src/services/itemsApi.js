import api from './api';

export const itemsApi = {
  getByProject: async (projectId) => {
    const response = await api.get(`/projects/${projectId}/items`);
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/items/${id}`);
    return response.data;
  },

  create: async (projectId, data) => {
    const response = await api.post(`/projects/${projectId}/items`, data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/items/${id}`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/items/${id}`);
    return response.data;
  },
};

export default itemsApi;
