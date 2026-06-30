import socket
import sys
import time
import random
from threading import Thread

def sender(target_ip, target_port, data, duration, delay, jitter, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            pkt = (data * (packet_size // len(data) + 1))[:packet_size]
            sock.sendto(pkt.encode(), (target_ip, target_port))
            time.sleep(max(0.001, delay + random.uniform(-jitter, jitter)))
        except:
            pass
    sock.close()

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 udpsend.py <IP> <PORT> <SECONDS>")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    
    # Optimized for GitHub Codespaces stress
    threads = 8
    delay = 0.008
    jitter = 0.003
    size = 1024
    data = "X" * 512
    
    print(f"UDP stress → {target_ip}:{target_port} for {duration}s")
    
    ts = []
    for _ in range(threads):
        t = Thread(target=sender, args=(target_ip, target_port, data, duration, delay, jitter, size))
        ts.append(t)
        t.start()
    
    for t in ts:
        t.join()
    
    print("Done.")

if __name__ == "__main__":
    main()