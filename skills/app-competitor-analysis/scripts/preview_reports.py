#!/usr/bin/env python3
"""Serve a verified immutable report snapshot on loopback, including Design.md.

Only manifest-listed HTML, design/*/Design.md and hashed reader assets are served.
"""
import argparse,hashlib,json,mimetypes,re
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def snapshot(root):
    root=Path(root).resolve();raw=(root/'manifest.json').read_bytes();manifest=json.loads(raw)
    entries=manifest.get('files')
    if entries is None:
        entries=manifest['reports']+manifest.get('assets',[])+manifest.get('design_documents',[])+[{'file':'index.html','sha256':manifest['index_sha256']}]
    files={}
    for entry in entries:
        name=entry['file']
        if not re.fullmatch(r'(?:[a-zA-Z0-9_-]+\.html|design/[a-zA-Z0-9_-]+/Design\.md|assets/[a-f0-9]{64}\.(?:css|js|png|jpg|webp))',name):continue
        path=(root/name).resolve()
        if root not in path.parents:raise ValueError('manifest file leaves report directory')
        body=path.read_bytes()
        if hashlib.sha256(body).hexdigest()!=entry['sha256']:raise ValueError('manifest hash mismatch: '+name)
        files['/'+name]=body
    return hashlib.sha256(raw).hexdigest()[:12],files


def handler_for(revision,files,redirect_from):
    prefix='/reader/'+revision
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path=urlsplit(self.path).path
            if path=='/':path='/index.html'
            target=None
            if path in files and not path.startswith('/assets/'):target=path
            for old in redirect_from:
                oldprefix='/reader/'+old+'/'
                if path.startswith(oldprefix):
                    suffix='/'+path[len(oldprefix):]
                    if suffix in files:target=suffix
            if target:
                self.send_response(302);self.send_header('Location',prefix+target);self.send_header('Cache-Control','no-store');self.send_header('Content-Length','0');self.end_headers();return
            key=path[len(prefix):]if path.startswith(prefix+'/')else path
            if key not in files or(path.startswith('/reader/')and not path.startswith(prefix+'/')):self.send_error(404);return
            kind='text/plain; charset=utf-8'if key.endswith('.md')else(mimetypes.guess_type(key)[0]or'application/octet-stream')
            self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(files[key])));self.send_header('Cache-Control','public, max-age=31536000, immutable'if key.startswith('/assets/')else'no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'none'; connect-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'");self.end_headers();self.wfile.write(files[key])
        def log_message(self,*args):pass
    return Handler


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--port',type=int,default=8000);p.add_argument('--redirect-from',action='append',default=[]);a=p.parse_args()
    if any(not re.fullmatch(r'[a-f0-9]{12}',x)for x in a.redirect_from):p.error('invalid previous revision')
    revision,files=snapshot(a.root);server=ThreadingHTTPServer(('127.0.0.1',a.port),handler_for(revision,files,a.redirect_from))
    print(f'http://127.0.0.1:{server.server_port}/reader/{revision}/index.html',flush=True);server.serve_forever()

if __name__=='__main__':main()
