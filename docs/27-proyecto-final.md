# Día 27: Proyecto Final - Subscription Manager

En esta etapa, transformamos una aplicación genérica en un producto real con un problema que resolver: el **Gestor de Suscripciones**.

## El Problema Real

El auge de los modelos SaaS ha fragmentado el gasto de los usuarios. Es difícil rastrear cuándo cobran, cuánto se paga en total y qué suscripciones ya no son útiles.

## Definición del MVP

El MVP (Producto Mínimo Viable) se define con las siguientes capacidades:

-   **Rastreo de Costos**: Gestión de precios y ciclos de facturación (mensual/anual).
-   **Dashboard de Control**: Visualización del gasto mensual proyectado.
-   **Gestión de Ciclos**: Registro de fechas de próximo pago para evitar cobros inesperados.

## Evolución del Dominio

Se realizó un pivot en el esquema de datos:
-   `Item` ➔ `Subscription`
-   `Price` ➔ `Cost` + `Billing Cycle`

Esta transformación permite que la aplicación pase de ser un "juguete técnico" a una herramienta de utilidad financiera.
