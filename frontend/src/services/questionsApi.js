import api from './api';

export const questionsApi = {
  getByItem: async (itemId) => {
    const response = await api.get(`/items/${itemId}/questions`);
    return response.data;
  },

  updateAnswer: async (questionId, answer) => {
    const response = await api.put(`/questions/${questionId}`, { answer });
    return response.data;
  },

  validate: async (itemId) => {
    const response = await api.post(`/items/${itemId}/validate`);
    return response.data;
  },
};

export default questionsApi;
