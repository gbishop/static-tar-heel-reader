pages: dist/find.html dist/settings.html dist/favorites.html dist/choose.html dist/index.html

dist/%.html: src/%.html
	./copypage.py $<
	
dist/find.html: src/find.html src/find.css src/head.mako src/menu.mako

dist/choose.html: src/choose.html src/find.css src/head.mako src/menu.mako

dist/settings.html: src/settings.html src/settings.css src/head.mako src/menu.mako

dist/index.html: src/index.html src/index.css

watch:
	fswatch -o src -e ".*\\.swp" --event=Created --event=Updated --latency=2 | xargs -n1 -I{} $(MAKE) --no-print-directory

dist/%.js: src/%.ts
	npm run production

production: dist/find.js dist/book.js dist/favorites.js dist/index.js dist/worker.js
	$(MAKE) pages

tiny: production
	rm -f /var/www/static/tiny/*.js /var/www/static/tiny/*.css
	./generate.py out=/var/www/static/tiny Nselect=100
	cp -a dist/* /var/www/static/tiny/

dev: pages
	./generate.py out=/var/www/static/tiny Nselect=100
