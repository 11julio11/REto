# ☁️ Día 1: Cloud & Infrastructure as Code (IaC)

## ¿Qué es IaC?

**Infrastructure as Code** = definir tu infraestructura (servidores, redes, bases de datos) con archivos de código, en vez de hacer clic en una consola web.

## Deploy Manual vs. Código

| Aspecto | Manual (Consola Web) | IaC (Terraform/CDK) |
|---------|---------------------|----------------------|
| Repetible | ❌ Depende de la memoria | ✅ Siempre igual |
| Auditable | ❌ No sabes quién cambió qué | ✅ Todo en Git |
| Escalable | ❌ 1 servidor = OK, 50 = pesadilla | ✅ Un loop y listo |
| Rollback | ❌ Rezar | ✅ `git revert` |
| Documentación | ❌ "Pregúntale a Pedro" | ✅ El código ES la documentación |

## Herramientas principales

- **Terraform** (HashiCorp): Multi-cloud (AWS, GCP, Azure). Usa archivos `.tf` con lenguaje HCL.
- **AWS CDK**: Infraestructura con Python/TypeScript. Solo para AWS.
- **Pulumi**: Similar a Terraform pero con lenguajes de programación reales.

## Ejemplo mental: Terraform

```hcl
# Esto crea un servidor en AWS con 1 comando
resource "aws_instance" "api_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "reto-api"
  }
}
```

Luego: `terraform apply` → se crea el servidor. `terraform destroy` → se borra. Sin tocar la consola.

## Concepto clave: Estado

Terraform guarda un **archivo de estado** (`terraform.tfstate`) que registra qué recursos existen. Así sabe qué crear, actualizar o destruir.

## ¿Por qué importa para un developer?

> "Si no puedo recrear tu infraestructura con un comando, no la entiendo."

- En una entrevista, saber IaC te diferencia de otros devs.
- No necesitas ser experto en Terraform, pero sí entender el concepto.
- Tu `dockerfile` y `docker-compose.yml` ya son una forma básica de IaC.

## Conexión con este proyecto

En este reto, estamos usando:
- `dockerfile` → Define cómo se construye nuestro contenedor (IaC del app).
- `docker-compose.yml` → Define cómo se conectan los servicios (IaC del entorno).
- `.github/workflows/ci.yml` → Define cómo se valida y construye automáticamente (IaC del pipeline).
