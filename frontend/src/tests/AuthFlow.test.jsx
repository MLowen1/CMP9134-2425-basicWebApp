import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import { AuthProvider } from '../AuthContext';

describe('Authentication Flow', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.restoreAllMocks();
    // Stub fetch for initial contacts load
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ contacts: [] }),
      })
    );
  });
  afterEach(() => {
    jest.resetAllMocks();
  });

  test('shows login and register options when unauthenticated', () => {
    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Register')).toBeInTheDocument();
  });

  test('successful login and logout updates UI accordingly', async () => {
    // Mock login and @me endpoints
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/login')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ access_token: 'tok123' }),
        });
      }
      if (url.endsWith('/@me')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ id: 1, username: 'alice' }),
        });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Open login form
    fireEvent.click(screen.getByText('Login'));
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();

    // Fill and submit
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'alice' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'pass' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Wait for welcome message
    await waitFor(() => expect(screen.getByText(/welcome, alice/i)).toBeInTheDocument());
    expect(screen.getByText('Logout')).toBeInTheDocument();

    // Logout
    fireEvent.click(screen.getByText('Logout'));
    await waitFor(() => expect(screen.getByText('Login')).toBeInTheDocument());
    expect(screen.getByText('Register')).toBeInTheDocument();
  });

  test('login failure displays error message', async () => {
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/login')) {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ message: 'Invalid credentials' }),
        });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    fireEvent.click(screen.getByText('Login'));
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'bob' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument());
  });

  test('successful registration updates UI to authenticated state', async () => {
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/register')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ access_token: 'tokreg' }),
        });
      }
      if (url.endsWith('/@me')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ id: 2, username: 'newuser' }),
        });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Open register form
    fireEvent.click(screen.getByText('Register'));
    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument();

    // Fill and submit
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'newpass' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    // Wait for welcome message
    await waitFor(() => expect(screen.getByText(/welcome, newuser/i)).toBeInTheDocument());
  });
  
  test('registration failure displays error message', async () => {
    // Mock register endpoint to return error
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/register')) {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ message: 'Registration error' }),
        });
      }
      // Default fallback
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Open register form
    fireEvent.click(screen.getByText('Register'));
    // Fill in form fields
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'testpass' } });
    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    // Expect error message to appear
    await waitFor(() =>
      expect(screen.getByText(/registration error/i)).toBeInTheDocument()
    );
  });
  
  test('login missing fields displays error message', async () => {
    // Mock login endpoint to return missing-fields error
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/login')) {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ message: 'Username and password are required' }),
        });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Open login form and submit with missing password
    fireEvent.click(screen.getByText('Login'));
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'bob' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    await waitFor(() =>
      expect(screen.getByText(/username and password are required/i)).toBeInTheDocument()
    );
  });
  
  test('registration missing fields displays error message', async () => {
    // Mock register endpoint to return missing-fields error
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/register')) {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ message: 'Username and password are required' }),
        });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Open register form and submit with missing password
    fireEvent.click(screen.getByText('Register'));
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'alice' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    await waitFor(() =>
      expect(screen.getByText(/username and password are required/i)).toBeInTheDocument()
    );
  });
  
  test('switching between login and register clears error messages', async () => {
    // Mock login and register failures
    global.fetch = jest.fn((url, opts) => {
      if (url.endsWith('/login')) {
        return Promise.resolve({ ok: false, json: () => Promise.resolve({ message: 'Login error' }) });
      }
      if (url.endsWith('/register')) {
        return Promise.resolve({ ok: false, json: () => Promise.resolve({ message: 'Register error' }) });
      }
      return Promise.resolve({ ok: false, json: () => Promise.resolve({}) });
    });

    render(
      <AuthProvider>
        <App />
      </AuthProvider>
    );
    // Trigger login error
    fireEvent.click(screen.getByText('Login'));
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'user' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'pass' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    await waitFor(() => expect(screen.getByText(/login error/i)).toBeInTheDocument());
    // Switch to register, error should clear
    fireEvent.click(screen.getByText('Register'));
    expect(screen.queryByText(/login error/i)).not.toBeInTheDocument();
    // Trigger register error
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'user2' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'pass2' } });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));
    await waitFor(() => expect(screen.getByText(/register error/i)).toBeInTheDocument());
    // Switch back to login, register error should clear
    fireEvent.click(screen.getByText('Login'));
    expect(screen.queryByText(/register error/i)).not.toBeInTheDocument();
  });
});