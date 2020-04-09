import abc
import dataclasses
import enum
import struct


def generate_ack_bits(packet_buf, seq):
    ack = len(packet_buf) - 1
    ack_bits = 0
    for i in range(ack):
        if not packet_buf[i].acked:
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

    def __init__(self):
        self.seq = Packet.__COUNT
        Packet.__COUNT = Packet.__COUNT + 1

    def size(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


@dataclasses.dataclass
class AckPacket(Packet):
    """
    Data for reliable data transfer of sending sliced data.

    Attributes
    ----------
    ack
        the id that the client has received
    n_slices
        the number of slices
    ack_bits
        the marked slices received

    Notes
    -----
    Due to implementation of ack_bits, max amount of data is 32kib.
    """
    STATIC_SIZE = 10

    ack: int
    n_slices: int
    ack_bits: int = 0

    def size(self):
        return AckPacket.STATIC_SIZE

    def serialize(self):
        return struct.pack('HHHI', self.size(), self.seq, self.ack, self.ack_bits)


@dataclasses.dataclass
class DataPacket(Packet):
    """
    Data for reliable data transfer of sending sliced data.

    Attributes
    ----------
    slice_id
        the slice id that is being sent
    slide_bytes
        the size of this packet and data
    data
        serialized data to be sent over the network
    """
    STATIC_SIZE = 4

    slice_id: int
    data: str

    def size(self):
        return DataPacket.STATIC_SIZE + len(self.data)

    def serialize(self):
        return struct.pack('HHs', self.size(), self.seq, self.data)


class PacketType(enum.Enum):
    DATA = 0
    ACK = 1


class PacketFactory:
    def __init__(self, max_packet_size):
        self.max_packet_size = max_packet_size

    def create_packet(self, packet_type, *args, **kwargs):
        if packet_type == 0:
            dp = DataPacket(*args, **kwargs)
            if DataPacket.STATIC_SIZE + len(dp.data) >= self.max_packet_size:
                max_data_size = self.max_packet_size - DataPacket.STATIC_SIZE
                raise ValueError(f'Payload too large: len(load) > {max_data_size}')
            return dp
        elif packet_type == 1:
            return AckPacket(*args, **kwargs)
