import { useState } from 'react'
import { loginUser, registerUser } from '../api/api'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState('login')  // 'login' | 'register'
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (mode === 'register') {
        await registerUser({ username, password })
        // Auto-login logic
        const tokens = await loginUser({ username, password })
        localStorage.setItem('access_token', tokens.access_token)
        onLogin()
      } else {
        const tokens = await loginUser({ username, password })
        localStorage.setItem('access_token', tokens.access_token)
        onLogin()
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Error de autenticación')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-card">
      <div className="auth-logo">⚡</div>
      <h1>{mode === 'login' ? 'Iniciar Sesión' : 'Crear Cuenta'}</h1>
      <p className="auth-subtitle">Reto T-Shaped Engineer — Día 25</p>

      <form onSubmit={handleSubmit} className="auth-form">
        <div className="field">
          <label>Usuario</label>
          <input
            type="text"
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="field">
          <label>Contraseña</label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && (
          <div className={`auth-msg ${error.startsWith('✅') ? 'success' : 'error'}`}>
            {error}
          </div>
        )}

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Cargando...' : mode === 'login' ? 'Entrar' : 'Registrarme'}
        </button>
      </form>

      <p className="auth-toggle">
        {mode === 'login' ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
        <button onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError(null) }}>
          {mode === 'login' ? ' Regístrate' : ' Inicia Sesión'}
        </button>
      </p>
    </div>
  )
}
