"""Extract generated inline resources into a portable, deduplicated local folder.

Input is the renderer's own escaped HTML, not arbitrary third-party HTML.
No network access, image conversion, or changes to evidence bytes occur.
"""
import base64
import hashlib
import re

EXTENSIONS = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp'}
IMAGE = re.compile(r'(?P<prefix><img\b[^>]*?\bsrc=")data:(?P<mime>image/(?:png|jpeg|webp));base64,(?P<data>[A-Za-z0-9+/=]+)(?P<suffix>")')
STYLE = re.compile(r'<style>(.*?)</style>', re.S)
SCRIPT = re.compile(r'<script>(.*?)</script>', re.S)


def link_resources(pages):
    """Return rewritten pages and assets keyed by safe content-addressed paths."""
    assets = {}

    def add(raw, extension):
        name = 'assets/' + hashlib.sha256(raw).hexdigest() + '.' + extension
        assets[name] = raw
        return name

    linked = {}
    for name, page in pages.items():
        page = STYLE.sub(lambda m: '<link rel="stylesheet" href="' + add(m[1].encode('utf-8'), 'css') + '">', page)
        page = SCRIPT.sub(lambda m: '<script src="' + add(m[1].encode('utf-8'), 'js') + '" defer></script>', page)
        page = IMAGE.sub(lambda m: m['prefix'] + add(base64.b64decode(m['data'], validate=True), EXTENSIONS[m['mime']]) + m['suffix'], page)
        page = page.replace('离线 HTML · 无外部脚本、字体或图片依赖', '离线报告 · 请保留同目录 assets 资源文件夹')
        page = page.replace('Offline HTML · no external script, font or image dependency', 'Offline report · keep the local assets folder beside these pages')
        linked[name] = page
    return linked, assets
