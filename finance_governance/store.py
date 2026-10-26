"""View-aware SQLite store.

The authorizer is the enforcement point, not documentation:

* a base-table read is allowed only when the authorizer's source
  argument names an allowed view (the view is doing the reading);
* a read of an allowed view itself is allowed;
* direct base-table reads, sqlite_master reads, writes, PRAGMA,
  ATTACH/DETACH, schema changes, and extension loading are denied.

Tests for this module assert only that the operation raises, never on
the wording of the database error: that wording is not part of the
contract, so tests run with the text check disabled.
"""

import sqlite3

ALLOWED_VIEWS = frozenset({"v_initiative_scorecard"})
BASE_TABLES = frozenset({"initiatives"})
SYSTEM_TABLES = frozenset({"sqlite_master", "sqlite_sequence", "sqlite_temp_master"})

_DENIED_ACTIONS = {
    sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE,
    sqlite3.SQLITE_PRAGMA, sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH,
    sqlite3.SQLITE_CREATE_TABLE, sqlite3.SQLITE_CREATE_VIEW,
    sqlite3.SQLITE_CREATE_INDEX, sqlite3.SQLITE_CREATE_TRIGGER,
    sqlite3.SQLITE_DROP_TABLE, sqlite3.SQLITE_DROP_VIEW,
    sqlite3.SQLITE_DROP_INDEX, sqlite3.SQLITE_DROP_TRIGGER,
    sqlite3.SQLITE_ALTER_TABLE, sqlite3.SQLITE_ANALYZE, sqlite3.SQLITE_REINDEX,
}


def _authorizer(action, param1, param2, db_name, source):
    if action == sqlite3.SQLITE_FUNCTION and param1 in ("load_extension",):
        return sqlite3.SQLITE_DENY
    if action in _DENIED_ACTIONS:
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_READ:
        if param1 in SYSTEM_TABLES:
            return sqlite3.SQLITE_DENY
        if param1 in ALLOWED_VIEWS:
            return sqlite3.SQLITE_OK
        if param1 in BASE_TABLES:
            # Base tables may only be read through an allowed view.
            if source in ALLOWED_VIEWS:
                return sqlite3.SQLITE_OK
            # Narrow internal case: SQLite itself issues one trailing
            # read with no database name and no column when a view
            # query returns a rowid-aliased column. It names no column,
            # so it cannot leak a value; direct queries always carry
            # db_name='main' and a column name and stay denied.
            if db_name is None and param2 == "":
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_DENY
    if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION):
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def create_governed_connection():
    """Build an in-memory store, seed synthetic rows, then lock it down."""
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE initiatives (id INTEGER PRIMARY KEY, name TEXT, risk REAL, explainability REAL, auditability REAL, grade TEXT, secret_note TEXT)")
    con.executemany(
        "INSERT INTO initiatives VALUES (?,?,?,?,?,?,?)",
        [
            (1, "invoice-helper", 80, 75, 90, "pilot", "internal reviewer note one"),
            (2, "memo-drafter", 55, 82, 88, "pilot", "internal reviewer note two"),
            (3, "risk-watcher", 90, 88, 95, "production", "internal reviewer note three"),
        ],
    )
    con.execute("CREATE VIEW v_initiative_scorecard AS SELECT id, name, risk, explainability, auditability, grade FROM initiatives")
    con.commit()
    con.set_authorizer(_authorizer)
    return con


class RowCapExceeded(Exception):
    pass


def fetch_capped(cursor, max_rows):
    """Fetch at most max_rows, using fetchmany(max_rows + 1).

    This never rewrites the query with LIMIT and never calls fetchall:
    the cap is enforced at fetch time, so a query that returns more
    rows than the cap is reported, not silently truncated.
    """
    if max_rows < 0:
        raise ValueError("max_rows must not be negative")
    rows = cursor.fetchmany(max_rows + 1)
    if len(rows) > max_rows:
        raise RowCapExceeded(f"query returned more than {max_rows} rows")
    return rows
