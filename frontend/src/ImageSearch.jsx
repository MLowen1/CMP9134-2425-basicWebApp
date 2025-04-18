import React, { useState } from "react";

const ImageSearch = () => {
    const [query, setQuery] = useState("");
    const [images, setImages] = useState([]);  // Initialize as an empty array instead of undefined
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        setError(null); // Clear previous errors
        setImages([]); // Clear previous images
        try {
            // Corrected the URL to match the backend route /api/images/search
            const response = await fetch(`http://localhost:5000/api/images/search?q=${query}`);
            
            // Check if the response was not ok (status code 200-299)
            if (!response.ok) {
                let errorMsg = `HTTP error! status: ${response.status}`;
                try {
                    // Attempt to get more specific error from backend response body
                    const errorData = await response.json();
                    if (errorData && errorData.error) {
                        errorMsg = errorData.error; // Use backend error message
                    }
                } catch (jsonError) {
                    // If response body is not JSON or empty, keep the original HTTP error
                    console.error("Could not parse error response JSON:", jsonError);
                }
                throw new Error(errorMsg);
            }
            
            const data = await response.json();
            
            // The API returns results in a nested structure, so we need to extract the actual images
            if (data.results) {
                setImages(data.results.map(img => ({
                    url: img.thumbnail || img.url, // Prefer thumbnail, fallback to full url
                    title: img.title || 'Untitled Image'
                })));
            } else {
                setImages([]); // Handle cases where 'results' might be missing even on success
            }
            // setError(null); // Already cleared at the start

        } catch (e) {
            console.error("Error fetching images:", e);
            let displayError = e.message || "An unknown error occurred.";
            // Provide a more helpful message for generic network errors
            if (e.message === "Failed to fetch") {
                displayError = "Failed to connect to the backend. Please ensure it's running and accessible.";
            }
            // Display the refined error message
            setError(displayError);
            setImages([]);  // Ensure images are cleared on error
        }
    };

    return (
        <div>
            <h2>Image Search</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for images..."
            />
            <button onClick={handleSearch}>Search</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px" }}>
                {images.length > 0 ? (
                    images.map((image, index) => (
                        <div key={index}>
                            <img src={image.url} alt={image.title} style={{ maxWidth: "100%" }} />
                            <p>{image.title}</p>
                        </div>
                    ))
                ) : (
                    // Display message only if there's no error and no images after a search attempt
                    !error && <p>No images to display. Try searching for something!</p> 
                )}
            </div>
        </div>
    );
};

export default ImageSearch;