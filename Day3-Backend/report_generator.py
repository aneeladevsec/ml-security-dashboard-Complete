from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_pdf_report(scan_data, user_info=None):
    """Generate PDF security report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=30
    )
    
    # Title
    elements.append(Paragraph("AI Security Assessment Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Model Version:', scan_data.get('model_version', 'N/A')],
        ['Scan ID:', str(scan_data.get('id', 'N/A'))]
    ]
    
    if user_info:
        meta_data.append(['User:', user_info.get('username', 'Anonymous')])
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment
    risk_level = "HIGH RISK" if scan_data.get('prediction') == 1 else "LOW RISK"
    risk_color = colors.red if scan_data.get('prediction') == 1 else colors.green
    
    risk_data = [
        ['Risk Assessment', ''],
        ['Risk Level:', risk_level],
        ['Confidence Score:', f"{scan_data.get('confidence', 0) * 100:.2f}%"],
        ['Risk Score:', f"{scan_data.get('risk_score', 0) * 100:.2f}%"]
    ]
    
    risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
        ('TEXTCOLOR', (0, 1), (1, 1), risk_color),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Input Features
    features = scan_data.get('features', [])
    if features:
        elements.append(Paragraph("Input Features Analysis", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        feature_data = [['Feature', 'Value', 'Status']]
        for i, val in enumerate(features):
            status = 'High' if val > 0.7 else 'Medium' if val > 0.4 else 'Low'
            feature_data.append([f'Feature {i+1}', f'{val:.2f}', status])
        
        feature_table = Table(feature_data, colWidths=[2*inch, 2*inch, 2*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e94560')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(feature_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
