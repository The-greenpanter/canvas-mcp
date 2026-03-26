from canvas_client import canvas_get


async def get_modules(course_id: int) -> str:
    """Obtiene los módulos (secciones) de una materia."""
    data = await canvas_get(f"courses/{course_id}/modules", params={
        "per_page": 50,
    })

    if not data:
        return "No se encontraron módulos para esta materia."

    lines = []
    for m in data:
        name = m.get("name", "Sin nombre")
        module_id = m.get("id")
        state = m.get("state", "desconocido")
        items_count = m.get("items_count", 0)
        lines.append(f"• [{module_id}] {name} — {items_count} elementos (estado: {state})")

    return f"📂 Módulos ({len(lines)}):\n" + "\n".join(lines)


async def get_module_items(course_id: int, module_id: int) -> str:
    """Obtiene los elementos dentro de un módulo específico."""
    data = await canvas_get(f"courses/{course_id}/modules/{module_id}/items", params={
        "per_page": 50,
    })

    if not data:
        return "No se encontraron elementos en este módulo."

    lines = []
    for item in data:
        title = item.get("title", "Sin título")
        item_type = item.get("type", "desconocido")
        url = item.get("html_url", "")
        content_id = item.get("content_id", "")
        indent = item.get("indent", 0)
        prefix = "  " * indent + "• "
        lines.append(f"{prefix}[{item_type}] {title} (content_id: {content_id})\n    {url}")

    return f"📋 Elementos del módulo ({len(lines)}):\n" + "\n".join(lines)
