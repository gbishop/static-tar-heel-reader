deploy:
	npm run production
	python3 generate.py base=36 Nselect=1000 minPages=3 maxPages=100 out=/var/www/static/dlm query=DLM hasCat=0 hasAudience=0
	python3 generate.py out=/var/www/static/tiny Nselect=100
