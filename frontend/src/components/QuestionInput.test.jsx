import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import QuestionInput from './QuestionInput';

describe('QuestionInput', () => {
  describe('Text type', () => {
    it('renders textarea for text questions', () => {
      const question = { id: 1, question_type: 'Text' };
      render(<QuestionInput question={question} value="" onChange={() => {}} />);
      expect(screen.getByPlaceholderText('Enter your answer...')).toBeInTheDocument();
    });

    it('calls onChange when text is entered', () => {
      const onChange = vi.fn();
      const question = { id: 1, question_type: 'Text' };
      render(<QuestionInput question={question} value="" onChange={onChange} />);

      fireEvent.change(screen.getByPlaceholderText('Enter your answer...'), {
        target: { value: 'Test answer' },
      });
      expect(onChange).toHaveBeenCalledWith('Test answer');
    });
  });

  describe('MultipleChoice type', () => {
    const mcQuestion = {
      id: 1,
      question_type: 'MultipleChoice',
      options: ['Option A', 'Option B', 'Option C'],
    };

    it('renders radio buttons for each option', () => {
      render(<QuestionInput question={mcQuestion} value="" onChange={() => {}} />);
      expect(screen.getByText('Option A')).toBeInTheDocument();
      expect(screen.getByText('Option B')).toBeInTheDocument();
      expect(screen.getByText('Option C')).toBeInTheDocument();
    });

    it('selects the correct option based on value', () => {
      render(<QuestionInput question={mcQuestion} value="Option B" onChange={() => {}} />);
      const radios = screen.getAllByRole('radio');
      expect(radios[1]).toBeChecked();
    });

    it('calls onChange when option is selected', () => {
      const onChange = vi.fn();
      render(<QuestionInput question={mcQuestion} value="" onChange={onChange} />);

      fireEvent.click(screen.getByText('Option A'));
      expect(onChange).toHaveBeenCalledWith('Option A');
    });
  });

  describe('Checkbox type', () => {
    const cbQuestion = {
      id: 1,
      question_type: 'Checkbox',
      options: ['Check A', 'Check B', 'Check C'],
    };

    it('renders checkboxes for each option', () => {
      render(<QuestionInput question={cbQuestion} value="" onChange={() => {}} />);
      const checkboxes = screen.getAllByRole('checkbox');
      expect(checkboxes).toHaveLength(3);
    });

    it('checks the correct options based on value', () => {
      render(<QuestionInput question={cbQuestion} value="Check A, Check C" onChange={() => {}} />);
      const checkboxes = screen.getAllByRole('checkbox');
      expect(checkboxes[0]).toBeChecked();
      expect(checkboxes[1]).not.toBeChecked();
      expect(checkboxes[2]).toBeChecked();
    });

    it('calls onChange with updated values when checkbox is clicked', () => {
      const onChange = vi.fn();
      render(<QuestionInput question={cbQuestion} value="Check A" onChange={onChange} />);

      fireEvent.click(screen.getAllByRole('checkbox')[1]);
      expect(onChange).toHaveBeenCalledWith('Check A, Check B');
    });
  });
});
