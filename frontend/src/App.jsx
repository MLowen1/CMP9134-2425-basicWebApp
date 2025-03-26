import { useState, useEffect } from "react";
import ContactList from "./ContactList";
import "./App.css";
import ContactForm from "./ContactForm";

function App() {
  const [contacts, setContacts] = useState([]); // State to store the list of contacts
  const [isModalOpen, setIsModalOpen] = useState(false); // State to manage modal visibility
  const [currentContact, setCurrentContact] = useState({}); // State to store the contact being edited

  useEffect(() => {
    fetchContacts(); // Fetches the list of contacts when the component loads
  }, []);

  const fetchContacts = async () => {
    // Purpose: Fetch the list of contacts from the backend API
    const response = await fetch("http://127.0.0.1:5000/contacts"); // Sends a GET request to the backend
    const data = await response.json(); // Parses the JSON response
    setContacts(data.contacts); // Updates the state with the fetched contacts
    console.log(data.contacts); // Logs the contacts for debugging
  };

  const closeModal = () => {
    // Purpose: Close the modal and reset the current contact
    setIsModalOpen(false);
    setCurrentContact({});
  };

  const openCreateModal = () => {
    // Purpose: Open the modal for creating a new contact
    if (!isModalOpen) setIsModalOpen(true);
  };

  const openEditModal = (contact) => {
    // Purpose: Open the modal for editing an existing contact
    if (isModalOpen) return;
    setCurrentContact(contact); // Sets the contact to be edited
    setIsModalOpen(true);
  };

  const onUpdate = () => {
    // Purpose: Callback function to refresh the contact list after a create or update operation
    closeModal();
    fetchContacts(); // Fetches the updated list of contacts
  };

  return (
    <>
      {/* ContactList component displays the list of contacts */}
      {/* It receives the contacts data and functions for updating contacts */}
      <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate} />
      
      {/* Button to open the modal for creating a new contact */}
      <button onClick={openCreateModal}>Create New Contact</button>
      
      {/* Modal for creating or editing a contact */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            {/* ContactForm component handles the form for creating or updating a contact */}
            {/* It sends data to the backend API and triggers the onUpdate callback */}
            <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
          </div>
        </div>
      )}
    </>
  );
}

export default App;