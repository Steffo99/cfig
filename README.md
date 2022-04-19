# cfig

A configuration manager for Python 

```python
import cfig

config = cfig.Configuration()

@config.required()
def SECRET_KEY(val: str) -> str:
    """Secret string used to manage tokens."""
    return val

if __name__ == "__main__":
    config.cli()
```

```console
$ python -m cfig.sample
=== Configuration ===

SECRET_KEY    → Required, but not set.
Secret string used to manage HTTP session tokens.
```

\[ [**Documentation**](https://cfig.readthedocs.io/) | [**PyPI**](https://pypi.org/project/cfig/) \]