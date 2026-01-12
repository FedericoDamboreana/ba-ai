import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, FileText, Loader2 } from 'lucide-react';
import { useDocumentationItem } from '../hooks/useDocumentationItem';
import { useQuestions, useUpdateAnswer, useValidateItem } from '../hooks/useQuestions';
import { useGenerateDoc } from '../hooks/useGeneration';
import StatusBadge from '../components/StatusBadge';
import DeadlineWarning from '../components/DeadlineWarning';
import QuestionList from '../components/QuestionList';

function DocumentationItem() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: item, isLoading: itemLoading } = useDocumentationItem(id);
  const { data: questions, isLoading: questionsLoading } = useQuestions(id);
  const updateAnswer = useUpdateAnswer();
  const validateItem = useValidateItem();
  const generateDoc = useGenerateDoc();

  const handleSaveAnswer = async (questionId, answer) => {
    try {
      await updateAnswer.mutateAsync({ questionId, answer });
    } catch (err) {
      console.error('Failed to save answer:', err);
    }
  };

  const handleGenerate = async () => {
    try {
      // First validate
      const validation = await validateItem.mutateAsync(id);

      if (!validation.is_complete) {
        // More questions were added, they'll show in the list
        return;
      }

      // Generate documentation
      await generateDoc.mutateAsync(id);
      navigate(`/items/${id}/preview`);
    } catch (err) {
      console.error('Failed to generate:', err);
    }
  };

  if (itemLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-secondary">Loading...</div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-error">Documentation item not found</div>
      </div>
    );
  }

  // Check if already generated
  if (item.status === 'Generated' && item.generated_content) {
    navigate(`/items/${id}/preview`);
    return null;
  }

  const answeredCount = questions?.filter((q) => q.is_answered).length || 0;
  const totalCount = questions?.length || 0;
  const criticalQuestions = questions?.filter((q) => q.is_critical) || [];
  const allCriticalAnswered = criticalQuestions.every((q) => q.is_answered);
  const canGenerate = allCriticalAnswered && totalCount > 0;

  const isProcessing =
    updateAnswer.isPending || validateItem.isPending || generateDoc.isPending;

  return (
    <div className="pb-24">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-secondary mb-6">
        <Link to="/" className="hover:text-primary transition-colors">
          Projects
        </Link>
        <span>/</span>
        <Link
          to={`/projects/${item.project_id}`}
          className="hover:text-primary transition-colors"
        >
          Project
        </Link>
        <span>/</span>
        <span className="text-primary">{item.title}</span>
      </div>

      {/* Header */}
      <div className="bg-surface rounded-lg p-6 border border-gray-800 mb-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs text-secondary uppercase">
                {item.type}
              </span>
              <StatusBadge status={item.status} />
            </div>
            <h1 className="text-2xl font-bold mb-2">{item.title}</h1>
            <p className="text-secondary">{item.description}</p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <DeadlineWarning deadline={item.deadline} />
            <div className="text-sm text-secondary">
              {answeredCount}/{totalCount} answered
            </div>
          </div>
        </div>
      </div>

      {/* Questions */}
      {questionsLoading ? (
        <div className="text-secondary">Loading questions...</div>
      ) : (
        <QuestionList
          questions={questions}
          onSaveAnswer={handleSaveAnswer}
          isSaving={updateAnswer.isPending}
        />
      )}

      {/* Fixed Footer */}
      <div className="fixed bottom-0 left-0 right-0 bg-surface border-t border-gray-800 p-4">
        <div className="container mx-auto flex items-center justify-between">
          <Link
            to={`/projects/${item.project_id}`}
            className="flex items-center gap-2 text-secondary hover:text-primary transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Project
          </Link>

          <button
            onClick={handleGenerate}
            disabled={!canGenerate || isProcessing}
            className="flex items-center gap-2 px-6 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <FileText className="h-4 w-4" />
                Generate Documentation
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default DocumentationItem;
