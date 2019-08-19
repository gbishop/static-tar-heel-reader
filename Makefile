pages: dist/find.html dist/settings.html dist/favorites.html dist/choose.html dist/index.html

DEV ?= 1

dist/%.html: src/%.html
	./copypage.py dev=$(DEV) $<
	
dist/find.html: src/find.html src/find.css src/head.mako src/menu.mako

dist/choose.html: src/choose.html src/find.css src/head.mako src/menu.mako

dist/settings.html: src/settings.html src/settings.css src/head.mako src/menu.mako

dist/index.html: src/index.html src/index.css

watch:
	fswatch -o src -e ".*\\.swp" --event=Created --event=Updated --latency=2 | xargs -n1 -I{} $(MAKE) --no-print-directory

production: DEV=0
production:
	rm -rf dist
	npm run production
	$(MAKE) pages DEV=$(DEV)

tiny: production
	rm /var/www/static/tiny/*.js /var/www/static/tiny/*.css
	./generate.py out=/var/www/static/tiny Nselect=100 dev=0
	cp -a dist/* /var/www/static/tiny/
