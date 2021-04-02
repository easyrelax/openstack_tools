import eventlet
import SocketServer as socketserver
import time
from oslo_utils import timeutils


ip_port=("127.0.0.1",8000)

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.print_time("conn is: ", self.request)
        self.print_time("addr is: ", self.client_address)
 
        while True:
            try:
                data = self.request.recv(1024)
                if not data:
                    break
                self.print_time("Receive data: ", data.decode("utf-8"))
                with timeutils.StopWatch() as timer:
                    raw = self.count(20000000)
                    self.print_time("Took seconds to write to etcd: ", timer.elapsed())
                    self.print_time("Raw: ", raw)
                self.request.sendall(data.upper())
            except Exception as e:
                print(e)
                break

    def count(self, n):
        sum = 0
        for i in range(0, n+1):
            sum = sum + i
        return sum

    def print_time(self, s1, s2):
        print("{0} {1} {2}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), s1, s2))

if __name__ == "__main__":
    #eventlet.monkey_patch(thread=False)
    #eventlet.monkey_patch(time=False)
    s = socketserver.ThreadingTCPServer(ip_port,MyServer)
    s.serve_forever()
