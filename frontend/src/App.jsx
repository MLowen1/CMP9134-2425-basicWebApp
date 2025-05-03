import { useState, useEffect } from "react";
import ImageSearch from "./pages/ImageSearch.jsx";
import { useAuth } from './AuthContext.jsx';
import LoginForm from './LoginForm.jsx';
import RegisterForm from './RegisterForm.jsx';
import HomePage from './pages/HomePage.jsx';

function App() {
  const [activeTab, setActiveTab] = useState('home'); // Default to home tab
  const [authMode, setAuthMode] = useState(null); // 'login' or 'register' or null
  const { user, isAuthenticated, logout } = useAuth();

  // Automatically go to image search when logged in
  useEffect(() => {
    if (isAuthenticated) {
      setActiveTab('images');
    }
  }, [isAuthenticated]);

  // Removed tabButtonStyle, activeTabStyle, inactiveTabStyle, and tab navigation
  // Removed Login and Register buttons

  return (
    <div className="min-h-screen bg-background text-foreground p-4 sm:p-6 md:p-8 lg:p-12">
      <div className="max-w-5xl mx-auto  border border-border rounded-lg shadow-md">
        {/* Authentication Header */}
        <div className="auth-header mb-8 flex justify-end items-center space-x-4">
          {isAuthenticated ? (
            <>
              <span className="text-sm text-foreground-dark">Welcome, {user.username}</span>
              <button
                onClick={() => {
                  logout();
                  setAuthMode(null);
                  setActiveTab('home');
                }}
                className="px-3 py-1.5 text-sm bg-danger text-white rounded-md hover:bg-danger-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger transition-colors"
              >
                Logout
              </button>
            </>
          ) : authMode === 'login' ? (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
              <LoginForm 
                switchToRegister={() => setAuthMode('register')} 
                onClose={() => setAuthMode(null)} 
              />
            </div>
          ) : authMode === 'register' ? (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
              <RegisterForm 
                switchToLogin={() => setAuthMode('login')} 
                onClose={() => setAuthMode(null)} 
              />
            </div>
          ) : null}
        </div>

        {/* Removed tab navigation */}

        {/* Main Content Area */}
        {authMode === null || isAuthenticated ? (
          <div className="content-area">
            {/* Only HomePage and ImageSearch remain, but no buttons to switch */}
            {activeTab === 'home' && (
              <HomePage 
                onLoginClick={() => setAuthMode('login')}
                onRegisterClick={() => setAuthMode('register')}
              />
            )}
            {activeTab === 'images' && (
              <div className="images-tab">
                <ImageSearch />
              </div>
            )}
          </div>
        ) : (
          <div className="flex justify-center">
            {/* Authentication forms are shown above in the header */}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;