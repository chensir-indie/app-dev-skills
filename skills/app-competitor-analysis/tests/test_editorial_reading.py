"""Reading copy must stay concise without losing claim boundaries or full evidence."""
import copy
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import unittest
from test_render_reports import bundle, renderer

class TextLayers(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.primary=[];self.all=[]
    def handle_starttag(self,t,a):
        if t=='details':self.depth+=1
    def handle_endtag(self,t):
        if t=='details':self.depth-=1
    def handle_data(self,t):
        self.all.append(t)
        if not self.depth:self.primary.append(t)

class EditorialReadingTests(unittest.TestCase):
    def test_short_copy_keeps_material_qualification_and_full_record(self):
        section=dict(id='overview',title='Research',blocks=[dict(type='paragraph',text='Full version-pinned observation and locator.')],summary_blocks=[dict(type='paragraph',text='Draft reopening is declared; not observed.',sources=['E1'])])
        result=renderer.section_html(section,1,'.','en');layers=TextLayers();layers.feed(result)
        self.assertIn('Draft reopening is declared; not observed.',''.join(layers.primary))
        self.assertNotIn('Full version-pinned observation and locator.',''.join(layers.primary))
        self.assertIn('Full version-pinned observation and locator.',''.join(layers.all))
        self.assertIn('href="#source-E1"',result)
    def test_unknown_source_in_reading_copy_is_rejected(self):
        data=bundle();data['products'][0]['sections'][0]['summary_blocks']=[dict(type='paragraph',text='A concise finding.',sources=['invented'])]
        with self.assertRaisesRegex(ValueError,'source'):renderer.validate_bundle(data)
    def test_malformed_reading_copy_fails_before_render(self):
        for summary in ('text',[],[dict(type='table',columns=['a'],rows=[['x','y']])]):
            data=bundle();data['products'][0]['sections'][0]['summary_blocks']=summary
            with self.assertRaises(ValueError):renderer.validate_bundle(data)
    def test_brief_requires_authored_identity_and_deck(self):
        for brief in ('text',{'headline':'','deck':'A clear purpose.'},{'headline':'A clear identity.'}):
            data=bundle();data['products'][0]['brief']=brief
            with self.assertRaises(ValueError):renderer.validate_bundle(data)

if __name__=='__main__':unittest.main()
