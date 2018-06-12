# RPG Randomizer

This package provides the `rpgrand` cli tool and library for taking yaml or json configuration maps and generating structured output of randomized data.

## Installation
Requires python 3.6

```
git clone https://github.com/zls/rpgrand.git
cd rpgrand
pip3.6 install -e .
```

Make sure your PATH is setup correctly. On MacOS pip3.6 installs to *~/Library/Python/3.6/bin*. Check where pip installs for your OS.

## Usage
Adjust path to config file as necessary. Be aware that the config file will try and load additional files. For the examples change your current directory to the examples directory before running.

```
cd <path_to_examples>
rpgrand -c <configuration_map>
```

## Example

### Random human NPC using external source
```
cd <path_to_repo>/examples
rpgrand -c human_male.yml -o templates/npc.tmpl -n 10
```
