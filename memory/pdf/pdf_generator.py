import os
import json
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_patient_pdf(patient_json_text):
    try:
        patient_data = json.loads(patient_json_text)
    except:
        print("⚠️ Invalid JSON. PDF not generated.")
        return None

    os.makedirs("data/pdfs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/pdfs/patient_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    heading = styles["Heading1"]
    normal = styles["Normal"]

    # Title
    elements.append(Paragraph("Patient Intake Report", heading))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # Prepare table data
    table_data = []

    for key, value in patient_data.items():
        if isinstance(value, list):
            value = ", ".join(value) if value else "None"

        formatted_key = key.replace("_", " ").title()
        table_data.append([formatted_key, str(value)])

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elements.append(table)

    doc.build(elements)

    print("📄 PDF generated:", file_path)

    return file_path
