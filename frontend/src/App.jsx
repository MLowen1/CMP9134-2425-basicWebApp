import { useState, useEffect } from "react";
import { flushSync } from "react-dom";
import ContactList from "./ContactList";
import ContactForm from "./ContactForm";
import ImageSearch from "./ImageSearch";
import { useAuth } from './AuthContext.jsx';
import LoginForm from './LoginForm.jsx';
import RegisterForm from './RegisterForm.jsx';

function App() {
  const [contacts, setContacts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentContact, setCurrentContact] = useState({});
  const [activeTab, setActiveTab] = useState('contacts');
  const [authMode, setAuthMode] = useState(null); // 'login' or 'register' or null
  const { user, isAuthenticated, logout } = useAuth();
  const [fetchError, setFetchError] = useState(null); // State for fetch errors

  // Fetch contacts on mount, except during tests to avoid asynchronous state updates outside act
  useEffect(() => {
    if (process.env.NODE_ENV !== 'test' && activeTab === 'contacts') { // Fetch only if contacts tab is active
      fetchContacts();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]); // Add activeTab as dependency

  const fetchContacts = async () => {
    setFetchError(null); // Clear previous errors
    let response; // Define response outside try block to access it in catch
    try {
      response = await fetch("http://localhost:5000/contacts");
      if (!response.ok) {
        // Throw an error with status to be caught below
        const error = new Error(`HTTP error! status: ${response.status}`);
        error.status = response.status;
        // Attempt to get error message from response body
        try {
          const errorData = await response.json();
          error.message = errorData.message || error.message;
        } catch (jsonError) {
          // Ignore if response body is not JSON or empty
        }
        throw error;
      }
      const data = await response.json();
      // Ensure contacts is always an array
      const contactsArray = Array.isArray(data.contacts) ? data.contacts : [];
      flushSync(() => setContacts(contactsArray));
    } catch (error) {
      console.error("Failed to fetch contacts:", error);
      let errorMessage;
      if (error.message.includes('Failed to fetch')) {
        errorMessage = "Could not connect to the server. Please ensure the backend is running.";
      } else if (error.status === 401) {
        errorMessage = "Authentication required. Please log in to view contacts.";
        // Optionally, redirect to login or clear auth state here
      } else {
        // Use the message from the thrown error (which might include backend message)
        errorMessage = `Error fetching contacts: ${error.message}`;
      }
      flushSync(() => {
        setFetchError(errorMessage);
        setContacts([]); // Clear contacts on error
      });
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentContact({});
  };

  const openCreateModal = () => {
    setCurrentContact({});
    setIsModalOpen(true);
  };

  const openEditModal = (contact) => {
    setCurrentContact(contact);
    setIsModalOpen(true);
  };

  const onUpdate = () => {
    closeModal();
    if (activeTab === 'contacts') {
      fetchContacts();
    }
  };

  const tabButtonStyle = "px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary";
  const activeTabStyle = "bg-primary text-white shadow-sm"; // Added shadow for active tab
  const inactiveTabStyle = "bg-neutral text-neutral-dark hover:bg-neutral-medium";

  return (
    // Increased overall padding, especially on larger screens
    <div className="min-h-screen bg-neutral-light p-4 sm:p-6 md:p-8 lg:p-12">
      {/* Centered content with max-width */}
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
                // Consistent button styling
                className="px-3 py-1.5 text-sm bg-danger text-white rounded-md hover:bg-danger-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger transition-colors"
              >
                Logout
              </button>
            </>
          ) : authMode === 'login' ? (
            // Ensure forms are wrapped or styled appropriately if needed here
            <LoginForm switchToRegister={() => setAuthMode('register')} />
          ) : authMode === 'register' ? (
            <RegisterForm switchToLogin={() => setAuthMode('login')} />
          ) : (
            // Placed login/register buttons together
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

        {/* Tab Navigation */}
        {/* Added bottom border for separation */}
        <div className="mb-8 border-b border-neutral pb-4 flex justify-center space-x-4">
          <button
            className={`${tabButtonStyle} ${
              activeTab === 'contacts' ? activeTabStyle : inactiveTabStyle
            }`}
            onClick={() => setActiveTab('contacts')}
          >
            Contacts
          </button>
          <button
            className={`${tabButtonStyle} ${
              activeTab === 'images' ? activeTabStyle : inactiveTabStyle
            }`}
            onClick={() => setActiveTab('images')}
          >
            Image Search
          </button>
        </div>

        {/* Main Content Area */}
        <div className="content-area">
          {activeTab === 'contacts' && (
            // Removed redundant bg/shadow as parent might handle it
            <div className="contacts-tab">
              {/* Display fetch error message */}
              {fetchError && (
                <div className="mb-4 p-3 bg-danger-light text-danger-dark border border-danger rounded-md">
                  {fetchError}
                </div>
              )}
              <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate} />
              <button
                onClick={openCreateModal}
                // Consistent button styling, adjusted margin
                className="mt-6 px-4 py-2 bg-success text-white rounded-md hover:bg-success-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-success transition-colors"
              >
                Create New Contact
              </button>
            </div>
          )}

          {activeTab === 'images' && (
            <div className="images-tab">
              <ImageSearch />
            </div>
          )}
        </div>
      </div>

      {/* Modal Styling Refined */}
      {isModalOpen && activeTab === 'contacts' && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 p-4">
          {/* Added max-height and overflow for smaller screens */}
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md relative max-h-[90vh] overflow-y-auto">
            <button
              // Improved close button styling and positioning
              className="absolute top-3 right-3 text-neutral-medium hover:text-neutral-dark text-2xl leading-none focus:outline-none"
              onClick={closeModal}
              aria-label="Close modal"
            >
              &times; {/* Using times symbol */}
            </button>
            <h3 className="text-xl font-semibold mb-6 text-neutral-dark">
              {Object.keys(currentContact).length > 0 ? 'Update Contact' : 'Create New Contact'}
            </h3>
            <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;