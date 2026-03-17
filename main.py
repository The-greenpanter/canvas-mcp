import hmac
from fastmcp import FastMCP
from fastmcp.server.auth.providers.debug import DebugTokenVerifier
from config import MCP_HOST, MCP_PORT, MCP_SECRET
from tools.courses import get_courses
from tools.assignments import get_assignments
from tools.announcements import get_announcements
from tools.todo import get_upcoming, get_todo

# Auth: valida Bearer token contra MCP_SECRET
auth = DebugTokenVerifier(
    validate=lambda token: hmac.compare_digest(token, MCP_SECRET),
    client_id="claude-desktop",
    scopes=["read"],
)

mcp = FastMCP("Canvas UNIMINUTO", auth=auth)


# --- Tools MCP ---

@mcp.tool()
async def courses() -> str:
    """Obtiene las materias activas del semestre actual."""
    return await get_courses()


@mcp.tool()
async def assignments(course_id: int) -> str:
    """Obtiene las tareas de una materia con su fecha límite. Requiere course_id."""
    return await get_assignments(course_id)


@mcp.tool()
async def announcements(course_id: int) -> str:
    """Obtiene los anuncios de una materia. Requiere course_id."""
    return await get_announcements(course_id)


@mcp.tool()
async def upcoming() -> str:
    """Obtiene todo lo que vence pronto (vista unificada de eventos y tareas)."""
    return await get_upcoming()


@mcp.tool()
async def todo() -> str:
    """Obtiene los pendientes sin entregar."""
    return await get_todo()


if __name__ == "__main__":
    mcp.run(transport="sse", host=MCP_HOST, port=int(MCP_PORT))
