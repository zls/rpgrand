from setuptools import setup

setup(name="rpgrand",
      version="0.1",
      description="RPG randomizer",
      packages=["rpgrand"],
      entry_points = {
          "console_scripts": ["rpgrand=rpgrand.cli:main"],
      },
      zip_safe=False,
      install_requires=[
          "pip",
          "Jinja2",
          "PyYAML",
          "requests",
      ]
    )
