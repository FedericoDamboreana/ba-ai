function QuestionInput({ question, value, onChange }) {
  const { question_type, options } = question;

  if (question_type === 'Text') {
    return (
      <textarea
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        rows={3}
        className="w-full bg-background border border-gray-700 rounded-md px-3 py-2 text-primary focus:outline-none focus:border-primary resize-none"
        placeholder="Enter your answer..."
      />
    );
  }

  if (question_type === 'MultipleChoice') {
    return (
      <div className="space-y-2">
        {options?.map((option, idx) => (
          <label
            key={idx}
            className="flex items-center gap-2 cursor-pointer group"
          >
            <input
              type="radio"
              name={`question-${question.id}`}
              value={option}
              checked={value === option}
              onChange={(e) => onChange(e.target.value)}
              className="text-primary focus:ring-primary"
            />
            <span className="text-secondary group-hover:text-primary transition-colors">
              {option}
            </span>
          </label>
        ))}
        <label className="flex items-center gap-2 cursor-pointer group">
          <input
            type="radio"
            name={`question-${question.id}`}
            value="__other__"
            checked={value && !options?.includes(value) && value !== 'N/A'}
            onChange={() => onChange('')}
            className="text-primary focus:ring-primary"
          />
          <span className="text-secondary group-hover:text-primary transition-colors">
            Other:
          </span>
          {value && !options?.includes(value) && value !== 'N/A' && (
            <input
              type="text"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              className="flex-1 bg-background border border-gray-700 rounded-md px-2 py-1 text-primary focus:outline-none focus:border-primary"
              placeholder="Specify..."
            />
          )}
        </label>
      </div>
    );
  }

  if (question_type === 'Checkbox') {
    const selectedValues = value ? value.split(', ').filter(Boolean) : [];

    const handleCheckboxChange = (option, checked) => {
      let newValues;
      if (checked) {
        newValues = [...selectedValues, option];
      } else {
        newValues = selectedValues.filter((v) => v !== option);
      }
      onChange(newValues.join(', '));
    };

    return (
      <div className="space-y-2">
        {options?.map((option, idx) => (
          <label
            key={idx}
            className="flex items-center gap-2 cursor-pointer group"
          >
            <input
              type="checkbox"
              checked={selectedValues.includes(option)}
              onChange={(e) => handleCheckboxChange(option, e.target.checked)}
              className="text-primary focus:ring-primary rounded"
            />
            <span className="text-secondary group-hover:text-primary transition-colors">
              {option}
            </span>
          </label>
        ))}
      </div>
    );
  }

  return null;
}

export default QuestionInput;
