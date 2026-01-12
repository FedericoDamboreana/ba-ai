import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ProjectCard from './ProjectCard';

const mockProject = {
  id: 1,
  name: 'Test Project',
  client: 'Test Client',
  description: 'This is a test project description',
  status: 'Active',
  doc_count: 5,
  updated_at: '2026-01-10T10:00:00Z',
};

describe('ProjectCard', () => {
  const renderWithRouter = (project) => {
    return render(
      <MemoryRouter>
        <ProjectCard project={project} />
      </MemoryRouter>
    );
  };

  it('renders project name', () => {
    renderWithRouter(mockProject);
    expect(screen.getByText('Test Project')).toBeInTheDocument();
  });

  it('renders client name', () => {
    renderWithRouter(mockProject);
    expect(screen.getByText('Test Client')).toBeInTheDocument();
  });

  it('renders project description', () => {
    renderWithRouter(mockProject);
    expect(screen.getByText('This is a test project description')).toBeInTheDocument();
  });

  it('renders status badge', () => {
    renderWithRouter(mockProject);
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('renders doc count', () => {
    renderWithRouter(mockProject);
    expect(screen.getByText('5 docs')).toBeInTheDocument();
  });

  it('links to project detail page', () => {
    renderWithRouter(mockProject);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/projects/1');
  });

  it('renders without client when not provided', () => {
    const projectWithoutClient = { ...mockProject, client: null };
    renderWithRouter(projectWithoutClient);
    expect(screen.queryByText('Test Client')).not.toBeInTheDocument();
  });
});
