"""Genera las páginas estáticas a partir del catálogo local: python3 scripts/build_site.py."""
import json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'content.json').read_text());PAGES=DATA['pages']
def e(s):return html.escape(str(s),quote=True)
def href(key):return 'index.html' if key=='index' else key+'.html'
CATEGORIES=['pintura','ilustracion','fotografia','eroticos','arquitectura']
def card(im,index):
 title=im.get('title') or f'Obra {index+1:02}'
 return f'<a class="artwork" href="{e(im["src"])}" data-image="{index}" aria-label="Ampliar: {e(title)}"><span class="image-wrap"><img src="{e(im["src"])}" alt="{e(title)}" loading="{"eager" if index<3 else "lazy"}" decoding="async"></span><span class="art-caption"><span>{e(title)}</span><span aria-hidden="true">↗</span></span></a>'
def section(title,body,extra=''):
 return f'<section {extra}><div class="section-label"><h2>{e(title)}</h2></div>{body}</section>'
def paragraphs(items):return ''.join(f'<p>{e(t)}</p>' for t in items if t not in ['\u200b','Anterior','Siguiente','Atrás'])
for key,page in PAGES.items():
 kind=page['kind'];images=page.get('images',[])
 nav='<a href="index.html#obras">Todas las obras</a>'+''.join(f'<a href="{href(c)}" {"aria-current=page" if key==c or page.get("category")==c else ""}>{e(PAGES[c]["title"])}</a>' for c in CATEGORIES)+'<a href="informacion.html" '+('aria-current="page"' if key=='informacion' else '')+'>Información ↗</a>'
 header=f'<header class="header"><a class="wordmark" href="index.html">MATIAS GAJARDO</a><details class="navigation" open><summary>Menú <span aria-hidden="true">＋</span></summary><nav aria-label="Navegación principal">{nav}</nav></details></header>'
 footer='<footer id="contacto"><div><p class="eyebrow">MATIAS GAJARDO</p><p class="footer-title">Hablemos<span aria-hidden="true">↗</span></p><p>Artista visual / Ilustrador / Arquitecto</p></div><div class="contact"><h2>Contacto</h2><a href="mailto:matiasgajardo.correo@gmail.com">matiasgajardo.correo@gmail.com</a><a href="tel:+56983612310">+569 8361 2310</a></div><div class="footer-bottom"><span>MATIAS GAJARDO</span><a href="#inicio">Volver arriba ↑</a></div></footer>'
 content=''
 if kind=='home':
  content='<section class="intro"><p class="eyebrow">PORTFOLIO / MATIAS GAJARDO</p><h1>Artista visual<span class="slash"> / </span><br>Ilustrador<span class="slash"> / </span>Arquitecto</h1><a class="explore" href="#obras">Explorar obras ↓</a></section>'
  content+=section('Destacados', '<div class="featured gallery">'+''.join(card(im,i) for i,im in enumerate(images[:6]))+'</div>','id="destacados"')
  content+=section('Obras / Disciplinas','<div class="discipline-list">'+''.join(f'<a href="{href(c)}"><span>0{i+1}</span><h3>{e(PAGES[c]["title"])}</h3><span>↗</span></a>' for i,c in enumerate(CATEGORIES))+'</div>','id="obras"')
  content+=section('Obras / Todo','<div class="archive gallery">'+''.join(card(im,i) for i,im in enumerate(images))+'</div>')
 elif kind=='category':
  content=f'<section class="page-intro"><p class="eyebrow"><a href="index.html#obras">OBRAS</a> / {e(page["title"].upper())}</p><h1>{e(page["title"])}</h1><div class="prose">{paragraphs(page["paragraphs"])}</div></section>'
  cards=''
  for child in page['children']:
   cp=PAGES[child];ci=next((im for im in images if im['remote'] in [x['remote'] for x in cp['images']]),cp['images'][0] if cp['images'] else None)
   # La portada elegida en Wix se corresponde por orden con sus series.
   i=page['children'].index(child)
   if i<len(images):ci=images[i]
   cards+=f'<a class="artwork project-card" href="{href(child)}"><span class="image-wrap"><img src="{e(ci["src"])}" alt="{e(cp["title"])}" loading="lazy"></span><h3>{e(cp["title"])}</h3><p>{len(cp["images"])} imágenes <span aria-hidden="true">↗</span></p></a>'
  content+=section('Series y proyectos','<div class="projects gallery">'+cards+'</div>')
 elif kind=='series':
  parent=page['category'];items=page['paragraphs'][:]
  while items and (items[0].upper()==PAGES[parent]['title'].upper() or items[0].upper()==page['title'].upper()):items.pop(0)
  content=f'<section class="page-intro"><p class="eyebrow"><a href="{href(parent)}">← {e(PAGES[parent]["title"])}</a></p><h1>{e(page["title"])}</h1><div class="prose">{paragraphs(items)}</div></section>'
  content+=section(f'Galería / {len(images)} imágenes','<div class="series-gallery gallery">'+''.join(card(im,i) for i,im in enumerate(images))+'</div>')
  siblings=PAGES[parent]['children'];pos=siblings.index(key)
  content+='<nav class="series-nav" aria-label="Otras series">'+(f'<a href="{href(siblings[pos-1])}">← {e(PAGES[siblings[pos-1]]["title"])}</a>' if pos else f'<a href="{href(parent)}">← Todas las series</a>')+(f'<a href="{href(siblings[pos+1])}">{e(PAGES[siblings[pos+1]]["title"])} →</a>' if pos+1<len(siblings) else f'<a href="{href(parent)}">Todas las series →</a>')+'</nav>'
 else:
  content='<section class="page-intro"><p class="eyebrow">INFORMACIÓN / CONTACTO</p><h1>Matias Gajardo</h1><div class="prose biography">'+paragraphs(page['paragraphs'][1:])+'</div></section>'
  content+=section('Escríbeme','<form id="contact-form" class="contact-form"><p>Completa el mensaje para abrirlo en tu aplicación de correo.</p><label>Nombre<input name="name" autocomplete="name" required maxlength="150"></label><label>Email<input type="email" name="email" autocomplete="email" required maxlength="200"></label><label>Asunto<input name="subject" required maxlength="200"></label><label>Mensaje<textarea name="message" required rows="6" maxlength="10000"></textarea></label><button type="submit">Abrir mensaje en mi correo ↗</button><p id="form-status" role="status"></p></form>')
 viewer='<dialog id="viewer" aria-labelledby="image-title"><button class="close" type="button" aria-label="Cerrar visor">Cerrar ×</button><button class="previous" type="button" aria-label="Imagen anterior">←</button><figure><img id="full-image" alt=""><figcaption><strong id="image-title"></strong><p id="image-description"></p><div class="viewer-tools"><span id="image-counter" aria-live="polite"></span><a id="image-download" download>Descargar imagen ↓</a><button id="copy-link" type="button">Copiar enlace ↗</button></div><span id="viewer-status" role="status"></span></figcaption></figure><button class="next" type="button" aria-label="Imagen siguiente">→</button></dialog>'
 payload=json.dumps(images,ensure_ascii=False).replace('<','\\u003c')
 document=f'<!doctype html>\n<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(page["title"])} — Portfolio de Matias Gajardo, artista visual, ilustrador y arquitecto."><meta name="theme-color" content="#f6f5f1"><title>{e(page["title"])} — Matias Gajardo</title><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head><body><a class="skip-link" href="#inicio">Saltar al contenido</a>{header}<main id="inicio" tabindex="-1">{content}</main>{footer}{viewer}<script id="gallery-data" type="application/json">{payload}</script></body></html>\n'
 (ROOT/href(key)).write_text(document)
print(f'{len(PAGES)} páginas HTML generadas.')
