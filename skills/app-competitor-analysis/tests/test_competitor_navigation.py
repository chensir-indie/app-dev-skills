"""Every report can switch products without sacrificing independent offline links."""
import copy
from html.parser import HTMLParser
import unittest
from test_render_reports import bundle,renderer

class Nav(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[];self.reading_navs=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if 'competitor-link'in a.get('class','').split():self.links.append(a)
        if 'data-section-nav'in a:self.reading_navs+=1

class CompetitorNavigationTests(unittest.TestCase):
    def collection(self):
        b=bundle();p=copy.deepcopy(b['products'][0]);p.update(id='other-app',name='Other <App>');b['products'].append(p);return b
    def test_every_product_has_real_offline_switch_links_and_one_current_product(self):
        b=self.collection()
        for p in b['products']:
            page=renderer.report_page(b,p,1,'.');n=Nav();n.feed(page)
            self.assertEqual([a['href']for a in n.links],['example-notes.html','other-app.html'])
            self.assertEqual([a['href']for a in n.links if a.get('aria-current')=='page'],[p['id']+'.html'])
            self.assertEqual(len(n.ids),len(set(n.ids)))
            self.assertEqual(n.reading_navs,1)
            self.assertIn('Other &lt;App&gt;',page)
    def test_index_has_same_complete_switcher_without_a_false_current_product(self):
        b=self.collection();n=Nav();n.feed(renderer.index_page(b))
        self.assertEqual(len(n.links),2)
        self.assertFalse(any(a.get('aria-current')for a in n.links))
    def test_switcher_keeps_native_links_and_only_fetches_selected_same_origin_report(self):
        text=renderer.report_page(self.collection(),self.collection()['products'][0],1,'.')
        self.assertNotIn('<iframe',text)
        self.assertIn("if(location.protocol==='file:'){location.assign(dest.href)",text)
        self.assertIn("fetch(dest.pathname,{signal:controller.signal,credentials:'same-origin'})",text)
        self.assertNotIn('rel="prefetch"',text)
        self.assertIn('data-competitor-search',text)
        self.assertIn('data-section-nav',text)

if __name__=='__main__':unittest.main()
