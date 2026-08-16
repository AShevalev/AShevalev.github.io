# AShevalev.github.io

Personal website of Andrey Shevalev, built with [Jekyll](https://jekyllrb.com/)
and served through [GitHub Pages](https://pages.github.com/).

## Local development

Requires Ruby (3.1+) and Bundler.

```bash
bundle install                 # install Jekyll and the github-pages gems
bundle exec jekyll serve       # build + serve at http://localhost:4000
```

The site auto-rebuilds as you edit content. Add `--livereload` to refresh the
browser automatically.

## Structure

- `index.md`, `about.md` — top-level pages
- `_posts/` — blog posts (`YYYY-MM-DD-title.md`)
- `_config.yml` — site configuration
- `Gemfile` — pins the `github-pages` gem so local builds match production

## Cloud Agent environment

`.cursor/environment.json` and `.cursor/Dockerfile` define a ready-to-use
[Cursor Cloud Agent](https://cursor.com/docs/cloud-agent) environment: a Ruby
image, `bundle install`, and a `jekyll serve` terminal.
