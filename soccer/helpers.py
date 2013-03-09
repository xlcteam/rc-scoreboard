from wkhtmltopdf.views import PDFTemplateResponse 

def render_to_pdf(request, template_name, context_dict):
    return PDFTemplateResponse(request, template_name, context_dict)

# code from
# http://code.activestate.com/recipes/65200-round-robin-pairings-generator/
def round_robin(units, sets=None):
    """ Generates a schedule of "fair" pairings from a list of units """
    if len(units) % 2:
        units.append(None)
    count    = len(units)
    sets     = sets or (count - 1)
    half     = count / 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            if units[i] is None or units[count-i-1] is None:
                continue
            pairings.append((units[i], units[count-i-1]))
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule

