 # -*- coding: utf-8 -*-
import os
import sys
import csv
from bs4 import BeautifulSoup
import urllib2
import sqlite3

lexicolist = sys.argv[1]

conn = sqlite3.connect('lexicogender.db')
c = conn.cursor()

curdir = os.getcwd()
lexicolist = curdir + '/' + lexicolist
print lexicolist

countertotal = 0
counterinvalid = 0
counteracronym = 0

with open(lexicolist, 'rb') as lexicocsv, open('lexicostats.txt', 'wb') as lexicostatscsv:
	lexicoreader = csv.reader(lexicocsv, delimiter = ';', quotechar='|')
	lexicostatswriter = csv.writer(lexicostatscsv, delimiter = ';', quotechar='|')
	for l in lexicoreader:
		lexicourl = str(l[0])
		print lexicourl
		lexicoreq = urllib2.Request(lexicourl)
		handle = urllib2.urlopen(lexicoreq)
		lexicopage = handle.read()
		#print lexicopage

		lexicosoup = BeautifulSoup(lexicopage,"html.parser")
		for li in lexicosoup.find_all('li'):
			if str(li)[5:10] == 'a hre':
				countertotal = countertotal + 1
				libalise = str(li)[5:10]
				lititle = str(li).split('title="')[1].split('"')[0]
				liurl = "https://fr.wiktionary.org/wiki/" + str(li).split('wiki/')[1].split('"')[0]
				print l[1]
				print libalise,' ', lititle,' ', liurl
				if lititle.startswith("Catégorie") or len(lititle.split(' ')) > 1 or lititle.split(' ')[0].endswith('isme') or lititle.split(' ')[0].endswith('tion'):
					counterinvalid = counterinvalid + 1
					continue
				elementreq = urllib2.Request(liurl)
				handle = urllib2.urlopen(elementreq)
				elementpage = handle.read()
				elementsoup = BeautifulSoup(elementpage,"html.parser")
				index = str(elementsoup).find("ligne-de-forme")
				genre = str(elementsoup)[index+19:index+27]
				print genre
				femininbool = 0
				masculinbool = 0
				if genre == "féminin":
					femininbool =  1
				elif genre == "masculin":
				    masculinbool = 1
				print femininbool, masculinbool
				if str(elementsoup).find('<span id="acronyme"></span><i>') > 0:
					print "ACRONYME"
					counteracronym = counteracronym + 1
					continue
				c.execute("SELECT count(*) FROM lexico_element WHERE lexico = \'" + l[1] + "\' and title = \'" + lititle + "\';")
				checkduplicate = c.fetchone()[0]
				print checkduplicate
				if checkduplicate == 0:
					print "on insère"
					#print "INSERT INTO lexico_element (title, url, lexico, lexico_url, feminin, masculin) VALUES (\'" + lititle +"\',\'" + liurl +"\',\'" + l[1] +"\',\'" +l[0] +"\'," + str(femininbool) + "," + str(masculinbool) +");"
					c.execute("INSERT INTO lexico_element (title, url, lexico, lexico_url, feminin, masculin) VALUES (\'" + lititle +"\',\'" + liurl +"\',\'" + l[1] +"\',\'" +l[0] +"\'," + str(femininbool) + "," + str(masculinbool) +");")
					conn.commit()
	print countertotal, counterinvalid, counterinvalid


#Retirer : tous les plus d'un mots mais pas les mots composés, retirer les tion, retirer les isme, istes, retirer les acronymes
