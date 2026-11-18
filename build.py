import re, os, glob
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(D, p), encoding='utf-8').read()
szablon = rd('szablon.html')
szablon = szablon.replace('{{BADGE_STYLE}}', rd('badge_style.part').replace('<style>', '').replace('</style>', ''))
szablon = szablon.replace('{{BADGE_LINK}}', rd('badge_link.part'))

def widths(name):
    ws = []
    for f in glob.glob(os.path.join(D, 'img', name + '-*.webp')):
        m = re.match(re.escape(name) + r'-(\d+)\.webp$', os.path.basename(f))
        if m: ws.append(int(m.group(1)))
    return sorted(set(ws))

def img(m):
    name, sizes, alt = m.group(1), m.group(2), m.group(3)
    ws = widths(name)
    W, H = Image.open(os.path.join(D, 'img', f'{name}-{ws[-1]}.webp')).size
    ss = ', '.join(f'img/{name}-{w}.webp {w}w' for w in ws)
    return (f'<img src="img/{name}-{ws[0]}.webp" srcset="{ss}" sizes="{sizes}" width="{W}" height="{H}" '
            f'alt="{alt}" loading="lazy" decoding="async">')

def lbsrc(m):
    ws = widths(m.group(1)); return f'img/{m.group(1)}-{ws[-1]}.webp'

for f in sorted(glob.glob(os.path.join(D, 'strony', '*.html'))):
    src = open(f, encoding='utf-8').read()
    meta = dict(re.findall(r'<!--(TITLE|DESC|PRELOAD|STRONA)\s(.*?)-->', src, re.S))
    tresc = re.sub(r'<!--(TITLE|DESC|PRELOAD|STRONA)\s.*?-->\n?', '', src, flags=re.S)
    s = szablon.replace('{{TITLE}}', meta['TITLE'].strip()).replace('{{DESC}}', meta['DESC'].strip())
    s = s.replace('{{PRELOAD}}', meta.get('PRELOAD', '').strip()).replace('{{TRESC}}', tresc)
    strona = meta.get('STRONA', 'start').strip()
    s = s.replace('data-s="' + strona + '"', 'data-s="' + strona + '" class="on" aria-current="page"')
    s = re.sub(r'\{\{LB ([\w-]+)\}\}', lbsrc, s)
    s = re.sub(r'\{\{IMG ([\w-]+)\|([^|]*)\|([^}]*)\}\}', img, s)
    out = os.path.basename(f)
    open(os.path.join(D, out), 'w', encoding='utf-8').write(s)
    print('ok', out, len(s))
