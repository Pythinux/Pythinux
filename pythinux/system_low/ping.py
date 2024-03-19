import socket
import struct
import time

def checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i + 1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum
def ping(host, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ICMP) as sock:
        sock.settimeout(timeout)

        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = 12345
        icmp_sequence = 1
        payload = b"PING"
        packet = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence) + payload
        icmp_checksum = checksum(packet)
        packet = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_sequence) + payload

        # Send the packet
        sock.sendto(packet, (host, 0))

        # Record the time the packet was sent
        send_time = time.time()

        try:
            data, addr = sock.recvfrom(1024)
            receive_time = time.time()
            rtt = (receive_time - send_time) * 1000
            return str(rtt) ## Ensures .startswith() does not fail
        except socket.timeout:
            return "TIMEOUT"
        except socket.herror as e:
            return "HERROR:{}".format(e)

def main(args):
    if args:
        for arg in args:
            result = ping(arg)
            if result == "TIMEOUT":
                print("ERROR: Request to {} timed out.".format(arg))
            elif result.startswith("HERROR:"):
                print("ERROR ({}): {}".format(arg, result[7:]))
            else:
                print("{}: {}ms".format(arg, result))
    else:
        div()
        print("ping [list of addresses]")
        div()
        print("Checks to see if a host is alive.")
        div()
        print("Trivia: This program is a fully Pythonic implementation of the ping utility and does NOT rely on your OS's ping command.")
        div()
