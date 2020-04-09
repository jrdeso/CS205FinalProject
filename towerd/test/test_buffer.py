import unittest

from ..network.buffer import SequenceBuffer


class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.max_length = 32
        self.seq_buffer = SequenceBuffer(self.max_length)

        self.man_idx = 10
        self.man_val = 12
        self.seq_buffer.buf[self.man_idx] = self.man_val

    def test_setter_getter(self):
        i = 38
        val = 23

        self.seq_buffer[i] = val
        self.assertEqual(self.seq_buffer[i], val)

    def test_len(self):
        self.assertEqual(self.max_length, len(self.seq_buffer))

    def test_contains(self):
        self.assertTrue(0 in self.seq_buffer)
        self.assertFalse(32 in self.seq_buffer)

    def test_index(self):
        self.assertEqual(self.man_idx, self.seq_buffer.index(self.man_val))
