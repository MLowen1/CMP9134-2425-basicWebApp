import React from "react";

const ContactList = ({ contacts, updateContact, updateCallback }) => {
  const onDelete = async (id) => {
    // Purpose: Delete a contact by sending a DELETE request to the backend API
    try {
      const options = {
        method: "DELETE", // HTTP method used for deleting a resource
      };
      const response = await fetch(
        `http://localhost:5000/delete_contact/${id}`, // Use localhost consistently
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
    // Added overflow-x-auto for responsiveness on small screens
    <div className="overflow-x-auto bg-white shadow rounded-lg">
      {/* Removed redundant h2 as it's likely handled in App.jsx */}
      {/* <h2 className="text-2xl font-semibold mb-4 text-neutral-dark p-4 sm:p-6">Contacts</h2> */}
      <table className="min-w-full divide-y divide-neutral-DEFAULT">
        <thead className="bg-neutral-light">
          <tr>
            {/* Adjusted padding and text style */}
            <th className="px-4 py-3 sm:px-6 text-left text-xs font-semibold text-secondary uppercase tracking-wider">First Name</th>
            <th className="px-4 py-3 sm:px-6 text-left text-xs font-semibold text-secondary uppercase tracking-wider">Last Name</th>
            <th className="px-4 py-3 sm:px-6 text-left text-xs font-semibold text-secondary uppercase tracking-wider">Email</th>
            <th className="px-4 py-3 sm:px-6 text-left text-xs font-semibold text-secondary uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-neutral-DEFAULT">
          {contacts.length > 0 ? (
            contacts.map((contact) => (
              // Subtle hover effect
              <tr key={contact.id} className="hover:bg-neutral-light transition-colors duration-150 ease-in-out">
                {/* Adjusted padding and text style */}
                <td className="px-4 py-4 sm:px-6 whitespace-nowrap text-sm text-neutral-dark">{contact.firstName}</td>
                <td className="px-4 py-4 sm:px-6 whitespace-nowrap text-sm text-neutral-dark">{contact.lastName}</td>
                <td className="px-4 py-4 sm:px-6 whitespace-nowrap text-sm text-neutral-dark">{contact.email}</td>
                <td className="px-4 py-4 sm:px-6 whitespace-nowrap text-sm font-medium space-x-2">
                  {/* Consistent button styling */}
                  <button 
                    onClick={() => updateContact(contact)} 
                    className="px-3 py-1.5 text-xs bg-primary text-white rounded-md hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
                  >
                    Update
                  </button>
                  <button 
                    onClick={() => onDelete(contact.id)} 
                    className="px-3 py-1.5 text-xs bg-danger text-white rounded-md hover:bg-danger-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger transition-colors"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            // Display a message when there are no contacts
            <tr>
              <td colSpan="4" className="px-4 py-6 sm:px-6 text-center text-sm text-neutral-medium">
                No contacts found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ContactList;