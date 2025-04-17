import React, { useState, useEffect } from "react";
import ContactList from "./ContactList";
import ContactForm from "./ContactForm";
import ImageSearch from "./ImageSearch";

function App() {
  const [contacts, setContacts] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentContact, setCurrentContact] = useState({});
  const [activeTab, setActiveTab] = useState('contacts');

  useEffect(() => {
    if (activeTab === 'contacts') {
      fetchContacts();
    }
  }, [activeTab]);

  const fetchContacts = async () => {
    try {
      const response = await fetch("http://localhost:5000/contacts");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setContacts(data.contacts);
      console.log(data.contacts);
    } catch (error) {
      console.error("Failed to fetch contacts:", error);
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

  const tabButtonStyle = "px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500";
  const activeTabStyle = "bg-blue-600 text-white";
  const inactiveTabStyle = "bg-gray-200 text-gray-700 hover:bg-gray-300";

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto mb-6">
        <div className="bg-white shadow rounded-lg p-4 flex justify-center space-x-4">
          <button
            className={`${tabButtonStyle} ${activeTab === 'contacts' ? activeTabStyle : inactiveTabStyle}`}
            onClick={() => setActiveTab('contacts')}
          >
            Contacts
          </button>
          <button
            className={`${tabButtonStyle} ${activeTab === 'images' ? activeTabStyle : inactiveTabStyle}`}
            onClick={() => setActiveTab('images')}
          >
            Image Search
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto">
        {activeTab === 'contacts' && (
          <div className="contacts-tab bg-white shadow rounded-lg p-4 sm:p-6">
            <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate} />
            <button
              onClick={openCreateModal}
              className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
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

      {isModalOpen && activeTab === 'contacts' && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md relative">
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-3xl font-bold"
              onClick={closeModal}
              aria-label="Close modal"
            >
              ×
            </button>
            <h3 className="text-xl font-semibold mb-4">
              {Object.keys(currentContact).length > 0 ? 'Update Contact' : 'Create New Contact'}
            </h3>
            <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
          </div>
        </div>
      )}
    </div>
}

export default App;