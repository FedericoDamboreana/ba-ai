import api from './api';

export const generationApi = {
  generate: async (itemId) => {
    const response = await api.post(`/items/${itemId}/generate`, {});
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

    // Extract filename from Content-Disposition header
    // Supports both RFC 5987 filename*=UTF-8'' format and standard filename="..."
    const contentDisposition = response.headers['content-disposition'];
    let filename = `documentation-${itemId}.docx`;

    if (contentDisposition) {
      // Try filename*=UTF-8'' format first (RFC 5987 for non-ASCII characters)
      const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
      if (utf8Match) {
        try {
          filename = decodeURIComponent(utf8Match[1]);
        } catch {
          // Fall through to standard filename extraction
        }
      }

      // Fallback to standard filename="..." or filename=...
      if (filename === `documentation-${itemId}.docx`) {
        const standardMatch = contentDisposition.match(/filename="([^"]+)"/);
        if (standardMatch) {
          filename = standardMatch[1];
        } else {
          // Try without quotes: filename=something.docx
          const unquotedMatch = contentDisposition.match(/filename=([^;]+)/);
          if (unquotedMatch) {
            filename = unquotedMatch[1].trim();
          }
        }
      }
    }

    return { blob: response.data, filename };
  },
};

export default generationApi;
