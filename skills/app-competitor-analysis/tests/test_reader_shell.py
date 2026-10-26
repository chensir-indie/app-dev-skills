"""All report material must belong to a reachable, URL-addressable reader view."""
from html.parser import HTMLParser
import unittest
from test_render_reports import bundle,renderer

class Reader(HTMLParser):
    def __init__(self):super().__init__();self.stack=[];self.views=[];self.contents={};self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='div':
            key=a.get('data-reader-view');self.stack.append(key)
            if key:self.views.append(key);self.contents[key]=[]
        current=next((x for x in reversed(self.stack)if x),None)
        if current and a.get('id'):self.contents[current].append(a['id'])
        if tag=='a'and 'data-reader-link'in a:self.links.append(a['href'])
    def handle_endtag(self,tag):
        if tag=='div'and self.stack:self.stack.pop()

class ReaderShellTests(unittest.TestCase):
    def test_complete_content_is_owned_by_reachable_views_for_brief_and_legacy_input(self):
        for brief in [False,True]:
            b=bundle();p=b['products'][0]
            if brief:p['brief']={'headline':'Recover the draft','deck':'Write, interrupt and recover.'}
            r=Reader();r.feed(renderer.report_page(b,p,1,'.'))
            self.assertEqual(r.views,['overview','capabilities','interface','interaction','technology','decisions','sources'])
            expected={'overview':['overview'],'capabilities':['atlas','map-features'],'interface':['ui','map-screens'],'interaction':['interaction','map-journey'],'technology':['technology','map-dataflow'],'decisions':['business','strengths','decisions','validation'],'sources':['sources']}
            for key,ids in expected.items():
                for ident in ids:self.assertIn(ident,r.contents[key])
            self.assertEqual(len(r.links),8)
            # HTML content exists without JavaScript; runtime chooses one view.
            html=renderer.report_page(b,p,1,'.')
            self.assertNotIn('data-reader-view="overview" hidden',html)

if __name__=='__main__':unittest.main()
