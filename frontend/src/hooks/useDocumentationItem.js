import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import itemsApi from '../services/itemsApi';

export function useProjectItems(projectId) {
  return useQuery({
    queryKey: ['items', projectId],
    queryFn: () => itemsApi.getByProject(projectId),
    enabled: !!projectId,
  });
}

export function useDocumentationItem(id) {
  return useQuery({
    queryKey: ['item', id],
    queryFn: () => itemsApi.getById(id),
    enabled: !!id,
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ projectId, data }) => itemsApi.create(projectId, data),
    onSuccess: (_, { projectId }) => {
      queryClient.invalidateQueries({ queryKey: ['items', projectId] });
    },
  });
}

export function useUpdateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }) => itemsApi.update(id, data),
    onSuccess: (data, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['item', id] });
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}

export function useDeleteItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: itemsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
