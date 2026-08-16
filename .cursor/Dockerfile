# Base image for the Cloud Agent development environment.
#
# GitHub Pages builds this site with Ruby + Jekyll (via the `github-pages` gem),
# so the environment mirrors that toolchain. The full `ruby` image is based on
# buildpack-deps, which already provides git, curl, and a C toolchain needed to
# compile the native gems that github-pages pulls in (nokogiri, sass, etc.).
FROM ruby:3.3-bookworm

# Match the Bundler version pinned in Gemfile.lock so `bundle install` does not
# have to self-install a different version at setup time.
RUN gem install bundler -v 4.0.18 --no-document

# The repository is checked out separately by Cursor; nothing is COPYed in here.
WORKDIR /workspace
