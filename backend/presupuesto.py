from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generar_presupuesto_pdf(productos, total):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Presupuesto Fresco Lubricentro")

    # Subtítulo
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Detalle de productos seleccionados:")

    y = height - 110
    for prod in productos:
        descripcion = prod["descripcion"]
        precio = f"${prod['precio_final']}"
        c.drawString(60, y, f"- {descripcion} ............ {precio}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 30, f"TOTAL: ${total:,.2f}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
