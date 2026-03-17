from canvas_client import canvas_get


async def get_assignments(course_id: int) -> str:
    """Obtiene las tareas de una materia con su fecha límite."""
    data = await canvas_get(f"courses/{course_id}/assignments", params={
        "order_by": "due_at",
        "per_page": 30,
    })

    if not data:
        return "No se encontraron tareas para esta materia."

    lines = []
    for a in data:
        name = a.get("name", "Sin título")
        due = a.get("due_at", "Sin fecha límite")
        points = a.get("points_possible", 0)
        submitted = a.get("has_submitted_submissions", False)
        estado = "✅ Entregada" if submitted else "⏳ Pendiente"
        lines.append(f"• {name}\n  Fecha: {due} | Puntos: {points} | {estado}")

    return f"📝 Tareas ({len(lines)}):\n" + "\n".join(lines)
