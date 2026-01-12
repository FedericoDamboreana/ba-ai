import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import StatusBadge from './StatusBadge';

describe('StatusBadge', () => {
  it('renders Active status correctly', () => {
    render(<StatusBadge status="Active" />);
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('renders On Hold status correctly', () => {
    render(<StatusBadge status="OnHold" />);
    expect(screen.getByText('On Hold')).toBeInTheDocument();
  });

  it('renders Completed status correctly', () => {
    render(<StatusBadge status="Completed" />);
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });

  it('renders Archived status correctly', () => {
    render(<StatusBadge status="Archived" />);
    expect(screen.getByText('Archived')).toBeInTheDocument();
  });

  it('renders In Progress status correctly', () => {
    render(<StatusBadge status="InProgress" />);
    expect(screen.getByText('In Progress')).toBeInTheDocument();
  });

  it('renders Generated status correctly', () => {
    render(<StatusBadge status="Generated" />);
    expect(screen.getByText('Generated')).toBeInTheDocument();
  });

  it('renders Draft status for unknown status', () => {
    render(<StatusBadge status="Unknown" />);
    expect(screen.getByText('Draft')).toBeInTheDocument();
  });
});
