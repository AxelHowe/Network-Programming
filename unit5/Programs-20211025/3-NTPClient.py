####################################################
#  Network Programming - Unit 5  User Datagram Protocol          
#  Program Name: 3-NTPClient.py                                      			
#  This program implements NTP client.           		
#  2021.07.16                                                  									
####################################################
import sys
import socket
import struct
import binascii
import time
import datetime
import math

PORT = 123				# NTP port
BUF_Size = 1024

"""
	// NTP Packet Format       Total: 384 bits or 48 bytes.
    //uint8_t li_vn_mode;      // Eight bits. li, vn, and mode.
                               // li.   Two bits.   Leap indicator.
                               // vn.   Three bits. Version number of the protocol.
                               // mode. Three bits. Client will pick mode 3.

    //uint8_t stratum;         // Eight bits. Stratum level of the local clock.
    //uint8_t poll;            // Eight bits. Maximum interval between successive messages.
    //uint8_t precision;       // Eight bits. Precision of the local clock.

    //uint32_t rootDelay;      // 32 bits. Total round trip delay time.
    //uint32_t rootDispersion; // 32 bits. Max error aloud from primary clock source.
    //uint32_t refId;          // 32 bits. Reference clock identifier.

    //uint32_t refTm_s;        // 32 bits. Reference time-stamp seconds.
    //uint32_t refTm_f;        // 32 bits. Reference time-stamp fraction of a second.

    //uint32_t origTm_s;       // 32 bits. Originate time-stamp seconds.
    //uint32_t origTm_f;       // 32 bits. Originate time-stamp fraction of a second.

    //uint32_t rxTm_s;         // 32 bits. Received time-stamp seconds.
    //uint32_t rxTm_f;         // 32 bits. Received time-stamp fraction of a second.

    //uint32_t txTm_s;         // 32 bits and the most important field the client cares about. Transmit time-stamp seconds.
    //uint32_t txTm_f;         // 32 bits. Transmit time-stamp fraction of a second.
"""

class NTPMessage:
	def __init__(self, packed_data):			# the input is the received NTP message block
		s = struct.Struct('!' + '48B')				# Convert to byte array
		value = s.unpack(packed_data)
		
		self.leapIndicator = (value[0] >> 6) & 3	# 2 bits
		self.version = (value[0] >> 3) & 7				# 3 bits
		self.msg_mode = value[0] & 7					# 3 bits
		
		self.stratum = value[1]
		self.poll = value[2]
		self.precision = value[3]

		self.rootDelay  = (float(value[4]) * 256) + float(value[5]) + (float(value[6]) / 256) + (float(value[7]) / 65536)
				# fraction point between bits 15 and 16
		self.rootDispersion = (float(value[8]) * 256) + float(value[9]) + (float(value[10]) / 256) + (float(value[11]) / 65536)
				# fraction point between bits 15 and 16
		
		s = struct.Struct('!' + 'B B B B')
		temp = (value[12], value[13], value[14], value[15])
		temp = s.pack(*temp)
		s = struct.Struct('!' + 'I')
		self.refid = s.unpack(temp)[0]
		
		self.refTm = self.getTimestamp(value, 16)
		self.origTm = self.getTimestamp(value, 24)
		self.rxTm = self.getTimestamp(value, 32)
		self.txTm = self.getTimestamp(value, 40)
	# end of __init__()
	
	def getTimestamp(self, v, base):
		r = float(0)
		for i in range(8):
			r += v[base+i] * math.pow(2, (3-i)*8)
		return r
	# end of getTimestamp()
	
	def toString(self):
		retStr = "Leap indicator: " + str(self.leapIndicator) + "\n" + \
			 "Version: " + str(self.version) + "\n" + \
			 "Mode: "	+ str(self.msg_mode) + "\n" +\
			 "Stratum: " + str(self.stratum) + "\n" +\
			 "Poll: " + str(self.poll) + "\n" +\
			 "Precision: " + str(self.precision) + "\n" +\
			 "Root delay: " + str(self.rootDelay * 1000) + " ms\n" +\
			 "Root dispersion: " + str(self.rootDispersion * 1000) + " ms\n" +\
			 "Reference identifier: " + self.refid2String() + "\n" +\
			 "Reference timestamp: "	+ time.ctime(self.refTm - float(2208988800.0)) + "\n" +\
			 "Originate timestamp: "	+ time.ctime(self.origTm - float(2208988800.0)) + "\n" +\
			 "Receive timestamp: " + time.ctime(self.rxTm - float(2208988800.0)) + "\n" +\
			 "Transmit timestamp: " + time.ctime(self.txTm - float(2208988800.0))
		return retStr
	# end of toString
	
	def refid2String(self):
		s = struct.Struct('!' + 'I')
		temp = s.pack(*(self.refid, ))
		s = struct.Struct('!' + 'B B B B')
		temp = s.unpack(temp)
		# In the case of NTP Version 3 or Version 4 stratum-0 (unspecified)
		# or stratum-1 (primary) servers, this is a four-character ASCII
		# string, left justified and zero padded to 32 bits.
		if(self.stratum == 0) or (self.stratum == 1):
			return chr(temp[0]) + chr(temp[1]) + chr(temp[2]) + chr(temp[3])
		
		# In NTP Version 3 secondary servers, this is the 32-bit IPv4
		# address of the reference source.
		elif(self.version == 3):
			return str(temp[0]) + '.' + str(temp[1]) + '.' + str(temp[2]) + '.' + str(temp[3])

		# In NTP Version 4 secondary servers, this is the low order 32 bits
		# of the latest transmit timestamp of the reference source.
		elif(self.version == 4):
			val = (float(temp[0]) / 256) + (float(temp[1]) / 65536) + (float(temp[2]) / 16777216) + (float(temp[3]) / 4294967296)
			return str(val)
		else:
			return ''
	# end of refid2String
# end of class NTPMessage

def requestMessage():
	# get current time
	ct = datetime.datetime.now()
	ts = ct.timestamp() + float(2208988800.0)
	
	# transfer ts into 64 bits integer and assign to txTm
	buf = [0] * 8
	for i in range(8):
		# 2^24, 2^16, 2^8, .. 2^-32
		base = math.pow(2, (3-i)*8)
		buf[i] = int(ts / base)
		ts = ts - float(buf[i]) * base
	s = struct.Struct('!' + 'B B B B B B B B')
	packed_data = s.pack(*buf)
	s = struct.Struct('!' + 'Q')
	txTm = s.unpack(packed_data)[0]

	# prepare data
	leapIndicator=0
	version=3
	msg_mode=3
	first_byte = ((leapIndicator & 3) << 6) | ((version & 7) << 3) | (msg_mode & 7)
	stratum=0
	poll=0
	precision=0
	rootDelay=0
	rootDispersion=0
	refid=0
	refTm=0
	origTm=0
	rxTm=0

	# pack message
	s = struct.Struct('!' + 'B B B B I I I Q Q Q Q')
	value = (first_byte, stratum, poll, precision, rootDelay, rootDispersion, refid, refTm, origTm, rxTm, txTm)
	packed_data = s.pack(*value)
	
	return packed_data
# end of packTime

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 3-NTPClient.py ServerIP (Ex: clock.stdtime.gov.tw) \n")
		exit(1)

	# Get server IP
	serverIP = socket.gethostbyname(sys.argv[1])
	
	# Create a UDP client socket
	dgramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	# Create a NTP request message and send
	req_meaasge = requestMessage()
	# print('Packed Value   :', binascii.hexlify(req_meaasge))
	dgramSocket.sendto(req_meaasge, (serverIP, PORT))

	# Receive server reply
	srv_msg, (rip, rport) = dgramSocket.recvfrom(BUF_Size)
	msg = 'Receive reply from IP: ' + str(rip) + ' port: ' + str(rport)
	print(msg)
	# print('Packed Value   :', binascii.hexlify(srv_msg))
	ntp_msg = NTPMessage(srv_msg)
	print(ntp_msg.toString())

	# Close the UDP socket
	dgramSocket.close()
# end of main

if __name__ == '__main__':
	main()
