# Phen2Gene Runner for PhEval
This is the Phen2Gene plugin for PhEval. Highly experimental. Do not use.

## Developers

An example skeleton `config.yaml` has been provided (`pheval.phen2gene/config.yaml`) which should be be correctly filled and moved to the `input-dir` location.

Warning, the pheval library currently needs to be included as a file reference in the toml file.

```
poetry add /Users/yaseminbridges/Documents/GitHub/pheval

poetry lock

poetry install
```

This will change when pheval is published on pypi.

To install the Phen2Gene plugin:

``` 
git clone https://github.com/yaseminbridges/pheval.phen2gene.git

cd pheval.phen2gene/

poetry add /path/to/local/pheval

poetry lock

poetry install
```

To install PhEval:

```
git clone https://github.com/monarch-initiative/pheval.git 
```
