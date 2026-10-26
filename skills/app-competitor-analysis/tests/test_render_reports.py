"""Portable HTML delivery tests using original, non-camera fixtures."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('render_reports', ROOT / 'scripts/render_reports.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def bundle():
    return json.loads((ROOT / 'assets/report-bundle.example.json').read_text())


class RenderReportsTests(unittest.TestCase):
    def test_validation_keeps_authored_evidence_and_decision_visible(self):
        class ReadingText(HTMLParser):
            def __init__(self):
                super().__init__(); self.depth = 0; self.visible = []
            def handle_starttag(self, tag, attrs):
                if tag == 'details': self.depth += 1
            def handle_endtag(self, tag):
                if tag == 'details': self.depth -= 1
            def handle_data(self, text):
                if not self.depth: self.visible.append(text)
        blocks = [dict(type='paragraph', text=t) for t in
                  ['A saved draft exists.', 'Reopening was not observed.',
                   'Defer automatic replacement.', 'Detailed recruitment plan.']]
        page = renderer.section_html(dict(id='validation', title='Research',
                                         blocks=blocks, lead_blocks=3), 8, '.', 'en')
        reader = ReadingText(); reader.feed(page)
        visible = ''.join(reader.visible)
        for block in blocks[:3]: self.assertIn(block['text'], visible)
        self.assertNotIn(blocks[3]['text'], visible)
        self.assertIn(blocks[3]['text'], page)

    def test_presentation_hints_reject_invalid_types_and_hidden_block_ranges(self):
        for value in (-1, 999, True, '2'):
            data = bundle()
            data['products'][0]['sections'][0]['lead_blocks'] = value
            with self.assertRaisesRegex(ValueError, 'lead_blocks'):
                renderer.validate_bundle(data)
        for value in ('not an object', {'lead': ''}):
            data = bundle()
            data['products'][0]['presentation'] = value
            with self.assertRaises(ValueError):
                renderer.validate_bundle(data)

    def test_invalid_image_viewport_is_rejected(self):
        data = bundle()
        for viewport in (
            {'x': -1, 'y': 0, 'width': 50, 'height': 50, 'source_width': 100, 'source_height': 100},
            {'x': 80, 'y': 0, 'width': 50, 'height': 50, 'source_width': 100, 'source_height': 100},
            {'x': 0, 'y': 0, 'width': 0, 'height': 50, 'source_width': 100, 'source_height': 100},
            {'x': 0, 'y': 0, 'width': float('nan'), 'height': 50, 'source_width': 100, 'source_height': 100},
        ):
            data['products'][0]['sections'][1]['blocks'] = [{
                'type':'image','path':'unused.png','alt':'Original fixture',
                'caption':'Viewport validation must run before file loading',
                'viewport':viewport,'sources':['E1']}]
            with self.assertRaisesRegex(ValueError, 'viewport'):
                renderer.validate_bundle(data)

    def test_visual_atlas_is_required_not_a_text_only_report(self):
        data = bundle()
        data['products'][0].pop('visuals', None)
        with self.assertRaisesRegex(ValueError, 'visuals'):
            self.render(data)

    def test_visual_graphs_reject_dangling_edges_and_unsupported_facts(self):
        for mutation in ('dangling', 'uncited', 'overlap', 'missing_graph'):
            data = bundle()
            visuals = data['products'][0]['visuals']
            graph = visuals['journey']
            if mutation == 'dangling':
                graph['edges'][0]['to'] = 'absent'
            elif mutation == 'uncited':
                graph['nodes'][0].update(status='observed', sources=[])
            elif mutation == 'overlap':
                graph['nodes'][1].update(col=graph['nodes'][0]['col'], row=graph['nodes'][0]['row'])
            else:
                del visuals['screens']
            with self.assertRaises(ValueError):
                self.render(data)

    def test_diagrams_have_real_relationships_and_traceable_node_details(self):
        page = self.render(bundle())['example-notes.html']
        data=bundle()['products'][0]['visuals']
        for m in data['features']['modules']:
            for n in m['features']:
                self.assertEqual(page.count(f'data-node-detail="features-{n["id"]}"'),1)
        self.assertEqual(page.count('data-edge-from='),sum(len(data[k]['edges'])for k in ('journey','screens','dataflow')))
        self.assertIn('class="journey-spine"',page)
        self.assertIn('class="graph-edge', page)
        self.assertIn('data-node-detail=', page)
        self.assertIn('class="node-template"', page)
        self.assertIn('marker-end=', page)

    def render(self, data):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'reports'
            renderer.render_bundle(data, output, ROOT / 'assets')
            return {p.name: p.read_text() for p in output.iterdir() if p.suffix in ('.html', '.json')}

    def test_one_readable_standalone_page_per_product_and_index(self):
        data = bundle()
        second = copy.deepcopy(data['products'][0])
        second.update(id='different-note', name='Example Notes', identity='example.other')
        data['products'].append(second)
        result = self.render(data)
        self.assertEqual(set(result), {'index.html', 'example-notes.html', 'different-note.html', 'manifest.json'})
        for name in ('example-notes.html', 'different-note.html'):
            self.assertIn('<style>', result[name])
            self.assertIn('id="technology"', result[name])
            self.assertIn("if(location.protocol==='file:'){location.assign(dest.href)", result[name])
        self.assertIn('different-note.html', result['index.html'])
        manifest = json.loads(result['manifest.json'])
        self.assertEqual(len(manifest['reports']), 2)

    def test_source_citations_resolve_inside_each_report(self):
        page = self.render(bundle())['example-notes.html']
        self.assertIn('href="#source-E1"', page)
        self.assertIn('id="source-E1"', page)

    def test_missing_app_section_is_rejected_without_partial_output(self):
        data = bundle()
        data['products'][0]['sections'].pop()
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'reports'
            with self.assertRaisesRegex(ValueError, 'sections'):
                renderer.render_bundle(data, out)
            self.assertFalse(out.exists())

    def test_all_coverage_dimensions_required(self):
        data = bundle()
        data['products'][0]['coverage'].pop()
        with self.assertRaisesRegex(ValueError, 'coverage'):
            self.render(data)

    def test_unknown_source_and_duplicate_source_fail(self):
        for mutation in ('unknown', 'duplicate'):
            data = bundle()
            p = data['products'][0]
            if mutation == 'unknown':
                p['sections'][0]['blocks'][0]['sources'] = ['wrong']
            else:
                p['sources'].append(copy.deepcopy(p['sources'][0]))
            with self.assertRaisesRegex(ValueError, 'source'):
                self.render(data)

    def test_duplicate_and_unsafe_filenames_fail(self):
        for ident in ('index', '../escape', 'manifest', 'x/y'):
            data = bundle()
            data['products'][0]['id'] = ident
            with self.assertRaises(ValueError):
                self.render(data)
        data = bundle()
        data['products'].append(copy.deepcopy(data['products'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.render(data)

    def test_text_is_escaped_and_active_links_rejected(self):
        data = bundle()
        data['products'][0]['name'] = '<script>alert(1)</script>'
        page = self.render(data)['example-notes.html']
        self.assertNotIn('<script>alert(1)</script>', page)
        self.assertIn('&lt;script&gt;', page)
        data['products'][0]['sources'][0]['url'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'URL'):
            self.render(data)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            (out / 'keep.txt').write_text('user work')
            with self.assertRaisesRegex(ValueError, 'empty'):
                renderer.render_bundle(bundle(), out)
            self.assertEqual((out / 'keep.txt').read_text(), 'user work')

    def test_images_are_embedded_and_not_remote_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            # Original tiny PNG; no third-party capture.
            import base64
            (source / 'pixel.png').write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aBYkAAAAASUVORK5CYII='))
            data = bundle()
            data['products'][0]['sections'][1]['blocks'].append({
                'type': 'image', 'path': 'pixel.png', 'alt': 'Original test pixel',
                'caption': 'Synthetic fixture, not competitor UI', 'sources': ['E1']})
            renderer.render_bundle(data, source / 'out', source)
            page = (source / 'out/example-notes.html').read_text()
            self.assertIn('data:image/png;base64,', page)
            self.assertNotIn('src="pixel.png"', page)

    def test_image_failure_happens_before_writing(self):
        data = bundle()
        data['products'][0]['sections'][1]['blocks'].append({
            'type': 'image', 'path': 'missing.png', 'alt': 'Missing', 'caption': 'Missing', 'sources': ['E1']})
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'out'
            with self.assertRaises(ValueError):
                renderer.render_bundle(data, out, Path(folder))
            self.assertFalse(out.exists())

    def test_ui_pairing_preserves_observations_citations_and_original_image(self):
        import base64
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)
            encoded = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aBYkAAAAASUVORK5CYII='
            (source / 'pixel.png').write_bytes(base64.b64decode(encoded))
            section = {'id': 'ui', 'title': 'Visual analysis', 'blocks': [
                {'type': 'image', 'path': 'pixel.png', 'alt': 'Original fixture',
                 'caption': 'Synthetic source context', 'sources': ['E1'],
                 'viewport': dict(x=0, y=0, width=1, height=1, source_width=1, source_height=1)},
                {'type': 'table', 'columns': ['Region', 'Seen', 'Interpretation'],
                 'rows': [['Compose', 'One visible action', 'Persistence remains untested']],
                 'status': 'Observed and inferred are distinct', 'sources': ['E2']},
                {'type': 'paragraph', 'text': 'Following qualification', 'sources': ['E1']}
            ]}
            html = renderer.section_html(section, 2, source, 'en')
            for text in ('Region', 'Seen', 'Interpretation', 'Compose', 'One visible action',
                         'Persistence remains untested', 'Observed and inferred are distinct',
                         'Following qualification', 'Synthetic source context'):
                self.assertIn(text, html)
            self.assertEqual(html.count(encoded), 2, 'The display window and complete original must both remain available')
            self.assertIn('href="#source-E2"', html)
            self.assertIn('<details class="original-image">', html)

    def test_no_empty_shells_or_unsupported_blocks(self):
        for blocks in ([], [{'type': 'invented', 'text': 'x'}]):
            data = bundle()
            data['products'][0]['sections'][0]['blocks'] = blocks
            with self.assertRaises(ValueError):
                self.render(data)

    def test_unicode_language_and_print_support(self):
        data = bundle()
        data.update(lang='zh-CN', title='竞品分析')
        html = self.render(data)['example-notes.html']
        self.assertIn('lang="zh-CN"', html)
        self.assertIn('@media print', html)
        self.assertIn('viewport', html)


if __name__ == '__main__':
    unittest.main()
