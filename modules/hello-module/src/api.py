from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import os, yaml

router = APIRouter()

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
with open(os.path.join(MODULE_DIR, "manifest.yaml"), encoding="utf-8") as f:
    manifest = yaml.safe_load(f)

module_template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web_template"))
module_name = os.path.dirname(__file__), ".."
module_jinja_env = Environment(loader=FileSystemLoader(module_template_dir), autoescape=True)
module_tpl = module_jinja_env.get_template("module_panel.html")
widget_tpl = module_jinja_env.get_template("widget.html")

@router.post("/console", response_class=HTMLResponse)
def module_panel():
    return module_tpl.render(module=manifest["name"])

@router.get("/widget", response_class=HTMLResponse)
def widget():
    return widget_tpl.render(module=manifest["name"])

def get_app():
    app = FastAPI()
    app.include_router(router)
    return app