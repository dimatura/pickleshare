from __future__ import print_function
import os

from jsonshare import JsonShareDB


def test_jsonshare(tmpdir):
    db = JsonShareDB(tmpdir)
    db.clear()
    print("Should be empty:", db.items())
    assert len(db) == 0
    db["hello"] = 15
    assert db["hello"] == 15
    db["aku ankka"] = [1, 2, 313]
    assert db["aku ankka"] == [1, 2, 313]
    db["paths/nest/ok/keyname"] = [1, [5, 46]]
    assert db["paths/nest/ok/keyname"] == [1, [5, 46]]

    db.hset("hash", "aku", 12)
    db.hset("hash", "ankka", 313)
    assert db.hget("hash", "aku") == 12
    assert db.hget("hash", "ankka") == 313

    print("all hashed", db.hdict("hash"))
    print(db.keys())
    print(db.keys("paths/nest/ok/k*"))
    print(dict(db))  # snapsot of whole db
    db.uncache()  # frees memory, causes re-reads later

    # shorthand for accessing deeply nested files
    lnk = db.getlink("myobjects/test")
    lnk.foo = 2
    lnk.bar = lnk.foo + 5
    assert lnk.bar == 7


def test_stress(tmpdir):
    db = JsonShareDB(tmpdir)
    import time, sys

    for i in range(100):
        for j in range(500):
            if i % 15 == 0 and i < 70:
                if str(j) in db:
                    del db[str(j)]
                continue

            if j % 33 == 0:
                time.sleep(0.02)

            db[str(j)] = db.get(str(j), []) + [(i, j, "proc %d" % os.getpid())]
            db.hset("hash", str(j), db.hget("hash", j, 15) + 1)

        print(i, end=" ")
        sys.stdout.flush()
        if i % 10 == 0:
            db.uncache()


if __name__ == "__main__":
    #test_jsonshare('tmpdb')
    test_stress('tmpdb')
