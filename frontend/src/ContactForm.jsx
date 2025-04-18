import { useState } from "react";

const ContactForm = ({ existingContact = {}, updateCallback }) => {
  // State variables to store form input values
  const [firstName, setFirstName] = useState(existingContact.firstName || ""); // First name of the contact
  const [lastName, setLastName] = useState(existingContact.lastName || ""); // Last name of the contact
  const [email, setEmail] = useState(existingContact.email || ""); // Email of the contact

  // Determine if the form is being used to update an existing contact
  const updating = Object.entries(existingContact).length !== 0;

  const onSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior

    // Prepare the data to be sent to the backend
    const data = {
      firstName,
      lastName,
      email,
    };

    // Determine the API endpoint and HTTP method based on whether it's an update or create operation
    const url =
      `http://localhost:5000/` + // Use localhost consistently
      (updating ? `update_contact/${existingContact.id}` : "create_contact");
    const options = {
      method: updating ? "PATCH" : "POST", // PATCH for updating, POST for creating
      headers: {
        "Content-Type": "application/json", // Specify the content type as JSON
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
    };

    // Send the request to the backend API
    const response = await fetch(url, options);

    // Handle the response from the backend
    if (response.status !== 201 && response.status !== 200) {
      // If the response indicates an error, display an alert with the error message
      const message = await response.json();
      alert(message.message);
    } else {
      // If the operation is successful, trigger the callback to refresh the contact list
      updateCallback();
    }
  };

  return (
    <form onSubmit={onSubmit}>
      {/* Input field for the first name */}
      <div>
        <label htmlFor="firstName">First Name:</label>
        <input
          type="text"
          id="firstName"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)} // Update the state when the input changes
        />
      </div>

      {/* Input field for the last name */}
      <div>
        <label htmlFor="lastName">Last Name:</label>
        <input
          type="text"
          id="lastName"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)} // Update the state when the input changes
        />
      </div>

      {/* Input field for the email */}
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="text"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)} // Update the state when the input changes
        />
      </div>

      {/* Submit button with dynamic text based on the operation */}
      <button type="submit">{updating ? "Update" : "Create"}</button>
    </form>
  );
};

export default ContactForm;