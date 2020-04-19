import time

from towerd.network.packet_factory import PacketFactory, PacketType

_PF = PacketFactory(1024)


class ChunkSendManager:
    """
    Manager for sending chunks of data. When out of data to send, the manager
    uses a null terminator.

    :var data: data to send
    :var max_slice_size: maximum amount of data in a slice of data
    :var max_slice_per_chunk: maximum amount of slices in a chunk
    :var min_delay: minimum delay before resending a packet
    :var max_chunk_size: maximum amount of data in a chunk
    :var max_chunks: maximum amount of chunks

    :var chunk_id: the current chunk of data to send
    :var slice_id: the current slice of chunk to send
    :var acked: a bitset representing the slices that were acked
    :var n_acked: the number of acked slices
    :var last_sent: a list of times that the slices were last sent
    """
    def __init__(self, data, max_slice_size, max_slice_per_chunk, min_delay=100):
        self.data = data
        self.done = False
        self.max_slice_size = max_slice_size
        self.max_slice_per_chunk = max_slice_per_chunk
        self.min_delay = min_delay

        # determine number of chunks; math.ceil but more efficient and accurate
        self.max_chunks = -(-len(self.data) // (max_slice_per_chunk * max_slice_size))
        self.max_chunk_size = self.max_slice_per_chunk * self.max_slice_size

        self.chunk_id = 0
        self.prep_chunk()

    def __iter__(self):
        return self

    def __next__(self):
        if self.n_acked == self.n_slices:
            return None

        # find the next slice of data to send
        data = None
        for i in range(self.max_slice_per_chunk):
            slice_id = (self.slice_id + i) % self.max_slice_per_chunk

            ack_bits = 1 << slice_id
            if self.acked & ack_bits:
                continue

            time_idle = time.time() - self.last_sent[slice_id]
            if time_idle >= self.min_delay:
                data = self.get_slice(slice_id)
                break

        self.slice_id = (self.slice_id + 1) % self.n_slices
        return data

    def update_last_sent(self, slice_id):
        """
        Update the time the slice was last sent.

        :param slice_id: the slice to update its time last sent
        """
        self.last_sent[slice_id] = time.time()

    def prep_chunk(self):
        """
        Prepare the manager for sending a chunk based on the current chunk id.
        """
        self.slice_id = 0
        self.acked = 0
        self.n_acked = 0
        self.last_sent = list((0,) * self.max_slice_per_chunk)

        chunk_start = self.chunk_id * self.max_chunk_size
        chunk_end = chunk_start + self.max_chunk_size
        self.chunk_data = self.data[chunk_start:chunk_end]
        if self.chunk_data == "":
            self.chunk_data = "\0"
            self.done = True
        self.n_slices = max(1, len(self.chunk_data) // self.max_slice_size)

    def get_slice(self, slice_id):
        """
        Gets the slice of data within the chunk to send.

        :param slice_id: the slice to send
        """
        slice_start = slice_id * self.max_slice_size
        slice_end = slice_start + self.max_slice_size

        dp = _PF.create_packet(PacketType.CHUNK)
        dp.chunk_id = self.chunk_id
        dp.slice_id = self.slice_id
        dp.n_slices = self.n_slices
        dp.data = self.chunk_data[slice_start:slice_end]

        return dp

    def receive(self, ack_packet):
        """
        Reads the AckChunkPacket to update the data that should be sent when
        iterating.

        :param ack_packet: an instance of AckChunkPacket
        """
        if not self.acked & ack_packet.ack_bits:
            self.n_acked += 1
        self.acked |= ack_packet.ack_bits

        if ack_packet.n_slices == self.n_slices and self.chunk_id != self.max_chunks:
            self.chunk_id += 1
            self.prep_chunk()


class ChunkReceiveManager:
    """
    Manager for receiving chunks of data.

    :var max_slice_size: maximum amount of data in a slice of data
    :var max_slice_per_chunk: maximum amount of slices in a chunk
    :var done: whether all chunks have been received
    :var ready: whether all slices have been received from the current chunk

    :var chunk_id: whether all chunks have been received
    :var received: a bitset representing the slices that were received
    :var n_received: the number of slices received
    :var data: the data received from the chunk so far
    """
    def __init__(self, max_slice_size, max_slice_per_chunk):
        self.done = False
        self.max_slice_size = max_slice_size
        self.max_slice_per_chunk = max_slice_per_chunk

        self.chunk_id = 0
        self.prep_chunk()

    def prep_chunk(self):
        """
        Prepare the manager for receiving a chunk based on the current chunk id.
        """
        self.ready = False
        self.received = 0
        self.n_received = 0
        self.data = list((0,) * self.max_slice_per_chunk)

    def retrieve_data(self, prep_next_chunk=True):
        """
        Grab the data from the chunk.

        :param prep_next_chunk: whether to prepare to get the next chunk
        """
        data = "".join([data for data in self.data if data != 0])
        if data[-1] != "\0":
            self.ready = False
            self.chunk_id += 1
        else:
            data = data[:-1]
            self.done = True
        self.prep_chunk()
        return data

    def receive(self, data_packet):
        """
        Receive a data packet.

        :param data_packet: the data packet
        """
        receive_bit = 1 << data_packet.slice_id

        if self.chunk_id != data_packet.chunk_id:
            return

        # not already received
        if not self.received & receive_bit:
            self.n_received += 1
        else:
            return

        if data_packet.n_slices == self.n_received:
            self.ready = True

        self.received |= receive_bit
        self.data[data_packet.slice_id] = data_packet.data

        ap = _PF.create_packet(PacketType.ACK_CHUNK)
        ap.ack_chunk = data_packet.chunk_id
        ap.ack_slice = data_packet.slice_id
        ap.n_slices = self.n_received
        ap.ack_bits = self.received

        return ap
