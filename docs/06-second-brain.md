# 🧠 Día 6: Sistema Personal - Zettelkasten o "Second Brain"

## ¿Por qué un "Segundo Cerebro"?

"La mente es para tener ideas, no para guardarlas." — David Allen (GTD)

Los humanos somos malos recordando comandos complejos de terminal. Un Ingeniero Senior no confía en su memoria, confía indiscutiblemente en su **Documentación**.
En la industria, el talento que sabe *cómo hacerlo* es costoso, pero aquel que también documenta **cómo y por qué lo hizo**, es quien promueven y escala equipos enteros.

## Estructuras y Filosofías

### Zettelkasten (El Método Tradicional de Alemania)
Traducido como "Caja de Notas". Creado por Niklas Luhmann, consiste en tarjetas de una sola idea atómica que contienen enlaces con otras notas. 
- *Notas Fugaces:* Algo pasajero.
- *Notas de Literatura:* Lo rescatable e interpretado de un libro.
- *Notas Permanentes:* Conocimiento base indexado e interrelacionado.

Para software, utilizamos algo similar en repositorios `Markdown`: Notas en grafo (por ejemplo, el software Obsidian o Logseq).

## Aplicado en Ingeniería (El Contexto de Este Proyecto)

Un repositorio no debería llenarse solo del código productivo fuente y dependencias ajenas, sino tener en su raíz un subdirectorio `docs/`.

A la hora en que necesites redondear para una entrevista: "Dime qué retoños y arquitecturas has implementado", puedes simplemente volver a tu Second Brain e interconectar tu repositorio.
Además, tus compañeros sabrán la razón de que escogiste hacer algo:

**Technical Decision Records (TDR)**:
¿Por qué preferimos PostgreSQL frente a MySQL en este caso? ¿Por qué usar Redis y K8s o solo Docker? Anotarlo prevendrá meses de dudas.

Crear la carpeta `/docs` es consolidar esta disciplina: si aprendes cómo realizar CI/CD e inyección de secretos con variables de entorno temporalizado con Multi-stage builds, te obligas a ti mismo a documentarlo como los repositorios de Días 1 al 7 recién creados.
