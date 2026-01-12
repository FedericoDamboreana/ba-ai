import { useState } from 'react';
import { Copy, Check, Edit2 } from 'lucide-react';
import BDDScenario from './BDDScenario';

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="text-secondary hover:text-primary transition-colors"
      title="Copy"
    >
      {copied ? (
        <Check className="h-4 w-4 text-success" />
      ) : (
        <Copy className="h-4 w-4" />
      )}
    </button>
  );
}

function EditableField({ label, value, onSave }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);

  const handleSave = () => {
    onSave(editValue);
    setIsEditing(false);
  };

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-medium text-secondary">{label}</label>
        <div className="flex items-center gap-2">
          <CopyButton text={value} />
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="text-secondary hover:text-primary transition-colors"
          >
            <Edit2 className="h-4 w-4" />
          </button>
        </div>
      </div>
      {isEditing ? (
        <div>
          <textarea
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary resize-none"
            rows={3}
          />
          <div className="flex gap-2 mt-2">
            <button
              onClick={handleSave}
              className="px-3 py-1 bg-primary text-white rounded text-sm"
            >
              Save
            </button>
            <button
              onClick={() => {
                setEditValue(value);
                setIsEditing(false);
              }}
              className="px-3 py-1 border border-gray-700 text-secondary rounded text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <p className="text-primary">{value}</p>
      )}
    </div>
  );
}

function DocumentationOutput({ content, type, onUpdate }) {
  if (!content) {
    return (
      <div className="text-center py-8 text-secondary">
        No documentation generated yet.
      </div>
    );
  }

  // Handle User Story type
  if (type === 'UserStory' && content.user_story) {
    const userStoryText = `As a ${content.user_story.as_a}, I want ${content.user_story.i_want}, so that ${content.user_story.so_that}`;

    return (
      <div>
        <EditableField
          label="Title"
          value={content.title}
          onSave={(val) => onUpdate({ ...content, title: val })}
        />

        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-secondary">
              User Story
            </label>
            <CopyButton text={userStoryText} />
          </div>
          <div className="bg-surface p-4 rounded-lg border border-gray-800">
            <p className="text-primary">
              <span className="text-secondary">As a</span>{' '}
              {content.user_story.as_a},{' '}
              <span className="text-secondary">I want</span>{' '}
              {content.user_story.i_want},{' '}
              <span className="text-secondary">so that</span>{' '}
              {content.user_story.so_that}
            </p>
          </div>
        </div>

        <div className="mb-6">
          <label className="text-sm font-medium text-secondary block mb-3">
            Acceptance Criteria
          </label>
          <div className="space-y-4">
            {content.acceptance_criteria?.map((scenario, idx) => (
              <BDDScenario key={idx} scenario={scenario} />
            ))}
          </div>
        </div>

        {content.notes && (
          <EditableField
            label="Notes"
            value={content.notes}
            onSave={(val) => onUpdate({ ...content, notes: val })}
          />
        )}

        {content.dependencies?.length > 0 && (
          <div className="mb-6">
            <label className="text-sm font-medium text-secondary block mb-2">
              Dependencies
            </label>
            <ul className="list-disc list-inside text-primary">
              {content.dependencies.map((dep, idx) => (
                <li key={idx}>{dep}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  // Generic output for other types
  return (
    <div>
      {content.title && (
        <EditableField
          label="Title"
          value={content.title}
          onSave={(val) => onUpdate({ ...content, title: val })}
        />
      )}

      {content.summary && (
        <EditableField
          label="Summary"
          value={content.summary}
          onSave={(val) => onUpdate({ ...content, summary: val })}
        />
      )}

      {content.sections?.map((section, idx) => (
        <div key={idx} className="mb-6">
          <label className="text-sm font-medium text-secondary block mb-2">
            {section.heading}
          </label>
          <div className="text-primary whitespace-pre-wrap">{section.content}</div>
        </div>
      ))}
    </div>
  );
}

export default DocumentationOutput;
