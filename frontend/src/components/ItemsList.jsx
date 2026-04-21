import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { fetchSubscriptions, createSubscription, deleteSubscription } from '../api/api'
import { useToast } from '../context/ToastContext'

export default function ItemsList() {
  const queryClient = useQueryClient()
  const { addToast } = useToast()
  const [form, setForm] = useState({ 
    name: '', 
    description: '', 
    cost: '', 
    billing_cycle: 'monthly',
    next_payment: new Date().toISOString().split('T')[0]
  })

  const { data: subscriptions, isLoading, isError, error } = useQuery({
    queryKey: ['subscriptions'],
    queryFn: fetchSubscriptions,
  })

  const createMutation = useMutation({
    mutationFn: createSubscription,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
      setForm({ 
        name: '', 
        description: '', 
        cost: '', 
        billing_cycle: 'monthly',
        next_payment: new Date().toISOString().split('T')[0]
      })
      addToast(`Suscripción "${data.name}" añadida.`, 'success')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteSubscription,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
      addToast('Suscripción eliminada.', 'info')
    },
  })

  const handleCreate = (e) => {
    e.preventDefault()
    createMutation.mutate({ ...form, cost: parseFloat(form.cost) })
  }

  if (isLoading) return (
    <div className="state-box">
      <div className="spinner" />
      <p>Cargando suscripciones...</p>
    </div>
  )

  if (isError) return (
    <div className="state-box error">
      <span>💥</span>
      <p>Error: {error.message}</p>
    </div>
  )

  const totalMonthlyCost = subscriptions.reduce((acc, sub) => {
    const cost = sub.cost || 0
    return acc + (sub.billing_cycle === 'monthly' ? cost : cost / 12)
  }, 0)

  return (
    <div className="items-container">
      <div className="dashboard-summary">
        <div className="summary-card">
          <span>Gasto Mensual Estimado</span>
          <strong>${totalMonthlyCost.toFixed(2)}</strong>
        </div>
        <div className="summary-card">
          <span>Suscripciones Activas</span>
          <strong>{subscriptions.length}</strong>
        </div>
      </div>

      <h2>💳 Mis Suscripciones</h2>

      <form onSubmit={handleCreate} className="create-form">
        <input
          placeholder="Servicio (Netflix, AWS...)"
          value={form.name}
          onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
          required
        />
        <input
          type="number"
          placeholder="Costo"
          value={form.cost}
          onChange={e => setForm(f => ({ ...f, cost: e.target.value }))}
          step="0.01"
          required
        />
        <select
          value={form.billing_cycle}
          onChange={e => setForm(f => ({ ...f, billing_cycle: e.target.value }))}
          className="auth-input"
        >
          <option value="monthly">Mensual</option>
          <option value="yearly">Anual</option>
        </select>
        <input
          type="date"
          value={form.next_payment}
          onChange={e => setForm(f => ({ ...f, next_payment: e.target.value }))}
          required
        />
        <button type="submit" className="btn-primary" disabled={createMutation.isPending}>
          {createMutation.isPending ? 'Añadiendo...' : '+ Añadir'}
        </button>
      </form>

      {subscriptions.length === 0 ? (
        <p className="empty">No tienes suscripciones registradas.</p>
      ) : (
        <div className="items-grid">
          {subscriptions.map(sub => (
            <div key={sub.id} className="item-card">
              <div className="item-info">
                <strong>{sub.name}</strong>
                <p>{sub.description || `Pago ${sub.billing_cycle === 'monthly' ? 'mensual' : 'anual'}`}</p>
                <p className="hint">Próximo cobro: {sub.next_payment}</p>
              </div>
              <div className="item-actions">
                <span className="price">${sub.cost.toFixed(2)}</span>
                <button
                  className="btn-delete"
                  onClick={() => deleteMutation.mutate(sub.id)}
                  disabled={deleteMutation.isPending}
                >
                  🗑
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
