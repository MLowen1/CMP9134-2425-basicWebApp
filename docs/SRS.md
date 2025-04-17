# Software Requirements Specification (SRS)

## 2. Functional Requirements

### 2.1 User Account Management

The system shall provide functionality for user account creation, authentication, and secure session management.

#### FR1: User Registration
- The system shall allow a new user to register by supplying a unique username and a password.
- The username must be unique; duplicate usernames are not permitted.
- Both username and password are required fields; attempts to register with missing fields shall result in an error.
- Upon successful registration, the system shall store the user's credentials securely and issue a JWT access token.

#### FR2: User Authentication (Login)
- The system shall allow an existing user to authenticate by supplying their username and password.
- If the credentials are valid, the system shall issue a new JWT access token.
- If the credentials are invalid or the user does not exist, the system shall reject the request with an appropriate error.
- Both username and password are required; missing fields shall result in an error.

#### FR3: Password Security
- The system shall not store plaintext passwords.
- Passwords shall be hashed using a strong, industry-standard algorithm (e.g., PBKDF2 via Werkzeug).
- The system shall provide functionality to verify a plaintext password against the stored hash.

#### FR4: Token-Based Session Management
- The system shall use JSON Web Tokens (JWT) for stateless session management.
- JWTs shall be signed with a server-side secret key.
- Upon successful registration or login, the client shall receive an access token to include in subsequent requests to protected endpoints.

#### FR5: Error Handling and Validation
- Input validation errors (e.g., missing fields) shall return a 400 Bad Request with a descriptive message.
- Authentication failures shall return a 401 Unauthorized with a descriptive message.

### 2.2 Protected Resources (Future Enhancement)
- (Not implemented in current version) Certain endpoints may require a valid JWT access token; the system shall enforce token validation.

## 2.3 Session Management and Profile

#### FR6: Session and Profile Endpoints
- The system shall allow an authenticated user to view their profile via a `/@me` endpoint.
- The system shall allow an authenticated user to logout via a `/logout` endpoint, revoking their current JWT.
- Both `/@me` and `/logout` shall require a valid access token; unauthorized requests shall be rejected with a 401 status.

## 3. Non-Functional Requirements

### 3.1 Security Requirements
- Passwords shall never be stored in plaintext; the system must hash passwords using PBKDF2 (Werkzeug’s `generate_password_hash`).
- The system shall use JWTs for stateless authentication, signed with a securely stored secret key.
- JWTs shall include a unique identifier (JTI) to support token revocation on logout.
- All authentication endpoints shall enforce HTTPS in production to protect credentials in transit.
- The server shall maintain a token revocation mechanism (in-memory blocklist for current version; scalable store in production).

---
*Note: This document outlines the draft functional requirements for user account management in the current iteration of the application.*