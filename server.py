#!/usr/bin/env python3
import os
import re
import sys
import socket
import urllib.parse
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DualStackThreadingServer(ThreadingHTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()

class RangeRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Concise logging to avoid huge logs
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.address_string()} {format % args}\n")

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/', parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        try:
            fs = os.fstat(f.fileno())
            file_len = fs[6]
            range_header = self.headers.get("Range")

            if range_header:
                m = re.match(r"^bytes=(\d*)-(\d*)$", range_header.strip())
                if m:
                    start_str, end_str = m.groups()
                    if start_str == "" and end_str == "":
                        start = 0
                        end = file_len - 1
                    elif start_str == "":
                        start = max(0, file_len - int(end_str))
                        end = file_len - 1
                    elif end_str == "":
                        start = int(start_str)
                        end = file_len - 1
                    else:
                        start = int(start_str)
                        end = min(file_len - 1, int(end_str))

                    if start > end or start >= file_len:
                        self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE, f"Range not satisfiable: {range_header}")
                        f.close()
                        return None

                    length = end - start + 1
                    self.send_response(HTTPStatus.PARTIAL_CONTENT)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                    self.send_header("Content-Length", str(length))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()

                    f.seek(start)
                    return _LimitedFileReader(f, length)

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(file_len))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return f
        except Exception:
            f.close()
            raise

class _LimitedFileReader:
    def __init__(self, file_obj, length):
        self._file = file_obj
        self._remaining = length

    def read(self, size=-1):
        if self._remaining <= 0:
            return b""
        if size < 0 or size > self._remaining:
            size = self._remaining
        data = self._file.read(size)
        self._remaining -= len(data)
        return data

    def close(self):
        self._file.close()

if __name__ == "__main__":
    PORT = 8080
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    server_address = ("", PORT)
    httpd = DualStackThreadingServer(server_address, RangeRequestHandler)
    print(f"Portfolio server serving on port {PORT} (IPv4 + IPv6 dual-stack, Range-enabled)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
