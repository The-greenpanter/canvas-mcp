from canvas_client import canvas_get


async def get_upcoming() -> str:
    """Obtiene todo lo que vence pronto (vista unificada)."""
    data = await canvas_get("users/self/upcoming_events", params={
        "per_page": 20,
    })

    if not data:
        return "No hay eventos próximos."

    lines = []
    for e in data:
        title = e.get("title", "Sin título")
        date = e.get("start_at") or e.get("end_at", "Sin fecha")
        event_type = e.get("type", "evento")
        lines.append(f"• {title}\n  Tipo: {event_type} | Fecha: {date}")

    return f"📅 Próximos eventos ({len(lines)}):\n" + "\n".join(lines)


async def get_todo() -> str:
    """Obtiene los pendientes sin entregar."""
    data = await canvas_get("users/self/todo", params={
        "per_page": 20,
    })

    if not data:
        return "No hay pendientes. ¡Estás al día!"

    lines = []
    for t in data:
        assignment = t.get("assignment", {})
        name = assignment.get("name", "Sin título")
        due = assignment.get("due_at", "Sin fecha límite")
        course = t.get("context_name", "Materia desconocida")
        lines.append(f"• {name}\n  Materia: {course} | Fecha: {due}")

    return f"🔔 Pendientes ({len(lines)}):\n" + "\n".join(lines)
