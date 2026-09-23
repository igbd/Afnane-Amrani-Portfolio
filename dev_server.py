import os
import re
import sys
import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

class VideoStreamingRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        if 'Range' not in self.headers:
            self.send_header('Accept-Ranges', 'bytes')
        # Prevent browser caching of code edits
        if self.path.endswith(('.html', '.css', '.js')) or self.path in ('/', ''):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        range_header = self.headers.get('Range')
        path = self.translate_path(self.path)

        # If it's a file and Range request was requested (critical for HTML5 videos)
        if range_header and os.path.isfile(path):
            file_size = os.path.getsize(path)
            m = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if m:
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else file_size - 1
                if start >= file_size:
                    self.send_response(416)
                    self.send_header('Content-Range', f'bytes */{file_size}')
                    self.end_headers()
                    return

                end = min(end, file_size - 1)
                length = end - start + 1
                ctype = self.guess_type(path)

                self.send_response(206)
                self.send_header('Content-Type', ctype)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.send_header('Content-Length', str(length))
                self.send_header('Accept-Ranges', 'bytes')
                self.end_headers()

                try:
                    with open(path, 'rb') as f:
                        f.seek(start)
                        bytes_left = length
                        chunk_size = 64 * 1024
                        while bytes_left > 0:
                            read_size = min(chunk_size, bytes_left)
                            data = f.read(read_size)
                            if not data:
                                break
                            self.wfile.write(data)
                            bytes_left -= len(data)
                except (BrokenPipeError, ConnectionResetError, socket.error):
                    pass
                return

        # Default handler for normal requests
        try:
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError, socket.error):
            pass

    def log_message(self, format, *args):
        # Suppress noisy logs, print simple one-liner
        msg = format % args
        if "404" in msg or "500" in msg:
            sys.stderr.write(f"[dev_server] {msg}\n")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server_address = ('0.0.0.0', port)
    
    # Enable address reuse immediately
    ThreadingHTTPServer.allow_reuse_address = True
    httpd = ThreadingHTTPServer(server_address, VideoStreamingRequestHandler)
    print(f"Portfolio server running at http://localhost:{port} and http://127.0.0.1:{port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
