import React, { useState } from "react";

const ImageSearch = () => {
    const [mode, setMode] = useState('image');
    // State for the search query
    const [query, setQuery] = useState("");
    // State to store the search results (images)
    const [images, setImages] = useState([]);
    // State to store any error messages
    const [error, setError] = useState(null);
    // State to indicate if the search is currently loading
    const [loading, setLoading] = useState(false);

    // State for filter parameters - using names that align with frontend controls
    const [license, setLicense] = useState(''); // Maps to license in API
    const [orientation, setOrientation] = useState(''); // Maps to aspect_ratio in API
    const [imageCount, setImageCount] = useState(0); // Maps to page_size in API
    const [imageSize, setImageSize] = useState(''); // Maps to size in API
    const [imageColor, setImageColor] = useState(''); // Maps to color in API
    const [imageCategory, setImageCategory] = useState(''); // Maps to category in API
    // Note: Image Sort was removed from the previous code snippet, so it's not included here.
    // If you need it back, add the state and the select element.

    const [tab, setTab] = useState('image'); // 'image' or 'audio'

    // Audio search state
    const [audioQuery, setAudioQuery] = useState("");
    const [audioResults, setAudioResults] = useState([]);
    const [audioLoading, setAudioLoading] = useState(false);
    const [audioError, setAudioError] = useState(null);

    // Search history state (with localStorage persistence)
    const [imageHistory, setImageHistory] = useState(() => {
        const saved = localStorage.getItem('imageSearchHistory');
        return saved ? JSON.parse(saved) : [];
    });
    const [audioHistory, setAudioHistory] = useState(() => {
        const saved = localStorage.getItem('audioSearchHistory');
        return saved ? JSON.parse(saved) : [];
    });

    // Helper to update localStorage
    const updateHistory = (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    };

    // Function to handle the search button click
    const handleSearch = async () => {
        // Prevent search if the query is empty
        if (!query) {
            setError("Please enter a search query.");
            setImages([]);
            return;
        }

        // Add to image search history (avoid duplicates, most recent first)
        if (query && (!imageHistory.length || imageHistory[0] !== query)) {
            const newHistory = [query, ...imageHistory.filter(q => q !== query)].slice(0, 10);
            setImageHistory(newHistory);
            updateHistory('imageSearchHistory', newHistory);
        }

        // Set loading state and clear previous results and errors
        setLoading(true);
        setError(null);
        setImages([]);

        try {
            // Base URL for the backend search endpoint
            let url = `http://localhost:5000/api/images/search?q=${encodeURIComponent(query)}`;

            // Append filter parameters only if they have a value
            // Use the parameter names that your backend expects (which should map to API names)

            if (license) {
                url += `&license=${encodeURIComponent(license)}`;
            }

            // Map frontend orientation values to backend/API aspect_ratio values
            if (orientation) {
                 // Your backend maps orientation to aspect_ratio, so send 'orientation'
                 // The backend will handle the mapping to 'aspect_ratio' for the API call.
                url += `&orientation=${encodeURIComponent(orientation)}`;
            }

            // imageCount maps to page_size in the backend
            if (imageCount > 0) { // Only include if greater than 0
                url += `&imageCount=${encodeURIComponent(imageCount)}`;
            }

            // imageSize maps to size in the backend
            if (imageSize) {
                 // Your backend maps imageSize to size, so send 'imageSize'
                 // The backend will handle the mapping to 'size' for the API call.
                url += `&imageSize=${encodeURIComponent(imageSize)}`;
            }

            // imageColor maps to color in the backend
            if (imageColor) {
                 // Your backend maps imageColor to color, so send 'imageColor'
                 // The backend will handle the mapping to 'color' for the API call.
                url += `&imageColor=${encodeURIComponent(imageColor)}`;
            }

            // imageCategory maps to category in the backend
            if (imageCategory) {
                 // Your backend maps imageCategory to category, so send 'imageCategory'
                 // The backend will handle the mapping to 'category' for the API call.
                url += `&imageCategory=${encodeURIComponent(imageCategory)}`;
            }

            // Note: imageSort parameter was removed from the frontend state and UI.
            // If you add it back, append it here:
            // if (imageSort) {
            //     url += `&imageSort=${encodeURIComponent(imageSort)}`;
            // }


            console.log("Fetching URL:", url); // Log the generated URL for debugging

            // Fetch data from the backend API
            const response = await fetch(url, {
                headers: {
                    // 'Authorization': `Bearer ${token}` // Uncomment if needed for protected routes
                }
            });

            // Check if the response was successful
            if (!response.ok) {
                let errorMsg = `HTTP error! status: ${response.status}`;
                try {
                    // Attempt to parse JSON error response from the backend
                    const errorData = await response.json();
                    if (errorData && errorData.error) {
                        errorMsg = errorData.error;
                    }
                } catch (jsonError) {
                    console.error("Could not parse error response JSON:", jsonError);
                }
                // Throw an error with a descriptive message
                throw new Error(errorMsg);
            }

            // Parse the JSON response
            const data = await response.json();

            // Update the images state with the results
            if (data.results) {
                setImages(data.results.map(img => ({
                    // Use thumbnail if available, otherwise fallback to url
                    url: img.thumbnail || img.url,
                    title: img.title || 'Untitled Image',
                    // Include other relevant image properties if needed for display
                    // e.g., img.creator, img.license, img.tags
                })));
            } else {
                // If results array is empty or missing, set images to an empty array
                setImages([]);
            }

        } catch (e) {
            // Handle errors during the fetch operation
            console.error("Error fetching images:", e);
            // Provide a user-friendly error message
            let displayError = e.message || "An unknown error occurred.";
            if (e.message.includes("Failed to fetch")) {
                 displayError = "Failed to connect to the backend. Please ensure it's running and accessible on http://localhost:5000.";
            } else if (e.message.includes("Backend configuration error")) {
                 // Display the specific backend configuration error if available
                 displayError = e.message;
            }
            setError(displayError);
            setImages([]); // Clear images on error
        } finally {
            // Set loading to false regardless of success or failure
            setLoading(false);
        }
    };

    // Audio search handler
    const handleAudioSearch = async () => {
        if (!audioQuery) {
            setAudioError("Please enter a search query.");
            setAudioResults([]);
            return;
        }

        // Add to audio search history (avoid duplicates, most recent first)
        if (audioQuery && (!audioHistory.length || audioHistory[0] !== audioQuery)) {
            const newHistory = [audioQuery, ...audioHistory.filter(q => q !== audioQuery)].slice(0, 10);
            setAudioHistory(newHistory);
            updateHistory('audioSearchHistory', newHistory);
        }

        setAudioLoading(true);
        setAudioError(null);
        setAudioResults([]);
        try {
            let url = `http://localhost:5000/api/audio/search?q=${encodeURIComponent(audioQuery)}`;
            const response = await fetch(url);
            if (!response.ok) {
                let errorMsg = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    if (errorData && errorData.error) {
                        errorMsg = errorData.error;
                    }
                } catch {}
                throw new Error(errorMsg);
            }
            const data = await response.json();
            if (data.results) {
                setAudioResults(data.results.map(aud => ({
                    url: aud.url,
                    title: aud.title || 'Untitled Audio',
                })));
            } else {
                setAudioResults([]);
            }
        } catch (e) {
            setAudioError(e.message || "An unknown error occurred.");
            setAudioResults([]);
        } finally {
            setAudioLoading(false);
        }
    };

    return (
        <>
            <div className="flex flex-col items-center justify-center min-h-[80vh] w-full">
                {/* Tab Switcher as prominent buttons */}
                <div className="flex w-full max-w-2xl mt-12 mb-6 gap-2">
                    <button
                        className={`flex-1 py-3 text-xl font-bold rounded-t-lg focus:outline-none transition-colors ${tab === 'image' ? 'bg-blue-600 text-white shadow' : 'bg-gray-800 text-blue-300 hover:bg-blue-700 hover:text-white'}`}
                        onClick={() => setTab('image')}
                    >
                        Image Search
                    </button>
                    <button
                        className={`flex-1 py-3 text-xl font-bold rounded-t-lg focus:outline-none transition-colors ${tab === 'audio' ? 'bg-blue-600 text-white shadow' : 'bg-gray-800 text-blue-300 hover:bg-blue-700 hover:text-white'}`}
                        onClick={() => setTab('audio')}
                    >
                        Audio Search
                    </button>
                </div>
                <div className="w-full max-w-5xl bg-gray-900 rounded-b-lg shadow-2xl p-0">
                    {tab === 'image' && (
                        <div className="p-10">
                            <h2 className="text-3xl font-bold mb-6 text-center text-blue-400">Open License Image Search</h2>
                            {/* Search Input and Button */}
                            <div className="flex flex-col sm:flex-row gap-4 mb-6">
                                <input
                                    type="text"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="Search for images..."
                                    className="flex-grow px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100 placeholder-gray-400"
                                />
                                <button
                                    onClick={handleSearch}
                                    disabled={loading || !query}
                                    className="px-6 py-2 rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 ease-in-out"
                                >
                                    {loading ? 'Searching...' : 'Search'}
                                </button>
                            </div>
                            {/* Image Search History */}
                            {imageHistory.length > 0 && (
                                <div className="mb-4">
                                    <div className="text-gray-400 mb-1 text-sm">Recent Searches:</div>
                                    <div className="flex flex-wrap gap-2">
                                        {imageHistory.map((item, idx) => (
                                            <button
                                                key={idx}
                                                onClick={() => { setQuery(item); handleSearch(); }}
                                                className="px-3 py-1 rounded bg-gray-800 text-blue-300 hover:bg-blue-700 hover:text-white text-sm transition"
                                            >
                                                {item}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}
                            {/* Filter Controls Section */}
                            <div className="mb-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                {/* License Filter Dropdown */}
                                <select
                                    value={license}
                                    onChange={e => setLicense(e.target.value)}
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100"
                                >
                                    <option value="">All Licenses</option>
                                    <option value="cc0">CC0</option>
                                    <option value="by">CC BY</option>
                                    <option value="by-sa">CC BY-SA</option>
                                    <option value="by-nd">CC BY-ND</option>
                                    <option value="by-nc">CC BY-NC</option>
                                    <option value="by-nc-sa">CC BY-NC-SA</option>
                                    <option value="by-nc-nd">CC BY-NC-ND</option>
                                </select>
                                {/* Orientation Filter Dropdown */}
                                <select
                                    value={orientation}
                                    onChange={e => setOrientation(e.target.value)}
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100"
                                >
                                    <option value="">All Orientations</option>
                                    <option value="landscape">Landscape</option>
                                    <option value="portrait">Portrait</option>
                                    <option value="square">Square</option>
                                </select>
                                {/* Image Count Input */}
                                <input
                                    type="number"
                                    min="1"
                                    max="100"
                                    value={imageCount}
                                    onChange={e => setImageCount(Number(e.target.value))}
                                    placeholder="Count"
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100 placeholder-gray-400 w-full"
                                />
                                {/* Image Size Dropdown */}
                                <select
                                    value={imageSize}
                                    onChange={e => setImageSize(e.target.value)}
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100"
                                >
                                    <option value="">All Sizes</option>
                                    <option value="small">Small</option>
                                    <option value="medium">Medium</option>
                                    <option value="large">Large</option>
                                    <option value="xlarge">Extra Large</option>
                                </select>
                                {/* Image Color Dropdown */}
                                <select
                                    value={imageColor}
                                    onChange={e => setImageColor(e.target.value)}
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100"
                                >
                                    <option value="">All Colors</option>
                                    <option value="black_and_white">Black & White</option>
                                    <option value="transparent">Transparent</option>
                                    <option value="red">Red</option>
                                    <option value="orange">Orange</option>
                                    <option value="yellow">Yellow</option>
                                    <option value="green">Green</option>
                                    <option value="blue">Blue</option>
                                    <option value="purple">Purple</option>
                                    <option value="pink">Pink</option>
                                    <option value="brown">Brown</option>
                                    <option value="gray">Gray</option>
                                    <option value="white">White</option>
                                    <option value="black">Black</option>
                                </select>
                                {/* Image Category Dropdown */}
                                <select
                                    value={imageCategory}
                                    onChange={e => setImageCategory(e.target.value)}
                                    className="px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100"
                                >
                                    <option value="">All Categories</option>
                                    <option value="nature">Nature</option>
                                    <option value="people">People</option>
                                    <option value="architecture">Architecture</option>
                                    <option value="animals">Animals</option>
                                    <option value="food">Food</option>
                                    <option value="travel">Travel</option>
                                    <option value="technology">Technology</option>
                                    <option value="sports">Sports</option>
                                    <option value="fashion">Fashion</option>
                                </select>
                            </div>
                            {/* Loading and Error Messages */}
                            {loading && <p className="text-center text-blue-400 mt-4">Loading images...</p>}
                            {error && <p className="text-center text-red-500 mt-4">{error}</p>}
                            {/* Image Results Display */}
                            {images.length > 0 && (
                                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 mt-6">
                                    {images.map((image, index) => (
                                        <div key={index} className="border border-gray-700 rounded-lg overflow-hidden shadow-md bg-gray-700">
                                            <img
                                                src={image.url}
                                                alt={image.title}
                                                className="w-full h-32 object-cover"
                                                onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/150x150/cccccc/333333?text=Image+Error'; }}
                                            />
                                            <p className="text-sm text-gray-300 p-2 truncate">{image.title}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                            {!loading && !error && images.length === 0 && query && (
                                <p className="text-center text-gray-400 mt-4">No images found for your search criteria. Try a different query or filters.</p>
                            )}
                            {!loading && !error && images.length === 0 && !query && (
                                <p className="text-center text-gray-400 mt-4">Enter a search query to find images.</p>
                            )}
                        </div>
                    )}
                    {tab === 'audio' && (
                        <div className="p-16 text-center text-gray-400 text-2xl min-h-[400px] flex flex-col items-center justify-center w-full">
                            <h2 className="text-3xl font-bold mb-6 text-center text-blue-400">Open License Audio Search</h2>
                            <div className="flex flex-col sm:flex-row gap-4 mb-6 w-full max-w-xl mx-auto">
                                <input
                                    type="text"
                                    value={audioQuery}
                                    onChange={e => setAudioQuery(e.target.value)}
                                    placeholder="Search for audio..."
                                    className="flex-grow px-4 py-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-100 placeholder-gray-400"
                                />
                                <button
                                    onClick={handleAudioSearch}
                                    disabled={audioLoading || !audioQuery}
                                    className="px-6 py-2 rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 ease-in-out"
                                >
                                    {audioLoading ? 'Searching...' : 'Search'}
                                </button>
                            </div>
                            {/* Audio Search History */}
                            {audioHistory.length > 0 && (
                                <div className="mb-4">
                                    <div className="text-gray-400 mb-1 text-sm">Recent Searches:</div>
                                    <div className="flex flex-wrap gap-2">
                                        {audioHistory.map((item, idx) => (
                                            <button
                                                key={idx}
                                                onClick={() => { setAudioQuery(item); handleAudioSearch(); }}
                                                className="px-3 py-1 rounded bg-gray-800 text-blue-300 hover:bg-blue-700 hover:text-white text-sm transition"
                                            >
                                                {item}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            )}
                            {audioLoading && <p className="text-blue-400 mt-4">Loading audio...</p>}
                            {audioError && <p className="text-red-500 mt-4">{audioError}</p>}
                            {audioResults.length > 0 && (
                                <div className="w-full max-w-2xl mx-auto mt-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
                                    {audioResults.map((audio, idx) => (
                                        <div key={idx} className="bg-gray-800 rounded-lg p-4 flex flex-col items-center shadow">
                                            <audio controls className="w-full mb-2">
                                                <source src={audio.url} />
                                                Your browser does not support the audio element.
                                            </audio>
                                            <p className="text-base text-gray-200 truncate w-full text-center">{audio.title}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                            {!audioLoading && !audioError && audioResults.length === 0 && audioQuery && (
                                <p className="text-gray-400 mt-4">No audio found for your search criteria. Try a different query.</p>
                            )}
                            {!audioLoading && !audioError && audioResults.length === 0 && !audioQuery && (
                                <p className="text-gray-400 mt-4">Enter a search query to find audio.</p>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </>
    );
};

export default ImageSearch;
