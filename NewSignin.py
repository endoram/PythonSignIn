#!/bin/python
import mysql.connector			#Import the mysql libray that allows us to connect to the database
import re, datetime, subprocess		#Import re to handle strings and datetime to get current date and time

f = open("password","r")		#Open the file for the mysql database password
userpass = f.readlines()
userpass = [x.strip() for x in userpass]
userpass = ''.join(userpass)
f.close()				#Close the file


def check(userinput):
  #This function validates the input from barcode
	inputcheck = userinput.isdigit()    #makes sure the input is all numbers
	if (inputcheck == False):           #If it is not:
		print("		INVALID CAPID")
		print("	      Please try again")
		readbarcode()


def gettime():
	'''This function gets the current date and time saves into variable now'''
	global now
	now = datetime.datetime.now()

def addtosheet(name, userinput):
	'''addtosheet take to arguments name and userinput, this function determins if you are signing in or out'''
	global now
	gettime()
	date = now.strftime("%Y-%m-%d")			#Strips down to get year month date
	
	gettime()					#Refresh the var to get hour min second
	time = now.strftime("%H:%M:%S")
	
	#Connects to database
	cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')
	cursor = cnx.cursor()
	
	#MYSQL Command / our query
	query = ("SELECT capid FROM TuesdayMeeting WHERE capid={} AND date='{}';".format(userinput, date))
	
	cursor.execute(query)		#Execute the query
	rows = cursor.fetchall()
	if rows == []:			#If nothing is returned:
		
		#Ths query add the user scanned to the TuesdayMeeting table in the BoiseCAP073 database
		query = ("INSERT INTO TuesdayMeeting (date, capid, name, time_in) VALUES ('{0}', '{1}', '{2}', '{3}');".format(date, userinput, name, time))
		cursor.execute(query)
		cnx.commit()				#If we dont commit our changes will not be recognized when we SELECT * next
		subprocess.call(["clear"])
		print(name)
		print("Member signed in")
		
	else:						#If rows returned a value other then empty
  :
		#Update the line already in the database instead of adding a new row
		query = ("UPDATE TuesdayMeeting SET time_out = '{0}' WHERE capid={1} AND date='{2}';".format(time, userinput, date))
		cursor.execute(query)
		cnx.commit()
		subprocess.call(["clear"])
		print(name)
		print("Member signed out")
		
	cursor.close()
	cnx.close()
	readbarcode()

def adduser(userinput):
	print("		USER NOT IN DATABASE")
	print("        Please talk to (INSERT CADET NAME HERE)")
	readbarcode()

  #This is commented out becuase it slows down the process of cadets signing in
	'''This function is called when the scanned id is not in the database
	#raw_input is used to get input from the user
	first_name = raw_input("Please enter your First name:")
	last_name = raw_input("Please enter your Last name:")
	membertype = raw_input("Are you a cadet, senior, visiter:")
	
	print("Cap ID:" + userinput)
	print("First name:" + first_name)
	print("Last name:" + last_name)
	print("Member type:" + membertype)
	
	yesno = raw_input("Is the information correct?[y/n]:")

	#If state ment that checks if you answer yes or no
	if yesno != "n" and yesno != "N":
		cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')	#Connect to database
		cursor = cnx.cursor()

		#This addes them as a member in the SQmembers table
		query = ("INSERT INTO SQmembers (capid, First_name, Last_name, member_type) VALUES ({0}, '{1}', '{2}', '{3}');".format(userinput, first_name, last_name, membertype))

		cursor.execute(query)
		cnx.commit()
	
		cursor.close()
		cnx.close()
		readbarcode()

	else:
		print("Going back to readbarcode")
		readbarcode()		#If you enter no it will take you back to scan a card

	'''

def readbarcode():
	'''The read barcode function takes in userinput'''
	userinput = raw_input("Please enter CAP ID:")
	check(userinput)        #Validates user input might be a cap ID
	connect(userinput)	#Pass the var userinput into the connect function
	


	
def connect(userinput):
	'''connect function is used to check if you are a valid user or not'''
	cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')
	cursor = cnx.cursor()
	
	#Check if your cap id is in the database
	query = ("SELECT First_name, Last_name FROM SQmembers WHERE capid={};".format(userinput))
	

	cursor.execute(query)

	rows = cursor.fetchall()
	if rows == []:adduser(userinput)		#Check if there is anything from the query
	
	cursor.execute(query)
	for (Last_name) in cursor:
		name = ""
		blank = " "
		for key in Last_name:			#Loops through Last_name array and puts them into a plsent way to view them
			name = name + blank + key

		name = name + blank + userinput
#		print(name)
		
	cursor.close()
	cnx.close()
	addtosheet(name, userinput)			#If a vaild user is present then it will go back up to add to sheet

#Keeps program running
while True:
	readbarcode()
