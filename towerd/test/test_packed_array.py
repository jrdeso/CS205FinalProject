import unittest

from ..util.PackedArray import PackedArray, MappedPackedArray, MappedPackedOverflowArray


class TestPackedArray(unittest.TestCase):
    def setUp(self):
        self.pa = PackedArray(maxLength=5)

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
        self.pa = MappedPackedArray(maxLength=5)

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

        self.pa.removeKey('T2')
        expected.pop(1)
        self.assertSequenceEqual(expected, self.pa.arr[:self.pa.size])


class TestMappedPackedOverflowArray(unittest.TestCase):
    def setUp(self):
        self.pa = MappedPackedOverflowArray(maxLength=5)

    def test_access(self):
        n_elems = 9
        keys = [f'T{i}' for i in range(n_elems)]
        for key, i in zip(keys, range(n_elems)):
            self.pa.append(i, key=key)

        expected = [5, 6, 7, 8, 4]
        expected_keys = [f'T{i}' for i in expected]
        self.assertEqual(expected[1], self.pa[expected_keys[1]])
        self.assertSequenceEqual(expected, self.pa.arr)

        key = self.pa.idx2map[1]
        self.assertEqual(self.pa.map2idx[key], 1)

        self.pa.remove(1)
        expected = [5, 4, 7, 8]
        self.assertEqual(self.pa['T7'], 7)
        self.assertSequenceEqual(expected, self.pa.arr[:self.pa.size])

        self.pa.removeKey('T7')
        expected = [5, 4, 8]
        self.assertEqual(self.pa.idx, 3)
        self.assertSequenceEqual(expected, self.pa.arr[:self.pa.size])
