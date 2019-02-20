 # -*- coding: utf-8 -*-
import os
import sys
import csv
import sqlite3

conn = sqlite3.connect('lexicogender.db')
c = conn.cursor()

c.execute("select lexico, sum(feminin), sum(masculin), count(*) from lexico_element group by lexico;")

with open(os.getcwd() + '/lexicostats.csv', 'wb') as csvstats, open(os.getcwd() + '/lexicoelements.csv', 'wb') as csvelements:
	csvwriter = csv.writer(csvstats, delimiter = ';', quotechar = '|')
	elementswriter = csv.writer(csvelements, delimiter = ';', quotechar = '|')

	for row in c.fetchall():
		lexico = row[0].encode("utf8")
		print [lexico,row[2:]]
		csvwriter.writerow([lexico,row[1],row[2],row[3]])

	c.execute("select * from lexico_element ")
	for r in c.fetchall():
		print r
		elementswriter.writerow([r[1].encode("utf8"), str(r[2]).encode("utf8"), r[3].encode("utf8"), str(r[4]).encode("utf8"), r[5], r[6]])
		#elementswriter.writerow(r)