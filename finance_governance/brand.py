"""Brand check: blocklist stored as hashes, never as plain names.

is_blocked_hash() lets tests prove the mechanism works using a digest
taken from the set itself, without any plain blocked name appearing in
this repo. A non-empty set is itself asserted in tests: an empty
blocklist would check nothing.
"""

import hashlib

# SHA-256 digests (lowercased names) of names that must not appear as
# clients, partners, or affiliations in this repo. Digests only.
BLOCKLIST_HASHES = frozenset({
    "c952a08fdb0ff916b78a489ff321a4eb73d258612ededdd834c5a7c55fbc6c70",
    "17e9b17189f2f67e00b4c8dce8a6bedb38051ee221602fd52c88650ef9f68687",
    "fd3323cb0659a996fea1945f6a61764e604ab93ff6f27d39f4be71cdd113e18c",
    "30ec2ecf6bb730f8770c417133bc8b35d14543cfa31a85a8a1f487089c7eadfa",
})


def is_blocked_hash(digest):
    return digest in BLOCKLIST_HASHES


def digest_of(name):
    return hashlib.sha256(name.strip().lower().encode("utf-8")).hexdigest()
