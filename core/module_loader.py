import os, yaml, importlib

class ModuleLoader:
    def __init__(self, modules_dir=os.getcwd() + '\\modules\\'):
        print(modules_dir)
        self.modules_dir = modules_dir
        self.modules = {}
        self.subapps = {}
        self.widget_info = {}
        
    def discover(self):
        for name in os.listdir(self.modules_dir):
            path = os.path.join(self.modules_dir, name)
            mfile = os.path.join(path, 'manifest.yaml')
            if os.path.isdir(path) and os.path.isfile(mfile):
                with open(mfile, 'r', encoding='utf-8') as f:
                    manifest = yaml.safe_load(f)
                mod_path, cls_name = manifest['entry_point'].split(':')
                module = importlib.import_module(f"modules.{name}.{mod_path}")
                cls = getattr(module, cls_name)
                inst = cls(manifest, path)
                self.modules[manifest['name']] = inst

                api_spec = manifest.get('api')
                if api_spec:
                    api_modpath, fn_name = api_spec.split(':')
                    api_mod = importlib.import_module(f"modules.{name}.{api_modpath}")
                    factory = getattr(api_mod, fn_name)
                    self.subapps[manifest['name']] = factory()

                widget_meta = manifest.get('widget', {})
                if widget_meta:
                    if widget_meta.get('enabled'):
                        self.widget_info[manifest['name']] = {
                            **widget_meta['default'],
                            "min_size": widget_meta['min_size'],
                            "route": widget_meta['route']
                        }
        return self.modules