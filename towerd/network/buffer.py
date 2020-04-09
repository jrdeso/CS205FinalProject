import dataclasses


@dataclasses.dataclass
class SequenceData:
    seq: int = 0
    time: float = 0
    acked: bool = False


class SequenceBuffer:
    def __init__(self, max_length):
        self.buf = list((0,) * max_length)
        self.dat = list((None,) * max_length)
        self.max_length = max_length

        self.index = self.buf.index

    def __getitem__(self, seq):
        i = seq % self.max_length
        return self.dat[i] if self.buf[i] == seq else None

    def __setitem__(self, seq, val):
        i = seq % self.max_length
        self.buf[i] = seq
        self.dat[i] = val

    def __len__(self):
        return self.max_length

    def __contains__(self, item):
        return item in self.buf

    def __iter__(self):
        return iter(self.buf)
