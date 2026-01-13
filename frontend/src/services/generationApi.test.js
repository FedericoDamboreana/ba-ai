import { describe, it, expect, vi, beforeEach } from 'vitest';
import generationApi from './generationApi';
import api from './api';

// Mock the api module
vi.mock('./api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

describe('generationApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('generate', () => {
    it('calls the correct endpoint', async () => {
      const mockResponse = { data: { item_id: 1, content: {} } };
      api.post.mockResolvedValue(mockResponse);

      await generationApi.generate(123);

      expect(api.post).toHaveBeenCalledWith('/items/123/generate', {});
    });

    it('returns the response data', async () => {
      const mockData = { item_id: 1, content: { title: 'Test' } };
      api.post.mockResolvedValue({ data: mockData });

      const result = await generationApi.generate(1);

      expect(result).toEqual(mockData);
    });
  });

  describe('regenerate', () => {
    it('calls the correct endpoint with feedback', async () => {
      const mockResponse = { data: { item_id: 1, content: {} } };
      api.post.mockResolvedValue(mockResponse);

      await generationApi.regenerate(123, 'Make it better');

      expect(api.post).toHaveBeenCalledWith('/items/123/regenerate', {
        feedback: 'Make it better',
      });
    });
  });

  describe('export', () => {
    it('calls the correct endpoint with blob responseType', async () => {
      const mockBlob = new Blob(['test'], { type: 'application/octet-stream' });
      api.get.mockResolvedValue({
        data: mockBlob,
        headers: { 'content-disposition': 'attachment; filename="test.docx"' },
      });

      await generationApi.export(123);

      expect(api.get).toHaveBeenCalledWith('/items/123/export', {
        responseType: 'blob',
      });
    });

    describe('filename extraction', () => {
      it('extracts filename from standard quoted format', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition': 'attachment; filename="Project - Document.docx"',
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('Project - Document.docx');
      });

      it('extracts filename from UTF-8 encoded format (RFC 5987)', async () => {
        const mockBlob = new Blob(['test']);
        // URL-encoded Spanish characters
        const encodedFilename = 'Pedidos%20Ya%20-%20Tablero%20de%20Tickets.docx';
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition': `attachment; filename="fallback.docx"; filename*=UTF-8''${encodedFilename}`,
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('Pedidos Ya - Tablero de Tickets.docx');
      });

      it('extracts filename with special characters from UTF-8 format', async () => {
        const mockBlob = new Blob(['test']);
        // URL-encoded: "Gestión de Pedidos - Información.docx"
        const encodedFilename =
          'Gesti%C3%B3n%20de%20Pedidos%20-%20Informaci%C3%B3n.docx';
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition': `attachment; filename*=UTF-8''${encodedFilename}`,
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('Gestión de Pedidos - Información.docx');
      });

      it('falls back to standard filename when UTF-8 decoding fails', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            // Invalid UTF-8 encoding
            'content-disposition':
              'attachment; filename="fallback.docx"; filename*=UTF-8\'\'%invalid%',
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('fallback.docx');
      });

      it('extracts filename from unquoted format', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition': 'attachment; filename=simple.docx',
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('simple.docx');
      });

      it('uses default filename when no content-disposition header', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {},
        });

        const result = await generationApi.export(42);

        expect(result.filename).toBe('documentation-42.docx');
      });

      it('uses default filename when content-disposition has no filename', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition': 'attachment',
          },
        });

        const result = await generationApi.export(99);

        expect(result.filename).toBe('documentation-99.docx');
      });

      it('prefers UTF-8 filename over standard filename', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition':
              'attachment; filename="ascii-fallback.docx"; filename*=UTF-8\'\'%C3%A9special.docx',
          },
        });

        const result = await generationApi.export(1);

        // Should use UTF-8 version (éspecial.docx), not the ASCII fallback
        expect(result.filename).toBe('éspecial.docx');
      });

      it('handles filename with spaces correctly', async () => {
        const mockBlob = new Blob(['test']);
        api.get.mockResolvedValue({
          data: mockBlob,
          headers: {
            'content-disposition':
              'attachment; filename*=UTF-8\'\'My%20Project%20-%20My%20Document.docx',
          },
        });

        const result = await generationApi.export(1);

        expect(result.filename).toBe('My Project - My Document.docx');
      });
    });

    it('returns blob and filename', async () => {
      const mockBlob = new Blob(['test content']);
      api.get.mockResolvedValue({
        data: mockBlob,
        headers: {
          'content-disposition': 'attachment; filename="test.docx"',
        },
      });

      const result = await generationApi.export(1);

      expect(result.blob).toBe(mockBlob);
      expect(result.filename).toBe('test.docx');
    });
  });
});
