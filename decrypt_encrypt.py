#Decrypt/Encrypt Files

import socket
import select
import sys
import os
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

# Encryption and Decryption function
def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "(encrypted)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)

# Key for encryption and decryption
def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

# Main Function
def Main():
	host = '127.0.0.1'
	port = 5000

	s = socket.socket()
	s.bind((host, port))
	s.listen(5)

	print("Server Started.")
	c, addr = s.accept()
	print("Client connected ip:<" + str(addr) + ">")

	while True:
		command = input("Enter command: ")
		if command == 'quit':
			c.send(command.encode('utf-8'))
			break
		elif command == 'list':
			c.send(command.encode('utf-8'))
			data = c.recv(1024).decode('utf-8')
			print(data)
		elif 'download' in command:
			c.send(command.encode('utf-8'))
			data = c.recv(1024).decode('utf-8')
			if data[:6] == 'EXISTS':
				filesize = int(data[6:])
				message = input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
				if message == 'Y':
					c.send('OK'.encode('utf-8'))
					f = open('new_'+command[9:], 'wb')
					data = c.recv(1024)
					totalRecv = len(data)
					f.write(data)
					while totalRecv < filesize:
						data = c.recv(1024)
						totalRecv += len(data)
						f.write(data)
						print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done")
					print("Download Complete!")
			else:
				print("File Does Not Exist!")
		elif 'upload' in command:
			c.send(command.encode('utf-8'))
			data = c.recv(1024).decode('utf-8')
			if data[:6] == 'EXISTS':
				filesize = int(data[6:])
				message = input("File exists, " + str(filesize) +"Bytes, upload? (Y/N)? -> ")
				if message == 'Y':
					c.send('OK'.encode('utf-8'))
					f = open('new_'+command[7:], 'rb')
					data = f.read(1024)
					totalSend = len(data)
					while True:
						c.send(data)
						data = f.read(1024)
						totalSend += len(data)
						print("{0:.2f}".format((totalSend/float(filesize))*100)+ "% Done")
						if not data:
							break
					f.close()
					print("Upload Complete!")
			else:
				print("File Does Not Exist!")
		elif 'encrypt' in command:
			c.send(command.encode('utf-8'))
			key = getKey(input("Enter password: "))
			filename = input("File to encrypt: ")
			encrypt(key, filename)
			print("Done Encryption!")
		elif 'decrypt' in command:
			c.send(command.encode('utf-8'))
			key = getKey(input("Enter password: "))
			filename = input("File to decrypt: ")
			decrypt(key, filename)
			print("Done Decryption!")
		else:
			c.send(command.encode('utf-8'))
			data = c.recv(1024).decode('utf-8')
			print(data)

	c.close()

if __name__ == '__main__':
	Main()
