from canvas_client import canvas_get


async def get_announcements(course_id: int) -> str:
    """Obtiene los anuncios de una materia."""
    data = await canvas_get("announcements", params={
        "context_codes[]": f"course_{course_id}",
        "per_page": 10,
    })

    if not data:
        return "No hay anuncios para esta materia."

    lines = []
    for a in data:
        title = a.get("title", "Sin título")
        date = a.get("posted_at", "Sin fecha")
        author = a.get("author", {}).get("display_name", "Desconocido")
        lines.append(f"• {title}\n  Por: {author} | Fecha: {date}")

    return f"📢 Anuncios ({len(lines)}):\n" + "\n".join(lines)
