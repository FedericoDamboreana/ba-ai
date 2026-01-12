import { useState } from 'react';
import { X } from 'lucide-react';

const DOC_TYPES = [
  { value: 'PRD', label: 'Project Requirements Document' },
  { value: 'Epic', label: 'Epic Documentation' },
  { value: 'UserStory', label: 'User Story + Acceptance Criteria' },
  { value: 'FRS', label: 'Functional Requirements Specification' },
];

function ItemForm({ onSubmit, onClose, isLoading }) {
  const [formData, setFormData] = useState({
    type: 'UserStory',
    title: '',
    description: '',
    deadline: '',
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      const data = { ...formData };
      if (!data.deadline) {
        delete data.deadline;
      }
      onSubmit(data);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-surface rounded-lg w-full max-w-md mx-4 border border-gray-800">
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <h2 className="text-lg font-semibold">New Documentation</h2>
          <button
            onClick={onClose}
            className="text-secondary hover:text-primary transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Document Type
            </label>
            <select
              name="type"
              value={formData.type}
              onChange={handleChange}
              className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary"
            >
              {DOC_TYPES.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Title <span className="text-error">*</span>
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary"
              placeholder="Enter title"
            />
            {errors.title && (
              <p className="text-error text-xs mt-1">{errors.title}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Description <span className="text-error">*</span>
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary resize-none"
              placeholder="Describe what needs to be documented"
            />
            {errors.description && (
              <p className="text-error text-xs mt-1">{errors.description}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Deadline (optional)
            </label>
            <input
              type="date"
              name="deadline"
              value={formData.deadline}
              onChange={handleChange}
              className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-700 rounded-md text-secondary hover:text-primary transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-primary hover:bg-primary-light text-white rounded-md transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Creating...' : 'Start Documentation'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ItemForm;
