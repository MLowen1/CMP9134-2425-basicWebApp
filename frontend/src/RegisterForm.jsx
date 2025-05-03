import React, { useState } from 'react';
import { useAuth } from './AuthContext.jsx';

function RegisterForm({ switchToLogin, onClose }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    
    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await register(username, email, password);
      setSuccessMessage('Registration successful! You can now log in.');
      // Clear the form
      setUsername('');
      setEmail('');
      setPassword('');
      setConfirmPassword('');
      
      // Automatically switch to login after a short delay
      setTimeout(() => {
        switchToLogin();
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
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
        aria-label="Close register modal"
      >
        ×
      </button>
      <h2 className="text-2xl font-semibold text-center mb-6">Register Account</h2>
      
      {error && (
        <div className="bg-danger-light text-danger p-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      {successMessage && (
        <div className="bg-success-light text-success p-3 rounded-md mb-4">
          {successMessage}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-medium text-neutral-dark mb-1">
            Username
          </label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-3 py-2 border border-neutral rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            required
          />
        </div>
        
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
        
        <div className="mb-4">
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
        
        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-neutral-dark mb-1">
            Confirm Password
          </label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
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
                ? 'bg-secondary-light cursor-not-allowed'
                : 'bg-secondary hover:bg-secondary-hover'
            }`}
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </button>
          
          <div className="text-center">
            <button
              type="button"
              onClick={switchToLogin}
              className="text-primary hover:text-primary-hover text-sm"
            >
              Already have an account? Sign in here
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default RegisterForm;