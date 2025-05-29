from .module_loader import ModuleLoader
import sys
import os

import uvicorn
from .api import app

# Добавляем корневую директорию проекта (там, где modules/) в sys.path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def main():
    loader = ModuleLoader()
    modules = loader.discover()
    print("Загруженные модули:")
    for name, module in modules.items():
        print(f" - {name} v{module.manifest['version']}")
    
    uvicorn.run(app, host="127.0.0.1", port=8000) # Старт сервера
if __name__ == '__main__':
    main()