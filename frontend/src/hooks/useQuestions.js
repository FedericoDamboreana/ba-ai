import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import questionsApi from '../services/questionsApi';

export function useQuestions(itemId) {
  return useQuery({
    queryKey: ['questions', itemId],
    queryFn: () => questionsApi.getByItem(itemId),
    enabled: !!itemId,
  });
}

export function useUpdateAnswer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ questionId, answer }) => questionsApi.updateAnswer(questionId, answer),
    onSuccess: (data) => {
      // Invalidate questions for this item
      queryClient.invalidateQueries({ queryKey: ['questions'] });
      queryClient.invalidateQueries({ queryKey: ['item'] });
    },
  });
}

export function useValidateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: questionsApi.validate,
    onSuccess: (_, itemId) => {
      queryClient.invalidateQueries({ queryKey: ['questions', itemId] });
      queryClient.invalidateQueries({ queryKey: ['item', itemId] });
    },
  });
}
