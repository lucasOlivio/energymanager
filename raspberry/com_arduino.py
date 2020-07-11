import time
import sys
import socket
import select
import traceback
from conectarBD import Conect

# Estabilishes connection with DB and define Arduino's connection data
conection = Conect()

UDP_IP = "192.168.15.20"
UDP_PORT = 5005
MESSAGE = "OK"
GC = "1"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

# Starts listening socket
sock = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP

sock.setblocking(0)

sock.bind((UDP_IP, UDP_PORT))

try:
	while True:
		# Receives data from arduino and insert on DB
		ready = select.select([sock], [], [], 0)
		if ready[0]:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

			print ("received message:", data, "ip: ", addr[0])

			addr[0].replace(" ", "")

			if "CS: " in data.decode():
				id = conection.select('id', 'tb_arduinos', "ip = '%s'" %addr[0])
				#print (id)
				conection.insert('tb_currents', 'id_arduino, current', '%d, %f'%(id[0][0], float(data[4:])))
			elif "OK" in data.decode():
				existe = conection.select('id', 'tb_arduinos', "ip = ' %s'"%addr[0])
				if len(existe) > 0:
					print(existe)
				else:
					print("inserindo...")
					local = input("Informe o local monitorado pelo arduino: ")
					conection.insert('tb_arduinos','local, ip', local+', '+addr[0])

		time.sleep(5)

		listaArduinos = conection.select("ip", "tb_arduinos")
		for i, arduino in enumerate(listaArduinos):
			arduino[0].replace(" ", "")
			#print(arduino[0])
			sock.sendto(GC.encode(), (arduino[0], UDP_PORT))
					
except Exception as e:
	# If some problem occurs closes socket and db connection
	Te = sys.exc_info()[0]
	print ("{0}".format(e))
	print (Te)
	print ("Closing connections...")
	sock.close()
	conection.closeCon()
