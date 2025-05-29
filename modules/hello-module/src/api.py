from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import os

router = APIRouter()

module_template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web_template"))
module_name = os.path.dirname(__file__), ".."
module_jinja_env = Environment(loader=FileSystemLoader(module_template_dir), autoescape=True)
module_tpl = module_jinja_env.get_template("module_panel.html")

@router.post("/{name}/console", response_class=HTMLResponse)
def module_panel(name: str):
    return module_tpl.render(module=name)

def get_app():
    app = FastAPI()
    app.include_router(router)
    return app