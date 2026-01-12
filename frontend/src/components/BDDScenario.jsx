import { Copy, Check } from 'lucide-react';
import { useState } from 'react';

function BDDScenario({ scenario }) {
  const [copied, setCopied] = useState(false);

  const formatScenario = () => {
    const lines = [`Scenario: ${scenario.scenario_name}`];
    scenario.given?.forEach((g) => lines.push(`  Given ${g}`));
    scenario.when?.forEach((w) => lines.push(`  When ${w}`));
    scenario.then?.forEach((t) => lines.push(`  Then ${t}`));
    return lines.join('\n');
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(formatScenario());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-background rounded-lg border border-gray-800 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-surface/50 border-b border-gray-800">
        <span className="text-sm font-medium text-primary">
          {scenario.scenario_name}
        </span>
        <button
          onClick={handleCopy}
          className="text-secondary hover:text-primary transition-colors"
        >
          {copied ? (
            <Check className="h-4 w-4 text-success" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </button>
      </div>
      <pre className="p-4 text-sm font-mono overflow-x-auto">
        <code>
          {scenario.given?.map((g, i) => (
            <div key={`given-${i}`}>
              <span className="text-success">Given</span>{' '}
              <span className="text-secondary">{g}</span>
            </div>
          ))}
          {scenario.when?.map((w, i) => (
            <div key={`when-${i}`}>
              <span className="text-warning">When</span>{' '}
              <span className="text-secondary">{w}</span>
            </div>
          ))}
          {scenario.then?.map((t, i) => (
            <div key={`then-${i}`}>
              <span className="text-primary">Then</span>{' '}
              <span className="text-secondary">{t}</span>
            </div>
          ))}
        </code>
      </pre>
    </div>
  );
}

export default BDDScenario;
