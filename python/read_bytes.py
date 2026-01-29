def read_to_crnlcrnl(stream: BinaryIO) -> tuple[bytes, bytes]:
    search_start = 0
    chunks = []
    while chunk := stream.buffer.read(8 * 1024):
        last_two = (chunks or [''])[-1] + chunk
        before, _, after = last_two.partition(b"\r\n\r\n")
        if after:
            return ''.join(chunks and chunks[:-1]) + before, after

    raise ValueError
