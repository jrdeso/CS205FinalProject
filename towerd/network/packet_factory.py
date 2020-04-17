import enum

from towerd.network.packet import ChunkPacket, AckPacket, AckChunkPacket


class PacketType(enum.Enum):
    ACK = enum.auto()
    ACK_CHUNK = enum.auto()
    CHUNK = enum.auto()


class PacketFactory:
    def __init__(self, max_packet_size):
        self.max_packet_size = max_packet_size

    def create_packet(self, packet_type, *args, **kwargs):
        if packet_type == PacketType.CHUNK:
            dp = ChunkPacket(*args, **kwargs)
            if ChunkPacket.STATIC_SIZE + len(dp.data) >= self.max_packet_size:
                max_data_size = self.max_packet_size - ChunkPacket.STATIC_SIZE
                raise ValueError(f'Payload too large: len(load) > {max_data_size}')
            return dp
        elif packet_type == PacketType.ACK:
            return AckPacket(*args, **kwargs)
        elif packet_type == PacketType.ACK_CHUNK:
            return AckChunkPacket(*args, **kwargs)
