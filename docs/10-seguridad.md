# Día 10: Seguridad, JWT, Refresh Tokens y Hashing (Argon2 / Bcrypt)

En aplicaciones modernas, asegurar las rutas de la API es vital para evitar el acceso malintencionado. Usamos una combinación de técnicas de seguridad y criptografía.

## Conceptos Clave

1. **JWT (JSON Web Token)**: Es un estándar abierto (RFC 7519) que define una forma compacta y autónoma de transmitir información de forma segura entre las partes como un objeto JSON. La información puede ser verificada y confiada porque está firmada digitalmente (generalmente con un secreto HMAC o par de claves públicas/privadas RSA/ECDSA).

2. **Access Token y Refresh Token**:
    - **Access Token**: Un JWT de corta duración (p. ej., 15 minutos) que se envía en cada solicitud (generalmente en la cabecera `Authorization: Bearer <token>`).
    - **Refresh Token**: Un token de larga duración (p. ej., 7 días) que se usa única y exclusivamente para conseguir un nuevo _Access Token_ cuando este último expira, evitando que el usuario tenga que escribir su contraseña una y otra vez, y mitigando el riesgo si un _Access Token_ es robado.

3. **Hashing de Contraseñas (Bcrypt / Argon2)**:
    - Nunca guardamos contraseñas en texto plano. Se debe aplicar una función de cifrado de una vía (_hash_).
    - Usamos algoritmos diseñados intencionalmente para ser lentos, lo que previene ataques de fuerza bruta. `Bcrypt` y `Argon2` son los estándares actuales que además añaden un elemento aleatorio llamado _Salt_ para proteger contra ataques de diccionarios (Rainbow Tables).

4. **Manejo de Sesión**:
    - Aunque los JWT son comúnmente "Stateless" (sin estado guardado en el servidor), un manejo de sesiones real a menudo requiere mecanismos de revocación de _Refresh Tokens_ (ej. una lista negra de tokens, o almacenarlos en la BD).

---

## Ejemplo Completo de Flujo

### 1: Registro o Creación de Hash
El usuario envía su contraseña: `"mypassword123"`
El servidor no la guarda así. Usa Bcrypt:
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("mypassword123")
# Resultado (Ejemplo): $2b$12$R.S2u..6F9...y1v.B.g..R...
# Esto se guarda en la base de datos de Usuarios
```

### 2: Login y Generación de JWT
El usuario quiere iniciar sesión.
- Pasa `"mypassword123"`.
- El servidor la comprueba contra el hash guardado de manera matemática usando la librería.
- Si es válido, se generan los Tokens:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWZyZXNoIjoidHJ1ZSIsImV4c...",
  "token_type": "bearer"
}
```

### 3: Acceso a Rutas Protegidas
Para ver sus detalles en el API (por ejemplo `GET /items`), añade el token a su petición:

```http
GET /items HTTP/1.1
Host: api.ejemplo.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI...
```

El servidor toma la cabecera, verifica criptográficamente la firma con su **Secret Key** interna. Si coincide y el tiempo no ha expirado, responde con los datos.

### 4: Refresco de Token
Cuando el _Access Token_ haya caducado (15 min después), el Frontend mandará el _Refresh Token_ al endpoint de `/auth/refresh`. El servidor comprueba la validez del refresh y contesta con un NUEVO _Access Token_ de 15 minutos de duración.
