"""A report's diagrams must explain the adjacent task, not be hidden tab content."""
from html.parser import HTMLParser
import copy
import re
import unittest
import xml.etree.ElementTree as ET
from test_render_reports import bundle, renderer
from test_visual_atlas import atlas, diagram, node, edge


class DiagramLocations(HTMLParser):
    def __init__(self):
        super().__init__();self.sections=[];self.locations={};self.disclosures=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='details':self.disclosures+=1
        if tag=='section':
            if 'data-atlas-panel'in a:self.locations[a['data-atlas-panel']]=(list(self.sections),self.disclosures)
            self.sections.append(a.get('id'))
    def handle_endtag(self,tag):
        if tag=='section':self.sections.pop()
        if tag=='details':self.disclosures-=1


class IntegratedDiagramTests(unittest.TestCase):
    def test_brief_report_places_each_full_map_with_its_explanation(self):
        b=bundle();b['products'][0]['brief']={'headline':'Keep the current draft','deck':'Write, reopen and export a note.'}
        page=renderer.report_page(b,b['products'][0],1,'.');reader=DiagramLocations();reader.feed(page)
        for kind,parent in [('features','atlas'),('screens','ui'),('journey','interaction'),('dataflow','technology')]:
            self.assertIn(parent,reader.locations[kind][0])
            self.assertEqual(reader.locations[kind][1],0,'A full diagram must remain outside research disclosures')
        self.assertIn('href="#map-dataflow"',page)
        self.assertIn('data-atlas-mode="integrated"',page)

    def test_feature_meaning_is_visible_beside_its_label(self):
        n=node('save');n['detail']='Creates a durable local note before export.'
        text=atlas.feature_tree({'modules':[{'label':'Delivery','features':[n]}]},'Notes',atlas.words('en'))
        self.assertIn('<span class="feature-meaning">Creates a durable local note before export.</span>',text)

    def test_authored_diagram_reading_rejects_unknown_citations(self):
        b=bundle();b['products'][0]['visuals']['dataflow']['reading']={'text':'Local persistence precedes export.','sources':['invented']}
        with self.assertRaisesRegex(ValueError,'source'):renderer.validate_bundle(b)

    def test_disconnected_routes_keep_all_nodes_edges_without_a_fake_bridge(self):
        g=diagram([node('a'),node('b',1),node('c',row=3),node('d',1,3)],
                  [edge('a','b','Write'),edge('c','d','Export')])
        groups=atlas.graph_components(g)
        self.assertEqual([set(n['id']for n in x['nodes'])for x in groups],[{'a','b'},{'c','d'}])
        self.assertEqual(sum(len(x['edges'])for x in groups),2)
        self.assertEqual(max(n['row']for n in groups[1]['nodes']),0)

    def test_diagram_reading_is_not_a_silent_untyped_extension(self):
        for reading in ('text',{'text':'','sources':[]},{'text':'A statement','sources':'E1'}):
            b=bundle();b['products'][0]['visuals']['features']['reading']=reading
            with self.assertRaises(ValueError):renderer.validate_bundle(b)

    def test_connector_labels_do_not_cover_each_other_or_unrelated_nodes(self):
        nodes=[node(str(i),i%3,i//3)for i in range(6)]
        graph=diagram(nodes,[edge('0','1','同屏包含'),edge('0','2','同屏包含'),
                            edge('3','0','进入关系？'),edge('4','0','使用自有参考'),edge('0','5','实际路由？')])
        svg=ET.fromstring(re.search(r'(<svg\b.*?</svg>)',atlas.graph_svg(graph,'screens',atlas.words('zh-CN'))).group(1))
        box=lambda r:tuple(float(r.attrib[k])for k in ('x','y','width','height'))
        overlap=lambda a,b:a[0]<b[0]+b[2]and a[0]+a[2]>b[0]and a[1]<b[1]+b[3]and a[1]+a[3]>b[1]
        labels=[box(g.find('rect'))for g in svg.findall("g[@class='graph-edge-label']")]
        node_boxes=[box(a.find('rect'))for a in svg.findall('a')]
        for i,label in enumerate(labels):
            self.assertFalse(any(overlap(label,other)for other in labels[:i]+node_boxes))

    def test_oversized_caption_fails_before_silent_svg_clipping(self):
        b=bundle();b['products'][0]['visuals']['dataflow']['nodes'][0]['caption']='A long explanation. '*20
        with self.assertRaisesRegex(ValueError,'caption'):renderer.validate_bundle(b)


if __name__=='__main__':unittest.main()
