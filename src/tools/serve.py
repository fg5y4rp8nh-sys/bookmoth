import http.server, os, sys, functools, json
D = sys.argv[1]
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + '.html'): return p + '.html'
        return p
    def end_headers(self):
        try:
            cfg = json.load(open(os.path.join(D, 'vercel.json')))
            for h in cfg.get('headers', [{}])[0].get('headers', []):
                if h['key'] != 'Strict-Transport-Security':
                    self.send_header(h['key'], h['value'].replace('; upgrade-insecure-requests', ''))
        except Exception:
            pass
        super().end_headers()
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', 4175), functools.partial(H, directory=D)).serve_forever()
