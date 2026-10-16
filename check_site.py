"""Checks a built _site: em dashes in the source, unused or missing images, broken internal links and anchors.
usage: python3 check_site.py <github-site dir> <built _site dir>"""
import re, os, glob, sys
src, site = (os.path.abspath(a) for a in sys.argv[1:3])
bad = [f for f in glob.glob(src + '/**/*', recursive=True)
       if os.path.isfile(f) and f.endswith(('.md', '.html', '.yml', '.scss', '.svg')) and '—' in open(f, encoding='utf-8').read()]
print('files with em dashes:', bad)
imgs = set(os.listdir(src + '/images')); used = set()
for f in glob.glob(src + '/**/*.*', recursive=True):
    if f.endswith(('.md', '.html', '.yml')) and not f.endswith('README.md'):
        used |= set(re.findall(r'/images/([\w\-\.]+)', open(f, encoding='utf-8').read()))
print('unused images:', sorted(imgs - used)); print('missing images:', sorted(used - imgs))
pages = {f[len(site):-len('index.html')]: open(f, encoding='utf-8').read() for f in glob.glob(site + '/**/index.html', recursive=True)}
probs = []
for url, h in pages.items():
    for href in re.findall(r'href="(/[^"]*)"', h):
        if href.startswith(('/assets', '/feed.xml')): continue
        if href.startswith('/images'):
            if not os.path.exists(site + href): probs.append((url, href, 'missing file'))
            continue
        path, _, anc = href.partition('#')
        if path not in pages: probs.append((url, href, 'no page'))
        elif anc and f'id="{anc}"' not in pages[path]: probs.append((url, href, 'no anchor'))
    for s in re.findall(r'src="(/images/[^"]+)"', h):
        if not os.path.exists(site + s): probs.append((url, s, 'missing image'))
print('link problems:', probs)
