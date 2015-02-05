
build:
	python setup.py build

dev:
	python setup.py develop

upload:
	python setup.py sdist upload

lint:
	flake8 --show-source .

test:
	python -m unittest tests/*.py

clean:
	rm -rf build dist README MANIFEST ent.egg-info
