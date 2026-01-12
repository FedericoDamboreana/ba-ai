import { AlertTriangle } from 'lucide-react';

function DeadlineWarning({ deadline }) {
  if (!deadline) return null;

  const deadlineDate = new Date(deadline);
  const today = new Date();
  const diffTime = deadlineDate - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays > 3) return null;

  const isOverdue = diffDays < 0;
  const message = isOverdue
    ? `Overdue by ${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''}`
    : diffDays === 0
    ? 'Due today'
    : `Due in ${diffDays} day${diffDays !== 1 ? 's' : ''}`;

  return (
    <div
      className={`flex items-center gap-1 text-xs ${
        isOverdue ? 'text-error' : 'text-warning'
      }`}
    >
      <AlertTriangle className="h-3 w-3" />
      <span>{message}</span>
    </div>
  );
}

export default DeadlineWarning;
