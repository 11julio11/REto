import { createContext, useContext, useState, useCallback, useMemo } from 'react'

// ── Context ───────────────────────────────────────────────────────────────
const ToastContext = createContext(null)

let toastId = 0

// ── Provider ──────────────────────────────────────────────────────────────
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const addToast = useCallback((message, type = 'error', duration = 4000) => {
    const id = ++toastId
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id))
    }, duration)
  }, [])

  const dismiss = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const value = useMemo(() => ({ addToast }), [addToast])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} onDismiss={dismiss} />
    </ToastContext.Provider>      
  )
}

// ── Hook público ─────────────────────────────────────────────────────────
// Uso: const { addToast } = useToast()
// addToast('Mensaje', 'success' | 'error' | 'warning' | 'info')
export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast debe usarse dentro de <ToastProvider>')
  return ctx
}

// ── UI: contenedor de toasts ──────────────────────────────────────────────
const ICONS = {
  error:   '💥',
  success: '✅',
  warning: '⚠️',
  info:    'ℹ️',
}

function ToastContainer({ toasts, onDismiss }) {
  return (
    <div className="toast-container" role="region" aria-label="Notificaciones">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`toast toast-${toast.type}`}
          role="alert"
          onClick={() => onDismiss(toast.id)}
        >
          <span className="toast-icon">{ICONS[toast.type]}</span>
          <span className="toast-msg">{toast.message}</span>
          <button className="toast-close" onClick={() => onDismiss(toast.id)}>✕</button>
        </div>
      ))}
    </div>
  )
}
