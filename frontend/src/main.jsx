import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
<<<<<<< HEAD
import './tailwind.css'
=======
import './index.css'
import { AuthProvider } from './AuthContext.jsx'
<<<<<<< HEAD
>>>>>>> 3360de8433e9c349d4875dd3f15be616af263587
=======
>>>>>>> 3360de8433e9c349d4875dd3f15be616af263587

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>,
)
