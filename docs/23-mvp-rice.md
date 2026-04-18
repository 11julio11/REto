# Día 23: MVP Thinking & RICE Framework

En el desarrollo de software y construcción de productos, los recursos (tiempo, dinero, talento) son siempre limitados. Por ello, la priorización de tareas no puede basarse en la intuición o en "lo que suene más divertido de programar", sino en el marco de la maximización del valor. Aquí es donde entran el **MVP Thinking** y el **Framework RICE**.

## 1. MVP Thinking (Producto Mínimo Viable)

El MVP no es un producto "a medias" ni una herramienta llena de errores. Se define como la versión de un nuevo producto que permite a un equipo recolectar la máxima cantidad de aprendizaje validado sobre los clientes con el **menor esfuerzo posible**.

* **No es:** Construir una rueda, luego dos ruedas, luego el chasis y por último el coche (el usuario no recibe valor hasta el final).
* **Sí es:** Construir una patineta, luego una bicicleta, luego una motocicleta, luego un coche. En cada iteración el usuario obtiene un medio de transporte funcional (valor) y el equipo adquiere retroalimentación (aprendizaje).

Si estamos desarrollando un "Módulo de Asistencias", el MVP podría ser simplemente un botón para marcar a todos los alumnos como presentes y desmarcar a los ausentes, registrándolo en la base de datos, en vez de arrancar con gráficos complejos, IA predictiva de ausencias o notificaciones automáticas por SMS a los padres.

## 2. El Framework RICE

Para decidir qué funcionalidades construir en nuestro MVP o en futuras iteraciones, utilizamos frameworks de priorización estructurados. **RICE** es uno de los sistemas más populares y pragmáticos, creado por Intercom. 

Se basa en calificar 4 factores para cada funcionalidad en el backlog:

### R - Reach (Alcance)
¿A cuántas personas afectará esta función en un periodo de tiempo determinado?
* *Ejemplo:* Si tienes 100 usuarios activos diarios y estimas que el 50% de ellos usará la funcionalidad de exportar PDF cada mes, tu alcance es de **50 usuarios/mes**.
* *Métrica típica:* Usuarios por mes o trimestre.

### I - Impact (Impacto)
Si un usuario utiliza esta funcionalidad, ¿cuánto valor le aporta o cuánto nos acerca a nuestro objetivo de negocio (retención, conversión, usabilidad)?
* **3:** Impacto Masivo
* **2:** Impacto Alto
* **1:** Impacto Medio
* **0.5:** Impacto Bajo
* **0.25:** Impacto Mínimo

### C - Confidence (Confianza)
Para evitar que nuestro optimismo infle las estimaciones de Alcance e Impacto, debemos ser honestos sobre qué tan seguros estamos de nuestros datos.
* **100%:** Alta confianza (Tenemos datos, investigaciones, encuestas de usuarios).
* **80%:** Confianza media (Tenemos algo de datos o intuición fundamentada).
* **50%:** Confianza baja (Es una "corazonada", no tenemos evidencia sólida).
* *Porcentaje menor a 50%:* "Moonshot", extremadamente especulativo.

### E - Effort (Esfuerzo)
¿Cuánto tiempo le tomará al equipo (producto, diseño, ingeniería) completar esto?
* *Métrica típica:* "Person-months" (Meses de trabajo por persona), "Semanas" o "Días".
* *Ejemplo:* Si toma una semana de diseño y dos de programación, son 3 semanas. Para proyectos individuales en días, el esfuerzo de 4 días es E = 4.

## 3. La Fórmula RICE y el Scoring

Una vez que tenemos los valores, aplicamos la fórmula:

**Score RICE = (Reach × Impact × Confidence) / Effort**

### Ejemplo de Priorización

Supongamos que en un Sistema Escolar tenemos dos tareas pendientes:

**Tarea A: Reparar Bug en Login (Los usuarios con correos '.edu' a veces fallan al acceder)**
* **Reach:** 500 usuarios (todos los afectados mensuales).
* **Impact:** 3 (Masivo, sin esto no pueden usar el sistema).
* **Confidence:** 100% (Tenemos los logs y sabemos exactamente el problema).
* **Effort:** 0.5 semanas.
* **Score:** (500 × 3 × 1) / 0.5 = **3000**

**Tarea B: Dashboard Analítico Moderno 3D para Directores**
* **Reach:** 5 usuarios (sólo los directivos lo ven periódicamente).
* **Impact:** 2 (Alto, pero la operación diaria corre sin ello).
* **Confidence:** 50% (Sospechamos que lo quieren, pero no lo han pedido explícitamente).
* **Effort:** 4 semanas.
* **Score:** (5 × 2 × 0.5) / 4 = **1.25**

### Conclusión

La matemática del RICE destruye nuestro sesgo cognitivo. El "Dashboard 3D" (Tarea B) podría sonar fenomenal para programar por el reto técnico, pero el RICE de **1.25 vs 3000** nos obliga estratégicamente a enfocarnos en asegurar el embudo principal (el Login) que en realidad aporta mayor retorno a la estabilidad del negocio e incrementa el alcance operativo (Reach).
