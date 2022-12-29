from hashlib import blake2s
import io
import os

# You can choose others
OFFSETS = list(3 + 7 ** i for i in range(20))
ENDINGS = 16


def hash_file(filename: str) -> str:
    hasher = blake2s()
    file_size = os.path.getsize(filename)

    with open(filename, 'rb') as fp:
        hasher.update(fp.read(ENDINGS))

        fp.seek(-ENDINGS, io.SEEK_END)
        hasher.update(fp.read(ENDINGS))

        for offset in OFFSETS:
            if offset < file_size:
                fp.seek(offset)
                hasher.update(fp.read(10))

    return hasher.hexdigest()
