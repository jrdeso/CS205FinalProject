import time
import unittest

from ..network.comm import ChunkSendManager, ChunkReceiveManager
from ..network.packet_factory import PacketFactory, PacketType


class TestComm(unittest.TestCase):
    def setUp(self):
        max_slice_size = 2
        max_slice_per_chunk = 3
        self.pf = PacketFactory(1024)
        self.csm = ChunkSendManager(
            "The red fox jumped.", max_slice_size, max_slice_per_chunk, min_delay=0
        )
        self.crm = ChunkReceiveManager(max_slice_size, max_slice_per_chunk)

    def test_get_slice(self):
        data1 = self.csm.get_slice(0)
        data2 = self.csm.get_slice(2)

        self.assertEqual(data1.data, "Th")
        self.assertEqual(data2.data, "re")

        self.csm.chunk_id = 3
        self.csm.prep_chunk()

        data3 = self.csm.get_slice(0)
        self.assertEqual(data3.data, ".")

    def test_sender_receive(self):
        ap = self.pf.create_packet(PacketType.ACK)
        ap.ack = 1
        ap.n_slices = 1
        ap.ack_bits = expected_ack = 1 << 2

        self.csm.receive(ap)
        self.assertEqual(self.csm.acked, expected_ack)
        self.assertEqual(self.csm.n_acked, 1)

    def test_receiver_receive(self):
        data = "Hello World!"
        dp1 = self.pf.create_packet(
            PacketType.CHUNK, chunk_id=0, slice_id=0, n_slices=1, data=data
        )
        self.crm.receive(dp1)

        self.assertTrue(self.crm.ready)
        self.assertEqual(self.crm.received, 1)
        self.assertEqual(self.crm.n_received, 1)
        self.assertEqual(self.crm.data[0], data)

        self.crm.retrieve_data()

        self.assertEqual(self.crm.chunk_id, 1)

    def test_chunk_manager(self):
        start = time.time()
        data = ""
        while not self.crm.done:
            while not self.crm.ready:
                dp = next(self.csm)
                if dp is not None:
                    self.csm.mark_sent(dp.slice_id)
                    ap = self.crm.receive(dp)
                    if ap is not None:
                        self.csm.receive(ap)
                if time.time() - start > 0.1:
                    raise Exception("Timeout: took longer than 100 ms")
            data += self.crm.retrieve_data()
        self.assertEqual(self.csm.data, data)
