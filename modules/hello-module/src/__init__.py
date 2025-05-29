import yaml

class HelloModule:
    def __init__(self, manifest, path):
        self.manifest = manifest
        cfg = path + '/config.yaml'
        with open(cfg, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
    def ping(self):
        return self.config['greeting']
