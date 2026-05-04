import markdown
from weasyprint import HTML

def convert_md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    html = markdown.markdown(text, extensions=['tables'])
    
    # Añadimos un poco de CSS básico para que las tablas se vean bien en el PDF
    styled_html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    HTML(string=styled_html).write_pdf(pdf_file)

if __name__ == "__main__":
    convert_md_to_pdf('UI_GYP_DESIGN.md', 'UI_GYP_DESIGN.pdf')
    print("PDF generado exitosamente.")
