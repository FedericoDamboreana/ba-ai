import { useState, useEffect } from 'react';
import { Check, Circle, ChevronDown, ChevronUp } from 'lucide-react';
import QuestionInput from './QuestionInput';

function QuestionRow({ question, onSaveAnswer, isSaving }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [answer, setAnswer] = useState(question.answer || '');
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    setAnswer(question.answer || '');
    setHasChanges(false);
  }, [question.answer]);

  const handleAnswerChange = (value) => {
    setAnswer(value);
    setHasChanges(value !== (question.answer || ''));
  };

  const handleSave = () => {
    onSaveAnswer(question.id, answer);
    setHasChanges(false);
    setIsExpanded(false);
  };

  const handleMarkNA = () => {
    onSaveAnswer(question.id, 'N/A');
    setAnswer('N/A');
    setHasChanges(false);
    setIsExpanded(false);
  };

  const isAnswered = question.is_answered;
  const isCritical = question.is_critical;

  return (
    <div className="border border-gray-800 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-start gap-3 p-4 hover:bg-surface/50 transition-colors text-left"
      >
        <div className="flex-shrink-0 mt-0.5">
          {isAnswered ? (
            <Check className="h-5 w-5 text-success" />
          ) : (
            <Circle className="h-5 w-5 text-secondary" />
          )}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start gap-2">
            <p className="text-primary">
              {question.question_text}
              {isCritical && <span className="text-error ml-1">*</span>}
            </p>
          </div>
          {isAnswered && !isExpanded && (
            <p className="text-sm text-secondary mt-1 truncate">
              {question.answer}
            </p>
          )}
        </div>

        <div className="flex-shrink-0">
          {isExpanded ? (
            <ChevronUp className="h-5 w-5 text-secondary" />
          ) : (
            <ChevronDown className="h-5 w-5 text-secondary" />
          )}
        </div>
      </button>

      {isExpanded && (
        <div className="px-4 pb-4 pt-2 border-t border-gray-800 bg-surface/30">
          <QuestionInput
            question={question}
            value={answer}
            onChange={handleAnswerChange}
          />

          <div className="flex items-center gap-3 mt-4">
            <button
              onClick={handleSave}
              disabled={isSaving || !hasChanges}
              className="px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Saving...' : 'Save Answer'}
            </button>

            {!isCritical && (
              <button
                onClick={handleMarkNA}
                disabled={isSaving}
                className="px-4 py-2 border border-gray-700 text-secondary hover:text-primary rounded-md transition-colors disabled:opacity-50"
              >
                Not Applicable
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuestionRow;
