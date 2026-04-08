# Día 13: Manejo de Errores Global — Toasts desde el Backend

Cuando múltiples componentes hacen fetching, cada uno podría manejar errores por separado con sus propios `try/catch` y `useState`. Eso crea inconsistencia: algunos componentes muestran texto rojo, otros ignoran el error silenciosamente, y el usuario no sabe qué pasó.

**La solución profesional:**  un canal global de errores → un sistema unificado de Toasts.

## Arquitectura del Sistema

```
Axios Interceptor (api.js)
    ↓ onGlobalError(message, type)
setGlobalErrorHandler() — registrado en App.jsx
    ↓ llama a addToast()
ToastContext (React Context)
    ↓ estado global de notificaciones
ToastContainer
    ↓ renderiza los Toasts flotantes en pantalla
```

## Dos niveles de manejo

### 1. Interceptor de Axios (errores de red/HTTP)
El interceptor de respuesta centraliza y clasifica TODOS los errores antes de que lleguen al componente:

```js
// api.js
apiClient.interceptors.response.use(
  (response) => response, // ✅ pasa sin tocar
  (error) => {
    const status = error.response?.status
    
    if (!error.response)   addToast('Sin conexión al servidor', 'error')
    else if (status === 401) addToast('Sesión expirada', 'warning')
    else if (status === 404) addToast('Recurso no encontrado', 'info')
    else if (status >= 500) addToast('Error del servidor', 'error')
    
    return Promise.reject(error) // re-lanza para componentes que necesiten saberlo
  }
)
```

### 2. Toasts de éxito (en componentes)
Las mutaciones exitosas disparan toasts de `success` directamente:

```js
const createMutation = useMutation({
  mutationFn: createItem,
  onSuccess: (data) => {
    addToast(`Item "${data.name}" creado correctamente.`, 'success')
    // ...
  }
})
```

## Context vs Prop Drilling

Sin Context, para que un interceptor de Axios dispare un Toast habría que pasar callbacks por props a través de múltiples capas. Con `ToastContext`, cualquier módulo importa `useToast()` y ya tiene acceso al sistema de notificaciones:

```js
const { addToast } = useToast()
addToast('Mensaje', 'success' | 'error' | 'warning' | 'info')
```

## Tipos de Toast y cuándo usarlos

| Tipo      | Cuándo                                    | Color    |
|-----------|-------------------------------------------|----------|
| `error`   | Error 5xx, red caída                      | 🔴 Rojo  |
| `warning` | 401 Expirado, 403 Prohibido, datos mal    | 🟡 Ámbar |
| `info`    | 404 No encontrado, eliminación de item    | 🔵 Azul  |
| `success` | Creación exitosa, login, registro         | 🟢 Verde |
