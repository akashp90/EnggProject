import jinja2

def render_jinja_html(file_name,**context):
    template_loc = '/Users/akashparvatikar/Projects/EnggProject/templates'

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_loc+'/')
        ).get_template(file_name).render(context)