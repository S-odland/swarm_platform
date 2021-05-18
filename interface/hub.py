

import sys
import serial

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from data_handler import data_in
from helpful import int_to_bin_str
from comm_packet import packet
import data_dicts
from data_dicts import letters
from data_dicts import numbers
from data_dicts import policydict
from data_dicts import regiondict

import time
import threading
def task1(data_in, num_its):
	print("inside 1")
	global current_read
	global end_flag
	end_flag = 0
	print("idx: {} num_its: {}", data_in.data_idx)

	while((data_in.data_idx < num_its) & (end_flag == 0)):
		current_read = data_in.read()
		print("This is current_read: ", current_read)
		time.sleep(0.002) # changed from 0.002
		print(data_in.data_idx)
		print('this is the other loop')
	data_in.to_csv()
	print("wrote to csv")

def task2():
	global task2_flag
	task2_flag = 0
	thing = 0
	while (task2_flag == 0):
		thing += 1
		# print('Yeehaw we threading')
		# time.sleep(1)
	# Main task: Constantly evaluate current_read
	# 1. Ensure current bot is in dictionary--if not, add to dictionary
	# 2. Check if any values deviate from the dictionary--note what has changed (target vs policy vs region)
	# 3. If Case 1 or Case 2 conditions have been met--send new policy when returned to region 0. Include delay.
	# constantly check for two cases

class UI(QWidget):
	def __init__(self):
		super().__init__()
		self.curr_pack = packet()
		grid = QGridLayout()
		self.setLayout(grid)

		#data handler stuff
		self.data_sock = data_in(21) ##############################	CURRENT COM PORT NUMBER ##################

		# #Flags
		global end_flag
		global task2_flag
		end_flag = 1
		task2_flag = 0


		print("open")
		label = QLabel("Swarm Control GUI")
		header = QHBoxLayout()
		header.addWidget(label)
		label.setAlignment(Qt.AlignCenter)
		grid.addLayout(header, 0, 0, 1, 12)

		# self.csv_name = QGroupBox("csv name")

		# grid.addLayout(csv_name_box, 0, 1, 1, 1)

		cmd_group = QGroupBox("commands")
		cmd_grid = QGridLayout()
		ID_edit = QLineEdit()
		ID_edit.setPlaceholderText("Robot ID <press Enter>")
		ID_edit.returnPressed.connect(self.set_mach_id)
		cmd_grid.addWidget(ID_edit, 0,0, 1, 6)
		start_btn = QPushButton("start",self)
		stop_btn = QPushButton("stop",self)


		cmd_grid.addWidget(start_btn, 1,0, 1, 3)
		cmd_grid.addWidget(stop_btn, 1, 3, 1, 3)

		self.ID_edit = ID_edit
		self.policy_combo_box = QComboBox()
		# self.policy_combo_box.setPlaceholderText("set policy")

		# To return to policy structure:
		for i in range(pow(2,5)):
			self.policy_combo_box.addItem(int_to_bin_str(i, 5))
		# cmd_grid.addWidget(self.policy_combo_box,2, 0, 1, 6) ## to add old policy system
		send_pol_btn = QPushButton("send policy")
		send_pol_btn.clicked[bool].connect(self.upload_pol)

		# KB new policy stuff--a letter, a number, and a region

		## Letters:
		self.letter_box = QComboBox()
		for i in range(0,len(letters)):
			self.letter_box.addItem(letters[i])
		cmd_grid.addWidget(self.letter_box,3,0,1,2)

		## Numbers:
		self.number_box = QComboBox()
		for i in range(0,len(numbers)):
			self.number_box.addItem(numbers[i])
		cmd_grid.addWidget(self.number_box,3,2,1,2)

		## Region:
		self.region_box = QComboBox()
		for i in range(0,10):
			self.region_box.addItem(str(i))
		cmd_grid.addWidget(self.region_box,3,4,1,2)

		cmd_grid.addWidget(send_pol_btn,4, 3, 1, 3)
		disp_info_btn = QPushButton("disp info") ## use this button to display info
		cmd_grid.addWidget(disp_info_btn,4, 0, 1, 3)


		cmd_group.setLayout(cmd_grid)
		grid.addWidget(cmd_group, 1,0,1,3)

		self.enable_btns = [start_btn, stop_btn, disp_info_btn] ## added pol button
		start_btn.clicked[bool].connect(self.enable)
		stop_btn.clicked[bool].connect(self.enable)
		disp_info_btn.clicked[bool].connect(self.enable)


		# ## KB section
		# kb_group = QGroupBox('Bot Reset')
		# kb_group_grid = QGridLayout()

		# ## Type bot of interest
		# ID2_edit = QLineEdit()
		# ID2_edit.setPlaceholderText("Robot ID <press Enter>")
		# ID2_edit.returnPressed.connect(self.set_mach_id)
		# kb_group_grid.addWidget(ID2_edit, 0,0, 1, 2)

		# ## Add a dropdown option for S&G's
		# self.kb_fun = QComboBox()
		# self.kb_fun.addItem('bb_idx')
		# self.kb_fun.addItem('yeehaw')
		# kb_group_grid.addWidget(self.kb_fun,1,0,1,1)

		# self.kb_fun2 = QComboBox()
		# self.kb_fun2.addItem('state')
		# self.kb_fun2.addItem('yeehaw')
		# kb_group_grid.addWidget(self.kb_fun2,1,1,1,1)

		# ## Add a new button for S&G's
		# new_test_btn = QPushButton('send policy')
		# kb_group_grid.addWidget(new_test_btn,2,0,1,2)

		# # Configure new items
		# kb_group.setLayout(kb_group_grid)
		# grid.addWidget(kb_group, 0,1,2,1)


		trail_group = QGroupBox("data collect")
		trail_group_grid = QGridLayout()

		csv_name_edit = QLineEdit()
		csv_name_edit.setPlaceholderText("CSV Name <press Enter>")
		csv_name_box = QHBoxLayout()
		csv_name_box.addWidget(csv_name_edit)
		csv_name_edit.returnPressed.connect(self.csv_rename)
		self.csv_name_edit = csv_name_edit
		trail_group_grid.addWidget(self.csv_name_edit, 0,0,1,2)
		
		begin_trial_btn = QPushButton("begin")
		end_trial_btn = QPushButton("end")
		self.idx_counter = QLabel("data idx: {}".format(self.data_sock.data_idx))

		begin_trial_btn.clicked[bool].connect(self.begin_trial)
		end_trial_btn.clicked[bool].connect(self.end_trial)
		self.csv_num_el_edit = QLineEdit()
		self.csv_num_el_edit.setPlaceholderText("input # enteries")
		self.csv_num_el_edit.returnPressed.connect(self.num_el_edit)
		self.num_els = 100

		trail_group_grid.addWidget(begin_trial_btn, 1,0,1,1)
		trail_group_grid.addWidget(end_trial_btn, 2,0,1,1)
		trail_group_grid.addWidget(self.csv_num_el_edit, 1, 1, 1, 1)
		trail_group_grid.addWidget(self.idx_counter,2, 1, 1,1)
		trail_group.setLayout(trail_group_grid)
		grid.addWidget(trail_group, 1,4,2,4) ## KB changed from 0,1,2,1

		self.info_disp = QLabel("info:")
		grid.addWidget(self.info_disp, 3,0,1,2)

		# self.line_edit = QLineEdit()
		# enter_line = QPushButton("Enter",self)
		# enter_line.clicked[bool].connect(self.transmit)
		# self.line_edit.returnPressed.connect(self.transmit)
		# liney = QHBoxLayout()
		# liney.addWidget(self.line_edit)
		# liney.addWidget(enter_line)
		# self.line_edit.setPlaceholderText("ex: ID CMD")
		# grid.addLayout(liney, 1, 0, 1, 1)

		self.setWindowTitle('Swarm Interface')
		self.resize(550, 250) ## KB changed from 500,250
		self.center()
		self.show()

	def set_mach_id(self):
		self.curr_pack.set_mach_id(self.ID_edit.text())
		self.ID_edit.setPlaceholderText(self.ID_edit.text())
		self.info_disp.setText("curr bot: {}".format(self.ID_edit.text())) ## add policy lookup in similar format
		self.ID_edit.setText("")

	def enable(self):
		global current_read
		global end_flag
		source = self.sender()
		self.curr_pack.set_cmd("enable")
		if (source == self.enable_btns[0]):
			self.curr_pack.set_info(1)
			txt = "on"
			self.data_sock.write_packet(self.curr_pack)
			self.info_disp.setText("turning bot {} {}".format(self.curr_pack.mach_id, txt))
		if (source == self.enable_btns[1]):
			self.curr_pack.set_info(0)
			txt = "off"
			self.data_sock.write_packet(self.curr_pack)
			self.info_disp.setText("turning bot {} {}".format(self.curr_pack.mach_id, txt))
		if (source == self.enable_btns[2]):
			# print('New serial read: ', self.ser.readline().decode('utf-8'))
			# self.info_disp.setText("The policy for bot {} is {} ".format(self.curr_pack.mach_id, self.ser.readline().decode('utf-8')))
			# self.data_sock.write_packet(self.curr_pack)
			# curr_pol = self.data_sock.get_Cpolicy(self.curr_pack, self.curr_pack.mach_id) ## this is where a loop was used previously
			# self.info_disp.setText("{}".format(curr_pol))

			## Cases to check if reading csv or not:

			## Fun times with threading and deciphering whether or not we're currently writing to csv
			## To remedy this issue, default csv_flag is 0; if this changes, we change
			## As soon as we have a csv_flag falling edge, we can just rely on bool to check whether we running or not
			## default falling edge = 0
			if end_flag == 0: ## if we're in the csv thread
				self.data_sock.edge = 0 # in csv mode
			else:
				self.data_sock.edge = 1 # not in csv mode
				
			self.info_disp.setText("{}".format(self.find_bot()))
			# print("Current CSV Flag: ", self.data_sock.csv_flag)
			# print('Thread Status: ', self.check_thread())

		
	def find_bot(self):
		errorcount = 0
		if (self.data_sock.edge == 0):
			while (current_read[0] != self.curr_pack.mach_id):
				time.sleep(0.002)
				errorcount +=1
				if errorcount == 100:
					return 'CSV but Bot not found'
			curr_read = current_read		
		elif (self.data_sock.edge == 1):
			self.data_sock.clean_putty()
			time.sleep(0.002)
			curr_read = self.data_sock.read()
			print('This is the current read: ', curr_read)
			while (curr_read[0] != self.curr_pack.mach_id):
				time.sleep(0.002)
				errorcount +=1
				if errorcount == 100:
					return 'No CSV, Bot not found'
				curr_read = self.data_sock.read()
			self.data_sock.data_idx = 0

		return curr_read

	def upload_pol(self):
		# print('Letter: ', self.letter_box.currentText())
		# print('Number: ', self.number_box.currentText())
		print(policydict[self.letter_box.currentText() + self.number_box.currentText()])
		# self.curr_pack.set_info(self.policy_combo_box.currentText()) #with old system
		self.curr_pack.set_info(policydict[self.letter_box.currentText() + self.number_box.currentText()]) #with new system
		self.curr_pack.set_cmd("set_pol") ## would need to replicate this to add other commands

		print('This is the region: ', self.region_box.currentText()) # this works
		self.curr_pack.set_region(regiondict[self.region_box.currentText()]) # does this work?
		print('packet set: ', self.curr_pack.region) # does not work
		
		self.data_sock.write_packet(self.curr_pack)

	def center(self):
		qr = self.frameGeometry()
		#print(qr)
		cp = QDesktopWidget().availableGeometry().center()
		#print(cp)
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def csv_rename(self):
		self.data_sock.set_csv_name(self.csv_name_edit.text())
		self.csv_name_edit.setPlaceholderText(self.csv_name_edit.text())
		self.csv_name_edit.setText("")

	def begin_trial(self):
		self.data_sock.data_idx = 0
		self.csv_flag = 1
		self.ser_read = threading.Thread(target=task1, args=[self.data_sock, self.num_els])
		self.ser_read.start()

		# self.bot_tracking = threading.Thread(target=task2)
		# self.bot_tracking.start()
		# while(self.data_sock.data_idx < self.num_els):
		# 	print(self.data_sock.data_idx)
		# 	self.data_sock.read()
		# 	self.idx_counter.setText("data idx: {}".format(self.data_sock.data_idx))

		# self.data_sock.to_csv()
	
	def end_trial(self):
		global end_flag
		end_flag = 1

		global task2_flag
		task2_flag = 1
		# time.sleep(0.02)
		# self.data_sock.data_idx = -1

	def check_thread(self):
		return str(self.ser_read.is_alive())

	def num_el_edit(self):
		self.data_sock.data_idx = 0 # will set to 0 once csv file is started
		self.num_els = int(self.csv_num_el_edit.text())
		self.csv_num_el_edit.setPlaceholderText(str(self.num_els))
		self.csv_num_el_edit.setText("")
		self.idx_counter.setText("data idx: {}/{}".format(self.data_sock.data_idx, self.num_els))

if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = UI()
	# ex.data_sock.ser.close()
	sys.exit(app.exec_())