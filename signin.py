#!/bin/python
import mysql.connector
import re, datetime

f = open("password","r")
userpass = f.readlines()
userpass = [x.strip() for x in userpass]
userpass = ''.join(userpass)
f.close()

def gettime():
	global now
	now = datetime.datetime.now()

def addtosheet(name, userinput):
	global now
	gettime()
	date = now.strftime("%Y-%m-%d")
	
	gettime()
	time = now.strftime("%H:%M:%S")
	
	cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')
	cursor = cnx.cursor()
	
	query = ("SELECT capid FROM TuesdayMeeting WHERE capid={} AND date='{}';".format(userinput, date))
	
	cursor.execute(query)
	rows = cursor.fetchall()
	if rows == []:
		query = ("INSERT INTO TuesdayMeeting (date, capid, name, time_in) VALUES ('{0}', '{1}', '{2}', '{3}');".format(date, userinput, name, time))
		cursor.execute(query)
		cnx.commit()
		print("Member signed in")
		
	else:
		print("Signing out")
		query = ("UPDATE TuesdayMeeting SET time_out = '{0}' WHERE capid={1} AND date='{2}';".format(time, userinput, date))
		cursor.execute(query)
		cnx.commit()
		print("Member signed out")

def adduser(userinput):
	first_name = raw_input("Please enter your First name:")
	last_name = raw_input("Please enter your Last name:")
	membertype = raw_input("Are you a cadet, senior, visiter:")
	
	print("Cap ID:" + userinput)
	print("First name:" + first_name)
	print("Last name:" + last_name)
	print("Member type:" + membertype)
	
	yesno = raw_input("Is the information correct?[y/n]:")

	if yesno == "y":
		cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')
		cursor = cnx.cursor()

		query = ("INSERT INTO SQmembers (capid, First_name, Last_name, member_type) VALUES ({0}, '{1}', '{2}', '{3}');".format(userinput, first_name, last_name, membertype))

		cursor.execute(query)
		cnx.commit()
	
		cursor.close()
		cnx.close()

	else:readbarcode()

def readbarcode():
	userinput = raw_input("Plese enter CAP ID:")
	connect(userinput)
	
	
def connect(userinput):
	cnx = mysql.connector.connect(user='root', password=userpass, host='localhost', database='BoiseCAP073')
	cursor = cnx.cursor()
	
	query = ("SELECT First_name, Last_name FROM SQmembers WHERE capid={};".format(userinput))
	
	cursor.execute(query)
	
	rows = cursor.fetchall()
	if rows == []:adduser(userinput)
	
	cursor.execute(query)
	for (Last_name) in cursor:
		name = ""
		blank = " "
		for key in Last_name:
			name = name + blank + key

		name = name + blank + userinput
		print(name)
		
	cursor.close()
	cnx.close()
	addtosheet(name, userinput)

while True:
	readbarcode()
