import abc
import dataclasses
import enum
import struct


class PacketType(enum.IntEnum):
    ACK = enum.auto()
    ACK_CHUNK = enum.auto()
    CHUNK = enum.auto()
    DATA = enum.auto()


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
    STATIC_SIZE = 7
    SERIALIZE_FORMAT = '<HHHB'

    def __init__(self, packet_type):
        self.seq = Packet.__COUNT
        self.type = packet_type
        Packet.__COUNT = Packet.__COUNT + 1

    def size(self):
        raise NotImplementedError

    def serialize(self, auth_code):
        return struct.pack(Packet.SERIALIZE_FORMAT, self.size(), auth_code, self.seq, self.type)


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
    STATIC_SIZE = Packet.STATIC_SIZE + 6
    SERIALIZE_FORMAT = '<HI'

    ack: int = 0
    ack_bits: int = 0

    def __post_init__(self):
        super().__init__(PacketType.ACK)

    def size(self):
        return AckPacket.STATIC_SIZE

    def serialize(self, auth_code):
        parent_serial = super().serialize(auth_code)
        return parent_serial + struct.pack(AckPacket.SERIALIZE_FORMAT, self.ack, self.ack_bits)


@dataclasses.dataclass
class DataPacket(Packet):
    """
    Data for reliable data transfer of sending data.

    Attributes
    ----------
    data
        data to be sent
    """
    STATIC_SIZE = Packet.STATIC_SIZE
    SERIALIZE_FORMAT = '{:d}s'

    data: str = ''

    def __post_init__(self):
        super().__init__(PacketType.DATA)

    def size(self):
        return DataPacket.STATIC_SIZE

    def serialize(self, auth_code):
        parent_serial = super().serialize(auth_code)
        fmt_str = DataPacket.SERIALIZE_FORMAT.format(len(self.data))
        return parent_serial + struct.pack(fmt_str, self.data)


@dataclasses.dataclass
class AckChunkPacket(AckPacket):
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
    STATIC_SIZE = AckPacket.STATIC_SIZE + 6
    SERIALIZE_FORMAT = '<HHH'

    ack_chunk: int = 0
    ack_slice: int = 0
    n_slices: int = 0

    def __post_init__(self):
        super(AckPacket, self).__init__(PacketType.ACK_CHUNK)

    def size(self):
        return AckChunkPacket.STATIC_SIZE

    def serialize(self, auth_code):
        parent_serial = super().serialize(auth_code)
        return parent_serial + struct.pack(AckChunkPacket.SERIALIZE_FORMAT, self.ack_chunk, self.ack_slice, self.n_slices)


@dataclasses.dataclass
class ChunkPacket(Packet):
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
    STATIC_SIZE = Packet.STATIC_SIZE + 6
    SERIALIZE_FORMAT = '<HHH{:d}s'

    chunk_id: int = 0
    slice_id: int = 0
    n_slices: int = 0
    data: str = ''

    def __post_init__(self):
        super().__init__(PacketType.CHUNK)

    def size(self):
        return ChunkPacket.STATIC_SIZE + len(self.data)

    def serialize(self, auth_code):
        parent_serial = super().serialize(auth_code)
        encoded_data = self.data.encode('ascii')
        fmt_str = ChunkPacket.SERIALIZE_FORMAT.format(len(encoded_data))
        return parent_serial + struct.pack(fmt_str, self.chunk_id, self.slice_id, self.n_slices, encoded_data)
