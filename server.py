import socket, logging, threading, datetime

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

class ChatServer:
	def __init__(self, ip='127.0.0.1', port=9999):
		self.addr = (ip, port)
		self.sock = socket.socket()
		self.clients = {}

	def start(self):
		self.sock.bind(self.addr)
		self.sock.listen()

		threading.Thread(target=self.accept, name='accept').start()
		logging.info('waiting client to connect...')

	def accept(self):
		try:
			while True:
				conn, raddr = self.sock.accept()
				logging.info('%s has connected...', raddr)
				logging.info(conn)
				self.clients[raddr] = conn
				threading.Thread(target=self.recv, name='recv', args=(conn, raddr)).start()
		except:
			pass

	def recv(self, conn, raddr):
		try:
			data = conn.recv(1024)
			while data:
				logging.debug('%s: %s', raddr, data.decode())
				for k, v in self.clients.items():
					if k != raddr:
						logging.debug("%s -> %s" % (raddr, k))
						v.send('{} {}'.format(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'), data.decode()).encode())
				data = conn.recv(1024)
			self.clients.pop(raddr)
			conn.close()
		except:
			pass

	def stop(self):
		for s in self.clients.values():
			s.close()
		self.sock.close()

server = ChatServer()
server.start()
while True:
	cmd = input('>>>')
	if cmd.strip() == 'quit':
		server.stop()
		threading.Event().wait(3)
		logging.info('Server shut down...')
		break
	logging.info(threading.enumerate())