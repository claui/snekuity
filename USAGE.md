<!-- markdownlint-configure-file { "MD025": false } -->

# Description

Snekuity (pronounced like “equity”) provides a Pythonic API for
interacting with GnuCash.

It is a wrapper around, and works alongside, GnuCash’s own Python
package.

# Example

## Identify incomplete (imbalanced) transactions in a given account

```py
from pathlib import PosixPath

from gnucash import Session, SessionOpenMode
from snekuity import format_split, format_xact, incomplete_xacts

with Session(
    book_uri=PosixPath('~/Documents/example.gnucash').expanduser().as_uri(),
    mode=SessionOpenMode.SESSION_READ_ONLY,
) as session:
    for xact, split, sibling in incomplete_xacts(
        base='Assets.Capital.Checking account.Savings bank',
        imbalance='Imbalance-EUR',
        session=session,
    ):
        print(format_xact(xact))
        print(format_split(sibling, include_xact=False))
        print(format_split(split, include_xact=False))
        print()
```

# Environment

snekuity supports the following environment variable:

`SNEKUITY_DEBUG`
: If set to a non-zero value, causes snekuity to enable debug-level
: logging.

# See also

`gnucash`(1),
[GnuCash Python bindings](https://code.gnucash.org/docs/STABLE/python_bindings_page.html)
