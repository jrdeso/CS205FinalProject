import unittest

from ..network.buffer import SequenceBuffer, SequenceData
from ..network.packet_factory import PacketFactory, PacketType
from ..network.packet import AckPacket, AckChunkPacket, ChunkPacket, generate_ack_bits


class TestPacket(unittest.TestCase):
    def setUp(self):
        self.pf = PacketFactory(1024)

    def test_data_packet(self):
        slice_id = 65535
        data = 'Hello World!'
        packet_length = len(data) + ChunkPacket.STATIC_SIZE

        dp = self.pf.create_packet(PacketType.CHUNK, chunk_id=0, slice_id=slice_id, n_slices=1, data=data)

        self.assertEqual(dp.size(), packet_length)
        self.assertEqual(len(dp.serialize()), packet_length)

    def test_ack_packet(self):
        ack = 65535
        ack_chunk = 65535
        ack_slice = 65535
        n_slices = 65535

        max_length = 32
        seq_buffer = SequenceBuffer(max_length)

        expected_ack_bits = 0
        for i in range(max_length):
            acked = i % 2 == 0
            seq_buffer[i] = SequenceData(seq=i, acked=acked)
            if acked:
                expected_ack_bits |= 1 << (max_length - 1 - i)

        ack_bits = generate_ack_bits(seq_buffer, max_length - 1)
        self.assertEqual(ack_bits, expected_ack_bits)

        ap = self.pf.create_packet(PacketType.ACK_CHUNK, ack=ack, ack_chunk=ack_chunk, ack_slice=ack_slice, n_slices=n_slices, ack_bits=ack_bits)

        self.assertEqual(AckChunkPacket.STATIC_SIZE, ap.size())
        self.assertEqual(ap.size(), len(ap.serialize()))
