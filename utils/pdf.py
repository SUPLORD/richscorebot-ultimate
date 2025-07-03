from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def make_report(data):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.drawString(50,800, f"RICHSCORE: {data['name']}")
    c.drawString(50,780, f"Цель: {data['goal']} — {data['amount']:,} ₽")
    c.showPage()
    c.save()
    buf.seek(0)
    return buf
