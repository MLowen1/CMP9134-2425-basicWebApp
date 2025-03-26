import React from "react";

const ContactList = ({ contacts, updateContact, updateCallback }) => {
  const onDelete = async (id) => {
    // Purpose: Delete a contact by sending a DELETE request to the backend API
    try {
      const options = {
        method: "DELETE", // HTTP method used for deleting a resource
      };
      const response = await fetch(
        `http://127.0.0.1:5000/delete_contact/${id}`, // Backend API endpoint for deleting a contact
        options
      );

      if (response.status === 200) {
        // If the deletion is successful, refresh the contact list
        updateCallback();
      } else {
        console.error("Failed to delete contact:", await response.json());
        // Optionally handle error in the frontend (e.g., display an error message)
      }
    } catch (error) {
      console.error("Error deleting contact:", error);
      // Optionally handle error in the frontend (e.g., display an error message)
    }
  };

  return (
    <div>
      <h2>Contacts</h2>
      <table>
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map((contact) => (
            <tr key={contact.id}>
              {/* Display contact details */}
              <td>{contact.firstName}</td>
              <td>{contact.lastName}</td>
              <td>{contact.email}</td>
              <td>
                {/* Button to open the modal for updating a contact */}
                <button onClick={() => updateContact(contact)}>Update</button>
                {/* Button to delete a contact */}
                <button onClick={() => onDelete(contact.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContactList;