"""Verifica los enlaces de las 41 páginas, el catálogo y las imágenes locales."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent.parent
catalog=json.loads((ROOT/'content.json').read_text())
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.gallery=None;self.in_gallery=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for key in ('src','href'):
   value=a.get(key,'')
   if value and not re.match(r'^(https?:|mailto:|tel:)',value):self.refs.append(value)
  if tag=='script' and a.get('id')=='gallery-data':self.in_gallery=True
 def handle_endtag(self,tag):
  if tag=='script':self.in_gallery=False
 def handle_data(self,data):
  if self.in_gallery:self.gallery=json.loads(data)
pages={}
for file in ROOT.glob('*.html'):
 parser=Page();parser.feed(file.read_text());pages[file.name]=parser
assert len(pages)==len(catalog['pages']), 'Faltan páginas'
checked=set()
for name,page in pages.items():
 for ref in page.refs:
  target,_,anchor=ref.partition('#');target=target or name
  assert (ROOT/target).is_file(), f'{name}: referencia inexistente {ref}'
  if anchor and target in pages:assert anchor in pages[target].ids, f'{name}: ancla inexistente {ref}'
 for image in page.gallery:
  path=ROOT/image['src'];assert path.is_file(),f'Falta imagen: {path}'
  if path not in checked:
   data=path.read_bytes();assert len(data)>100, f'Imagen vacía: {path}'
   assert data.startswith((b'\xff\xd8\xff',b'\x89PNG',b'RIFF')) or b'ftyp' in data[:32],f'Formato de imagen no reconocido: {path}'
   checked.add(path)
for key,page in catalog['pages'].items():
 for child in page.get('children',[]):assert child in catalog['pages']
 if page['kind']=='series':assert page['images'],f'Galería vacía: {key}'
print(f'OK: {len(pages)} páginas, enlaces internos, anclas y {len(checked)} imágenes verificadas.')
