import { useState, useContext } from "react"; // Import useContext
import { AuthContext } from "./AuthContext"; // Import AuthContext

const ContactForm = ({ existingContact = {}, updateCallback }) => {
  // State variables to store form input values
  const [firstName, setFirstName] = useState(existingContact.firstName || ""); // First name of the contact
  const [lastName, setLastName] = useState(existingContact.lastName || ""); // Last name of the contact
  const [email, setEmail] = useState(existingContact.email || ""); // Email of the contact

  // Get token from AuthContext
  const { token } = useContext(AuthContext);

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
    // Use port 5001 and correct API path /api/contacts
    const url =
      `http://localhost:5001/api/contacts` + 
      (updating ? `/${existingContact.id}` : "");
    const options = {
      method: updating ? "PUT" : "POST", // Use PUT for update as per REST conventions
      headers: {
        "Content-Type": "application/json", // Specify the content type as JSON
        // Add Authorization header
        "Authorization": `Bearer ${token}` 
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
    };

    // Send the request to the backend API
    const response = await fetch(url, options);

    // Handle the response from the backend
    if (!response.ok) { // Check if response status is not 2xx
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        // Try to parse the response body as JSON
        const errorData = await response.json();
        // Use the message from JSON if available, otherwise keep the status text
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