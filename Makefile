install:
	echo "Not implemented yet"
	#pip install -r requirements.txt

tests:
	cd test && python3 -m pytest


# Docs
install-docs:
	pip install -r docs/requirements.txt

clean-docs-dependencies:
	echo "Not implemented yet"

serve-docs:
	mkdocs serve

build-docs:
	mkdocs build

deploy-docs:
	mkdocs gh-deploy


