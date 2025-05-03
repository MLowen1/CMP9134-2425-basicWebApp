import React from 'react';
import { useAuth } from '../AuthContext.jsx';
import RippleLogo from '../components/Ripple Logo.png';

function HomePage({ onLoginClick, onRegisterClick }) {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="flex justify-center min-h-screen p-4">
      <div className="w-full max-w-2xl p-4 pt-2 text-center mx-auto">
        {/* Logo and Title */}
        <img src={RippleLogo} alt="Ripple Logo" className="mx-auto mb-10 w-56 h-56 object-contain" />
        <h1 className="text-4xl font-bold mb-4 text-primary font-poppins">Discover Open License Media</h1>
        <p className="text-lg text-foreground-dark mb-6">
          Search for stunning images, videos, and audio released under Creative Commons licenses.
        </p>

        {/* Auth Links or Welcome Message */}
        <div className="auth-links flex justify-center gap-6 mt-10">
          {isAuthenticated ? (
            <span className="text-lg text-accent-cyan font-semibold">Welcome, {user.username}!</span>
          ) : (
            <>

              {/* Login Button */}
              <button
                onClick={onLoginClick}
                className="px-6 py-2 rounded-lg font-semibold bg-primary text-background hover:bg-primary-hover transition shadow-md focus:outline-none focus:ring-2 focus:ring-primary"
              >
                Login
              </button>

              {/* Register Button */}
              <button
                onClick={onRegisterClick}
                className="px-6 py-2 rounded-lg font-semibold bg-secondary text-background hover:bg-secondary-hover transition shadow-md focus:outline-none focus:ring-2 focus:ring-secondary"
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default HomePage;