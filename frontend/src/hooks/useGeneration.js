import { useMutation, useQueryClient } from '@tanstack/react-query';
import generationApi from '../services/generationApi';

export function useGenerateDoc() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: generationApi.generate,
    onSuccess: (_, itemId) => {
      queryClient.invalidateQueries({ queryKey: ['item', itemId] });
    },
  });
}

export function useRegenerateDoc() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ itemId, feedback }) => generationApi.regenerate(itemId, feedback),
    onSuccess: (_, { itemId }) => {
      queryClient.invalidateQueries({ queryKey: ['item', itemId] });
    },
  });
}

export function useExportDoc() {
  return useMutation({
    mutationFn: generationApi.export,
    onSuccess: (blob, itemId) => {
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `documentation-${itemId}.docx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
  });
}
