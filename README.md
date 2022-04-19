# cfig

A configuration manager for Python 

\[ [**Documentation**](https://cfig.readthedocs.io/) | [**PyPI**](https://pypi.org/project/cfig/) \]

## Example

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

```python
from mypackage.mycfig import SECRET_KEY

print(f"My SECRET_KEY is: {SECRET_KEY}")
```

```console
$ python -m mypackage.mycfig
=== Configuration ===

SECRET_KEY    → Required, but not set.
Secret string used to manage HTTP session tokens.
```
