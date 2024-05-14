<div align="center"> 

![](.media/icon-128x128_round.png)

# cfig

Configuration helper for Python 

</div>

## Links

[![PyPI](https://img.shields.io/pypi/v/cfig)](https://pypi.org/project/cfig)

[![Documentation](https://img.shields.io/readthedocs/cfig)](https://cfig.readthedocs.io/en/latest/)

## Example

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
