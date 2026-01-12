import { Link } from 'react-router-dom';
import { FileText } from 'lucide-react';

function Header() {
  return (
    <header className="bg-surface border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <FileText className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold text-primary">ba-ai</span>
          </Link>
          <nav className="flex items-center space-x-4">
            <Link
              to="/"
              className="text-secondary hover:text-primary transition-colors"
            >
              Projects
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
