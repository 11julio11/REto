# Estrategia de Testing (Día 26)

Este documento detalla el enfoque de pruebas para el proyecto REto, asegurando la robustez y seguridad del sistema.

## Enfoque de Pruebas

Siguiendo los principios de **Clean Architecture**, las pruebas se dividen en:

1.  **Tests Unitarios**: Validación de lógica de negocio y casos de borde en aislamiento (usando repositorios en memoria).
2.  **Tests de Integración**: Pruebas sobre los routers de FastAPI para asegurar que los contratos de entrada/salida son correctos.

## Cobertura de Casos de Borde (Edge Cases)

Se han implementado pruebas específicas para los siguientes escenarios críticos en `backend/tests/test_main.py`:

### Autenticación e Identidad
- **Registro de Duplicados**: Verificación de que el sistema no permite usuarios con el mismo nombre (Día 27 upgrade).
- **Contraseñas Erróneas**: Validación de que las credenciales incorrectas retornan `401 Unauthorized`.
- **Usuarios Inexistentes**: Asegurar que intentar loguearse con un usuario que no existe no revela información sensible y retorna `401`.

### Autorización y Seguridad
- **Rutas Protegidas**: Verificación de que el middleware de seguridad bloquea accesos sin `Bearer Token`.
- **Tokens Inválidos/Expirados**: Validación de que tokens malformados son rechazados.

### Integridad de Datos
- **IDs Inexistentes**: Pruebas de que los endpoints de obtención y borrado retornan `404 Not Found` en lugar de fallar catastróficamente.
- **Payloadds Malformados**: Validación de que Pydantic captura errores de tipo y campos faltantes (Retorna `422 Unprocessable Entity`).

## Guía para Desarrolladores

Para ejecutar las pruebas y verificar la cobertura:

```bash
# Ejecutar pytest
pytest

# Generar reporte de cobertura
pytest --cov=src tests/
```

> [!TIP]
> Mantén siempre una cobertura superior al 70% para garantizar la estabilidad del proyecto final.
