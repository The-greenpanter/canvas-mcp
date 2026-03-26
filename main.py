import hmac
from fastmcp import FastMCP
from fastmcp.server.auth.providers.debug import DebugTokenVerifier
from config import MCP_HOST, MCP_PORT, MCP_SECRET
from tools.courses import get_courses
from tools.assignments import get_assignments
from tools.announcements import get_announcements
from tools.todo import get_upcoming, get_todo
from tools.modules import get_modules, get_module_items
from tools.pages import get_pages, get_page
from tools.discussions import get_discussions, get_discussion_entries
from tools.files import get_files

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


@mcp.tool()
async def modules(course_id: int) -> str:
    """Obtiene los módulos (secciones) de una materia. Requiere course_id."""
    return await get_modules(course_id)


@mcp.tool()
async def module_items(course_id: int, module_id: int) -> str:
    """Obtiene los elementos dentro de un módulo. Requiere course_id y module_id."""
    return await get_module_items(course_id, module_id)


@mcp.tool()
async def pages(course_id: int) -> str:
    """Obtiene la lista de páginas de una materia. Requiere course_id."""
    return await get_pages(course_id)


@mcp.tool()
async def page_content(course_id: int, page_url: str) -> str:
    """Obtiene el contenido de una página por su slug URL. Requiere course_id y page_url."""
    return await get_page(course_id, page_url)


@mcp.tool()
async def discussions(course_id: int) -> str:
    """Obtiene los foros de discusión de una materia. Requiere course_id."""
    return await get_discussions(course_id)


@mcp.tool()
async def discussion_entries(course_id: int, topic_id: int) -> str:
    """Obtiene las entradas de un foro de discusión. Requiere course_id y topic_id."""
    return await get_discussion_entries(course_id, topic_id)


@mcp.tool()
async def files(course_id: int) -> str:
    """Obtiene los archivos disponibles en una materia. Requiere course_id."""
    return await get_files(course_id)


if __name__ == "__main__":
    mcp.run(transport="sse", host=MCP_HOST, port=int(MCP_PORT))
