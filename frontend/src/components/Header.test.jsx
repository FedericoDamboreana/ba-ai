import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Header from './Header';

describe('Header', () => {
  const renderWithRouter = () => {
    return render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>
    );
  };

  it('renders the ba-ai logo', () => {
    renderWithRouter();
    expect(screen.getByText('ba-ai')).toBeInTheDocument();
  });

  it('renders the Projects navigation link', () => {
    renderWithRouter();
    expect(screen.getByRole('link', { name: /projects/i })).toBeInTheDocument();
  });

  it('logo links to home page', () => {
    renderWithRouter();
    const logoLink = screen.getAllByRole('link')[0];
    expect(logoLink).toHaveAttribute('href', '/');
  });
});
