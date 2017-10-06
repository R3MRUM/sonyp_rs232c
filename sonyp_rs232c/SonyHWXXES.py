import serial
import binascii
import time

class SonyHWXXES():

	def __init__(self, port='COM1', baud=38400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN,
				 stopbits=serial.STOPBITS_ONE, timeout=3.2, verbose=False, commandDelay=.2):
		self.verbose=verbose
		self.commandDelay=commandDelay

		self.__itemList = {
							'Get':{
									'Input':					b'\x00\x01',
									'Calibration Preset': 		b'\x00\x02',
									'Contrast':					b'\x00\x10',
									'Brightness':				b'\x00\x11',
									'Color':					b'\x00\x12',
									'Hue':						b'\x00\x13',
									'Sharpness':				b'\x00\x14',
									'Color Temp':				b'\x00\x17',
									'Lamp Control':				b'\x00\x1A',
									'Contrast Enhancer':		b'\x00\x1C',
									'Advanced Iris':			b'\x00\x1D',
									'Real Color Processing':	b'\x00\x1E',
									'Film Mode':				b'\x00\x1F',
									'Aspect':					b'\x00\x20',
									'Gamma Correction':			b'\x00\x22',
									'Over Scan':				b'\x00\x23',
									'Screen Area':				b'\x00\x24',
									'Noise Reduction':			b'\x00\x25',
									'Picture Muting':			b'\x00\x30',
									'Color Space':				b'\x00\x3B',
									'User Gain Red':			b'\x00\x50',
									'User Gain Green':			b'\x00\x51',
									'User Gain Blue':			b'\x00\x52',
									'User Bias Red':			b'\x00\x53',
									'User Bias Green':			b'\x00\x54',
									'User Bias Blue':			b'\x00\x55',
									'Iris Manual':				b'\x00\x57',
									'Film Projection':			b'\x00\x58',
									'Motion Enhancer':			b'\x00\x59',
									'xvColor':					b'\x00\x5A',
									'2D-3D Display Select':		b'\x00\x60',
									'3D Format':				b'\x00\x61',
									'3D Depth Adjust':			b'\x00\x62',
									'Simulated 3D Effect':		b'\x00\x63',
									'3D Glasses Brightness':	b'\x00\x65',
									'Reality Creation':			b'\x00\x67',
									'Resolution':				b'\x00\x68',
									'Noise Filtering':			b'\x00\x69',
									'MPEG Noise Reduction':		b'\x00\x6C',
									'HDMI 1 - Dynamic Range':	b'\x00\x6E',
									'HDMI 2 - Dynamic Range':	b'\x00\x6F',
									'Settings Lock':			b'\x00\x73',
									'Status Error':				b'\x01\x01',
									'Status Power':				b'\x01\x02',
									'Lamp Timer':				b'\x01\x13',
									'Status Error (2)':			b'\x01\x25'
								},
							'Set':{
									'Input':					b'\x00\x01',
									'Calibration Preset': 		b'\x00\x02',
									'Contrast':					b'\x00\x10', #TODO
									'Brightness':				b'\x00\x11', #TODO
									'Color':					b'\x00\x12', #TODO
									'Hue':						b'\x00\x13', #TODO
									'Sharpness':				b'\x00\x14', #TODO
									'Color Temp':				b'\x00\x17',
									'Lamp Control':				b'\x00\x1A',
									'Contrast Enhancer':		b'\x00\x1C',
									'Advanced Iris':			b'\x00\x1D',
									'Real Color Processing':	b'\x00\x1E',
									'Film Mode':				b'\x00\x1F',
									'Aspect':					b'\x00\x20',
									'Gamma Correction':			b'\x00\x22',
									'Over Scan':				b'\x00\x23',
									'Screen Area':				b'\x00\x24',
									'Noise Reduction':			b'\x00\x25',
									'Picture Muting':			b'\x00\x30',
									'Color Space':				b'\x00\x3B',
									'User Gain Red':			b'\x00\x50', #TODO
									'User Gain Green':			b'\x00\x51', #TODO
									'User Gain Blue':			b'\x00\x52', #TODO
									'User Bias Red':			b'\x00\x53', #TODO
									'User Bias Green':			b'\x00\x54', #TODO
									'User Bias Blue':			b'\x00\x55', #TODO
									'Iris Manual':				b'\x00\x57', #TODO
									'Film Projection':			b'\x00\x58',
									'Motion Enhancer':			b'\x00\x59',
									'xvColor':					b'\x00\x5A',
									'2D-3D Display Select':		b'\x00\x60',
									'3D Format':				b'\x00\x61',
									'3D Depth Adjust':			b'\x00\x62', #TODO
									'Simulated 3D Effect':		b'\x00\x63',
									'3D Glasses Brightness':	b'\x00\x65', #TODO
									'Reality Creation':			b'\x00\x67',
									'Resolution':				b'\x00\x68', #TODO
									'Noise Filtering':			b'\x00\x69', #TODO
									'MPEG Noise Reduction':		b'\x00\x6C',
									'HDMI 1 - Dynamic Range':	b'\x00\x6E',
									'HDMI 2 - Dynamic Range':	b'\x00\x6F',
									'Settings Lock':			b'\x00\x73',
									'Motion Enhancer Toggle':	b'\x17\x05',
									'Contrast Enhancer Toggle':	b'\x17\x07',
									'Remote Film Projection':	b'\x17\x08',
									'Power Toggle':				b'\x17\x15',
									'Contrast +':				b'\x17\x18',
									'Contrast -':				b'\x17\x19',
									'Color +':					b'\x17\x1A',
									'Color -':					b'\x17\x1B',
									'Brightness +':				b'\x17\x1E',
									'Brightness -':				b'\x17\x1F',
									'Hue +':					b'\x17\x20',
									'Hue -':					b'\x17\x21',
									'Sharpness +':				b'\x17\x22',
									'Sharpness -':				b'\x17\x23',
									'Remote Picture Muting':	b'\x17\x24',
									'Status On':				b'\x17\x25',
									'Status Off':				b'\x17\x26',
									'Menu':						b'\x17\x29',
									'Input A':					b'\x17\x2B',
									'Component':				b'\x17\x2C',
									'Power On':					b'\x17\x2E',
									'Power Off':				b'\x17\x2F',
									'Cursor Right':				b'\x17\x33',
									'Cursor Left':				b'\x17\x34',
									'Cursor Up':				b'\x17\x35',
									'Cursor Down':				b'\x17\x36',
									'Pitch':					b'\x17\x47',
									'Shift':					b'\x17\x48',
									'Input Select':				b'\x17\x57',
									'Enter':					b'\x17\x5A',
									'HDMI 1':					b'\x17\x6F',
									'HDMI 2':					b'\x17\x70',
									'Reset':					b'\x17\x7B' 
								}
							}

		self.__validSettings = {
								'Input': {'Input A':b'\x00\x02','Component':b'\x00\x03','HDMI 1':b'\x00\x04', 'HDMI 2':b'\x00\x05'},
								'Calibration Preset': {'Cinema Film 1':b'\x00\x00','Cinema Film 2':b'\x00\x01','REF':b'\x00\x02','TV':b'\x00\x03','Photo':b'\x00\x04','Game':b'\x00\x05','Bright Cinema':b'\x00\x06','Bright TV':b'\x00\x07','User':b'\x00\x08'},
								'Contrast': None,
								'Brightness': None,
								'Color': None,
								'Hue': None,
								'Sharpness': None,
								'Color Temp': {'D93':b'\x00\x00','D75':b'\x00\x01','D65':b'\x00\x02','Custom 1':b'\x00\x03','Custom 2':b'\x00\x04','Custom 3':b'\x00\x05','Custom 4':b'\x00\x06','D55':b'\x00\x07','Custom 5':b'\x00\x08'},
								'Lamp Control': {'Low':b'\x00\x00','High':b'\x00\x01'},
								'Contrast Enhancer': {'Off':b'\x00\x00','Low':b'\x00\x01','High':b'\x00\x02','Middle':b'\x00\x03'},
								'Advanced Iris': {'Off':b'\x00\x00','Manual':b'\x00\x01','Auto Full':b'\x00\x02','Auto Limited':b'\x00\x03'},
								'Real Color Processing': {'Off':b'\x00\x00','User 1':b'\x00\x01','User 2':b'\x00\x02','User 3':b'\x00\x03'},
								'Film Mode': {'Off':b'\x00\x00','Auto 1':b'\x00\x01','Auto 2':b'\x00\x02'},
								'Aspect': {'Full':b'\x00\x00','Normal':b'\x00\x01','Wide Zoom':b'\x00\x02','Zoom':b'\x00\x03','V Stretch':b'\x00\x0B','Stretch':b'\x00\x0E','Squeeze':b'\x00\x0F'},
								'Gamma Correction': {'Off':b'\x00\x00','1.8':b'\x00\x01','2.0':b'\x00\x02','2.1':b'\x00\x03','2.2':b'\x00\x04','2.4':b'\x00\x05','2.6':b'\x00\x06','Gamma 7':b'\x00\x07','Gamma 8':b'\x00\x08','Gamma 9':b'\x00\x09','Gamma 10':b'\x00\x0A'},
								'Over Scan': {'Off':b'\x00\x00','On':b'\x00\x01'},
								'Screen Area': {'Full':b'\x00\x00','Through':b'\x00\x01'},
								'Noise Reduction': {'Off':b'\x00\x00','Low':b'\x00\x01','Middle':b'\x00\x02','High':b'\x00\x03'},
								'Picture Muting': {'Off':b'\x00\x00','On':'\x00\x01'},
								'Color Space': {'BT.709':b'\x00\x00','Color Space 1':'\x00\x01','Color Space 2':b'\x00\x02','Color Space 3':b'\x00\x03'},
								'User Gain Red': None,
								'User Gain Green': None,
								'User Gain Blue': None,
								'User Bias Red': None,
								'User Bias Green': None,
								'User Bias Blue': None,
								'Iris Manual': None,
								'Film Projection': {'Off':b'\x00\x00','On':b'\x00\x01'},
								'Motion Enhancer': {'Off':b'\x00\x00','Low':b'\x00\x01','High':b'\x00\x02'},
								'xvColor': {'Off':b'\x00\x00','On':b'\x00\x01'},
								'2D-3D Display Select': {'Auto':b'\x00\x00','3D':b'\x00\x01','2D':b'\x00\x02'},
								'3D Format': {'Simulated 3D':b'\x00\x00','Side-By-Side':b'\x00\x01','Over-Under':b'\x00\x02'},
								'3D Depth Adjust': None,
								'Simulated 3D Effect': {'High':b'\x00\x00','Middle':b'\x00\x01','Low':b'\x00\x02'},
								'3D Glasses Brightness': None,
								'Reality Creation': {'Off':b'\x00\x00','On':b'\x00\x01'},
								'Resolution': None,
								'Noise Filtering': None,
								'MPEG Noise Reduction': {'Off':b'\x00\x00','Low':b'\x00\x01','High':b'\x00\x02','Middel':b'\x00\x03'},
								'HDMI 1 Dynamic Range': {'Auto':b'\x00\x00','Limit':b'\x00\x01','Full':b'\x00\x02'},
								'HDMI 2 Dynamic Range': {'Auto':b'\x00\x00','Limit':b'\x00\x01','Full':b'\x00\x02'},
								'Settings Lock': {'Off':b'\x00\x00','Level A':b'\x00\x01','Level B':b'\x00\x02'}
								}

		self.__validResponses = {
					                b'\x02':{
					                        b'\x00\x01':{    #Input
					                                    b'\x00\x02':'Input A',
					                                    b'\x00\x03':'Component',
					                                    b'\x00\x04':'HDMI 1',
					                                    b'\x00\x05':'HDMI 2'
					                                    },
					                        b'\x00\x02':{    #Picture Mode
					                                    b'\x00\x00':'Cinema Film 1',
					                                    b'\x00\x01':'Cinema Film 2',
					                                    b'\x00\x02':'REF',
					                                    b'\x00\x03':'TV',
					                                    b'\x00\x04':'Photo',
					                                    b'\x00\x05':'Game',
					                                    b'\x00\x06':'Bright Cinema',
					                                    b'\x00\x07':'Bright TV',
					                                    b'\x00\x08':'User'
					                                    },
					                        b'\x00\x17':{    #Color Temp
					                                    b'\x00\x00':'D93',
					                                    b'\x00\x01':'D75',
					                                    b'\x00\x02':'D65',
					                                    b'\x00\x03':'Custom 1',
					                                    b'\x00\x04':'Custom 2',
					                                    b'\x00\x05':'Custom 3',
					                                    b'\x00\x06':'Custom 4',
					                                    b'\x00\x07':'D55',
					                                    b'\x00\x08':'Custom 5'
					                                    },
					                        b'\x00\x1A':{    #Lamp Control
					                                    b'\x00\x00':'Low',
					                                    b'\x00\x01':'High'
					                                    },
					                        b'\x00\x1C':{    #Contrast Enhancer
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'Low',
					                                    b'\x00\x02':'High',
					                                    b'\x00\x03':'Middle'
					                                    },
					                        b'\x00\x1D':{    #Advnced Iris
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'Manual',
					                                    b'\x00\x02':'Auto Full',
					                                    b'\x00\x03':'Auto Limited'
					                                    },
					                        b'\x00\x1E':{    #Real Color Processing
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'User 1',
					                                    b'\x00\x02':'User 2',
					                                    b'\x00\x03':'User 3'
					                                    },
					                        b'\x00\x1F':{	#Film Mode
					                        			b'\x00\x00':'Off',
					                                    b'\x00\x01':'Auto 1',
					                                    b'\x00\x02':'Auto 2'
					                                    },
					                        b'\x00\x20':{	#Aspect
					                        			b'\x00\x00':'Full',
					                                    b'\x00\x01':'Normal',
					                                    b'\x00\x02':'Wide Zoom',
					                                    b'\x00\x03':'Zoom',
					                                    b'\x00\x0B':'V Stretch',
					                                    b'\x00\x0E':'Stretch',
					                                    b'\x00\x0F':'Squeeze'
					                                    },
					                        b'\x00\x22':{    #Gamma Correction
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'1.8',
					                                    b'\x00\x02':'2.0',
					                                    b'\x00\x03':'2.1',
					                                    b'\x00\x04':'2.2',
					                                    b'\x00\x05':'2.4',
					                                    b'\x00\x06':'2.6',
					                                    b'\x00\x07':'Gamma 7',
					                                    b'\x00\x08':'Gamma 8',
					                                    b'\x00\x09':'Gamma 9',
					                                    b'\x00\x0A':'Gamma 10'
					                                    },
					                        b'\x00\x23':{	#Over Scan
					                        			b'\x00\x00':'Off',
					                                    b'\x00\x01':'On'
					                                    },
					                        b'\x00\x24':{	#Screen Area
					                        			b'\x00\x00':'Full',
					                                    b'\x00\x01':'Through'
					                                    },
					                        b'\x00\x25':{    #NR
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'Low',
					                                    b'\x00\x02':'Middle',
					                                    b'\x00\x03':'High'
					                                    },
					                        b'\x00\x30':{	#Picture Muting
					                        			b'\x00\x00':'Off',
					                                    b'\x00\x01':'On'
					                                    },
					                        b'\x00\x3B':{    #Color Space
					                                    b'\x00\x00':'BT.709',
					                                    b'\x00\x01':'Color Space 1',
					                                    b'\x00\x02':'Color Space 2',
					                                    b'\x00\x03':'Color Space 3'
					                                    },
					                        b'\x00\x58':{    #Film Projection
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'On'
					                                    },
					                        b'\x00\x59':{    #Motion Enhancer
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'Low',
					                                    b'\x00\x02':'High'
					                                    },
					                        b'\x00\x5A':{    #xvColor
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'On'
					                                    },
					                        b'\x00\x60':{	#2D-3D Display Select
					                        			b'\x00\x00':'Auto',
					                                    b'\x00\x01':'3D',
					                                    b'\x00\x02':'2D'
					                                    },
					                        b'\x00\x61':{	#3D Format
					                        			b'\x00\x00':'Simulated 3D',
					                                    b'\x00\x01':'Side-By-Side',
					                                    b'\x00\x02':'Over-Under'
					                                    },
					                        b'\x00\x63':{	#Simulated 3D Effect
					                        			b'\x00\x00':'High',
					                                    b'\x00\x01':'Middle',
					                                    b'\x00\x02':'Low'
					                                    },
					                        b'\x00\x67':{    #Reality Creation
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'On'
					                                    },
					                        b'\x00\x6C':{    #MPEG NR
					                                    b'\x00\x00':'Off',
					                                    b'\x00\x01':'Low',
					                                    b'\x00\x02':'High',
					                                    b'\x00\x03':'Middel'
					                                    },
					                        b'\x00\x6E':{	#HDMI 1 Dynamic Range
					                        			b'\x00\x00':'Auto',
					                                    b'\x00\x01':'Limit',
					                                    b'\x00\x02':'Full'
					                                    },
					                        b'\x00\x6F':{	#HDMI 2 Dynamic Range
					                        			b'\x00\x00':'Auto',
					                                    b'\x00\x01':'Limit',
					                                    b'\x00\x02':'Full'
					                                    },
					                        b'\x00\x73':{	#Settings Lock
					                        			b'\x00\x00':'Off',
					                                    b'\x00\x01':'Level A',
					                                    b'\x00\x02':'Level B'
					                                    },
					                        b'\x01\x01':{    #Status Error
					                                    b'\x00\x00':'No Error',
					                                    b'\x00\x01':'Lamp Error',
					                                    b'\x00\x02':'Fan Error',
					                                    b'\x00\x04':'Cover Error',
					                                    b'\x00\x08':'Temp Error',
					                                    b'\x00\x10':'D5V Error',
					                                    b'\x00\x20':'Power Error',
					                                    b'\x00\x40':'Warning Error',
					                                    b'\x00\x80':'NVM Data Error'
					                                    },
					                        b'\x01\x02':{    #Status Power
					                                    b'\x00\x00':'Standby',
					                                    b'\x00\x01':'Start Up',
					                                    b'\x00\x02':'Startup Lamp',
					                                    b'\x00\x03':'Power On',
					                                    b'\x00\x04':'Cooling1',
					                                    b'\x00\x05':'Cooling2',
					                                    b'\x00\x06':'Saving Cooling1',
					                                    b'\x00\x07':'Saving Cooling2',
					                                    b'\x00\x08':'Saving Standby'
					                                    },
					                        b'\x01\x25':{    #Status Error
					                                    b'\x00\x00':'No Error',
					                                    b'\x00\x20':'Highland Warning'
					                                    }
					                        },
					                b'\x03':{    #Quick Reply
					                        b'\x00\x00':'ACK Success',
					                        b'\x01\x01':'Undefined Command',
					                        b'\x00\x04':'Size Error',
					                        b'\x01\x05':'Select Error',
					                        b'\x01\x06':'Range Over',
					                        b'\x01\x0A':'Not Applicable',
					                        b'\xF0\x10':'Checksum Error',
					                        b'\xF0\x20':'Framing Error',
					                        b'\xF0\x30':'Parity Error',
					                        b'\xF0\x40':'Over Rub Error',
					                        b'\xF0\x50':'Other Comm Error'
					                        }
					            }

		if self.verbose: print('Initiating Serial Object')
		self.__serialObj = serial.Serial(port=port, baudrate=baud, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout)
		if self.verbose: print('Serial Object Initiated')

	def __getCommand(self, action, item, data=b'\x00\x00'):
		startCode = b'\xA9'
		endCode = b'\x9A'
		actionList = {'Get': b'\x01', 'Set': b'\x00'}
		checksum = self.__getChecksum(actionList[action], self.__itemList[action][item], data)
		command = startCode
		command += self.__itemList[action][item]
		command += actionList[action]
		command += data
		command += checksum
		command += endCode
		return command

	def __getChecksum(self, action, item, data):
		#if self.verbose: print("Calculating Checksum")
		item += action
		item += data
		result = 0x00
		for hexValue in item:
			#if self.verbose: print("Checksum: %s OR'd with %s = %s" % (result, hexValue, result|hexValue))
			result = result|hexValue
		return bytes([result])

	def __sendPing(self):
		if self.verbose: print("Sending Ping")
		if not self.__serialObj.isOpen():
			self.__serialObj.open()
		currentSerialSettings = self.getSerialSettings()
		self.setSerialSetting('timeout', .05)
		self.__serialObj.write(self.__getCommand('Get', 'Status Power'))
		if self.verbose: print("Ping Sent")
		self.__serialObj.read(size=8)
		self.setSerialSetting('timeout', currentSerialSettings['timeout'])

	def __sendCommand(self, command, response=True):
		resp = b''
		
		while resp == b'':
			if not self.__serialObj.isOpen():
				self.__serialObj.open()
				#print('sending ' + binascii.hexlify(command).decode("utf-8") + ' to ' + self.__serialObj.name)
			bwritten = self.__serialObj.write(command)
			time.sleep(self.commandDelay)
				#print("Bytes Written: %s" % bwritten)
			if response:
				resp = bytearray(self.__serialObj.read(size=8))
			else:
				return b''
		return resp

	def __parseResult(self, result):
	    
	    contrast        =b'\x00\x10'
	    brightness      =b'\x00\x11'
	    color           =b'\x00\x12'
	    hue             =b'\x00\x13'
	    sharpness       =b'\x00\x14'
	    user_gain_red   =b'\x00\x50'
	    user_gain_green =b'\x00\x51'
	    user_gain_blue  =b'\x00\x52'
	    user_bias_red   =b'\x00\x53'
	    user_bias_green =b'\x00\x54'
	    user_bias_blue  =b'\x00\x55'
	    iris_manual     =b'\x00\x57'
	    ThreeD_depth_adj=b'\x00\x62'
	    ThreeD_glasses_brightness=b'\x00\x65'
	    resolution 		=b'\x00\x68'
	    noice_filtering	=b'\x00\x69'
	    lamp_timer      =b'\x01\x13'

	    startCode=bytes([result[0]])
	    itemAck = bytes(result[1:3])
	    replyType = bytes([result[3]])
	    rcvData = bytes(result[4:6])
	    checksum = bytes([result[6]])
	    endCode= bytes([result[7]])

	    if replyType == b'\x02':
	        if itemAck in [contrast, brightness, color, hue, sharpness,
	                        user_gain_red, user_gain_green, user_gain_blue, 
	                        user_bias_red, user_bias_green, user_bias_blue,
	                        iris_manual, ThreeD_depth_adj, ThreeD_depth_adj, 
	                        ThreeD_glasses_brightness, resolution, noice_filtering, lamp_timer]:
	            value=int(binascii.hexlify(rcvData), 16)
	            if value > 0x7FFFFFFF:
	                value -= 0x100000000
	            return value
	        else:
	            return self.__validResponses[replyType][itemAck][rcvData]
	    elif replyType == b'\x03':
	        return self.__validResponses[replyType][itemAck]

	def __setSetting(self, item, value):
		data=b''
		if item in self.__validSettings and value in self.__validSettings[item]:
			data = self.__validSettings[item][value]
		else:
			print('ERROR: Invalid item/value combination: %s[%s]' % (item, value))
			return False	
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Set', item, data=data)))
		if result == 'ACK Success':
			return True
		else:
			return False

##############################################
####### Remote Control Button Functions ######
##############################################

	def rMotionEnhancerToggle(self):
		self.__sendCommand(self.__getCommand('Set', 'Motion Enhancer Toggle'), response=False)

	def rContrastEnhancerToggle(self):
		self.__sendCommand(self.__getCommand('Set', 'Contrast Enhancer Toggle'), response=False)

	def rFilmProjection(self):
		self.__sendCommand(self.__getCommand('Set', 'Remote Film Projection'), response=False)

	def rPowerToggle(self):
		self.__sendCommand(self.__getCommand('Set', 'Power Toggle'), response=False)

	def rContrastPlus(self):
		self.__sendCommand(self.__getCommand('Set', 'Contrast +'), response=False)

	def rContrastMinus(self):
		self.__sendCommand(self.__getCommand('Set', 'Contrast -'), response=False)

	def rColorPlus(self):
		self.__sendCommand(self.__getCommand('Set', 'Color +'), response=False)

	def rColorMinus(self):
		self.__sendCommand(self.__getCommand('Set', 'Color -'), response=False)

	def rBrightnessPlus(self):
		self.__sendCommand(self.__getCommand('Set', 'Brightness +'), response=False)

	def rBrightnessMinus(self):
		self.__sendCommand(self.__getCommand('Set', 'Brightness -'), response=False)

	def rHuePlus(self):
		self.__sendCommand(self.__getCommand('Set', 'Hue +'), response=False)

	def rHueMinus(self):
		self.__sendCommand(self.__getCommand('Set', 'Hue -'), response=False)

	def rSharpnessPlus(self):
		self.__sendCommand(self.__getCommand('Set', 'Sharpness +'), response=False)

	def rSharpnessMinus(self):
		self.__sendCommand(self.__getCommand('Set', 'Sharpness -'), response=False)

	def rPictureMuting(self):
		self.__sendCommand(self.__getCommand('Set', 'Remote Picture Muting'), response=False)

	def rStatusOn(self):
		self.__sendCommand(self.__getCommand('Set', 'Status On'), response=False)

	def rStatusOff(self):
		self.__sendCommand(self.__getCommand('Set', 'Status Off'), response=False)

	def rMenu(self):
		self.__sendCommand(self.__getCommand('Set', 'Menu'), response=False)

	def rInputA(self):
		self.__sendCommand(self.__getCommand('Set', 'Input A'), response=False)

	def rComponent(self):
		self.__sendCommand(self.__getCommand('Set', 'Component'), response=False)

	def rPowerOn(self):
		if self.verbose: print("Turning Power On")
		self.__sendCommand(self.__getCommand('Set', 'Power On'), response=False)

		currentPhase = None
		previousPhase = None

		while True:
			currentPhase = self.getStatusPower()
			if currentPhase != previousPhase:
				previousPhase = currentPhase
				if self.verbose: print("Phase: %s" % currentPhase)
				if currentPhase == 'Power On':
					return True

	def rPowerOff(self):
		if self.verbose: print("Turning Power Off")
		self.__sendCommand(self.__getCommand('Set', 'Power Off'), response=False)

		currentPhase = None
		previousPhase = None

		while True:
			currentPhase = self.getStatusPower()
			if currentPhase != previousPhase:
				previousPhase = currentPhase
				if currentPhase in ('Power Off', 'Standby'):
					if self.verbose: print("Phase: %s" % currentPhase)
					return True
				else:
					if self.verbose: print("Phase: %s" % currentPhase)

	def rCursorUp(self):
		self.__sendCommand(self.__getCommand('Set', 'Cursor Up'), response=False)

	def rCursorDown(self):
		self.__sendCommand(self.__getCommand('Set', 'Cursor Down'), response=False)

	def rCursorLeft(self):
		self.__sendCommand(self.__getCommand('Set', 'Cursor Left'), response=False)

	def rCursorRight(self):
		self.__sendCommand(self.__getCommand('Set', 'Cursor Right'), response=False)

	def rPitch(self):
		self.__sendCommand(self.__getCommand('Set', 'Pitch'), response=False)

	def rInputSelect(self):
		self.__sendCommand(self.__getCommand('Set', 'Input Select'), response=False)

	def rEnter(self):
		self.__sendCommand(self.__getCommand('Set', 'Enter'), response=False)

	def rHDMI1(self):
		self.__sendCommand(self.__getCommand('Set', 'HDMI 1'), response=False)

	def rHDMI2(self):
		self.__sendCommand(self.__getCommand('Set', 'HDMI 2'), response=False)

	def rReset(self):
		self.__sendCommand(self.__getCommand('Set', 'Reset'), response=False)

##############################################
####### Getter Functions - Code Values #######
##############################################

	def getValidSourceInputs(self):
		return self.__validSettings['Input'].keys()

	def getSerialSettings(self):
		return self.__serialObj.get_settings()

##############################################
#### Getter Functions - Projector Values #####
##############################################

	def getCurrentState(self):
		settings = self.__itemList['Get']
		settingValues = {}

		for key in settings.keys():
			settingValue = self.__parseResult(self.__sendCommand(self.__getCommand('Get', key)))
			if key == 'Status Power' and settingValue == 'Not Applicable':
				settingValues[key] = 'Power Off'
			elif settingValue != 'Not Applicable':
				settingValues[key] = settingValue

		return settingValues

	def getInput(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Input')))
		return result

	def getCalibrationPreset(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Calibration Preset')))
		return result

	def getContrast(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Contrast')))
		return result

	def getBrightness(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Brightness')))
		return result

	def getColor(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Color')))
		return result

	def getHue(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Hue')))
		return result

	def getSharpness(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Sharpness')))
		return result

	def getColorTemp(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Color Temp')))
		return result

	def getLampControl(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Lamp Control')))
		return result

	def getContrastEnhancer(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Contrast Enhancer')))
		return result

	def getAdvancedIris(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Advanced Iris')))
		return result

	def getRealColorProcessing(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Real Color Processing')))
		return result

	def getFilmMode(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Film Mode')))
		return result

	def getAspect(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Aspect')))
		return result

	def getGammaCorrection(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Gamma Correction')))
		return result

	def getOverScan(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Over Scan')))
		return result

	def getScreenArea(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Screen Area')))
		return result

	def getNoiseReduction(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Noise Reduction')))
		return result

	def getPictureMuting(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Picture Muting')))
		return result

	def getColorSpace(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Color Space')))
		return result

	def getUserGainRed(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Gain Red')))
		return result

	def getUserGainGreen(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Gain Green')))
		return result

	def getUserGainBlue(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Gain Blue')))
		return result

	def getUserBiasRed(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Bias Red')))
		return result

	def getUserBiasGreen(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Bias Green')))
		return result

	def getUserBiasBlue(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'User Bias Blue')))
		return result

	def getIrisManual(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Iris Manual')))
		return result

	def getFilmProjection(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Film Projection')))
		return result

	def getMotionEnhancer(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Motion Enhancer')))
		return result

	def getxvColor(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'xvColor')))
		return result

	def get2D3DDisplaySelect(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', '2D-3D Display Select')))
		return result

	def get3DFormat(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', '3D Format')))
		return result

	def get3DDepthAdjust(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', '3D Depth Adjust')))
		return result

	def getSimulated3DEffect(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Simulated 3D Effect')))
		return result

	def get3DGlassesBrightness(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', '3D Glasses Brightness')))
		return result

	def getRealityCreation(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Reality Creation')))
		return result

	def getResolution(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Resolution')))
		return result

	def getNoiseFiltering(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Noise Filtering')))
		return result

	def getMPEGNoiseReduction(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'MPEG Noise Reduction')))
		return result

	def getHDMI1DynamicRange(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'HDMI 1 - Dynamic Range')))
		return result

	def getHDMI2DynamicRange(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'HDMI 2 - Dynamic Range')))
		return result

	def getSettingsLock(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Settings Lock')))
		return result

	def getStatusError(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Status Error')))
		return result

	def getStatusPower(self):
		powerStatus = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Status Power')))
		if powerStatus == 'Not Applicable':
			powerStatus = 'Power Off'
		return powerStatus

	def getLampTimer(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Lamp Timer')))
		return result

	def getStatusError2(self):
		result = self.__parseResult(self.__sendCommand(self.__getCommand('Get', 'Status Error (2)')))
		return result


##############################################
####### Setter Functions - Code Values #######
##############################################

	def setSerialSetting(self, key, value):
		if self.verbose: print("Setting Serial Setting [%s] to [%s]" % (key, value))
		serialSettings = self.getSerialSettings()
		if key in serialSettings:
			serialSettings[key] = value
			self.__serialObj.apply_settings(serialSettings)
			return True
		else:
			print('Error: Setting [%s] is invalid' % key)
			return False

#####################################################
## Setter Functions - Pre-Defined Projector Values ##
#####################################################

	def setInput(self, value):
		result = self.__setSetting('Input', value)
		return result

	def setCalibrationPreset(self, value):
		result = self.__setSetting('Calibration Preset', value)
		return result

	def setColorTemp(self, value):
		result = self.__setSetting('Color Temp', value)
		return result

	def setLampControl(self, value):
		result = self.__setSetting('Lamp Control', value)
		return result

	def setContrastEnhancer(self, value):
		result = self.__setSetting('Contrast Enhancer', value)
		return result

	def setAdvancedIris(self, value):
		result = self.__setSetting('Advanced Iris', value)
		return result

	def setRealColorProcessing(self, value):
		result = self.__setSetting('Real Color Processing', value)
		return result

	def setFilmMode(self, value):
		result = self.__setSetting('Film Mode', value)
		return result

	def setAspect(self, value):
		result = self.__setSetting('Aspect', value)
		return result

	def setGammaCorrection(self, value):
		result = self.__setSetting('Gamma Correction', value)
		return result

	def setOverScan(self, value):
		result = self.__setSetting('Over Scan', value)
		return result

	def setScreenArea(self, value):
		result = self.__setSetting('Screen Area', value)
		return result

	def setNoiseReduction(self, value):
		result = self.__setSetting('Noise Reduction', value)
		return result

	def setPictureMuting(self, value):
		result = self.__setSetting('Picture Muting', value)
		return result

	def setColorSpace(self, value):
		result = self.__setSetting('Color Space', value)
		return result

	def setFilmProjection(self, value):
		result = self.__setSetting('Film Projection', value)
		return result

	def setMotionEnhancer(self, value):
		result = self.__setSetting('Motion Enhancer', value)
		return result

	def setxvColor(self, value):
		result = self.__setSetting('xvColor', value)
		return result

	def set2D3DDisplaySelect(self, value):
		result = self.__setSetting('2D-3D Display Select', value)
		return result

	def set3DFormat(self, value):
		result = self.__setSetting('3D Format', value)
		return result

	def setSimulated3DEffect(self, value):
		result = self.__setSetting('Simulated 3D Effect', value)
		return result

	def setRealityCreation(self, value):
		result = self.__setSetting('Reality Creation', value)
		return result

	def setMPEGNoiseReduction(self, value):
		result = self.__setSetting('MPEG Noise Reduction', value)
		return result

	def setHDMI1DynamicRange(self, value):
		result = self.__setSetting('HDMI 1 - Dynamic Range', value)
		return result

	def setHDMI2DynamicRange(self, value):
		result = self.__setSetting('HDMI 2 - Dynamic Range', value)
		return result

	def setSettingsLock(self, value):
		result = self.__setSetting('Settings Lock', value)
		return result