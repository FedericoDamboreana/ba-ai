import { useState } from 'react';
import { Plus, FolderOpen } from 'lucide-react';
import { useProjects, useCreateProject } from '../hooks/useProjects';
import ProjectCard from '../components/ProjectCard';
import ProjectForm from '../components/ProjectForm';

const STATUS_FILTERS = [
  { value: null, label: 'All' },
  { value: 'Active', label: 'Active' },
  { value: 'Archived', label: 'Archived' },
];

function ProjectsList() {
  const [statusFilter, setStatusFilter] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const { data: projects, isLoading, error } = useProjects(statusFilter);
  const createProject = useCreateProject();

  const handleCreateProject = async (data) => {
    try {
      await createProject.mutateAsync(data);
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create project:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-secondary">Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-error">
          Error loading projects: {error.message}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold">Projects</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors"
        >
          <Plus className="h-4 w-4" />
          New Project
        </button>
      </div>

      <div className="flex gap-2 mb-6">
        {STATUS_FILTERS.map((filter) => (
          <button
            key={filter.value || 'all'}
            onClick={() => setStatusFilter(filter.value)}
            className={`px-4 py-2 rounded-md transition-colors ${
              statusFilter === filter.value
                ? 'bg-primary text-white'
                : 'bg-surface text-secondary hover:text-primary'
            }`}
          >
            {filter.label}
          </button>
        ))}
      </div>

      {projects?.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          <FolderOpen className="h-16 w-16 text-secondary mb-4" />
          <h2 className="text-xl font-semibold mb-2">No projects yet</h2>
          <p className="text-secondary mb-4">
            Create your first project to start documenting requirements.
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors"
          >
            <Plus className="h-4 w-4" />
            Create Project
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}

      {showForm && (
        <ProjectForm
          onSubmit={handleCreateProject}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}

export default ProjectsList;
