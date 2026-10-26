import copy,json,tempfile,unittest
from pathlib import Path
from test_render_reports import bundle,renderer
import design_spec


def dossier():
    p=bundle()['products'][0];source=p['sources'][0]['id']
    record={'status':'observed','sources':[source]}
    return dict(scope='One supplied screen; runtime not observed.',intent='Keep the draft visible while writing.',
        coverage='partial',regions=[dict(name='Editor',elements=['Title field','Body field','Save button'],role='Write and retain a draft',**record)],
        rules=[dict(category=k,value='Visible arrangement in the supplied screen',method=None,**record)for k in design_spec.RULES],
        components=[dict(name='Save',anatomy='Label and action target',shown='Ready',unknown='Loading, failure, success',verify='Save offline and reopen',**record)],
        ux=dict(goal='Resume a saved draft',entry='Open editor',object='Draft',choice='Edit or resume',feedback='Visible saved state',recovery='Failed write preserves draft',completion='Reopen same content',
          findings=[dict(title='Saving needs a durable result',observation='Save is visible',consequence='A tap may not establish persistence',alternative='A local write may already be durable',decision='Expose retry when persistence fails',protocol=dict(start='Existing draft',action='Save then reopen',pass_result='Same draft reopens',reverse='If autosave is reliable, remove explicit save',status='not_run'),**record)]))

class DesignSpecTests(unittest.TestCase):
    def test_missing_evidence_rejected(self):
        p=bundle()['products'][0];p['design']=dossier();p['design']['regions'][0]['sources']=['MISSING']
        with self.assertRaisesRegex(ValueError,'source'):design_spec.validate_design(p)
    def test_measured_token_requires_measurement_method(self):
        p=bundle()['products'][0];p['design']=dossier();p['design']['rules'][0].update(status='measured',value='#123456')
        with self.assertRaisesRegex(ValueError,'method'):design_spec.validate_design(p)
    def test_missing_dimension_and_reversal_rejected(self):
        p=bundle()['products'][0];p['design']=dossier();p['design']['rules'].pop()
        with self.assertRaises(ValueError):design_spec.validate_design(p)
        p['design']=dossier();del p['design']['ux']['findings'][0]['protocol']['reverse']
        with self.assertRaisesRegex(ValueError,'reverse'):design_spec.validate_design(p)
    def test_unknown_value_stays_unknown(self):
        p=bundle()['products'][0];p['design']=dossier();p['design']['rules'][0].update(value=None,status='unknown',sources=[],verify='Inspect a native color asset')
        design_spec.validate_design(p);md,_=design_spec.design_markdown(p,'.','en')
        self.assertIn('Unknown',md);self.assertIn('Inspect a native color asset',md)
    def test_html_and_markdown_share_authored_inventory(self):
        b=bundle();p=b['products'][0];p['design']=dossier()
        with tempfile.TemporaryDirectory()as d:
            m=renderer.render_bundle(b,Path(d),delivery_format='linked')
            path=Path(d)/'design'/p['id']/'Design.md';self.assertTrue(path.is_file())
            md=path.read_text();html=(Path(d)/(p['id']+'.html')).read_text()
            for label in ['Title field','Body field','Save button']:
                self.assertIn(label,md);self.assertIn(label,html)
            self.assertIn('design/'+p['id']+'/Design.md',html)
            self.assertIn('Same draft reopens',md);self.assertIn('If autosave is reliable',md)
            self.assertEqual(m['design_documents'][0]['file'],str(path.relative_to(d)))
            self.assertIn('map-dataflow',html)

class PreviewSnapshotTests(unittest.TestCase):
    def test_preview_permits_only_same_origin_loading_and_manifest_files(self):
        from preview_reports import handler_for
        from http.server import ThreadingHTTPServer
        from threading import Thread
        from urllib.request import urlopen
        from urllib.error import HTTPError
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for('123456abcdef',{'/index.html':b'<h1>Report</h1>'},[]))
        thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            base='http://127.0.0.1:'+str(server.server_port)+'/reader/123456abcdef/'
            with urlopen(base+'index.html')as response:
                self.assertIn("connect-src 'self';",response.headers['Content-Security-Policy'])
                self.assertIn("default-src 'none';",response.headers['Content-Security-Policy'])
                self.assertEqual(response.read(),b'<h1>Report</h1>')
            with self.assertRaises(HTTPError)as error:urlopen(base+'private.txt')
            self.assertEqual(error.exception.code,404)
        finally:server.shutdown();server.server_close();thread.join()

    def test_design_document_hash_is_verified_and_non_report_file_not_served(self):
        from preview_reports import snapshot
        b=bundle();p=b['products'][0];p['design']=dossier()
        with tempfile.TemporaryDirectory()as d:
            renderer.render_bundle(b,Path(d),delivery_format='linked')
            (Path(d)/'private.txt').write_text('not part of delivery')
            rev,files=snapshot(d)
            self.assertIn('/design/'+p['id']+'/Design.md',files)
            self.assertNotIn('/private.txt',files)
            (Path(d)/'design'/p['id']/'Design.md').write_text('changed')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):snapshot(d)

if __name__=='__main__':unittest.main()
