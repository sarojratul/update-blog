# Minimal Jekyll stand-in for previewing the site offline (rubygems is blocked here).
# Supports: front matter, layouts chain, Jekyll-style include with params, _data, posts with permalink,
# kramdown GFM, a handful of Jekyll filters. Not a full Jekyll.
require "yaml"
require "date"
require "fileutils"
require "liquid"
require "kramdown"
require "kramdown-parser-gfm"

SRC = File.expand_path(ARGV[0])
DST = File.expand_path(ARGV[1])
FileUtils.rm_rf(DST)
FileUtils.mkdir_p(DST)

def split_fm(text)
  if text =~ /\A---\s*\n(.*?)\n---\s*\n?(.*)\z/m
    [YAML.safe_load($1, permitted_classes: [Date, Time]) || {}, $2]
  else
    [nil, text]
  end
end

config = YAML.safe_load(File.read(File.join(SRC, "_config.yml")), permitted_classes: [Date, Time])
data = {}
Dir[File.join(SRC, "_data", "*.yml")].each { |f| data[File.basename(f, ".yml")] = YAML.safe_load(File.read(f)) }

module JekyllFilters
  def relative_url(x) = x.to_s
  def absolute_url(x) = "https://sarojratul.github.io" + x.to_s
  def where(arr, key, val) = Array(arr).select { |h| h[key].to_s == val.to_s }
  def number_of_words(s) = s.to_s.gsub(/<[^>]+>/, " ").split.size
  def markdownify(s) = Kramdown::Document.new(s.to_s, input: "GFM", hard_wrap: false).to_html
  def xml_escape(s) = s.to_s.gsub("&", "&amp;").gsub("<", "&lt;").gsub(">", "&gt;")
end
Liquid::Template.register_filter(JekyllFilters)

class SeoTag < Liquid::Tag
  def render(ctx)
    page = ctx["page"] || {}
    t = page["title"] ? "#{page['title']} | #{ctx['site']['title']}" : ctx["site"]["title"]
    "<title>#{t}</title>"
  end
end
class NullTag < Liquid::Tag
  def render(_) = ""
end
class JInclude < Liquid::Tag
  def initialize(tag, markup, tokens)
    super
    @file, rest = markup.strip.split(/\s+/, 2)
    @params = {}
    (rest || "").scan(/(\w+)="([^"]*)"/) { |k, v| @params[k] = v }
  end
  def render(ctx)
    src = File.read(File.join(SRC, "_includes", @file))
    ctx.stack do
      ctx["include"] = @params
      Liquid::Template.parse(src).render(ctx)
    end
  end
end
Liquid::Template.register_tag("seo", SeoTag)
Liquid::Template.register_tag("feed_meta", NullTag)
Liquid::Template.register_tag("include", JInclude)

layouts = {}
Dir[File.join(SRC, "_layouts", "*.html")].each do |f|
  fm, body = split_fm(File.read(f))
  layouts[File.basename(f, ".html")] = [fm || {}, body]
end

def kd(text, config)
  opts = { input: "GFM", hard_wrap: false, auto_ids: true, toc_levels: (2..3), syntax_highlighter: nil }
  Kramdown::Document.new(text, opts).to_html
end

site = config.merge("data" => data, "time" => Time.now)
tz = "-06:00"

# Posts
posts = Dir[File.join(SRC, "_posts", "*.md")].map do |f|
  fm, body = split_fm(File.read(f))
  fm = (fm || {}).dup
  d = fm["date"]
  d = Time.parse(d.to_s) unless d.is_a?(Time)
  fm["date"] = d
  fm["url"] = fm["permalink"]
  fm["layout"] ||= "series-post"
  fm["path"] = f
  fm["raw"] = body
  fm
end.sort_by { |p| p["date"] }.reverse
site["posts"] = posts

def render_page(page, body, site, layouts, is_md)
  ctx = { "site" => site, "page" => page }
  html = Liquid::Template.parse(body, error_mode: :strict).render!(ctx, strict_filters: true)
  html = kd(html, nil) if is_md
  layout = page["layout"]
  while layout && layouts[layout]
    lfm, lbody = layouts[layout]
    html = Liquid::Template.parse(lbody, error_mode: :strict).render!({ "site" => site, "page" => page, "content" => html }, strict_filters: true)
    layout = lfm["layout"]
  end
  html
end

def out_path(url)
  url.end_with?("/") ? File.join(DST, url, "index.html") : File.join(DST, url)
end

posts.each do |p|
  html = render_page(p, p["raw"], site, layouts, true)
  path = out_path(p["url"])
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, html)
end

Dir[File.join(SRC, "*.{md,html}")].each do |f|
  next if File.basename(f) == "README.md"
  fm, body = split_fm(File.read(f))
  next unless fm
  fm = fm.dup
  url = fm["permalink"] || (File.basename(f, ".*") == "index" ? "/" : "/#{File.basename(f, '.*')}/")
  fm["url"] = url
  html = render_page(fm, body, site, layouts, f.end_with?(".md"))
  path = out_path(url)
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, html)
end

# Assets
fm, css = split_fm(File.read(File.join(SRC, "assets", "main.scss")))
FileUtils.mkdir_p(File.join(DST, "assets"))
File.write(File.join(DST, "assets", "main.css"), css)
FileUtils.cp_r(File.join(SRC, "images"), File.join(DST, "images"))
puts "built #{posts.size} posts"
