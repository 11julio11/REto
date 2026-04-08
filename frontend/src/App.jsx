import { useState, useEffect } from 'react'
import Login from './components/Login'
import ItemsList from './components/ItemsList'
import { ToastProvider, useToast } from './context/ToastContext'
import { setGlobalErrorHandler } from './services/api'
import './App.css'

// Componente interior que conecta el interceptor con el context de Toasts
function AppInner() {
  const { addToast } = useToast()

  const [isLoggedIn, setIsLoggedIn] = useState(
    () => !!localStorage.getItem('access_token')
  )

  // Registramos el handler global de axios al montar el árbol de componentes
  useEffect(() => {
    setGlobalErrorHandler((message, type) => addToast(message, type))
  }, [addToast])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setIsLoggedIn(false)
    addToast('Sesión cerrada correctamente.', 'info')
  }

  const handleLogin = () => {
    setIsLoggedIn(true)
    addToast('Bienvenido de nuevo 👋', 'success')
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <span className="logo">⚡</span>
          <span>Reto T-Shaped <em>Day 13</em></span>
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
          : <Login onLogin={handleLogin} />
        }
      </main>
    </div>
  )
}

// ToastProvider envuelve todo para que cualquier componente pueda disparar toasts
export default function App() {
  return (
    <ToastProvider>
      <AppInner />
    </ToastProvider>
  )
}
