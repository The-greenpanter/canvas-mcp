from canvas_client import canvas_get


async def get_discussions(course_id: int) -> str:
    """Obtiene los foros de discusión de una materia."""
    data = await canvas_get(f"courses/{course_id}/discussion_topics", params={
        "per_page": 30,
        "order_by": "recent_activity",
    })

    if not data:
        return "No se encontraron foros de discusión para esta materia."

    lines = []
    for d in data:
        title = d.get("title", "Sin título")
        topic_id = d.get("id")
        posted = d.get("posted_at", "")
        author = d.get("author", {}).get("display_name", "Desconocido")
        discussion_type = d.get("discussion_type", "")
        entry_count = d.get("discussion_subentry_count", 0)
        lines.append(
            f"• [{topic_id}] {title}\n"
            f"  Autor: {author} | Tipo: {discussion_type} | "
            f"Respuestas: {entry_count} | Publicado: {posted}"
        )

    return f"💬 Foros de discusión ({len(lines)}):\n" + "\n".join(lines)


async def get_discussion_entries(course_id: int, topic_id: int) -> str:
    """Obtiene las entradas/respuestas de un foro de discusión específico."""
    data = await canvas_get(f"courses/{course_id}/discussion_topics/{topic_id}/entries", params={
        "per_page": 30,
    })

    if not data:
        return "No se encontraron entradas en este foro."

    import re
    lines = []
    for entry in data:
        user = entry.get("user_name", "Anónimo")
        message = entry.get("message", "")
        created = entry.get("created_at", "")
        # Limpiar HTML
        clean_msg = re.sub(r"<[^>]+>", " ", message)
        clean_msg = re.sub(r"\s+", " ", clean_msg).strip()
        # Truncar mensajes largos
        if len(clean_msg) > 300:
            clean_msg = clean_msg[:300] + "..."
        lines.append(f"• {user} ({created}):\n  {clean_msg}")

    return f"💬 Entradas del foro ({len(lines)}):\n" + "\n".join(lines)
