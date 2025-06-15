from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from .module_loader import ModuleLoader
import os, sys, json

app = FastAPI(title="MeiAI CP")

templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "webApp", "templates"))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "webApp", "static"))
layout_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WebApp", "layout.json"))
app.mount("/static", StaticFiles(directory=static_dir), name="static")
jinja_env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)

loader = ModuleLoader(modules_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules")))
modules = loader.discover()
widget_info = loader.widget_info

if os.path.exists(layout_path):
    with open(layout_path, "r", encoding="utf-8") as f:
        widgets = json.load(f)
else:
    widgets = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tpl = jinja_env.get_template("index.html")
    return tpl.render(modules=modules, widgets=json.dumps(widgets), widgets_meta=json.dumps(loader.widget_info))

@app.get("/api/modules", response_class=JSONResponse)
async def list_modules():
    return list(widget_info.keys())

@app.get("/api/layout", response_class=JSONResponse)
async def get_layout():
    global widgets
    return JSONResponse(content=widgets)

@app.post("/api/layout", response_class=JSONResponse)
async def save_layout(new_layout: dict):
    global widgets
    widgets = new_layout
    with open(layout_path, "w", encoding="utf-8") as f:
        json.dump(widgets, f)
    return {"status": "OK"}

@app.post("/api/widget/add", response_class=JSONResponse)
async def add_widget(payload: dict):
    name = payload.get("name")
    if name not in widget_info:
        raise HTTPException(404, f"Параметр widget-enabled выключен у модуля {name}.")
    if name in widgets:
        return {"status": "Уже добавлен"}
    meta = widget_info[name].copy()
    widgets[name] = meta
    await save_layout(widgets)
    return {"status": "Добавлено", "widget": meta}

for name, subapp in loader.subapps.items():
    prefix = f"/modules/{name}"
    if hasattr(subapp, "routes"):
        app.mount(prefix, subapp)
    else:
        app.include_router(subapp, prefix=prefix)