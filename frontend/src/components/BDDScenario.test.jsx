import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import BDDScenario from './BDDScenario';

describe('BDDScenario', () => {
  const mockScenario = {
    scenario_name: 'User logs in successfully',
    given: ['the user is on the login page', 'the user has valid credentials'],
    when: ['the user enters their email and password', 'the user clicks login'],
    then: ['the user is redirected to the dashboard', 'a welcome message is displayed'],
  };

  beforeEach(() => {
    vi.clearAllMocks();
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn().mockResolvedValue(undefined),
      },
    });
  });

  it('renders scenario name', () => {
    render(<BDDScenario scenario={mockScenario} />);
    expect(screen.getByText('User logs in successfully')).toBeInTheDocument();
  });

  it('renders Given steps', () => {
    render(<BDDScenario scenario={mockScenario} />);
    expect(screen.getByText('the user is on the login page')).toBeInTheDocument();
    expect(screen.getByText('the user has valid credentials')).toBeInTheDocument();
  });

  it('renders When steps', () => {
    render(<BDDScenario scenario={mockScenario} />);
    expect(screen.getByText('the user enters their email and password')).toBeInTheDocument();
    expect(screen.getByText('the user clicks login')).toBeInTheDocument();
  });

  it('renders Then steps', () => {
    render(<BDDScenario scenario={mockScenario} />);
    expect(screen.getByText('the user is redirected to the dashboard')).toBeInTheDocument();
    expect(screen.getByText('a welcome message is displayed')).toBeInTheDocument();
  });

  it('copies scenario to clipboard when copy button is clicked', async () => {
    render(<BDDScenario scenario={mockScenario} />);
    const copyButton = screen.getByRole('button');

    fireEvent.click(copyButton);

    expect(navigator.clipboard.writeText).toHaveBeenCalled();
  });
});
