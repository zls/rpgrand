import os

from jinja2 import Environment, FileSystemLoader, PackageLoader

def render(template=None, ctx=None):
    if not template:
        return Environment(
            loader=PackageLoader("rpgrand", "templates"),
        ).get_template('default.tmpl').render(v=ctx)

    else:
        path, fname = os.path.split(template)
        return Environment(
            loader=FileSystemLoader(path or './')
        ).get_template(fname).render(v=ctx)
