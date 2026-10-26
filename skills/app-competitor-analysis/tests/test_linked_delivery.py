"""Portable fixtures for the actual repeated inline-resource delivery pattern."""
import base64
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
spec = importlib.util.spec_from_file_location('linked_renderer', ROOT/'scripts/render_reports.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9ZQmcAAAAASUVORK5CYII=')

class LinkedDeliveryTests(unittest.TestCase):
    def test_shared_resources_leave_html_and_preserve_original_once(self):
        data = json.loads((ROOT/'assets/report-bundle.example.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'evidence.png').write_bytes(PNG)
            for product in data['products']:
                product['sections'][1]['blocks'].append(dict(type='image', path='evidence.png', alt='Original synthetic image', caption='Fixture', sources=[product['sources'][0]['id']]))
            out = root/'out'
            manifest = renderer.render_bundle(data, out, root, delivery_format='linked')
            pages = [(out/(p['id']+'.html')).read_text() for p in data['products']]
            pages.append((out/'index.html').read_text())
            for page in pages:
                self.assertNotIn('data:image/', page)
                self.assertNotIn('<style>', page)
                self.assertNotIn('<script>', page)
                self.assertIn('src="assets/', page)
                self.assertIn('href="assets/', page)
            assets = list((out/'assets').iterdir())
            self.assertEqual(len([p for p in assets if p.suffix=='.css']), 1)
            self.assertEqual(len([p for p in assets if p.suffix=='.js']), 1)
            images = [p for p in assets if p.suffix=='.png']
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].read_bytes(), PNG)
            self.assertEqual(manifest['delivery_format'], 'linked')
            self.assertEqual(len(manifest['assets']), 3)

    def test_standalone_remains_explicit_and_overwrite_is_refused(self):
        data = json.loads((ROOT/'assets/report-bundle.example.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)/'standalone'
            renderer.render_bundle(data, out, delivery_format='standalone')
            self.assertIn('<style>', (out/'index.html').read_text())
            with self.assertRaisesRegex(ValueError, 'new or empty'):
                renderer.render_bundle(data, out, delivery_format='linked')

if __name__=='__main__':unittest.main()
