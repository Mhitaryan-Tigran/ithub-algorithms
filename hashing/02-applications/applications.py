import hashlib
import hmac
import os
import subprocess
import tempfile
from pathlib import Path


def file_checksum(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_password(password, salt=None):
    salt = salt or os.urandom(16)
    return salt, hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def check_password(password, salt, stored):
    return hmac.compare_digest(hash_password(password, salt)[1], stored)


def sign(secret, body):
    return hmac.new(secret, body, hashlib.sha256).hexdigest()


def git_blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def find_duplicate_files(paths):
    groups = {}
    for path in paths:
        groups.setdefault(file_checksum(path), []).append(path.name)
    return [names for names in groups.values() if len(names) > 1]


def shard(key, shards):
    return int.from_bytes(hashlib.md5(key.encode()).digest()[:8], "big") % shards


class BloomFilter:
    def __init__(self, bits=1024, hashes=4):
        self.bits = bytearray(bits)
        self.hashes = hashes

    def _positions(self, item):
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[4 * i:4 * i + 4], "big") % len(self.bits) for i in range(self.hashes)]

    def add(self, item):
        for p in self._positions(item):
            self.bits[p] = 1

    def might_contain(self, item):
        return all(self.bits[p] for p in self._positions(item))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "report.txt").write_text("quarterly report\n")
        (tmp / "copy.txt").write_text("quarterly report\n")
        (tmp / "other.txt").write_text("something else\n")
        print("1. Integrity of a download, SHA-256 of report.txt:", file_checksum(tmp / "report.txt"))
        before = file_checksum(tmp / "report.txt")
        (tmp / "report.txt").write_text("quarterly report!\n")
        print("   one character changed -> checksum differs:", before != file_checksum(tmp / "report.txt"))
        (tmp / "report.txt").write_text("quarterly report\n")
        duplicates = find_duplicate_files(sorted(tmp.iterdir()))
        print("2. Duplicate files found by content hash:", duplicates)

        data = b"hello hashing\n"
        (tmp / "blob.txt").write_bytes(data)
        ours = git_blob_id(data)
        theirs = subprocess.run(["git", "hash-object", str(tmp / "blob.txt")], capture_output=True, text=True).stdout.strip()
        print("3. Git stores files by hash, our id:", ours, "git hash-object:", theirs)

    salt, stored = hash_password("correct horse battery staple")
    print("4. Password stored as salt + scrypt hash:", salt.hex()[:16] + "...", stored.hex()[:16] + "...")
    print("   right password:", check_password("correct horse battery staple", salt, stored), "wrong password:", check_password("123456", salt, stored))

    secret, body = b"webhook-secret", b'{"order": 42, "paid": true}'
    signature = sign(secret, body)
    print("5. HMAC signature of a webhook:", signature[:32] + "...")
    print("   body untouched:", hmac.compare_digest(signature, sign(secret, body)), "body forged:", hmac.compare_digest(signature, sign(secret, body.replace(b"true", b"false"))))

    users = ["anna", "boris", "vera", "gleb", "dina", "egor"]
    print("6. Sharding users over 3 database servers:", {u: shard(u, 3) for u in users})

    seen = BloomFilter()
    for url in ["https://ithub.ru", "https://newlxp.ru", "https://github.com"]:
        seen.add(url)
    print("7. Bloom filter of visited pages: newlxp.ru", seen.might_contain("https://newlxp.ru"), "example.org", seen.might_contain("https://example.org"))

    table = {}
    table["ИСП9-Х36"] = 25
    print("8. Python dict is a hash table:", table, "hash of a string is deterministic within a run:", hash("ИСП9-Х36") == hash("ИСП9-Х36"))

    assert duplicates == [["copy.txt", "report.txt"]]
    assert ours == theirs
    assert check_password("correct horse battery staple", salt, stored) and not check_password("123456", salt, stored)
    assert shard("anna", 3) == shard("anna", 3)
    assert seen.might_contain("https://ithub.ru")
    print("checks passed")
