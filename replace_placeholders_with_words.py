import lxml.etree as ET 	#Import XML ETree tool into the script
import sqlite3		#Import SQLite3 into the script
import os.path

file_found=False

while file_found == False:
	file_name=input("Please enter the Tableou file name: ")
	print()

	try:
		print("Loading file.")
		o_tree = ET.parse('input/'+ file_name) 	#Read the XML file from the disk
		xml_file = o_tree.getroot() 
		print()
		print("File Loaded.")
		print()
		file_found=True
	except:
		print("Error, file does not exist, make sure to include the extension when entering name.")


db_found=False

while db_found==False:
	database_name=input("Please enter the Database file name: ")
	print()
	
	if os.path.isfile('db/'+database_name) == True:
		print("Loading Database.")
		db = sqlite3.connect('db/'+database_name) 	#Connect to the Database
		c = db.cursor() 	#Create a variable for the db coursor 
		print()
		print("Database loaded.")
		print()
		db_found=True
		table_name=input("Please enter the tabe name containing the translations: ")
	else:
		print("Error, file does not exist, make sure to include the extension when entering name.")
		

language=input("What language would you like English (enter e) or German (enter g)? ")

c.execute("SELECT "+language+" FROM "+table_name+" WHERE id LIKE 'replace_text_%'")
array=c.fetchall()

print(len(array))

number=0

while number < len(array):
	print(*array[number])
	number += 1

i = 0

while i < len(array):
	print(array[i])

	for ftext in xml_file.iter("formatted-text"):
		if ftext.find('run') != None:
			text_1 = ftext.find('run').text
			if text_1 == ("replace_text_"+str(i)):
				replace_word = ''.join(array[i])
				ftext.find('run').text = str(replace_word)

	for mtext in xml_file.iter('metadata-record'):
		if mtext.find('caption') != None:
			text_2 = mtext.find('caption').text
			if text_2 == ("replace_text_"+str(i)):
				replace_word = ''.join(array[i])
				mtext.find('caption').text = str(replace_word)

	for srule in xml_file.iter('style-rule'):
		if srule.find('format') != None:
			for form in srule.iter('format'):
				text_3 = form.attrib['value']
				if text_3 == ("replace_text_"+str(i)):
					replace_word = ''.join(array[i])
					form.attrib['value'] = str(replace_word)

	for aliases in xml_file.iter('aliases'):
		if aliases.find('alias') != None:
			for alias in aliases.iter('alias'):
				text_4 = alias.attrib['value']
				if text_4 == ("replace_text_"+str(i)):
					replace_word = ''.join(array[i])
					alias.attrib['value'] = str(replace_word)

	for mems in xml_file.iter('members'):
		if mems.find('member') != None: 
			for mem in mems.iter('member'):
				if 'alias' in mem.attrib:
					text_5 = mem.attrib['alias']
					if text_5 == ("replace_text_"+str(i)):
						replace_word = ''.join(array[i])
						mem.attrib['alias'] = str(replace_word)
	i += 1

output_name=input("What would you like to save the new XML file under? ")
o_tree.write('output/'+output_name+'.twb', xml_declaration=True, encoding='utf-8') 	#writes all changes to a new XML file called 'Report with placeholders.twb' with XML declaration at the top in UFT-8 encoding
