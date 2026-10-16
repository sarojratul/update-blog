# site-tools (update-blog skill toolbox)

Offline build, checks and delivery helpers for the `github-site` folder (sarojratul.github.io). Not part of the website; never upload this folder to the site repo. The canonical copy lives at github.com/sarojratul/update-blog (branch `main`); the update-blog skill downloads it at the start of every run and pushes new or improved scripts back at the end.

| Script | What it does | Usage |
|---|---|---|
| `preview.sh` | Clones Liquid 4.0.4, kramdown and kramdown-parser-gfm (rubygems is blocked in Claude's container), builds the site with `minijekyll.rb` into `<work>/_site`, then makes `<work>/preview` (relative links, preview banner) and `<work>/preview_files.json` | `bash preview.sh <github-site> <work>` |
| `minijekyll.rb` | Small Jekyll stand-in: front matter, layouts, Jekyll-style include, `_data`, posts, kramdown GFM. Not a full Jekyll | called by `preview.sh` |
| `build_preview.py` | Turns `_site` into the Artifact copy | called by `preview.sh` |
| `check_site.py` | Em dashes, unused or missing images, broken internal links and anchors | `python3 check_site.py <github-site> <work>/_site` |
| `site_diff.py` | Compares two folders by SHA-256: prints the GitHub upload list (Replace / New / Delete by hand), copies changed files to an outputs folder, prints `device_commit_files` JSON, or prints the Artifact `files` map of changed preview pages | `python3 site_diff.py ORIG EDITED [--outputs DIR --commit-json WINROOT] [--map --ignore 'class="preview-bar"']` |
| `new_post.py` | New post skeleton: next part number (turn signal roadmap kept last and bumped), filename, permalink, continuity link, contents box, section skeletons; refuses future dates | `python3 new_post.py <github-site> <series> YYYY-MM-DD <slug> "Title" [--time HH:MM] [--sections A B C]` |
| `make_zip.py` | Builds `sarojratul-github-site.zip` with `github-site/` as the top folder | `python3 make_zip.py <github-site> <out.zip>` |
| `figures/figstyle.py` | House style for matplotlib diagrams (1500 px, cream frame, amber traces, "What it shows:" footer) | imported by the `fig_*.py` templates |
| `figures/fig_*.py` | Templates: flowchart, timing diagram, HID report layout, turn signal state machine and timing | copy and edit for a new diagram |
