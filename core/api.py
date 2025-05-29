from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from .module_loader import ModuleLoader
import os

app = FastAPI(title="Hope CP")

templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "webApp", "templates"))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "webApp", "static"))
app.mount("/static", StaticFiles(directory=static_dir), name="static")
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)

loader = ModuleLoader(modules_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules")))
modules = loader.discover()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    tpl = jinja_env.get_template("modules_list.html")
    return tpl.render(modules=modules)

for name, subapp in loader.subapps.items():
    prefix = f"/modules"
    app.mount(prefix, subapp)