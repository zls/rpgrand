PYTHON=python3.6
PIP=pip3.6

all: sdist wheel

sdist:
	$(PYTHON) setup.py sdist

wheel:
	$(PYTHON) setup.py bdist_wheel

editable:
	$(PIP) install -e .

upload:
	twine upload dist/*