const statusConfig = {
  Active: { bg: 'bg-success/20', text: 'text-success', label: 'Active' },
  OnHold: { bg: 'bg-warning/20', text: 'text-warning', label: 'On Hold' },
  Completed: { bg: 'bg-primary/20', text: 'text-primary', label: 'Completed' },
  Archived: { bg: 'bg-gray-500/20', text: 'text-gray-400', label: 'Archived' },
  Draft: { bg: 'bg-gray-500/20', text: 'text-gray-400', label: 'Draft' },
  InProgress: { bg: 'bg-warning/20', text: 'text-warning', label: 'In Progress' },
  QuestionsComplete: { bg: 'bg-success/20', text: 'text-success', label: 'Ready' },
  Generated: { bg: 'bg-primary/20', text: 'text-primary', label: 'Generated' },
};

function StatusBadge({ status }) {
  const config = statusConfig[status] || statusConfig.Draft;

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
}

export default StatusBadge;
