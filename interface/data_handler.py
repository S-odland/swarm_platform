import serial 
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import sys 
import time

import data_dicts
from data_dicts import policydict
from data_dicts import decimalToBinary2
from data_dicts import ivd
from data_dicts import bbdict
import comm_packet
from helpful import int_to_bin_str
from add_robot import MAC_mem


def get_time():
	t = time.localtime()
	str_t = time.strftime("%H:%M:%S", t)
	return str_t

class data_in():
	def __init__(self, port):
		# self.data = pd.DataFrame(np.array(np.zeros((6, 10000))), index=["id", "tflag",  "pol", "bb_idx","state", "time"])
		self.data = pd.DataFrame(np.array(np.zeros((6, 10000))), index=["id", "stflag", "tflag",  "pol", "region", "time"]) 
		self.data.loc["id",:] = self.data.loc["id",:].astype(str)
		self.data.loc["time",:] = self.data.loc["time",:].astype(str)	
		self.data_idx = 0
		self.csv_name = ""
		self.Cpolicy = ""

		ser = serial.Serial()
		ser.baudrate = 115200
		ser.port = 'COM{}'.format(port)
		self.ser = ser
		self.ser.open()

		self.start_time = 0
	def to_csv(self):
		self.data.to_csv(self.csv_name)

	def set_csv_name(self, csv_name):
		self.csv_name = "logging/{}".format(csv_name)

	def read(self):
		# time.sleep(.1)
		mess = self.ser.readline().decode('utf-8')
		# print("we're in the read function!")
		print("this is mess: ", mess)
		# print(len(mess))
		if (len(mess) != 17 and len(mess) != 18 and len(mess) != 19):
			print("Incorrect Message Length")
			return

		id = mess[:4]
		state = np.fromstring(mess[5:], sep=",") # JOSH OG

		if(state.shape[0] != 5): # JOSH OG
			print('Incorrect Message Shape')
			return

		## KB additions:
		binrep = decimalToBinary2(int(state[2]), 5)
		polstring = ivd[binrep]
		region = bbdict[str(int(state[3])) + str(int(state[4]))]
		tracker = int(np.fromstring(state[0]))
		target = int(np.fromstring(state[1]))
		# target = int((np.fromstring(mess[6:7], sep=",")))
		new_state = np.append(tracker, [target, polstring, region])

		# entry = pd.Series(np.zeros(6), index=["id", "tflag", "pol", "bb_idx", "state", "time"]) #JOSH OG
		entry = pd.Series(np.zeros(6), index=["id", "stflag", "tflag", "pol", "region", "time"]) #KB update
		entry.id = entry.id.astype(str)
		entry.loc["id"] = id

		# entry.iloc[1:-1] = state # JOSH OG
		entry.iloc[1:-1] = new_state # KB version

		entry.loc["time"] = get_time()#time.time() - self.start_time
		self.data.iloc[:,self.data_idx] = entry
		# print(self.data.iloc[:,self.data_idx]) ## Line that prints the four element display
		
		
		self.data_idx += 1

		complete = np.append(id, new_state)
		# print('State: ', complete)

		return complete

	def write(self,info):
		ser.write(info)

	def write_packet(self,packet):
		mess = ""
		mess += int_to_bin_str(int(packet.mach_id,16), 16)
		# packet.region allocated first 4 bits
		# mess += '0' #padding, started all zeroes ##### for when kb does the region stuff
		mess += str(packet.region)
		# print("the region is: ", packet.region)
		mess += '0' #og -- use this bit for actual target flag
		# print('Will the region print? ' packet.region)
		mess += int_to_bin_str(packet.cmd, 3) #kb what does this do--packet the key?
		if not (isinstance(packet.info, str)): #kb what does this do
			mess += int_to_bin_str(packet.info, 8)
		else:
			mess += '000'
			mess += packet.info
		print('Mess: ', mess)
		hex_rep = hex(int(mess, 2)) + '\r'
		print('Hex_rep: ', hex_rep)
		self.ser.write(hex_rep.encode())
		print('Serial read from policy send: ', self.ser.read_until()) ## reading serial from C
		
		# print('Packet.cmd: ', packet.cmd)
		# print('Packet.info: ', packet.info)
		# print('New serial read from policy send: ', self.ser.readline().decode('utf-8'))
		print('New serial read from policy send: ', self.ser.readline())
		# print('Packet: ', packet)
	
	def clean_putty(self):
		self.ser.flushInput()
		self.ser.flushOutput()
		time.sleep(0.002)
		print('Putty Cleared')

	def get_Cpolicy(self, packet, machineid):
		# # initialize variables
		# count = 0
		# idx = 0
		# item = 0
		# mylist = []
		# mybool = True
		
		## To clear terminal:
		# self.ser.flushInput() # new guy
		# self.ser.flushOutput()
		# time.sleep(.1)
		# print('reading serial.')
		
		# time.sleep(.1)
		# kbpolicy = str(self.ser.readline()) # reads serial
		# time.sleep(.1)
		# kbpolicy = 2
		# string = policy[2:-5]
		# print('1st serial read: ', policy)

		# # ensure displaying info for current bot
		# while (string[0:4] != machineid):
		# 	print('bot not found')
		# 		# self.ser.flushInput() # new guy
		# 		# self.ser.flushOutput()
		# 		# print('tic')
		# 		# time.sleep(.1)
		# 		# print('toc')
		# 	policy = str(self.ser.read_until())
		# 	print('while loop serial read: ', policy)
		# 	string = policy[2:-5]
		# 	# elif string[0:4] == machineid:
		# 	# 	print('bot found')
		# 	# 	mybool = False

		# # returns info for correct bot
		# for i in range(0, len(string)):
		# 	if string[i] == ',':
		# 		mylist.append(string[idx:count])
		# 		idx = i + 1
		# 		item +=1
			
		# 	if item == 4:
		# 		mylist.append(string[idx:])
		# 		item +=1

		# 	count+=1

		# bin = decimalToBinary2(list[2], 5)	
		# list[2] = ivd[bin]
		# print(list[3] + list[4])

		# ## if desired, list[1] is target flag
		# result = list[0] + ' (policy: ' + list[2] + ', region: ' + bbdict[list[3] + list[4]] + ')'

		print('KB you pressed the display button')

		return kbpolicy # NEW

	def write_message(self, mess):
		self.ser.write(mess)

	# def trial(self):


if __name__ == '__main__':
	DI = data_in(0)
	while(DI.data_idx < 300):
		DI.read()
		print("{}".format(DI.data_idx))

	DI.ser.close()

	DI.to_csv("my_john.csv")
