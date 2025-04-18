import React, { useState } from 'react';
import { useAuth } from './AuthContext';

export default function LoginForm({ switchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    const result = await login(username, password);
    if (!result.success) {
      setError(result.message);
    }
  };

  return (
    <div className="auth-form bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs">
      <h2 className="text-xl font-semibold mb-4 text-center text-neutral-dark">Login</h2>
      {error && <p className="text-danger text-xs italic mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="username" className="block text-neutral-dark text-sm font-bold mb-2">Username:</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-neutral-dark leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-primary"
          />
        </div>
        <div>
          <label htmlFor="password" className="block text-neutral-dark text-sm font-bold mb-2">Password:</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-neutral-dark mb-3 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-primary"
          />
        </div>
        <button 
          type="submit" 
          className="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
        >
          Login
        </button>
      </form>
      <p className="text-center text-neutral-medium text-xs mt-4">
        Don't have an account?{' '}
        <button 
          type="button" 
          onClick={switchToRegister} 
          className="font-bold text-primary hover:text-primary-dark focus:outline-none"
        >
          Register
        </button>
      </p>
    </div>
  );
}