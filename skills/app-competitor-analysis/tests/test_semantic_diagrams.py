"""Semantic emphasis must not turn analysis into fabricated product behavior."""
import copy
import unittest
from test_render_reports import bundle, renderer
from test_visual_atlas import atlas


def semantic_bundle():
    b=bundle();v=b['products'][0]['visuals']
    ids=[n['id']for m in v['features']['modules']for n in m['features']]
    v['features']['priority']={'scope':'Write and keep a note','rationale':'Core means necessary to this task, not measured popularity.','core':ids[:1],'supporting':ids[1:],'extension':[],'sources':['E1']}
    g=v['journey'];e=g['edges'][0]
    g['focus']={'title':'Write to persistence','rationale':'One inspected path; alternatives remain visible.','path':[e['from'],e['to']],'sources':['E1']}
    g=v['dataflow'];e=g['edges'][0]
    g['contract']={'focus':[e['from'],e['to']],'roles':{n['id']:'input'if n['id']==e['from']else 'output'for n in g['nodes']},'boundary':{'title':'Local draft and exported file','detail':'Creating the draft does not establish external delivery.','sources':['E1']}}
    return b


class SemanticDiagramTests(unittest.TestCase):
    def test_rejects_priority_that_silently_loses_or_duplicates_a_feature(self):
        for mutate in (lambda p:p['core'].append(p['core'][0]),lambda p:p.update(core=[]),lambda p:p['extension'].append('fabricated')):
            b=semantic_bundle();mutate(b['products'][0]['visuals']['features']['priority'])
            with self.assertRaisesRegex(ValueError,'priority'):renderer.validate_bundle(b)

    def test_rejects_focus_path_without_an_actual_directed_edge(self):
        b=semantic_bundle();g=b['products'][0]['visuals']['journey'];g['focus']['path']=list(reversed(g['focus']['path']))
        with self.assertRaisesRegex(ValueError,'focus'):renderer.validate_bundle(b)

    def test_rejects_ambiguous_parallel_edges_on_selected_path(self):
        b=semantic_bundle();g=b['products'][0]['visuals']['journey']
        g['edges'].append(dict(g['edges'][0],label='Different condition'))
        with self.assertRaisesRegex(ValueError,'focus'):renderer.validate_bundle(b)

    def test_rejects_unknown_role_and_incomplete_technical_contract(self):
        for value in ('cloud',None):
            b=semantic_bundle();c=b['products'][0]['visuals']['dataflow']['contract'];ident=next(iter(c['roles']))
            if value is None:del c['roles'][ident]
            else:c['roles'][ident]=value
            with self.assertRaisesRegex(ValueError,'role'):renderer.validate_bundle(b)

    def test_rejects_uncited_boundary_and_priority_explanation(self):
        for kind in ('features','dataflow'):
            b=semantic_bundle();d=b['products'][0]['visuals'][kind]
            target=d['priority']if kind=='features'else d['contract']['boundary'];target['sources']=['made-up']
            with self.assertRaisesRegex(ValueError,'source'):renderer.validate_bundle(b)

    def test_render_preserves_all_nodes_edges_and_evidence_with_distinct_grammars(self):
        b=semantic_bundle();renderer.validate_bundle(b);p=b['products'][0];p['brief']={'headline':'Keep the draft','deck':'A write and export task.'}
        html=renderer.report_page(b,p,1,'.')
        self.assertIn('capability-landscape',html)
        self.assertIn('journey-spine',html)
        self.assertIn('technical-boundary',html)
        self.assertIn('data-semantic-role="input"',html)
        for k in ('features','journey','dataflow'):
            d=p['visuals'][k];nodes=[n for m in d['modules']for n in m['features']]if k=='features'else d['nodes']
            for n in nodes:self.assertEqual(html.count(f'data-node-detail="{k}-{n["id"]}"'),1)
        self.assertEqual(html.count('data-edge-from='),sum(len(p['visuals'][k]['edges'])for k in atlas.GRAPHS))

    def test_opening_preview_uses_authored_priority_not_module_array_order(self):
        p=semantic_bundle()['products'][0]
        before=renderer.abstract_preview(p,'en')
        p['visuals']['features']['modules'].reverse()
        self.assertEqual(renderer.abstract_preview(p,'en'),before)


if __name__=='__main__':unittest.main()
