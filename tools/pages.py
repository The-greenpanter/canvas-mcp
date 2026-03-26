from canvas_client import canvas_get


async def get_pages(course_id: int) -> str:
    """Obtiene la lista de páginas de una materia."""
    data = await canvas_get(f"courses/{course_id}/pages", params={
        "per_page": 50,
        "sort": "title",
    })

    if not data:
        return "No se encontraron páginas para esta materia."

    lines = []
    for p in data:
        title = p.get("title", "Sin título")
        url_slug = p.get("url", "")
        updated = p.get("updated_at", "")
        published = p.get("published", False)
        estado = "publicada" if published else "borrador"
        lines.append(f"• {title} (slug: {url_slug}) — {estado}, actualizada: {updated}")

    return f"📄 Páginas ({len(lines)}):\n" + "\n".join(lines)


async def get_page(course_id: int, page_url: str) -> str:
    """Obtiene el contenido completo de una página específica por su slug URL."""
    data = await canvas_get(f"courses/{course_id}/pages/{page_url}")

    if not data:
        return "No se encontró la página solicitada."

    title = data.get("title", "Sin título")
    body = data.get("body", "Sin contenido")
    updated = data.get("updated_at", "")

    # Limpiar HTML básico para legibilidad
    import re
    clean_body = re.sub(r"<[^>]+>", " ", body)
    clean_body = re.sub(r"\s+", " ", clean_body).strip()

    return (
        f"📄 {title}\n"
        f"Actualizada: {updated}\n"
        f"---\n"
        f"{clean_body}"
    )
