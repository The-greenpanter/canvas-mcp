# Guia de Deploy — Canvas MCP Server en VPS

> VPS: Hostinger Ubuntu 22.04 | Dominio: mcp.thegreenpanter.uk | Cloudflare Tunnel

---

## 1. Conectarse al VPS via SSH desde WSL

```bash
ssh root@<IP_DEL_VPS>
```

Si tienes configurado un alias en `~/.ssh/config`, puedes usar:

```bash
ssh hostinger
```

Para verificar que estas en el servidor correcto:

```bash
hostname
cat /etc/os-release
```

---

## 2. Verificar que Docker y Docker Compose estan instalados

```bash
docker --version
docker compose version
```

**Si Docker no esta instalado:**

```bash
apt update && apt upgrade -y
apt install -y ca-certificates curl gnupg lsb-release

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Verificar que el servicio esta corriendo:

```bash
systemctl status docker
```

---

## 3. Clonar el repositorio (o actualizar si ya existe)

**Primera vez:**

```bash
cd /opt
git clone https://github.com/The-greenpanter/canvas-mcp.git
cd canvas-mcp
```

**Si ya existe (actualizar):**

```bash
cd /opt/canvas-mcp
git pull origin main
```

---

## 4. Crear el archivo .env

El archivo `.env` contiene las variables sensibles y NO esta en el repositorio.

```bash
nano /opt/canvas-mcp/.env
```

Contenido del archivo (reemplazar los valores entre `<>`):

```env
CANVAS_BASE_URL=https://miaulavirtual.uniminuto.edu
CANVAS_TOKEN=<tu_token_de_canvas>
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_SECRET=<tu_secret_para_autenticar_claude>
```

| Variable | Descripcion |
|---|---|
| `CANVAS_BASE_URL` | URL base del LMS de UNIMINUTO |
| `CANVAS_TOKEN` | Token de acceso generado en Canvas > Configuracion > Tokens |
| `MCP_HOST` | Dejar en `0.0.0.0` para que escuche en todas las interfaces |
| `MCP_PORT` | Puerto del servidor MCP (debe coincidir con docker-compose y tunnel) |
| `MCP_SECRET` | Token secreto para que Claude Desktop se autentique contra el server |

Guardar con `Ctrl+O`, salir con `Ctrl+X`.

Verificar que el archivo se creo correctamente:

```bash
cat /opt/canvas-mcp/.env
```

---

## 5. Construir y levantar el contenedor

```bash
cd /opt/canvas-mcp
docker compose up -d --build
```

Esto hace lo siguiente:
- Construye la imagen desde el `Dockerfile` (python:3.12-slim)
- Instala las dependencias de `requirements.txt`
- Copia el codigo al contenedor
- Levanta el contenedor en segundo plano (`-d`)
- Mapea el puerto 8000 del contenedor al 8000 del host
- Carga las variables del archivo `.env`
- Configura reinicio automatico (`unless-stopped`)

---

## 6. Verificar que el contenedor esta corriendo

**Ver contenedores activos:**

```bash
docker ps
```

Deberias ver algo como:

```
CONTAINER ID   IMAGE              STATUS          PORTS                    NAMES
abc123def456   canvas-mcp         Up 2 minutes    0.0.0.0:8000->8000/tcp   canvas-mcp
```

**Ver logs del contenedor:**

```bash
docker compose logs -f
```

(`Ctrl+C` para salir de los logs sin detener el contenedor)

**Ver los ultimos 50 logs:**

```bash
docker compose logs --tail 50
```

---

## 7. Verificar que el Cloudflare Tunnel esta activo

```bash
systemctl status cloudflared
```

Deberia mostrar `active (running)`.

**Si no esta corriendo:**

```bash
systemctl start cloudflared
systemctl enable cloudflared
```

**Verificar la configuracion del tunnel:**

```bash
cat /etc/cloudflared/config.yml
```

La configuracion debe tener una entrada que apunte `mcp.thegreenpanter.uk` a `http://localhost:8000`:

```yaml
ingress:
  - hostname: mcp.thegreenpanter.uk
    service: http://localhost:8000
  - service: http_status:404
```

---

## 8. Probar el endpoint

**Desde el VPS (local):**

```bash
curl http://localhost:8000/sse
```

**Desde WSL o cualquier maquina (a traves del tunnel):**

```bash
curl -v https://mcp.thegreenpanter.uk/sse
```

Si funciona, deberia devolver una conexion SSE (Server-Sent Events) que se queda abierta. `Ctrl+C` para cerrarla.

**Prueba rapida de conectividad:**

```bash
curl -s -o /dev/null -w "%{http_code}" https://mcp.thegreenpanter.uk/sse
```

Un codigo `200` indica que todo esta funcionando.

---

## 9. Configurar Claude Desktop con el endpoint

En Windows, abrir el archivo de configuracion de Claude Desktop:

```
%APPDATA%\Claude\claude_desktop_config.json
```

Ruta completa tipica:

```
C:\Users\PC\AppData\Roaming\Claude\claude_desktop_config.json
```

Contenido:

```json
{
  "mcpServers": {
    "canvas-uniminuto": {
      "type": "sse",
      "url": "https://mcp.thegreenpanter.uk/sse",
      "headers": {
        "Authorization": "Bearer <MCP_SECRET>"
      }
    }
  }
}
```

Reemplazar `<MCP_SECRET>` con el mismo valor que pusiste en el `.env` del VPS.

Despues de guardar, **reiniciar Claude Desktop** completamente (cerrar y abrir).

Para verificar que la conexion funciona, preguntale a Claude:

> "Usa la herramienta get_courses para ver mis materias"

---

## 10. Troubleshooting comun

### El contenedor se cayo o no inicia

```bash
# Ver el estado
docker ps -a

# Ver logs de error
docker compose logs --tail 100

# Reiniciar
docker compose down
docker compose up -d --build
```

**Causas frecuentes:**
- Error de sintaxis en `.env` (espacios, comillas innecesarias)
- Puerto 8000 ocupado por otro proceso (`lsof -i :8000`)
- Error en el codigo Python (revisar logs)

### El tunnel de Cloudflare no funciona

```bash
# Ver estado
systemctl status cloudflared

# Ver logs de cloudflared
journalctl -u cloudflared --no-pager --lines 50

# Reiniciar el tunnel
systemctl restart cloudflared
```

**Causas frecuentes:**
- El servicio no esta habilitado (`systemctl enable cloudflared`)
- El archivo `config.yml` tiene errores de sintaxis
- El certificado del tunnel expiro (hay que re-autenticar con `cloudflared tunnel login`)

### El token de Canvas expiro

Sintomas: las herramientas devuelven errores 401 Unauthorized.

Solucion:
1. Ir a Canvas > Configuracion > Tokens de acceso
2. Generar un nuevo token
3. Actualizar `CANVAS_TOKEN` en `/opt/canvas-mcp/.env`
4. Reiniciar el contenedor:

```bash
cd /opt/canvas-mcp
docker compose down
docker compose up -d
```

### Claude Desktop no se conecta al MCP

- Verificar que el `MCP_SECRET` en `claude_desktop_config.json` coincide con el del `.env`
- Verificar que la URL es exactamente `https://mcp.thegreenpanter.uk/sse`
- Probar el endpoint con curl desde Windows/WSL
- Reiniciar Claude Desktop completamente

### Comandos utiles de referencia rapida

```bash
# Estado general
docker ps                              # Contenedores corriendo
systemctl status cloudflared           # Estado del tunnel

# Logs
docker compose logs -f                 # Logs en tiempo real
journalctl -u cloudflared -f           # Logs del tunnel en tiempo real

# Reinicio completo
cd /opt/canvas-mcp
docker compose down && docker compose up -d --build
systemctl restart cloudflared

# Actualizar el codigo
cd /opt/canvas-mcp
git pull origin main
docker compose down && docker compose up -d --build
```

---

## Resumen del flujo completo

```
1. ssh root@<IP_VPS>
2. cd /opt/canvas-mcp && git pull origin main
3. nano .env                    (verificar variables)
4. docker compose up -d --build
5. docker ps                    (verificar contenedor)
6. systemctl status cloudflared (verificar tunnel)
7. curl https://mcp.thegreenpanter.uk/sse  (probar endpoint)
```
