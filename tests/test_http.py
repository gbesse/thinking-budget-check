import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compare import call


class HttpTest(unittest.TestCase):
    def test_jeeves_think_switch(self):
        seen = {}
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_): pass
            def do_POST(self):
                seen['body'] = json.loads(self.rfile.read(int(self.headers['content-length'])))
                payload = json.dumps({'answers': {'route': {'choice': 'billing'}}}).encode()
                self.send_response(200); self.send_header('content-length', str(len(payload))); self.end_headers(); self.wfile.write(payload)
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.handle_request); thread.start()
        case = {'state': 'Double charge', 'instructions': 'Team?', 'options': {'billing': 'Charges', 'shipping': 'Delivery'}}
        try:
            result = call(f'http://127.0.0.1:{server.server_port}', case, False)
        finally:
            thread.join(3); server.server_close()
        self.assertEqual(result['choice'], 'billing')
        self.assertFalse(seen['body']['options']['think'])
