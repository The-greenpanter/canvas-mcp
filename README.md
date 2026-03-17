# Canvas MCP Server

MCP Server que conecta Claude Desktop con Canvas LMS, permitiendo monitorear tareas, entregas, anuncios y pendientes académicos directamente desde Claude.

## Tools disponibles

| Tool | Descripción |
|------|-------------|
| `courses` | Materias activas del semestre |
| `assignments(course_id)` | Tareas con fecha límite |
| `announcements(course_id)` | Anuncios de profesores |
| `upcoming` | Todo lo que vence pronto (vista unificada) |
| `todo` | Pendientes sin entregar |

## Requisitos

- Python 3.12+
- Token de API de Canvas LMS
- Docker y Docker Compose (opcional, para deploy)

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/canvas-mcp.git
cd canvas-mcp

# Crear entorno virtual e instalar dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu token de Canvas y configuración
```

## Configuración

Edita el archivo `.env` con tus datos:

```
CANVAS_BASE_URL=https://tu-instancia-canvas.edu
CANVAS_TOKEN=tu_token_de_canvas
MCP_HOST=127.0.0.1
MCP_PORT=8000
MCP_SECRET=tu_secreto_para_autenticar
```

### Obtener el token de Canvas

1. Inicia sesión en tu Canvas LMS
2. Ve a **Cuenta** → **Configuración**
3. En la sección **Tokens de acceso aprobados**, clic en **+ Nuevo token de acceso**
4. Copia el token generado y pégalo en `CANVAS_TOKEN`

## Uso

### Ejecutar localmente

```bash
source .venv/bin/activate
python main.py
```

El server arranca en `http://localhost:8000/sse`.

### Ejecutar con Docker

```bash
docker compose up -d
```

Para ver los logs:

```bash
docker compose logs -f
```

Para detener:

```bash
docker compose down
```

## Conectar con Claude Desktop

Agrega esto a tu `claude_desktop_config.json`:

**Local:**
```json
{
  "mcpServers": {
    "canvas": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**Remoto (con tunnel o VPS):**
```json
{
  "mcpServers": {
    "canvas": {
      "type": "sse",
      "url": "https://tu-dominio.com/sse",
      "headers": {
        "Authorization": "Bearer TU_MCP_SECRET"
      }
    }
  }
}
```

La ubicación del archivo de configuración:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

## Deploy en VPS

```bash
# En el servidor
git clone https://github.com/tu-usuario/canvas-mcp.git
cd canvas-mcp
cp .env.example .env
# Editar .env con los valores reales
docker compose up -d
```

## Stack

- **Python** + FastMCP + httpx + python-dotenv
- **Transporte:** SSE (Server-Sent Events)
- **Canvas API:** REST v1 con Bearer Token

## Licencia

MIT
