from canvas_client import canvas_get


async def get_files(course_id: int) -> str:
    """Obtiene la lista de archivos disponibles en una materia."""
    data = await canvas_get(f"courses/{course_id}/files", params={
        "per_page": 50,
        "sort": "updated_at",
        "order": "desc",
    })

    if not data:
        return "No se encontraron archivos para esta materia."

    lines = []
    for f in data:
        name = f.get("display_name", f.get("filename", "Sin nombre"))
        size = f.get("size", 0)
        content_type = f.get("content-type", "desconocido")
        url = f.get("url", "")
        updated = f.get("updated_at", "")

        # Formato legible del tamaño
        if size >= 1_048_576:
            size_str = f"{size / 1_048_576:.1f} MB"
        elif size >= 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size} B"

        lines.append(f"• {name} ({content_type}, {size_str}) — {updated}\n  {url}")

    return f"📁 Archivos ({len(lines)}):\n" + "\n".join(lines)
