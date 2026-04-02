# 🏗️ Día 4: CI/CD Pipeline y Testing Automático

CI/CD significa *Continuous Integration and Continuous Delivery* (Integraciones y Entregas Continuas).

Es el acto de asegurar que **nadie** pueda subir código roto al repositorio principal (`main` o `master`). Aquí es donde un repositorio personal de portafolio se transforma en uno de ingeniería real.

## Automatización: ¿Por qué GitHub Actions?

Automatizamos nuestra paranoia. Antes de aceptar un "Pull Request", exigimos a la máquina que pase 3 puertas obligatorias de validación:

### Puerta 1: Linting (El Estilista de Código)
Herramientas como `flake8` (Python), `ESLint` (JS) o `golangci-lint` (Go).
Busca errores de sintaxis, falta de paridad de formatos y variables que se llamaron y no se usan.
*¿Falla esto?* **Se detiene.**

### Puerta 2: Tests Unitarios (El Interrogador)
Aquí se validan bloques lógicos aislados a través de `pytest` o el `testing` de Go. 
Comprobamos que nuestra API de hecho retorna códigos estado `200 OK` y procesa mal un payload tirando `422 Unprocessable Entity` en un registro inválido.

*Regla de Orot:* Si tu código está mal acoplado dependencialmente y no usa Interfaces, entonces realizar unit-testing será imposible o miserable (necesitarás conectarte a una Base de datos real solo para testear tu backend - mala práctica).

### Puerta 3: Build de la imagen (El Empaquetado)
Sólo si todas las pruebas del interrogador pasaron se empaqueta la imagen Docker. Al empaquetarlo nos garantizamos de que las dependencias concuerdan. Si el build es exitoso, la imagen se etiqueta con el `commit SHA` para versionado único.

## Pipeline Code as Infrastructure

```yaml
jobs:
  lint:
    run: flake8 .
  test:
    needs: lint
    run: pytest tests/
  build:
    needs: test
    run: docker build -t miproject:latest .
```

Si implementamos a futuro una acción `Deploy`, se amarrará a la directiva `needs: build`. Si la integración continua no supera estas barreras, el botón "Merge" para GitHub brilla en gris previniendo una tragedia de código en producción.
