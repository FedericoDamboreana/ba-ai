import QuestionRow from './QuestionRow';

function QuestionList({ questions, onSaveAnswer, isSaving }) {
  if (!questions || questions.length === 0) {
    return (
      <div className="text-center py-8 text-secondary">
        No questions generated yet.
      </div>
    );
  }

  // Filter questions based on trigger conditions
  const visibleQuestions = questions.filter((question) => {
    if (!question.trigger_condition) return true;

    const { parent_question_id, required_answer } = question.trigger_condition;
    if (!parent_question_id) return true;

    const parentQuestion = questions.find((q) => q.id === parent_question_id);
    if (!parentQuestion || !parentQuestion.is_answered) return false;

    if (Array.isArray(required_answer)) {
      return required_answer.includes(parentQuestion.answer);
    }
    return parentQuestion.answer === required_answer;
  });

  const answeredCount = visibleQuestions.filter((q) => q.is_answered).length;
  const totalCount = visibleQuestions.length;
  const criticalCount = visibleQuestions.filter((q) => q.is_critical).length;
  const answeredCriticalCount = visibleQuestions.filter(
    (q) => q.is_critical && q.is_answered
  ).length;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <p className="text-secondary">
          {answeredCount}/{totalCount} answered
        </p>
        {criticalCount > 0 && answeredCriticalCount < criticalCount && (
          <p className="text-warning text-sm">
            {answeredCriticalCount}/{criticalCount} required questions answered
          </p>
        )}
      </div>

      <div className="space-y-3">
        {visibleQuestions.map((question) => (
          <QuestionRow
            key={question.id}
            question={question}
            onSaveAnswer={onSaveAnswer}
            isSaving={isSaving}
          />
        ))}
      </div>
    </div>
  );
}

export default QuestionList;
