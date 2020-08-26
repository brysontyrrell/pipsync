# Pipsync

_Pipsync_ is a utility to help keep `requirements.txt` files in sync with a parent `Pipfile` for Serverless Application Model (SAM) projects.

## Installation and Usage

_Pipsync_ will be published on PyPI in the future.

Install _Pipsync_ from GitHub:

```shell script
% pip install git+git://github.com/brysontyrrell/pipsync
```

### SAM Project Structure

_Pipsync_ is opinionated on how serverless projects are structured. The directory tree below is an example.

At the root the repository are the `Pipfile` and `Pipfile.lock` which manage the local development environment. Within the project directories for the various Lambda Functions with their respective `requirements.txt` files used by `sam build`.

The locations of the Lambda Functions are not important and these directories can be structured as you wish.

```text
MyApp/
├── src/
│   ├── function_A
│   │   ├── index.py
│   │   └── requirements.txt
│   └── function_B
│       ├── index.py
│       └── requirements.txt
├── Pipfile
├── Pipfile.lock
└── template.yaml
```

### CLI Options

After installing, view _Pipsync's_ options by running `pipsync -h`:

```text                                      
usage: pipsync [-h] [-x EXCLUDE] [-f] [--dev] [-v] [--version] PATH

Sync requirements.txt files with a project Pipfile.

positional arguments:
  PATH                  Project root / Pipfile location

optional arguments:
  -h, --help            show this help message and exit
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude top level directories from requirements.txt file search
  -f, --force           Remove packages in requirements.txt files that are not in the Pipfile
  --dev                 Include dev-packages from Pipfile.
  -v, --verbose         Verbose console output.
  --version             show program's version number and exit

```

_Pipsync_ will scan the `Pipfile` for all of the top-level packages you have installed. It will then scan for `requirements.txt` files within the directory structure. From there, _Pipsync_ will read each file, compare it to the top-level package list, and re-write using the pinned versions in `Pipfile.lock`.

#### Force Sync

By default, _Pipsync_ will ignore packages in `requirements.txt` files that are not listed in your `Pipfile`. These packages will be passed back in without a pinned version. Use the `-f/--force` argument to remove packages in `requirements.txt` that are not found in your `Pipfile`.

#### Dev Packages

By default, _Pipsync_ will not include `dev-packages` from your `Pipfile` when syncing. Use the `--dev` argument to include them.

### Use With Editors and IDEs

PyCharm FileWatcher instructions coming...
