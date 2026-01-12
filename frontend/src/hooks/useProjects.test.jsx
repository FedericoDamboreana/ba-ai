import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useProjects, useProject, useCreateProject } from './useProjects';
import projectsApi from '../services/projectsApi';

vi.mock('../services/projectsApi');

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useProjects hooks', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('useProjects', () => {
    it('fetches all projects', async () => {
      const mockProjects = [
        { id: 1, name: 'Project 1' },
        { id: 2, name: 'Project 2' },
      ];
      projectsApi.getAll.mockResolvedValue(mockProjects);

      const { result } = renderHook(() => useProjects(), {
        wrapper: createWrapper(),
      });

      await waitFor(() => expect(result.current.isSuccess).toBe(true));
      expect(result.current.data).toEqual(mockProjects);
      expect(projectsApi.getAll).toHaveBeenCalledWith(null);
    });

    it('fetches projects with status filter', async () => {
      projectsApi.getAll.mockResolvedValue([]);

      const { result } = renderHook(() => useProjects('Active'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => expect(result.current.isSuccess).toBe(true));
      expect(projectsApi.getAll).toHaveBeenCalledWith('Active');
    });
  });

  describe('useProject', () => {
    it('fetches a single project by id', async () => {
      const mockProject = { id: 1, name: 'Test Project' };
      projectsApi.getById.mockResolvedValue(mockProject);

      const { result } = renderHook(() => useProject(1), {
        wrapper: createWrapper(),
      });

      await waitFor(() => expect(result.current.isSuccess).toBe(true));
      expect(result.current.data).toEqual(mockProject);
      expect(projectsApi.getById).toHaveBeenCalledWith(1);
    });

    it('does not fetch when id is null', () => {
      const { result } = renderHook(() => useProject(null), {
        wrapper: createWrapper(),
      });

      expect(result.current.isLoading).toBe(false);
      expect(projectsApi.getById).not.toHaveBeenCalled();
    });
  });

  describe('useCreateProject', () => {
    it('creates a new project', async () => {
      const newProject = { name: 'New Project', description: 'Test' };
      const createdProject = { id: 1, ...newProject };
      projectsApi.create.mockResolvedValue(createdProject);

      const { result } = renderHook(() => useCreateProject(), {
        wrapper: createWrapper(),
      });

      result.current.mutate(newProject);

      await waitFor(() => expect(result.current.isSuccess).toBe(true));
      expect(projectsApi.create).toHaveBeenCalled();
      expect(projectsApi.create.mock.calls[0][0]).toEqual(newProject);
    });
  });
});
