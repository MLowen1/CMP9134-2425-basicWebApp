import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ImageSearch from '../ImageSearch';
import React from 'react';

// Mock fetch for testing
global.fetch = jest.fn(); // Initialize fetch mock

describe('ImageSearch Component', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockClear();
  });

  test('renders search input and button', () => {
    render(<ImageSearch />);
    
    expect(screen.getByPlaceholderText(/Search for images/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Search/i })).toBeInTheDocument();
  });

  test('displays initial message when no images', () => {
    render(<ImageSearch />);
    
    expect(screen.getByText(/No images to display/i)).toBeInTheDocument();
  });

  test('calls API and displays images when searching', async () => {
    // Mock successful fetch
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          results: [
            { thumbnail: 'image1.jpg', title: 'Image 1' },
            { thumbnail: 'image2.jpg', title: 'Image 2' }
          ]
        }),
      })
    );

    render(<ImageSearch />);
    
    // Enter search term
    const input = screen.getByPlaceholderText(/Search for images/i);
    fireEvent.change(input, { target: { value: 'nature' } });
    
    // Click search button
    const button = screen.getByRole('button', { name: /Search/i });
    fireEvent.click(button);
    
    // Verify fetch was called with the CORRECT endpoint
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/images/search?q=nature');
    
    // Wait for images to load
    await waitFor(() => {
        expect(screen.getByText('Image 1')).toBeInTheDocument();
        expect(screen.getByText('Image 2')).toBeInTheDocument();
        expect(screen.getAllByRole('img')).toHaveLength(2);
    });
  });

  test('displays error message when API call fails', async () => {
    // Mock failed fetch with a specific error message in the body
    const mockErrorMessage = "Backend service unavailable";
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        status: 503, // Simulate a server error like Service Unavailable
        json: () => Promise.resolve({ error: mockErrorMessage }), // Backend error structure
      })
    );

    render(<ImageSearch />);

    // Enter search term
    const input = screen.getByPlaceholderText(/Search for images/i);
    fireEvent.change(input, { target: { value: 'failure' } });

    // Click search button
    const button = screen.getByRole('button', { name: /Search/i });
    fireEvent.click(button);

    // Wait for the specific error message from the backend to appear
    await waitFor(() => {
      // Use a regex for flexibility or exact string match
      expect(screen.getByText(mockErrorMessage)).toBeInTheDocument(); 
    });

    // Ensure no images are displayed
    expect(screen.queryByRole('img')).not.toBeInTheDocument();
    
    // Check that the initial "No images" message is not displayed when an error occurs
    expect(screen.queryByText(/No images to display/i)).not.toBeInTheDocument();
  });
});