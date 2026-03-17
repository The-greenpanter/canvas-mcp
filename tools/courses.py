from canvas_client import canvas_get


async def get_courses() -> str:
    """Obtiene las materias activas del semestre actual."""
    data = await canvas_get("courses", params={
        "enrollment_state": "active",
        "per_page": 50,
    })

    if not data:
        return "No se encontraron materias activas."

    lines = []
    for c in data:
        name = c.get("name", "Sin nombre")
        code = c.get("course_code", "")
        course_id = c.get("id")
        lines.append(f"• [{course_id}] {name} ({code})")

    return f"📚 Materias activas ({len(lines)}):\n" + "\n".join(lines)
