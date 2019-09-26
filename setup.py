from setuptools import setup, find_packages

setup(
	name='pop-corpus',
	version='0.1',
	packages=['cli'],
	include_package_data=True,
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		pop-corpus=cli.cli:cli
	''',
	)
# from here: https://stackoverflow.com/questions/2051192/what-is-a-python-egg
# run: python setup.py bdist_egg

# to install, run pip install --editable .
