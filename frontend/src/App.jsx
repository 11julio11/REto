import { useState } from 'react'
import Login from './components/Login'
import ItemsList from './components/ItemsList'
import './App.css'

export default function App() {
  // Estado de sesión: comprobamos si ya hay token en localStorage
  const [isLoggedIn, setIsLoggedIn] = useState(
    () => !!localStorage.getItem('access_token')
  )

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setIsLoggedIn(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <span className="logo">⚡</span>
          <span>Reto T-Shaped <em>Day 12</em></span>
        </div>
        {isLoggedIn && (
          <button className="btn-logout" onClick={handleLogout}>
            Cerrar Sesión
          </button>
        )}
      </header>

      <main className="app-main">
        {isLoggedIn
          ? <ItemsList />
          : <Login onLogin={() => setIsLoggedIn(true)} />
        }
      </main>
    </div>
  )
}
