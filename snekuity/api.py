"""The primary module in snekuity."""

from collections.abc import Iterator
import locale
from typing import overload

from gnucash import (  # type: ignore
    Account,
    Book,
    Session,
    Split,
    Transaction,
)

from .logging import get_logger

logger = get_logger(__name__)


def siblings_of(split: Split) -> list[Split]:
    """Given a split, returns other splits from the same transaction.

    :return:
        a list of all splits in the same transaction that are not equal
        to the given split.
    """
    return [
        other for other in split.parent.GetSplitList() if other != split
    ]


def accounts_equal(account_1: Account, account_2: Account) -> bool:
    """Returns `True` if given accounts are equal, `False` otherwise.

    Shallow comparison to determine whether the two given accounts
    are equal in type, name, code, description, commodity, and GUID.

    Weaker than `account_1.Equal(account_2, check_guids=True)` but still
    useful because it suppresses logging.
    """
    return (
        account_1.GetType() == account_2.GetType()
        and account_1.name == account_2.name
        and account_1.GetCode() == account_2.GetCode()
        and account_1.GetDescription() == account_2.GetDescription()
        and bool(
            account_1.GetCommodity().equal(account_2.GetCommodity())
        )
        and bool(account_1.GetGUID().equal(account_2.GetGUID()))
    )


def format_xact(xact: Transaction) -> str:
    """Returns a string representation of the given split."""
    date = xact.GetDate()
    description = xact.GetDescription()
    return f'{f"{date:%x}":16s} {description[:45]:45}'


def format_split(split: Split, include_xact: bool = True) -> str:
    """Returns a string representation of the given split."""
    xact_date = split.parent.GetDate()
    xact_description = split.parent.GetDescription()
    account = split.account.name
    amount = locale.format_string(
        '%#16.2f', split.GetAmount(), grouping=True, monetary=True
    )
    return '    '.join(
        [
            f'{f"{xact_date:%x}":16s} {xact_description[:45]:45}'
            if include_xact
            else f'{" ":16s} {split.GetMemo()[:45]:45}',
            f'{account[:20]:20} {amount}',
        ]
    )


def _accounts_by_name(
    session: Session,
    account_names: list[str],
) -> list[Account]:
    book: Book = session.get_book()
    root = book.get_root_account()
    accounts = [
        root.lookup_by_full_name(account_name)
        for account_name in account_names
    ]
    for i, account in enumerate(accounts):
        if not account:
            raise RuntimeError(f'Account not found: {account_names[i]}')
    return accounts


@overload
def incomplete_xacts(
    base: Account,
    imbalance: Account,
) -> Iterator[tuple[Transaction, Split, Split]]: ...


@overload
def incomplete_xacts(
    base: str,
    imbalance: str,
    session: Session,
) -> Iterator[tuple[Transaction, Split, Split]]: ...


def incomplete_xacts(
    base: Account | str,
    imbalance: Account | str,
    session: Session | None = None,
) -> Iterator[tuple[Transaction, Split, Split]]:
    """Yields all incomplete transactions of a given base account.

    :param base: the account whose splits are to be iterated.

    :param imbalance:
        a reference account for comparison.
        Can be obtained e.g. by calling:
        ``root.lookup_by_full_name('Imbalance-EUR')``

    :param session:
        GnuCash session. Used for looking up accounts by name.
        Mandatory if one or both of `base` and `imbalance` are strings.

    :return:
        an iterator that yields triples of transaction, base
        split, and incomplete split.
    """
    if isinstance(base, str):
        assert session is not None
        [base_account, imbalance_account] = _accounts_by_name(
            session,
            [base, imbalance],
        )
    else:
        base_account, imbalance_account = base, imbalance
    for split in base_account.GetSplitList():
        if (
            len(siblings := siblings_of(split)) <= 1
            and (sibling := next(iter(siblings), None))
            and accounts_equal(sibling.GetAccount(), imbalance_account)
        ):
            yield split.parent, split, sibling
