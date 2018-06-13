from setuptools import setup, find_packages

from rpgrand import __version__

setup(
    name='rpgrand',
    version=__version__,
    description='Create structured randomized output from yaml or json files.',
    url='https://github.com/zls/rpgrand',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='rpg randomizer',
    project_urls={
        'Source': 'https://github.com/zls/rpgrand',
        'Tracker': 'https://github.com/zls/rpgrand/issues',
    },
    packages=['rpgrand'],
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['rpgrand=rpgrand.cli:main'],
    },
    zip_safe=False,
    install_requires=[
        'Jinja2',
        'PyYAML',
        'requests',
    ]
)
