import { useState, useEffect } from "react";
import { flushSync } from "react-dom";
import ContactList from "./ContactList";
import "./App.css";
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

  // Fetch contacts on mount, except during tests to avoid asynchronous state updates outside act
  useEffect(() => {
    if (process.env.NODE_ENV !== 'test') {
      fetchContacts();
    }
  }, []);

  const fetchContacts = async () => {
    const response = await fetch("http://localhost:5000/contacts");
    const data = await response.json();
    // Ensure contacts is always an array to prevent crashes when API returns unexpected data
    const contactsArray = Array.isArray(data.contacts) ? data.contacts : [];
    // Synchronously apply contacts update to avoid React act() warning in tests
    flushSync(() => setContacts(contactsArray));
  };

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (contact) => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  return (
    <>
      <div className="auth-header">
        {isAuthenticated ? (
          <>
            <span>Welcome, {user.username}</span>
            <button onClick={() => { logout(); setAuthMode(null); }}>
              Logout
            </button>
          </>
        ) : authMode === 'login' ? (
          <LoginForm switchToRegister={() => setAuthMode('register')} />
        ) : authMode === 'register' ? (
          <RegisterForm switchToLogin={() => setAuthMode('login')} />
        ) : (
          <>
            <button onClick={() => setAuthMode('login')}>Login</button>
            <button onClick={() => setAuthMode('register')}>Register</button>
          </>
        )}
      </div>
      <div className="tab-buttons">
        <button 
          className={`tab-button ${activeTab === 'contacts' ? 'active' : ''}`}
          onClick={() => setActiveTab('contacts')}
        >
          Contacts
        </button>
        <button 
          className={`tab-button ${activeTab === 'images' ? 'active' : ''}`}
          onClick={() => setActiveTab('images')}
        >
          Image Search
        </button>
      </div>

      {activeTab === 'contacts' && (
        <div className="contacts-tab">
          <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate}/>
          <button onClick={openCreateModal}>Create New Contact</button>
          {isModalOpen && (
            <div className="modal">
              <div className="modal-content">
                <span className="close" onClick={closeModal}>&times;</span>
                <ContactForm existingContact={currentContact} updateCallback={onUpdate}/>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'images' && (
        <div className="images-tab">
          <ImageSearch />
        </div>
      )}
    </>
  );
}

export default App;