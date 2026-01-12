import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import DeadlineWarning from './DeadlineWarning';

describe('DeadlineWarning', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-01-11'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('returns null when no deadline', () => {
    const { container } = render(<DeadlineWarning deadline={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('returns null when deadline is more than 3 days away', () => {
    const { container } = render(<DeadlineWarning deadline="2026-01-20" />);
    expect(container.firstChild).toBeNull();
  });

  it('shows "Due today" when deadline is today', () => {
    render(<DeadlineWarning deadline="2026-01-11" />);
    expect(screen.getByText('Due today')).toBeInTheDocument();
  });

  it('shows "Due in X days" when deadline is within 3 days', () => {
    render(<DeadlineWarning deadline="2026-01-13" />);
    expect(screen.getByText('Due in 2 days')).toBeInTheDocument();
  });

  it('shows "Due in 1 day" for singular day', () => {
    render(<DeadlineWarning deadline="2026-01-12" />);
    expect(screen.getByText('Due in 1 day')).toBeInTheDocument();
  });

  it('shows "Overdue by X days" when deadline has passed', () => {
    render(<DeadlineWarning deadline="2026-01-09" />);
    expect(screen.getByText('Overdue by 2 days')).toBeInTheDocument();
  });
});
