import abc
import dataclasses
import struct


def generate_ack_bits(seq_buf, ack):
    """
    Construct a bitset indicating whether or not a packet was acked.

    Attributes
    ----------
    seq_buf : towerd.network.buffer.SequenceBuffer
        a buffer of sequence data
    ack : int
        the sequence id of the packet to be acked
    """
    ack_bits = 0
    for i in range(32):
        seq = ack - i
        if seq_buf[seq].seq == seq and seq_buf[seq].acked:
            ack_bits |= 1 << i
    return ack_bits


class Packet(abc.ABC):
    """
    Base Packet.

    Attributes
    ----------
    seq
        the unique id for this packet
    """
    __COUNT = 0
    STATIC_SIZE = 2

    def __init__(self):
        self.seq = Packet.__COUNT
        Packet.__COUNT = Packet.__COUNT + 1

    def size(self):
        raise NotImplementedError

    def serialize(self):
        return struct.pack('<HH', self.size(), self.seq)


@dataclasses.dataclass
class AckPacket(Packet):
    """
    Data for reliable data transfer of sending sliced data.

    Attributes
    ----------
    ack
        the id that the client has received
    ack_bits
        the marked packets received

    Notes
    -----
    Due to implementation of ack_bits, max amount of data is 32kib.
    """
    STATIC_SIZE = super().STATIC_SIZE + 4

    ack: int = 0
    ack_bits: int = 0

    def __post_init__(self):
        super().__init__()

    def size(self):
        return AckPacket.STATIC_SIZE

    def serialize(self):
        return super().serialize() + struct.pack('<HI', self.ack, self.ack_bits)


@dataclasses.dataclass
class AckDataPacket(AckPacket):
    """
    Data for reliable data transfer of sending sliced data.

    Attributes
    ----------
    ack
        the id that the client has received
    n_slices
        the number of slices received
    ack_bits
        the marked slices received

    Notes
    -----
    Due to implementation of ack_bits, max amount of data is 32kib.
    """
    STATIC_SIZE = super().STATIC_SIZE + 6

    ack_chunk: int = 0
    ack_slice: int = 0
    n_slices: int = 0

    def __post_init__(self):
        super().__init__()

    def size(self):
        return AckPacket.STATIC_SIZE

    def serialize(self):
        return struct.pack('<HHH', self.ack_chunk, self.ack_slice, self.n_slices)


@dataclasses.dataclass
class DataPacket(Packet):
    """
    Data for reliable data transfer of sending sliced data.

    Attributes
    ----------
    chunk_id
        the chunk id
    slice_id
        the slice id that is being sent
    n_slices
        the total number of slices
    data
        serialized data to be sent over the network
    """
    STATIC_SIZE = 6

    chunk_id: int = 0
    slice_id: int = 0
    n_slices: int = 0
    data: str = ''

    def __post_init__(self):
        super().__init__()

    def size(self):
        return DataPacket.STATIC_SIZE + len(self.data)

    def serialize(self):
        return super().serialize() + struct.pack('<HHH', self.chunk_id, self.slice_id, self.n_slices) + self.data.encode('ascii')
