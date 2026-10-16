"""Turn the offline Jekyll build (_site) into a self-contained preview for an Artifact:
relative links, explicit index.html, data-theme aware colours, and a preview banner."""
import os, re, shutil, datetime, json, sys

# usage: python3 build_preview.py <built _site dir> <preview output dir> <files json output>
SRC, DST, FILES_JSON = (os.path.abspath(a) for a in sys.argv[1:4])
shutil.rmtree(DST, ignore_errors=True)
shutil.copytree(SRC, DST)

stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-6))).strftime("%-d %b %Y, %H:%M")
banner = ('<div class="preview-bar">Preview of sarojratul.github.io, built ' + stamp +
          '. Not the live site.</div>')

def rel(url, depth):
    if url.startswith("//"):
        return url
    path, _, anchor = url.partition("#")
    if path == "/feed.xml":
        return "#"
    if path.endswith("/"):
        path += "index.html"
    out = "../" * depth + path.lstrip("/")
    return out + ("#" + anchor if anchor else "")

files = {}
for root, _, names in os.walk(DST):
    for n in names:
        full = os.path.join(root, n)
        relpath = os.path.relpath(full, DST)
        if n.endswith(".html"):
            depth = relpath.count("/")
            h = open(full, encoding="utf-8").read()
            h = re.sub(r'(href|src)="(/[^"]*)"', lambda m: f'{m.group(1)}="{rel(m.group(2), depth)}"', h)
            h = h.replace("<body>", "<body>\n" + banner, 1)
            if relpath == "index.html":
                # The main page is wrapped in the Artifact skeleton, so keep only head content and body content.
                head = re.search(r"<head>(.*?)</head>", h, re.S).group(1)
                head = re.sub(r'<meta (charset|name="viewport")[^>]*>', "", head)
                body = re.search(r"<body>(.*)</body>", h, re.S).group(1)
                head = head.replace("<title>Saroj Ratul</title>", "<title>Build Log Preview</title>")
                h = head.strip() + "\n" + body.strip() + "\n"
            open(full, "w", encoding="utf-8").write(h)
        if relpath != "index.html":
            files[relpath] = full

css_path = os.path.join(DST, "assets", "main.css")
css = open(css_path, encoding="utf-8").read()
m = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}\s*\}", css, re.S)
dark = m.group(1)
css = css.replace(m.group(0),
                  "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {" + dark + " color-scheme: dark; }\n}\n"
                  ":root[data-theme=\"dark\"] {" + dark + " color-scheme: dark; }")
css += ("\n.preview-bar { font-family: var(--mono); font-size: 0.75rem; text-align: center; padding: 6px 16px;"
        " background: var(--accent-soft); color: var(--accent-ink); border-bottom: 1px solid var(--line); }\n")
open(css_path, "w", encoding="utf-8").write(css)

json.dump(files, open(FILES_JSON, "w"), indent=0)
print(len(files), "supporting files")
