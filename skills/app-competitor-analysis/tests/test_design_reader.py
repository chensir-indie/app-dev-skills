import unittest
from html.parser import HTMLParser
from test_design_spec import dossier
from test_render_reports import bundle,renderer
from design_reader import markdown_html,inline
class DesignReaderTests(unittest.TestCase):
 def test_spec_keeps_lists_table_cells_and_evidence_links(self):
  source='# Spec\n\n## Anatomy\n\n- Save\n- Retry\n\nField | Value\n--- | ---\nA | a\\|b\n\n[Evidence](../../demo.html#source-E1)\n'
  markup,outline=markdown_html(source)
  self.assertIn('<li>Save</li><li>Retry</li>',markup)
  self.assertIn('<td>a|b</td>',markup)
  self.assertIn('href="demo.html#source-E1"',markup)
  self.assertEqual(outline,[('design-section-1','Anatomy')])
 def test_source_text_cannot_create_executable_markup(self):
  markup=inline('<script>alert(1)</script> [x](javascript:alert) [remote](//evil.test)')
  self.assertNotIn('<script>',markup);self.assertNotIn('href=',markup)
 def test_report_has_same_complete_protocol_in_inert_reader(self):
  b=bundle();p=b['products'][0];p['design']=dossier()
  page=renderer.report_page(b,p,1,'.')
  part=page.split('<template id="design-document"',1)[1]
  for value in ['Save button','Loading, failure, success','Same draft reopens','If autosave is reliable']:
   self.assertIn(value,part)
  self.assertIn('class="spec-outline"',part)
if __name__=='__main__':unittest.main()
