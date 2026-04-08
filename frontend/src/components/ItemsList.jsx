import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { fetchItems, createItem, deleteItem } from '../services/api'
import { useToast } from '../context/ToastContext'

export default function ItemsList() {
  const queryClient = useQueryClient()
  const { addToast } = useToast()
  const [form, setForm] = useState({ name: '', description: '', price: '' })

  // ── useQuery: el corazón de TanStack Query ──────────────────────────────
  // - queryKey: clave única de caché. Si otros componentes piden ['items'],
  //   usan el mismo caché sin disparar un segundo fetch.
  // - queryFn: la función que realmente hace el fetch.
  // - isLoading, isError, data: estados derivados automáticamente, CERO useState manual.
  const { data: items, isLoading, isError, error } = useQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
  })

  // ── useMutation: para operaciones que cambian datos (POST, DELETE) ────────
  const createMutation = useMutation({
    mutationFn: createItem,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['items'] })
      setForm({ name: '', description: '', price: '' })
      addToast(`Item "${data.name}" creado correctamente.`, 'success')
    },
    onError: () => {}, // El interceptor global ya lo muestra
  })

  const deleteMutation = useMutation({
    mutationFn: deleteItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] })
      addToast('Item eliminado.', 'info')
    },
    onError: () => {},
  })

  const handleCreate = (e) => {
    e.preventDefault()
    createMutation.mutate({ ...form, price: parseFloat(form.price) })
  }

  if (isLoading) return (
    <div className="state-box">
      <div className="spinner" />
      <p>Cargando items desde la API...</p>
    </div>
  )

  if (isError) return (
    <div className="state-box error">
      <span>💥</span>
      <p>Error: {error.message}</p>
      <p className="hint">¿Está el backend corriendo en el puerto 8000?</p>
    </div>
  )

  return (
    <div className="items-container">
      <h2>📦 Items <span className="badge">{items.length}</span></h2>

      {/* Formulario de creación */}
      <form onSubmit={handleCreate} className="create-form">
        <input
          placeholder="Nombre"
          value={form.name}
          onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
          required
        />
        <input
          placeholder="Descripción (opcional)"
          value={form.description}
          onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
        />
        <input
          type="number"
          placeholder="Precio"
          value={form.price}
          onChange={e => setForm(f => ({ ...f, price: e.target.value }))}
          step="0.01"
          required
        />
        <button type="submit" className="btn-primary" disabled={createMutation.isPending}>
          {createMutation.isPending ? 'Creando...' : '+ Crear Item'}
        </button>
      </form>

      {/* Tabla de items */}
      {items.length === 0 ? (
        <p className="empty">No hay items aún. ¡Crea el primero!</p>
      ) : (
        <div className="items-grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <div className="item-info">
                <strong>{item.name}</strong>
                {item.description && <p>{item.description}</p>}
                <span className="price">${item.price.toFixed(2)}</span>
              </div>
              <button
                className="btn-delete"
                onClick={() => deleteMutation.mutate(item.id)}
                disabled={deleteMutation.isPending}
                title="Eliminar item"
              >
                🗑
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
