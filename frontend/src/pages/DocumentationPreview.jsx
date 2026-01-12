import { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Download,
  RefreshCw,
  Edit2,
  Loader2,
  X,
} from 'lucide-react';
import { useDocumentationItem, useUpdateItem } from '../hooks/useDocumentationItem';
import { useRegenerateDoc, useExportDoc } from '../hooks/useGeneration';
import DocumentationOutput from '../components/DocumentationOutput';

function DocumentationPreview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [showRegenerateModal, setShowRegenerateModal] = useState(false);
  const [feedback, setFeedback] = useState('');

  const { data: item, isLoading } = useDocumentationItem(id);
  const updateItem = useUpdateItem();
  const regenerateDoc = useRegenerateDoc();
  const exportDoc = useExportDoc();

  const handleContentUpdate = async (newContent) => {
    try {
      await updateItem.mutateAsync({
        id,
        data: { generated_content: newContent },
      });
    } catch (err) {
      console.error('Failed to update content:', err);
    }
  };

  const handleRegenerate = async () => {
    try {
      await regenerateDoc.mutateAsync({ itemId: id, feedback });
      setShowRegenerateModal(false);
      setFeedback('');
    } catch (err) {
      console.error('Failed to regenerate:', err);
    }
  };

  const handleExport = async () => {
    try {
      await exportDoc.mutateAsync(id);
    } catch (err) {
      console.error('Failed to export:', err);
    }
  };

  if (isLoading) {
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

  // Redirect if not generated yet
  if (!item.generated_content) {
    navigate(`/items/${id}`);
    return null;
  }

  const isProcessing = regenerateDoc.isPending || exportDoc.isPending;

  return (
    <div className="pb-8">
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
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link
            to={`/items/${id}`}
            className="flex items-center gap-2 text-secondary hover:text-primary transition-colors"
          >
            <Edit2 className="h-4 w-4" />
            Edit Answers
          </Link>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowRegenerateModal(true)}
            disabled={isProcessing}
            className="flex items-center gap-2 px-4 py-2 border border-gray-700 text-secondary hover:text-primary rounded-md transition-colors disabled:opacity-50"
          >
            <RefreshCw className="h-4 w-4" />
            Regenerate
          </button>
          <button
            onClick={handleExport}
            disabled={isProcessing}
            className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors disabled:opacity-50"
          >
            {exportDoc.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Download className="h-4 w-4" />
            )}
            Download Word
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="bg-surface rounded-lg p-6 border border-gray-800">
        <DocumentationOutput
          content={item.generated_content}
          type={item.type}
          onUpdate={handleContentUpdate}
        />
      </div>

      {/* Back Link */}
      <div className="mt-6">
        <Link
          to={`/projects/${item.project_id}`}
          className="inline-flex items-center gap-2 text-secondary hover:text-primary transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Project
        </Link>
      </div>

      {/* Regenerate Modal */}
      {showRegenerateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-surface rounded-lg w-full max-w-md mx-4 border border-gray-800">
            <div className="flex items-center justify-between p-4 border-b border-gray-800">
              <h2 className="text-lg font-semibold">Regenerate Documentation</h2>
              <button
                onClick={() => setShowRegenerateModal(false)}
                className="text-secondary hover:text-primary transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="p-4">
              <label className="block text-sm font-medium mb-2">
                Feedback (optional)
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                rows={4}
                className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary resize-none"
                placeholder="Describe what you'd like to change or improve..."
              />

              <div className="flex gap-3 mt-4">
                <button
                  onClick={() => setShowRegenerateModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-700 rounded-md text-secondary hover:text-primary transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleRegenerate}
                  disabled={regenerateDoc.isPending}
                  className="flex-1 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors disabled:opacity-50"
                >
                  {regenerateDoc.isPending ? (
                    <span className="flex items-center justify-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Regenerating...
                    </span>
                  ) : (
                    'Regenerate'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DocumentationPreview;
