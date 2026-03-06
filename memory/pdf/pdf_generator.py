import os
import json
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_FONT_NAME = "NotoSansDevanagari"
_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_FONT_PATH = os.path.join(_FONT_DIR, "NotoSansDevanagari-Regular.ttf")

try:
    pdfmetrics.registerFont(TTFont(_FONT_NAME, _FONT_PATH))
except Exception as e:
    print(f"⚠️ Could not register Devanagari font ({_FONT_PATH}): {e}")
    _FONT_NAME = "Helvetica"


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

    # Custom styles using Devanagari-compatible font
    heading_style = ParagraphStyle(
        "HindiHeading",
        fontName=_FONT_NAME,
        fontSize=16,
        leading=20,
        spaceAfter=6,
    )
    normal_style = ParagraphStyle(
        "HindiNormal",
        fontName=_FONT_NAME,
        fontSize=10,
        leading=14,
        wordWrap="CJK",
    )

    # Title
    elements.append(Paragraph("Patient Intake Report", heading_style))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # Prepare table data — flatten nested dicts
    table_data = []

    for key, value in patient_data.items():
        formatted_key = key.replace("_", " ").title()

        if isinstance(value, dict):
            # Add the section header row
            table_data.append([
                Paragraph(formatted_key, normal_style),
                Paragraph("", normal_style),
            ])
            # Add each nested key-value as its own row
            for sub_key, sub_val in value.items():
                sub_label = sub_key.replace("_", " ").title()
                if isinstance(sub_val, list):
                    sub_val = ", ".join(sub_val) if sub_val else "None"
                table_data.append([
                    Paragraph(f"  {sub_label}", normal_style),
                    Paragraph(str(sub_val), normal_style),
                ])
        else:
            if isinstance(value, list):
                value = ", ".join(value) if value else "None"
            table_data.append([
                Paragraph(formatted_key, normal_style),
                Paragraph(str(value), normal_style),
            ])

    table = Table(table_data, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), _FONT_NAME),
    ]))

    elements.append(table)

    doc.build(elements)

    print("📄 PDF generated:", file_path)

    return file_path
