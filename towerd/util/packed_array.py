class PackedArray:
    def __init__(self, max_length=None):
        arr = list((None,) * max_length) if max_length else []
        self.arr = arr
        self.max_length = max_length
        self.size = 0

    def __len__(self):
        return self.size

    def __getitem__(self, val):
        if isinstance(val, slice):
            start, stop, step = val.start, val.stop, val.step
            if stop is None or stop > self.size:
                stop = self.size
            return self.arr[start:stop:step]
        return self.arr[val]

    def __setitem__(self, idx, val):
        if idx >= self.size:
            raise IndexError('Index must be less than size of array.')
        self.arr[idx] = val

    def __contains__(self, val):
        return val in self.arr[:self.size]

    def __iter__(self):
        return iter(self.arr[:self.size])

    def append(self, object):
        if self.size >= self.max_length:
            raise IndexError('Array is full.')
        self.arr[self.size] = object
        self.size += 1

    def remove(self, idx):
        if idx >= self.size:
            raise IndexError('Index must be less than size of array.')
        self.arr[idx] = self.arr[self.size - 1]
        self.size -= 1


class MappedPackedArray(PackedArray):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map2idx = {}
        self.idx2map = {k: None for k in range(self.max_length)}

    def __getitem__(self, key):
        idx = self.map2idx[key]
        return self.arr[idx]

    def __setitem__(self, key, val):
        idx = self.map2idx[key]
        self.arr[idx] = val

    def __contains__(self, key):
        return key in self.map2idx

    def append(self, object, key=None):
        super().append(object)
        if key is None:
            key = object
        self.map2idx[key] = self.size - 1
        self.idx2map[self.size - 1] = key

    def remove(self, idx):
        super().remove(idx)
        removed_key = self.idx2map[idx]

        # don't decrement self.size since self.size was decremented in parent
        self.idx2map[idx] = self.idx2map[self.size]
        key = self.idx2map[idx]
        self.map2idx[key] = idx

        self.idx2map[self.size] = None
        del self.map2idx[removed_key]

    def remove_key(self, key):
        idx = self.map2idx[key]
        self.remove(idx)
