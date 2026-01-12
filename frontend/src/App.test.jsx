import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

// Mock the API calls
vi.mock('./services/projectsApi', () => ({
  default: {
    getAll: vi.fn().mockResolvedValue([]),
  },
}));

describe('App', () => {
  it('renders the header with ba-ai logo', () => {
    render(<App />);
    const logo = screen.getByText('ba-ai');
    expect(logo).toBeInTheDocument();
  });

  it('renders the Projects link in navigation', () => {
    render(<App />);
    const projectsLink = screen.getByRole('link', { name: /projects/i });
    expect(projectsLink).toBeInTheDocument();
  });
});
