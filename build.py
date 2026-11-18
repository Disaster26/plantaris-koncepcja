import re, os, glob
D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, 'src.html'), encoding='utf-8').read()
s = s.replace('{{BADGE_STYLE}}', open(os.path.join(D, 'badge_style.part'), encoding='utf-8').read().replace('<style>', '').replace('</style>', ''))
s = s.replace('{{BADGE_LINK}}', open(os.path.join(D, 'badge_link.part'), encoding='utf-8').read())

def widths(name):
    ws = []
    for f in glob.glob(os.path.join(D, 'img', name + '-*.webp')):
        m = re.match(re.escape(name) + r'-(\d+)\.webp$', os.path.basename(f))
        if m: ws.append(int(m.group(1)))
    return sorted(set(ws))

def img(m):
    name, sizes, alt = m.group(1), m.group(2), m.group(3)
    ws = widths(name)
    from PIL import Image
    big = os.path.join(D, 'img', f'{name}-{ws[-1]}.webp')
    W, H = Image.open(big).size
    ss = ', '.join(f'img/{name}-{w}.webp {w}w' for w in ws)
    return (f'<img src="img/{name}-{ws[0]}.webp" srcset="{ss}" sizes="{sizes}" width="{W}" height="{H}" '
            f'alt="{alt}" loading="lazy" decoding="async">')

def lbsrc(m):
    ws = widths(m.group(1)); return f'img/{m.group(1)}-{ws[-1]}.webp'

s = re.sub(r'\{\{LB ([\w-]+)\}\}', lbsrc, s)
s = re.sub(r'\{\{IMG ([\w-]+)\|([^|]*)\|([^}]*)\}\}', img, s)
open(os.path.join(D, 'index.html'), 'w', encoding='utf-8').write(s)
print('ok', len(s))
