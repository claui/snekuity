# pylint: disable=magic-value-comparison, missing-function-docstring, missing-module-docstring, no-self-use, too-many-public-methods

from collections.abc import Iterator
from pathlib import Path
from textwrap import dedent

from gnucash import Session, SessionOpenMode  # type: ignore
import pytest

from snekuity.api import incomplete_xacts


@pytest.fixture(name='path_to_empty_book')
def fixture_path_to_empty_book(tmp_path: Path) -> Path:
    path = tmp_path / 'empty.gnucash'
    with open(path, encoding='utf-8', mode='w') as file:
        file.write(
            dedent("""\
                <?xml version="1.0" encoding="utf-8" ?>
                <gnc-v2
                     xmlns:gnc="http://www.gnucash.org/XML/gnc"
                     xmlns:act="http://www.gnucash.org/XML/act"
                     xmlns:book="http://www.gnucash.org/XML/book"
                     xmlns:cd="http://www.gnucash.org/XML/cd"
                     xmlns:cmdty="http://www.gnucash.org/XML/cmdty"
                     xmlns:price="http://www.gnucash.org/XML/price"
                     xmlns:slot="http://www.gnucash.org/XML/slot"
                     xmlns:split="http://www.gnucash.org/XML/split"
                     xmlns:sx="http://www.gnucash.org/XML/sx"
                     xmlns:trn="http://www.gnucash.org/XML/trn"
                     xmlns:ts="http://www.gnucash.org/XML/ts"
                     xmlns:fs="http://www.gnucash.org/XML/fs"
                     xmlns:bgt="http://www.gnucash.org/XML/bgt"
                     xmlns:recurrence="http://www.gnucash.org/XML/recurrence"
                     xmlns:lot="http://www.gnucash.org/XML/lot"
                     xmlns:addr="http://www.gnucash.org/XML/addr"
                     xmlns:billterm="http://www.gnucash.org/XML/billterm"
                     xmlns:bt-days="http://www.gnucash.org/XML/bt-days"
                     xmlns:bt-prox="http://www.gnucash.org/XML/bt-prox"
                     xmlns:cust="http://www.gnucash.org/XML/cust"
                     xmlns:employee="http://www.gnucash.org/XML/employee"
                     xmlns:entry="http://www.gnucash.org/XML/entry"
                     xmlns:invoice="http://www.gnucash.org/XML/invoice"
                     xmlns:job="http://www.gnucash.org/XML/job"
                     xmlns:order="http://www.gnucash.org/XML/order"
                     xmlns:owner="http://www.gnucash.org/XML/owner"
                     xmlns:taxtable="http://www.gnucash.org/XML/taxtable"
                     xmlns:tte="http://www.gnucash.org/XML/tte"
                     xmlns:vendor="http://www.gnucash.org/XML/vendor">
                <gnc:count-data cd:type="book">1</gnc:count-data>
                <gnc:book version="2.0.0">
                <book:id type="guid">7618e1150aa54edc8c67016211b3c713</book:id>
                <gnc:count-data cd:type="commodity">1</gnc:count-data>
                <gnc:count-data cd:type="account">1</gnc:count-data>
                <gnc:commodity version="2.0.0">
                  <cmdty:space>template</cmdty:space>
                  <cmdty:id>template</cmdty:id>
                  <cmdty:name>template</cmdty:name>
                  <cmdty:xcode>template</cmdty:xcode>
                  <cmdty:fraction>1</cmdty:fraction>
                </gnc:commodity>
                <gnc:account version="2.0.0">
                  <act:name>Root Account</act:name>
                  <act:id type="guid">89c2e81567974ff087f1596101ada478</act:id>
                  <act:type>ROOT</act:type>
                </gnc:account>
                </gnc:book>
                </gnc-v2>
            """)
        )
    return path


@pytest.fixture(name='empty_book_session')
def fixture_empty_book_session(
    path_to_empty_book: Path,
) -> Iterator[Session]:
    with Session(
        book_uri=path_to_empty_book.as_uri(),
        mode=SessionOpenMode.SESSION_READ_ONLY,
    ) as session:
        yield session


@pytest.fixture(name='path_to_simple_book')
def fixture_path_to_simple_book(tmp_path: Path) -> Path:
    path = tmp_path / 'simple.gnucash'
    with open(path, encoding='utf-8', mode='w') as file:
        file.write(
            dedent("""\
                <?xml version="1.0" encoding="utf-8" ?>
                <gnc-v2
                     xmlns:gnc="http://www.gnucash.org/XML/gnc"
                     xmlns:act="http://www.gnucash.org/XML/act"
                     xmlns:book="http://www.gnucash.org/XML/book"
                     xmlns:cd="http://www.gnucash.org/XML/cd"
                     xmlns:cmdty="http://www.gnucash.org/XML/cmdty"
                     xmlns:price="http://www.gnucash.org/XML/price"
                     xmlns:slot="http://www.gnucash.org/XML/slot"
                     xmlns:split="http://www.gnucash.org/XML/split"
                     xmlns:sx="http://www.gnucash.org/XML/sx"
                     xmlns:trn="http://www.gnucash.org/XML/trn"
                     xmlns:ts="http://www.gnucash.org/XML/ts"
                     xmlns:fs="http://www.gnucash.org/XML/fs"
                     xmlns:bgt="http://www.gnucash.org/XML/bgt"
                     xmlns:recurrence="http://www.gnucash.org/XML/recurrence"
                     xmlns:lot="http://www.gnucash.org/XML/lot"
                     xmlns:addr="http://www.gnucash.org/XML/addr"
                     xmlns:billterm="http://www.gnucash.org/XML/billterm"
                     xmlns:bt-days="http://www.gnucash.org/XML/bt-days"
                     xmlns:bt-prox="http://www.gnucash.org/XML/bt-prox"
                     xmlns:cust="http://www.gnucash.org/XML/cust"
                     xmlns:employee="http://www.gnucash.org/XML/employee"
                     xmlns:entry="http://www.gnucash.org/XML/entry"
                     xmlns:invoice="http://www.gnucash.org/XML/invoice"
                     xmlns:job="http://www.gnucash.org/XML/job"
                     xmlns:order="http://www.gnucash.org/XML/order"
                     xmlns:owner="http://www.gnucash.org/XML/owner"
                     xmlns:taxtable="http://www.gnucash.org/XML/taxtable"
                     xmlns:tte="http://www.gnucash.org/XML/tte"
                     xmlns:vendor="http://www.gnucash.org/XML/vendor">
                <gnc:count-data cd:type="book">1</gnc:count-data>
                <gnc:book version="2.0.0">
                <book:id type="guid">c0609900833a4ed29a5839341593b82c</book:id>
                <book:slots>
                  <slot>
                    <slot:key>remove-color-not-set-slots</slot:key>
                    <slot:value type="string">true</slot:value>
                  </slot>
                </book:slots>
                <gnc:count-data cd:type="commodity">1</gnc:count-data>
                <gnc:count-data cd:type="account">6</gnc:count-data>
                <gnc:commodity version="2.0.0">
                  <cmdty:space>CURRENCY</cmdty:space>
                  <cmdty:id>EUR</cmdty:id>
                  <cmdty:get_quotes/>
                  <cmdty:quote_source>currency</cmdty:quote_source>
                  <cmdty:quote_tz/>
                </gnc:commodity>
                <gnc:commodity version="2.0.0">
                  <cmdty:space>template</cmdty:space>
                  <cmdty:id>template</cmdty:id>
                  <cmdty:name>template</cmdty:name>
                  <cmdty:xcode>template</cmdty:xcode>
                  <cmdty:fraction>1</cmdty:fraction>
                </gnc:commodity>
                <gnc:account version="2.0.0">
                  <act:name>Root Account</act:name>
                  <act:id type="guid">ce68be84013240cf9f355e682a6429f6</act:id>
                  <act:type>ROOT</act:type>
                </gnc:account>
                <gnc:account version="2.0.0">
                  <act:name>Assets</act:name>
                  <act:id type="guid">c9dbd3e8597347689f87d92fddc08e32</act:id>
                  <act:type>ASSET</act:type>
                  <act:commodity>
                    <cmdty:space>CURRENCY</cmdty:space>
                    <cmdty:id>EUR</cmdty:id>
                  </act:commodity>
                  <act:commodity-scu>100</act:commodity-scu>
                  <act:slots>
                    <slot>
                      <slot:key>balance-limit</slot:key>
                      <slot:value type="frame"/>
                    </slot>
                    <slot>
                      <slot:key>placeholder</slot:key>
                      <slot:value type="string">true</slot:value>
                    </slot>
                  </act:slots>
                  <act:parent type="guid">ce68be84013240cf9f355e682a6429f6</act:parent>
                </gnc:account>
                <gnc:account version="2.0.0">
                  <act:name>Capital</act:name>
                  <act:id type="guid">cafbc86f44e24e46859b318e9cfcf228</act:id>
                  <act:type>ASSET</act:type>
                  <act:commodity>
                    <cmdty:space>CURRENCY</cmdty:space>
                    <cmdty:id>EUR</cmdty:id>
                  </act:commodity>
                  <act:commodity-scu>100</act:commodity-scu>
                  <act:slots>
                    <slot>
                      <slot:key>balance-limit</slot:key>
                      <slot:value type="frame"/>
                    </slot>
                    <slot>
                      <slot:key>placeholder</slot:key>
                      <slot:value type="string">true</slot:value>
                    </slot>
                  </act:slots>
                  <act:parent type="guid">c9dbd3e8597347689f87d92fddc08e32</act:parent>
                </gnc:account>
                <gnc:account version="2.0.0">
                  <act:name>Checking account</act:name>
                  <act:id type="guid">6a33c06b1d8145149473ab1aff8fea60</act:id>
                  <act:type>ASSET</act:type>
                  <act:commodity>
                    <cmdty:space>CURRENCY</cmdty:space>
                    <cmdty:id>EUR</cmdty:id>
                  </act:commodity>
                  <act:commodity-scu>100</act:commodity-scu>
                  <act:slots>
                    <slot>
                      <slot:key>balance-limit</slot:key>
                      <slot:value type="frame"/>
                    </slot>
                    <slot>
                      <slot:key>placeholder</slot:key>
                      <slot:value type="string">true</slot:value>
                    </slot>
                  </act:slots>
                  <act:parent type="guid">cafbc86f44e24e46859b318e9cfcf228</act:parent>
                </gnc:account>
                <gnc:account version="2.0.0">
                  <act:name>Savings bank</act:name>
                  <act:id type="guid">d7426de2847644f8b41a77acc5a13e23</act:id>
                  <act:type>BANK</act:type>
                  <act:commodity>
                    <cmdty:space>CURRENCY</cmdty:space>
                    <cmdty:id>EUR</cmdty:id>
                  </act:commodity>
                  <act:commodity-scu>100</act:commodity-scu>
                  <act:slots>
                    <slot>
                      <slot:key>balance-limit</slot:key>
                      <slot:value type="frame"/>
                    </slot>
                  </act:slots>
                  <act:parent type="guid">6a33c06b1d8145149473ab1aff8fea60</act:parent>
                </gnc:account>
                <gnc:account version="2.0.0">
                  <act:name>Imbalance-EUR</act:name>
                  <act:id type="guid">0983c1cf3cee4fe7a774b1cd749ab5e7</act:id>
                  <act:type>BANK</act:type>
                  <act:commodity>
                    <cmdty:space>CURRENCY</cmdty:space>
                    <cmdty:id>EUR</cmdty:id>
                  </act:commodity>
                  <act:commodity-scu>100</act:commodity-scu>
                  <act:slots>
                    <slot>
                      <slot:key>balance-limit</slot:key>
                      <slot:value type="frame"/>
                    </slot>
                  </act:slots>
                  <act:parent type="guid">ce68be84013240cf9f355e682a6429f6</act:parent>
                </gnc:account>
                </gnc:book>
                </gnc-v2>
            """)
        )
    return path


@pytest.fixture(name='simple_book_session')
def fixture_simple_book_session(
    path_to_simple_book: Path,
) -> Iterator[Session]:
    with Session(
        book_uri=path_to_simple_book.as_uri(),
        mode=SessionOpenMode.SESSION_READ_ONLY,
    ) as session:
        yield session


def test_account_not_found(empty_book_session: Session) -> None:
    with pytest.raises(
        RuntimeError,
        match='Account not found: Assets.Capital.Checking account.Savings bank',
    ):
        next(
            incomplete_xacts(
                base='Assets.Capital.Checking account.Savings bank',
                imbalance='Imbalance-EUR',
                session=empty_book_session,
            )
        )


def test_no_incomplete_xacts(
    simple_book_session: Session,
) -> None:
    assert not list(
        incomplete_xacts(
            base='Assets.Capital.Checking account.Savings bank',
            imbalance='Imbalance-EUR',
            session=simple_book_session,
        )
    )
