from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class SPAHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        path = self.translate_path(self.path.split('?', 1)[0])
        requested = Path(path)
        if self.path.startswith('/palavras/') or self.path.startswith('/categoria/') or self.path.startswith('/sobre'):
            index = ROOT / 'index.html'
            self.path = '/index.html'
        elif requested.is_dir() and (requested / 'index.html').exists():
            self.path = self.path.rstrip('/') + '/index.html'
        super().do_GET()

if __name__ == '__main__':
    import os, sys
    host = '127.0.0.1'
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8765))
    print(f'Dicionário em http://{host}:{port}')
    ThreadingHTTPServer((host, port), SPAHandler).serve_forever()
