import hashlib


def create_file_hash(f):
    with open(f, "rb", buffering=0) as fp:
        return hashlib.file_digest(fp, "sha256").hexdigest()[:32]
