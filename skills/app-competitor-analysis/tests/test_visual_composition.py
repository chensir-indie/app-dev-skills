"""Presentation must preserve provenance and the original module boundaries."""
import copy
import unittest
from test_semantic_diagrams import semantic_bundle
from test_render_reports import renderer
from visual_composition import route_excerpt
from visual_atlas import STATES,words

class VisualCompositionTests(unittest.TestCase):
    def test_route_excerpt_retains_every_kind_of_evidence_without_upgrade(self):
        p=semantic_bundle()['products'][0];g=p['visuals']['journey'];ident=g['focus']['path'][0]
        for state in STATES:
            next(n for n in g['nodes']if n['id']==ident)['status']=state
            with self.subTest(state=state):
                html=route_excerpt(g,'zh-CN')
                self.assertIn('state-'+state,html)
                self.assertIn(words('zh-CN')['short_states'][state],html)
                self.assertNotIn('data-node-detail=',html,'Cover must not duplicate the full-map inspector targets')

    def test_equal_module_labels_do_not_merge_different_original_modules(self):
        b=semantic_bundle();p=b['products'][0];f=p['visuals']['features'];m=f['modules'][0]
        # Two distinct modules may legitimately have equal display labels.
        duplicate=copy.deepcopy(m);duplicate['features']=copy.deepcopy(m['features'])
        for n in duplicate['features']:n['id']='second-'+n['id']
        f['modules']=[m,duplicate]
        all_ids=[n['id']for module in f['modules']for n in module['features']]
        f['priority'].update(core=all_ids,supporting=[],extension=[])
        renderer.validate_bundle(b);html=renderer.report_page(b,p,1,'.')
        self.assertIn('data-module-index="0"',html)
        self.assertIn('data-module-index="1"',html)
        for ident in all_ids:self.assertEqual(html.count('data-node-detail="features-'+ident+'"'),1)

    def test_technical_reading_order_follows_objects_before_the_boundary(self):
        b=semantic_bundle();p=b['products'][0]
        html=renderer.report_page(b,p,1,'.')
        self.assertLess(html.index('class="contract-overview"'),html.index('class="technical-boundary"'))

if __name__=='__main__':unittest.main()
