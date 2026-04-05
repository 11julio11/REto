# 🧼 Día 8: Clean Architecture y Dependency Injection

A medida que una aplicación crece, tener toda tu lógica en el punto de entrada web (`main.py` o `main.go`) se vuelve una pesadilla inmodificable y difícil de testear en aislamiento.

Para solucionar esto, aplicamos los principios de **Clean Architecture** (Arquitectura Limpia).

## La idea central de Clean Architecture
La regla suprema de esta arquitectura es la **Regla de Dependencia**: el código interior o "central" de la aplicación (los dominios y lógicas de tus reglas de negocio) NUNCA debe saber nada del mundo exterior (las bases de datos externas, los frameworks de interfaz gráfica, o web como FastAPI).

Las capas apuntan hacia adentro:
1. **Dominios / Interfaces / Modelos (Punto 0):** Saben cómo se ve la información limpia de tu empresa. 
2. **Servicios (Casos de Uso):** Accionan mediante reglas (ej: "si la entidad no existe, tira error de nuestra app, no de postgres").
3. **Repositorios (Infraestructura):** Conectores, mapeadores. Transforman la estructura de tu SQL al Modelo nativo central de tu aplicación (punto 1).
4. **Handlers / Web (APIs):** Expone lo anterior a los usuarios y parsea peticiones.

## ¿Qué es la Inyección de Dependencias (DI)?

Es la práctica clave para asegurar la estabilidad de la Clean Architecture.

En vez de hacer esto (Fuerte Acoplamiento):
```python
# MALA PRÁCTICA (El servicio no es testeable si se cae tu postgresql)
class UserService:
    def __init__(self):
        self.db = ConexiónAPostgreSQL("credentials...")
```

Haces esto (Inyección de Dependencias + Interfaces):
```python
# BUENA PRÁCTICA (El servicio es agnóstico del motor)
class UserService:
    def __init__(self, repositorio: InterfaceOClaseBaseRepositorio):
        self.db = repositorio
```

## Beneficio Estelar en Testing (Los "Mocks")

A la hora de aplicar pruebas unitarias (Testing), conectarse a una DB real consume incontable tiempo y estresa la red o las cuotas, además de ser propenso a inestabilidades (flaky tests).

Con inyección de dependencias, construimos un "objeto falso" o **Mock** que cumpla las condiciones de la clase base (`InterfaceOClaseBaseRepositorio`) y lo inyectamos al servicio en los casos de prueba. Resultan en tests limpios y veloces que comprueban nuestra lógica pura y dura, evadiendo fallos externos a nuestro alcance.
