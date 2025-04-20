import { useState } from "react";
import ImageSearch from "./ImageSearch";
import { useAuth } from './AuthContext.jsx';
import LoginForm from './LoginForm.jsx';
import RegisterForm from './RegisterForm.jsx';

function App() {
  const [activeTab, setActiveTab] = useState('images'); // Default to images tab
  const [authMode, setAuthMode] = useState(null); // 'login' or 'register' or null
  const { user, isAuthenticated, logout } = useAuth();

  const tabButtonStyle = "px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary";
  const activeTabStyle = "bg-primary text-white shadow-sm"; // Added shadow for active tab

  return (
    <div className="min-h-screen bg-neutral-light p-4 sm:p-6 md:p-8 lg:p-12">
      <div className="max-w-5xl mx-auto">
        {/* Authentication Header */}
        <div className="auth-header mb-8 flex justify-end items-center space-x-4">
          {isAuthenticated ? (
            <>
              <span className="text-sm text-neutral-dark">Welcome, {user.username}</span>
              <button
                onClick={() => {
                  logout();
                  setAuthMode(null);
                }}
                className="px-3 py-1.5 text-sm bg-danger text-white rounded-md hover:bg-danger-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger transition-colors"
              >
                Logout
              </button>
            </>
          ) : authMode === 'login' ? (
            <LoginForm switchToRegister={() => setAuthMode('register')} />
          ) : authMode === 'register' ? (
            <RegisterForm switchToLogin={() => setAuthMode('login')} />
          ) : (
            <div className="flex space-x-2">
              <button
                onClick={() => setAuthMode('login')}
                className="px-3 py-1.5 text-sm bg-primary text-white rounded-md hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
              >
                Login
              </button>
              <button
                onClick={() => setAuthMode('register')}
                className="px-3 py-1.5 text-sm bg-secondary text-white rounded-md hover:bg-secondary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-secondary transition-colors"
              >
                Register
              </button>
            </div>
          )}
        </div>

        {/* Tab Navigation - Only Image Search */}
        <div className="mb-8 border-b border-neutral pb-4 flex justify-center space-x-4">
          <button
            className={`${tabButtonStyle} ${activeTabStyle}`}
          >
            Image Search
          </button>
        </div>

        {/* Main Content Area - Only Image Search */}
        <div className="content-area">
          <div className="images-tab">
            <ImageSearch />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;