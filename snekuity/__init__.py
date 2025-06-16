"""
Usage example:

.. code:: python

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
"""

# Re-export these symbols
# (This promotes them from snekuity.api to snekuity)
from snekuity.api import (
    accounts_equal as accounts_equal,
    format_split as format_split,
    format_xact as format_xact,
    incomplete_xacts as incomplete_xacts,
    siblings_of as siblings_of,
)

from snekuity.version import version

__all__ = [
    # Modules that every subpackage should see
    'settings',
]

__version__ = version()
