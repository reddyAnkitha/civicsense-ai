from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(path, data):
    c = canvas.Canvas(path, pagesize=letter)

    y = 750
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, y, "CivicSense AI Report")

    y -= 40
    c.setFont("Helvetica", 12)

    for k, v in data.items():
        c.drawString(80, y, f"{k}: {v}")
        y -= 25

    c.save()