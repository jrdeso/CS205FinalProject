import enum

from towerd.network.packet import DataPacket, AckPacket, AckDataPacket


class PacketType(enum.Enum):
    ACK = enum.auto()
    ACKDATA = enum.auto()
    DATA = enum.auto()


class PacketFactory:
    def __init__(self, max_packet_size):
        self.max_packet_size = max_packet_size

    def create_packet(self, packet_type, *args, **kwargs):
        if packet_type == PacketType.DATA:
            dp = DataPacket(*args, **kwargs)
            if DataPacket.STATIC_SIZE + len(dp.data) >= self.max_packet_size:
                max_data_size = self.max_packet_size - DataPacket.STATIC_SIZE
                raise ValueError(f'Payload too large: len(load) > {max_data_size}')
            return dp
        elif packet_type == PacketType.ACK:
            return AckPacket(*args, **kwargs)
        elif packet_type == PacketType.ACKDATA:
            return AckDataPacket(*args, **kwargs)
