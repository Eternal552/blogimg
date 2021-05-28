import docker 
import socket
import threading  
import time
import signal
import random
import logging

MAX_ALIVE_TIME = 3600
DEFAULT_PORT = 2714



def check_dolphine_service():
	return check_port_used(DEFAULT_PORT)



def run_image(image):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(('127.0.0.1',DEFAULT_PORT))
	sock.send("${}".format(image).encode('utf-8'))
	info = str(sock.recv(1024).strip(),encoding='utf-8')
	close_sock(sock)
	del sock
	if not info:
		return None
	else:
		return info.split('|')

def stop_image(name):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(('127.0.0.1',DEFAULT_PORT))
	print(name)
	sock.send("!{}".format(name).encode('utf-8'))
	close_sock(sock)
	del sock



def check_port_used(port):
	port_test_sock = socket.socket()
	try:
		port_test_sock.connect(('127.0.0.1',port))
		port_test_sock.shutdown(2) 
		port_test_sock.close()
		del port_test_sock
		return True
	except:
		port_test_sock.close()
		del port_test_sock
		return False

def close_sock(sock):
	sock.shutdown(2)
	sock.close()

	

if __name__ == "__main__":

	


	client = docker.from_env()
	living_container = {}  

	port_pool = [x for x in range(10000,50000)]
	random.shuffle(port_pool)

	ct_list_lock = threading.Lock()
	ports_lock = threading.Lock()

	def get_unused_port():
		ports_lock.acquire()
		p = port_pool.pop()
		while check_port_used(p):
			p = port_pool.pop()
		ports_lock.release()
		return p


	class SelfCleanContainer:
		def __init__(self,ct,p,mt=MAX_ALIVE_TIME):
			self.container = ct
			self.dead_time = time.time() + mt
			self.name = ct.name
			self.ports = p

		def selfclean(self):
			global port_pool
			if self.dead_time < time.time():
				self.container.stop()
				self.container.remove(force=True)
				ports_lock.acquire()
				port_pool += self.ports
				ports_lock.release()
				del self.ports
				return True
			else:
				return False
		def clean(self):
			global port_pool
			self.container.stop()
			self.container.remove(force=True)
			ports_lock.acquire()
			port_pool += self.ports
			ports_lock.release()
			del self.ports


	def bind_docker_socket(host="127.0.0.1",port=2174):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.bind((host,port))
		return s   

	def push_container(ct):
		ct_list_lock.acquire()
		living_container[ct.name] = ct
		ct_list_lock.release()

	def pop_container(name):
		ct_list_lock.acquire()
		if living_container.get(name):
			living_container[name].clean()
			del living_container[name]
		ct_list_lock.release()

	def run_image(image,cmd=None):

		default_ports = {'80/tcp':('0.0.0.0',get_unused_port()),
					'23333/tcp':('0.0.0.0',get_unused_port())}
		res = ''
		pl = []

		for k in default_ports.keys():
			p = default_ports[k][1]		
			res += '|{}:{}'.format(k,p)
			pl.append(p)		

		if not cmd:
			ct = client.containers.run(image,cmd,ports=default_ports,detach=True)
		else:
			ct = client.containers.run(image,ports=default_ports,detach=True)
		push_container(SelfCleanContainer(ct,pl))
		return ct.name + res
	

	def exec_image(c_sock):
		image = c_sock.recv(1024)
		if len(image) == 0:
			close_sock(c_sock)
			return

		image = str(image.strip(),encoding='utf-8')
		if not image or not image.strip():
			close_sock(c_sock)
			return
		
		if image[0] == '$':
			name = run_image(image[1:])
			c_sock.send((name).encode('utf-8'))
		elif image[0] == '!':
			pop_container(image[1:])
		close_sock(c_sock)


	def self_cleaner():
		ca = []
		while True:
			cn = 0
			time.sleep(1)
			ct_list_lock.acquire()
			for k in living_container.keys():
				if living_container.get(k):
					if living_container[k].selfclean():
						ca.append(k)
						cn += 1
			for i in range(cn):
				del living_container[ca.pop()]

			ct_list_lock.release()
  
	def dispatch_server(sock,l=10):
		print("Running Dispatch Server...")
		sock.listen(l)
		t = threading.Thread(target=self_cleaner)
		t.setDaemon(True)
		t.start() 
		while True:
			try:
				c_sock,addr = sock.accept()
				print("accept from: {}".format(addr))
				t = threading.Thread(target=exec_image,args=(c_sock,))
				t.setDaemon(True)
				t.start()
			except:
				exit()   


	def quit_handler_wraper(sock):
		def quit_handler(signum,frame):
			close_sock(sock)
			print("Exit Controller ...")
	
		signal.signal(signal.SIGINT, quit_handler)
		signal.signal(signal.SIGHUP, quit_handler)
		signal.signal(signal.SIGTERM, quit_handler)


	print("")
	print("A Plugin for CTFd to generate dynamic enviroment")
	print("Designed by s0duku")
	print("")


	dispatcher_sock = bind_docker_socket(port=DEFAULT_PORT)
	quit_handler_wraper(dispatcher_sock)
	dispatch_server(dispatcher_sock)
	
