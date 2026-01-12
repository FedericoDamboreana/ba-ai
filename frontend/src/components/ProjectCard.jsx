import { Link } from 'react-router-dom';
import { Calendar, FileText } from 'lucide-react';
import StatusBadge from './StatusBadge';

function ProjectCard({ project }) {
  const formattedDate = new Date(project.updated_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <Link
      to={`/projects/${project.id}`}
      className="block bg-surface rounded-lg p-6 border border-gray-800 hover:border-primary transition-colors"
    >
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-lg font-semibold text-primary truncate flex-1">
          {project.name}
        </h3>
        <StatusBadge status={project.status} />
      </div>

      {project.client && (
        <p className="text-sm text-secondary mb-2">{project.client}</p>
      )}

      <p className="text-sm text-secondary line-clamp-2 mb-4">
        {project.description}
      </p>

      <div className="flex items-center justify-between text-xs text-secondary">
        <div className="flex items-center gap-1">
          <FileText className="h-3 w-3" />
          <span>{project.doc_count || 0} docs</span>
        </div>
        <div className="flex items-center gap-1">
          <Calendar className="h-3 w-3" />
          <span>{formattedDate}</span>
        </div>
      </div>
    </Link>
  );
}

export default ProjectCard;
