import unittest

from ..util.packed_array import PackedArray, MappedPackedArray


class TestPackedArray(unittest.TestCase):
    def setUp(self):
        self.pa = PackedArray(max_length=5)

    def test_access(self):
        n_elems = 3
        for i in range(n_elems):
            self.pa.append(i)

        expected = list(range(n_elems))
        self.assertSequenceEqual(expected, self.pa[:n_elems])

        self.pa.remove(n_elems // 2)
        expected.pop(n_elems // 2)

        self.assertSequenceEqual(expected, self.pa[:])


class TestMappedPackedArray(unittest.TestCase):
    def setUp(self):
        self.pa = MappedPackedArray(max_length=5)

    def test_access(self):
        n_elems = 3
        keys = [f'T{i}' for i in range(n_elems)]
        for key, i in zip(keys, range(n_elems)):
            self.pa.append(i, key=key)

        expected = list(range(n_elems))
        self.assertEqual(expected[1], self.pa[keys[1]])

        key = self.pa.idx2map[1]
        self.assertEqual(self.pa.map2idx[key], 1)

        self.pa.remove(1)
        expected.pop(1)
        self.assertEqual(self.pa['T2'], 2)
        self.assertSequenceEqual(expected, self.pa.arr[:self.pa.size])

        self.pa.remove_key('T2')
        expected.pop(1)
        self.assertSequenceEqual(expected, self.pa.arr[:self.pa.size])
