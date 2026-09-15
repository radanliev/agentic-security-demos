"""
In-kernel / stream-level TCP Reassembler for InterceptBound.
Prevents fragmented-packet prompt injection evasion by reassembling bidirectional TCP streams.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class TCPPacket:
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    seq_num: int
    payload: bytes
    syn: bool = False
    fin: bool = False
    ack: bool = False


@dataclass
class StreamState:
    expected_seq: int
    out_of_order_chunks: Dict[int, bytes] = field(default_factory=dict)
    reassembled_buffer: bytearray = field(default_factory=bytearray)


class TCPStreamReassembler:
    """Reassembles bidirectional TCP segments into coherent application streams."""

    def __init__(self):
        self.sessions: Dict[Tuple[str, int, str, int], StreamState] = {}

    def _get_flow_key(self, pkt: TCPPacket) -> Tuple[str, int, str, int]:
        return (pkt.src_ip, pkt.src_port, pkt.dst_ip, pkt.dst_port)

    def process_packet(self, pkt: TCPPacket) -> Tuple[bytes, bool]:
        """
        Processes a TCP packet.
        Returns (newly_reassembled_bytes, is_complete).
        """
        key = self._get_flow_key(pkt)
        if key not in self.sessions:
            self.sessions[key] = StreamState(expected_seq=pkt.seq_num)

        state = self.sessions[key]

        if pkt.seq_num == state.expected_seq:
            state.reassembled_buffer.extend(pkt.payload)
            state.expected_seq += len(pkt.payload)

            # Check if out-of-order chunks can now be attached
            while state.expected_seq in state.out_of_order_chunks:
                next_chunk = state.out_of_order_chunks.pop(state.expected_seq)
                state.reassembled_buffer.extend(next_chunk)
                state.expected_seq += len(next_chunk)

            new_bytes = bytes(state.reassembled_buffer)
            return new_bytes, pkt.fin
        elif pkt.seq_num > state.expected_seq:
            # Buffer future out-of-order packet
            state.out_of_order_chunks[pkt.seq_num] = pkt.payload
            return b"", False
        else:
            # Duplicate / retransmitted packet
            return b"", False

    def close_stream(self, key: Tuple[str, int, str, int]) -> bytes:
        if key in self.sessions:
            res = bytes(self.sessions[key].reassembled_buffer)
            del self.sessions[key]
            return res
        return b""
