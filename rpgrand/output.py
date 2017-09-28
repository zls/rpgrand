import os

from jinja2 import Environment, FileSystemLoader

def render(template, ctx):
    path, fname = os.path.split(template)
    return Environment(
        loader=FileSystemLoader(path or './')
    ).get_template(fname).render(ctx)
