"""Portable regressions for graph routes and complete hierarchy output."""
import importlib.util
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('visual_atlas', ROOT / 'scripts/visual_atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)


def node(ident, col=0, row=0):
    return dict(id=ident, label=f'Capability {ident}', detail=f'Detail for {ident}',
                status='declared', sources=['E1'], col=col, row=row)


def edge(a, b, label='Retry after review'):
    return dict(**{'from': a, 'to': b}, label=label, status='inferred', sources=[])


def diagram(nodes, edges):
    return dict(title='Original test map', summary='Test fixture', nodes=nodes, edges=edges)


def rendered_svg(graph):
    text = atlas.graph_svg(graph, 'journey', atlas.words('en'))
    return ET.fromstring(re.search(r'(<svg\b.*?</svg>)', text).group(1)), text


class VisualAtlasTests(unittest.TestCase):
    def test_self_loop_is_a_visible_route_not_a_collapsed_line(self):
        # A capability can retry itself. The former route doubled back over
        # the same vertical segment and looked like no loop at all.
        svg, text = rendered_svg(diagram([node('retry')], [edge('retry', 'retry')]))
        route = svg.find(".//g[@class='graph-edge uncertain']/path").attrib['d']
        self.assertGreaterEqual(route.count('H'), 2)
        self.assertGreaterEqual(route.count('V'), 2)
        self.assertIn('marker-end', svg.find(".//g[@class='graph-edge uncertain']/path").attrib)
        self.assertIn('Capability retry → Capability retry', text)

    def test_outer_routes_and_multiline_labels_fit_inside_viewbox(self):
        # A long vertical skip needs a side gutter even in the last column.
        nodes = [node('start'), node('middle', row=1), node('finish', row=2)]
        graph = diagram(nodes, [edge('start', 'finish', 'Optional secondary route'),
                                edge('finish', 'finish')])
        svg, _ = rendered_svg(graph)
        _, _, width, height = map(float, svg.attrib['viewBox'].split())
        for rect in svg.findall('.//rect'):
            x, y, w, h = (float(rect.attrib[k]) for k in ('x', 'y', 'width', 'height'))
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + w, width)
            self.assertLessEqual(y + h, height)

    def test_branch_loop_and_unknown_keep_sources_and_accessible_details(self):
        unknown = node('unknown', 1, 1)
        unknown.update(status='unknown', sources=[])
        nodes = [node('start'), node('choose', 1), unknown]
        edges = [edge('start', 'choose', 'Continue'),
                 edge('choose', 'start', 'Change selection'),
                 edge('choose', 'unknown', 'Failure')]
        svg, text = rendered_svg(diagram(nodes, edges))
        self.assertEqual(len(svg.findall(".//g[@class='graph-edge uncertain']")), 3)
        for n in nodes:
            self.assertIn(f'id="journey-index-{n["id"]}"', text)
            self.assertIn(f'id="journey-{n["id"]}"', text)
        for e in edges:
            self.assertIn(e['label'], text)
        self.assertIn('href="#source-E1"', text)
        self.assertIn('class="graph-index"', text)

    def test_feature_details_and_sources_exist_outside_inert_templates(self):
        declared, unknown = node('capture'), node('save')
        unknown.update(status='unknown', sources=[])
        features = dict(modules=[dict(label='Capture and save', features=[declared, unknown])])
        text = atlas.feature_tree(features, 'Original test product', atlas.words('en'))
        # Template content is unavailable without JS and is not printed. Every
        # feature must also join its explanation, status and sources in HTML.
        static = re.sub(r'<template\b.*?</template>', '', text, flags=re.S)
        root = ET.fromstring(f'<root>{static}</root>')
        index = root.find(".//details[@class='graph-index feature-index']")
        self.assertIsNotNone(index)
        self.assertNotIn('open', index.attrib)
        for item in (declared, unknown):
            detail = index.find(f".//li[@id='features-index-{item['id']}']")
            self.assertIsNotNone(detail)
            self.assertEqual(detail.find('strong').text, item['label'])
            self.assertEqual(detail.find('p').text, item['detail'])
            self.assertIn(item['status'], detail.find('span').attrib['class'])
            self.assertEqual([a.attrib['href'] for a in detail.findall('.//a')],
                             [f'#source-{source}' for source in item['sources']])
        links=root.findall('.//a[@data-node-detail]')
        self.assertEqual(len(links),2)
        self.assertEqual([a.attrib['href']for a in links],['#features-index-capture','#features-index-save'])
        self.assertEqual(text.count('class="node-template"'), 2)

    def test_wide_feature_inventory_keeps_every_module_and_node(self):
        modules = [
            dict(label=f'Module {i}', features=[node(f'm{i}a'), node(f'm{i}b')])
            for i in range(6)
        ]
        text = atlas.feature_tree(dict(modules=modules), 'Original test product', atlas.words('en'))
        self.assertEqual(text.count('class="feature-module"'), 6)
        self.assertEqual(text.count('data-node-detail="features-'), 12)
        self.assertEqual(text.count('class="node-template"'), 12)
        self.assertIn('6 modules · 12 capabilities', text)
        self.assertIn('Original test product', text)


if __name__ == '__main__':
    unittest.main()
