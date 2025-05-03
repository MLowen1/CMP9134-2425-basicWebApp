import React, { useState } from 'react';
import { useAuth } from './AuthContext.jsx';

function LoginForm({ switchToRegister, onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await login(email, password);
      // Success is handled by AuthContext which updates the isAuthenticated state
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to login. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-card p-6 rounded-lg shadow-md w-full max-w-md relative">
      {/* Exit Button */}
      <button
        type="button"
        onClick={onClose}
        className="absolute top-2 right-2 text-foreground-dark hover:text-danger text-xl font-bold focus:outline-none"
        aria-label="Close login modal"
      >
        ×
      </button>
      <h2 className="text-2xl font-semibold text-center mb-6">Login</h2>
      
      {error && (
        <div className="bg-danger-light text-danger p-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium text-neutral-dark mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border border-neutral rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            required
          />
        </div>
        
        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-medium text-neutral-dark mb-1">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border border-neutral rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            required
          />
        </div>
        
        <div className="flex flex-col space-y-4">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full px-4 py-2 text-white rounded-md ${
              isLoading
                ? 'bg-primary-light cursor-not-allowed'
                : 'bg-primary hover:bg-primary-hover'
            }`}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
          
          <div className="text-center">
            <button
              type="button"
              onClick={switchToRegister}
              className="text-primary hover:text-primary-hover text-sm"
            >
              Don't have an account? Register here
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;