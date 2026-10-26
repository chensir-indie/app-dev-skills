"""Image delivery regressions; original generated pixels only."""
import base64
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
import zlib
import hashlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reports_media', ROOT / 'scripts/render_reports.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def png(w, h):
    def chunk(k, v):
        return struct.pack('>I', len(v)) + k + v + struct.pack('>I', zlib.crc32(k + v) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress((b'\0' + bytes([80, 100, 120]) * w) * h)) + chunk(b'IEND', b''))


class MediaPerformanceTests(unittest.TestCase):
    def test_intrinsic_size_reserves_geometry_before_decode(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'original.png').write_bytes(png(800, 1600))
            html = renderer.image_html({'path':'original.png', 'alt':'fixture'}, p)
            self.assertTrue('width="800"' in html, 'Reserve source width before decode')
            self.assertTrue('height="1600"' in html, 'Reserve source height before decode')
            self.assertTrue('decoding="async"' in html, 'Decode away from synchronous layout')

    def test_large_cover_uses_reading_preview_while_catalog_stays_small(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);original=png(800,1600);thumbnail=png(100,200);reading=png(400,800)
            for name,raw in [('original.png',original),('thumbnail.png',thumbnail),('reading.png',reading)]:
                (p/name).write_bytes(raw)
            block=dict(path='original.png',thumbnail_path='thumbnail.png',preview_path='reading.png',alt='fixture')
            cover=renderer.image_html(block,p,preview=True)
            catalog=renderer.image_html(block,p,catalog=True)
            self.assertIn(base64.b64encode(reading).decode(),cover)
            self.assertIn('loading="eager"',cover)
            self.assertIn(base64.b64encode(thumbnail).decode(),catalog)

    def test_large_original_is_not_used_as_catalog_thumbnail(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); raw = png(800, 1600); (p/'original.png').write_bytes(raw)
            data = json.loads((ROOT/'assets/report-bundle.example.json').read_text())
            data['products'][0]['sections'][1]['blocks'].append(
                {'type':'image','path':'original.png','alt':'fixture','caption':'Original fixture'})
            html = renderer.index_page(data, p)
            self.assertFalse(base64.b64encode(raw).decode() in html,
                             'A tiny catalog tile must not decode a 1.28 MP original')

    def test_framed_derivative_with_wrong_viewport_aspect_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'original.png').write_bytes(png(1000,1000));(p/'wrong.png').write_bytes(png(200,100))
            block=dict(path='original.png',preview_path='wrong.png',preview_framed=True,alt='fixture',
                       viewport=dict(x=0,y=0,width=200,height=400,source_width=1000,source_height=1000))
            with self.assertRaisesRegex(ValueError,'framed preview'):
                renderer.image_html(block,p)

    def test_display_preview_keeps_exact_original_in_disclosure(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); raw = png(800, 1600); preview = png(100, 200)
            (p/'original.png').write_bytes(raw); (p/'preview.png').write_bytes(preview)
            html = renderer.block_html({'type':'image','path':'original.png','preview_path':'preview.png',
                                        'alt':'fixture','caption':'Display preview; inspect original'}, p)
            self.assertEqual(html.count(base64.b64encode(raw).decode()), 1)
            self.assertEqual(html.count(base64.b64encode(preview).decode()), 1)
            self.assertIn('original-image', html)

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'Optional derivative command requires Pillow')
    def test_optional_preparation_preserves_original_and_display_orientation(self):
        from PIL import Image
        spec = importlib.util.spec_from_file_location('prepare', ROOT/'scripts/prepare_previews.py')
        prepare = importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare)
        from media_info import dimensions
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);photo=p/'source.jpg';image=Image.new('RGB',(1700,900),(80,100,120))
            exif=Image.Exif();exif[274]=6;image.save(photo,exif=exif)
            before=hashlib.sha256(photo.read_bytes()).hexdigest()
            data={'products':[{'sections':[{'blocks':[{'type':'image','path':'source.jpg'}]}]}]}
            result, receipts=prepare.prepare(data,p,p/'derived')
            block=result['products'][0]['sections'][0]['blocks'][0]
            self.assertEqual(hashlib.sha256(photo.read_bytes()).hexdigest(),before)
            self.assertEqual(dimensions(photo.read_bytes()),(900,1700))
            for key,bound in [('thumbnail_path',480),('preview_path',1600)]:
                w,h=dimensions(Path(block[key]).read_bytes())
                self.assertLessEqual(max(w,h),bound)
                self.assertGreater(h,w,'Display derivative must match browser EXIF orientation')
            self.assertEqual(len(receipts),2)

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'Optional fixture encoder requires Pillow')
    def test_webp_header_variants_reserve_correct_geometry(self):
        from PIL import Image
        from media_info import dimensions
        import io
        for mode,lossless in [('RGB',False),('RGBA',False),('RGB',True)]:
            with self.subTest(mode=mode,lossless=lossless):
                im=Image.new(mode,(31,47));out=io.BytesIO()
                im.save(out,format='WEBP',lossless=lossless)
                self.assertEqual(dimensions(out.getvalue()),(31,47))

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'Optional preparation requires Pillow')
    def test_documented_window_is_framed_before_downsizing_not_applied_twice(self):
        spec=importlib.util.spec_from_file_location('prepare',ROOT/'scripts/prepare_previews.py')
        prepare=importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare)
        from media_info import dimensions
        with tempfile.TemporaryDirectory()as d:
            p=Path(d);(p/'source.png').write_bytes(png(1000,1000))
            block={'type':'image','path':'source.png','alt':'fixture','caption':'Documented window',
                   'viewport':dict(x=100,y=200,width=200,height=400,source_width=1000,source_height=1000)}
            data={'products':[{'sections':[{'blocks':[block]}]}]}
            result,_=prepare.prepare(data,p,p/'derived');out=result['products'][0]['sections'][0]['blocks'][0]
            self.assertEqual(dimensions(Path(out['thumbnail_path']).read_bytes()),(200,400))
            self.assertTrue(out['thumbnail_framed'])
            html=renderer.image_html(out,p,catalog=True)
            self.assertTrue('width:100%;left:0;top:0'in html,'Do not apply the source viewport to an already framed derivative')


if __name__ == '__main__':
    unittest.main()
