import React from "react";

const Navbar = ({ mode, setMode }) => (
  <nav style={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '1rem',
    background: '#222',
    color: '#fff',
    marginBottom: '2rem',
    gap: '2rem',
  }}>
    <button
      style={{
        background: 'none',
        border: 'none',
        color: '#fff',
        fontSize: '1.1rem',
        cursor: 'pointer',
        textDecoration: mode === 'image' ? 'underline' : 'none',
      }}
      onClick={() => setMode('image')}
    >
      Image Search
    </button>
    <button
      style={{
        background: 'none',
        border: 'none',
        color: '#fff',
        fontSize: '1.1rem',
        cursor: 'pointer',
        textDecoration: mode === 'audio' ? 'underline' : 'none',
      }}
      onClick={() => setMode('audio')}
    >
      Audio Search
    </button>
  </nav>
);

export default Navbar;
