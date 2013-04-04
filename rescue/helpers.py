from wkhtmltopdf.views import PDFTemplateResponse 

def render_to_pdf(request, template_name, context_dict):
    return PDFTemplateResponse(request, template_name, context_dict)
