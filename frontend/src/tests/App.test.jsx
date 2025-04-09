import { render, screen, fireEvent, waitFor } from '@testing-library/react'; // Add waitFor
import '@testing-library/jest-dom';
import App from '../App';
import React from 'react';

// Mock fetch globally - Reset implementation before each test
beforeEach(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ contacts: [] }), // Default empty contacts
      })
    );
});


describe('App Component', () => {
    // fetch.mockClear() is less critical if we reset implementation in beforeEach

    test('renders the app with tabs and contacts tab initially', async () => { // Make test async
        render(<App />);

        // Check tab buttons exist
        expect(screen.getByRole('button', {name: /Contacts/i })).toBeInTheDocument();
        expect(screen.getByRole('button', {name: /Image Search/i })).toBeInTheDocument();

        // Wait for the initial state update from fetch/useEffect
        await waitFor(() => {
            // Check for something uniquely in the Contacts tab after initial render
            expect(screen.getByText(/Create New Contact/i)).toBeInTheDocument();
        });
    });

    test('switches between tabs', async () => { // Make test async
        render(<App />);

        // 1. Wait for initial render to settle (Contacts tab)
        // We know this text should be present initially from the previous test's waitFor
        await waitFor(() => {
             expect(screen.getByText(/Create New Contact/i)).toBeInTheDocument();
        });


        // 2. Click on Image Search tab button
        // Using getByRole is slightly more robust for a button than getByText
        fireEvent.click(screen.getByRole('button', { name: /Image Search/i }));

        // 3. Wait for the re-render after the click
        await waitFor(() => {
            // Should now show Image Search content - USE CORRECT QUERY
            // expect(screen.getByText(/Search for images/i)).toBeInTheDocument(); // <<< This is WRONG
            expect(screen.getByPlaceholderText(/Search for images/i)).toBeInTheDocument(); // <<< This is CORRECT

            // Check that content from the other tab is gone
            expect(screen.queryByText(/Create New Contact/i)).not.toBeInTheDocument();
        });

        // 4. (Optional but good) Click back to Contacts tab
         fireEvent.click(screen.getByRole('button', { name: /Contacts/i }));

         // 5. Wait for re-render again
         await waitFor(() => {
            expect(screen.getByText(/Create New Contact/i)).toBeInTheDocument();
            expect(screen.queryByPlaceholderText(/Search for images/i)).not.toBeInTheDocument();
         });
    });
});