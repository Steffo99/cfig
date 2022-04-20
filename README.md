# cfig

A configuration manager for Python 

\[ [**Example**](https://github.com/Steffo99/cfig/tree/main/cfig/sample) | [**Documentation**](https://cfig.readthedocs.io/) | [**PyPI**](https://pypi.org/project/cfig/) \]

```python
import cfig

config = cfig.Configuration()

@config.required()
def SECRET_KEY(val: str) -> str:
    """Secret string used to manage HTTP session tokens."""
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
===== Configuration =====

SECRET_KEY    → Required, but not set.
Secret string used to manage HTTP session tokens.

===== End =====
```
