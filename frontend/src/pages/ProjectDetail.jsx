import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Plus,
  Edit2,
  Archive,
  Trash2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import {
  useProject,
  useUpdateProject,
  useArchiveProject,
  useDeleteProject,
} from '../hooks/useProjects';
import { useProjectItems, useCreateItem } from '../hooks/useDocumentationItem';
import StatusBadge from '../components/StatusBadge';
import DeadlineWarning from '../components/DeadlineWarning';
import ProjectForm from '../components/ProjectForm';
import ItemForm from '../components/ItemForm';

function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [showEditForm, setShowEditForm] = useState(false);
  const [showItemForm, setShowItemForm] = useState(false);
  const [showKnowledgeBase, setShowKnowledgeBase] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const { data: project, isLoading: projectLoading } = useProject(id);
  const { data: items, isLoading: itemsLoading } = useProjectItems(id);
  const updateProject = useUpdateProject();
  const archiveProject = useArchiveProject();
  const deleteProject = useDeleteProject();
  const createItem = useCreateItem();

  const handleUpdateProject = async (data) => {
    try {
      await updateProject.mutateAsync({ id, data });
      setShowEditForm(false);
    } catch (err) {
      console.error('Failed to update project:', err);
    }
  };

  const handleArchive = async () => {
    try {
      await archiveProject.mutateAsync(id);
    } catch (err) {
      console.error('Failed to archive project:', err);
    }
  };

  const handleDelete = async () => {
    try {
      await deleteProject.mutateAsync(id);
      navigate('/');
    } catch (err) {
      console.error('Failed to delete project:', err);
    }
  };

  const handleCreateItem = async (data) => {
    try {
      const newItem = await createItem.mutateAsync({ projectId: id, data });
      setShowItemForm(false);
      navigate(`/items/${newItem.id}`);
    } catch (err) {
      console.error('Failed to create item:', err);
    }
  };

  if (projectLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-secondary">Loading project...</div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-error">Project not found</div>
      </div>
    );
  }

  return (
    <div>
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-secondary mb-6">
        <Link to="/" className="hover:text-primary transition-colors">
          Projects
        </Link>
        <span>/</span>
        <span className="text-primary">{project.name}</span>
      </div>

      {/* Project Header */}
      <div className="bg-surface rounded-lg p-6 border border-gray-800 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold">{project.name}</h1>
              <StatusBadge status={project.status} />
            </div>
            {project.client && (
              <p className="text-secondary">{project.client}</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowEditForm(true)}
              className="p-2 text-secondary hover:text-primary transition-colors"
              title="Edit"
            >
              <Edit2 className="h-5 w-5" />
            </button>
            <button
              onClick={handleArchive}
              className="p-2 text-secondary hover:text-warning transition-colors"
              title={project.status === 'Archived' ? 'Unarchive' : 'Archive'}
            >
              <Archive className="h-5 w-5" />
            </button>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="p-2 text-secondary hover:text-error transition-colors"
              title="Delete"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        </div>
        <p className="text-secondary">{project.description}</p>
      </div>

      {/* Knowledge Base */}
      {project.knowledge_base && (
        <div className="bg-surface rounded-lg border border-gray-800 mb-6">
          <button
            onClick={() => setShowKnowledgeBase(!showKnowledgeBase)}
            className="w-full flex items-center justify-between p-4"
          >
            <span className="font-medium">Knowledge Base</span>
            {showKnowledgeBase ? (
              <ChevronUp className="h-5 w-5 text-secondary" />
            ) : (
              <ChevronDown className="h-5 w-5 text-secondary" />
            )}
          </button>
          {showKnowledgeBase && (
            <div className="px-4 pb-4 text-secondary whitespace-pre-wrap">
              {project.knowledge_base}
            </div>
          )}
        </div>
      )}

      {/* Documentation Items */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Documentation Items</h2>
        <button
          onClick={() => setShowItemForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Documentation
        </button>
      </div>

      {itemsLoading ? (
        <div className="text-secondary">Loading items...</div>
      ) : items?.length === 0 ? (
        <div className="bg-surface rounded-lg p-8 border border-gray-800 text-center">
          <p className="text-secondary mb-4">
            No documentation items yet. Create your first one.
          </p>
          <button
            onClick={() => setShowItemForm(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors"
          >
            <Plus className="h-4 w-4" />
            Create Documentation
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <Link
              key={item.id}
              to={`/items/${item.id}`}
              className="block bg-surface rounded-lg p-4 border border-gray-800 hover:border-primary transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-secondary uppercase">
                      {item.type}
                    </span>
                    <StatusBadge status={item.status} />
                  </div>
                  <h3 className="font-medium">{item.title}</h3>
                  <p className="text-sm text-secondary mt-1 line-clamp-1">
                    {item.description}
                  </p>
                </div>
                <DeadlineWarning deadline={item.deadline} />
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Modals */}
      {showEditForm && (
        <ProjectForm
          project={project}
          onSubmit={handleUpdateProject}
          onClose={() => setShowEditForm(false)}
        />
      )}

      {showItemForm && (
        <ItemForm
          onSubmit={handleCreateItem}
          onClose={() => setShowItemForm(false)}
          isLoading={createItem.isPending}
        />
      )}

      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-surface rounded-lg w-full max-w-sm mx-4 p-6 border border-gray-800">
            <h3 className="text-lg font-semibold mb-2">Delete Project?</h3>
            <p className="text-secondary mb-4">
              This action cannot be undone. All documentation items will be
              deleted.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 px-4 py-2 border border-gray-700 rounded-md text-secondary hover:text-primary transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 px-4 py-2 bg-error hover:bg-error/80 text-white rounded-md transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectDetail;
