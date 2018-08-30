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
	else:
		print("Error, file does not exist, make sure to include the extension when entering name.")
		
end = False		#Create end Variable for loop
found = False 	#Create found variable for loop

counter = 0 	#Create counter variable for loop

replaced_text=[] 	#Create empty array to later store all replaced words in


while end == False: 	#Create a loop that allow to enter words to search the XML file for and replace them with numbered placeholders
	
	found = False 	#If word was found and the user does not want to quit the script yet the variable found will have to be reset so the loop works correctly

	search_term=input("Enter a Word (Type END to stop): ") 	#Asks for the word to replace
	if search_term == "END": 	#Checks if the imput was END as this will terminate the script
		end = True 	#sets variable end to True which will quit the loop
	else: 
		
		for ftext in xml_file.iter('formatted-text'): 	#For every tag of <formatted-text> run the indented lines of code bellow
			if ftext.find('run') != None: 	#Failsafe to prevent a crash of the scrip as if the word is in a <metadata-record> tag and runs though this par of the script it will return a NoneType object which crashes the Script if you request its text value
				text_1 = ftext.find('run').text 	#Searches thought the current <formatted-text> tag for any text in a <run> tag
				if text_1 == search_term: 	#checks if the found text matches the searched word
					found = True 	#sets the variable found to true to make sure the if statement at the end that shows that nothing has been found does not bot return as possitive

					#print(text_1) 	#DEBUGGING ONLY Prints the word found
					#print("replace_text_"+str(counter)) 	#DEBUGGING ONLY Prints the placeholder the world will be replaced by

					if text_1 in replaced_text:
						index_number=replaced_text.index(text_1)
						ftext.find('run').text = str("replace_text_"+str(index_number)) 	#Replaces the word with the placeholder
					else:
						ftext.find('run').text = str("replace_text_"+str(counter)) 	#Replaces the word with the placeholder
						counter += 1 	#Counter varaible increased by one as one placeholder was used
						replaced_text.append(text_1) 	#Replaced word gets appended to array of replaced words

		for mtext in xml_file.iter('metadata-record'): 	#For every tag of <metadata-record> run the indented lines of code bellow
			if mtext.find('caption') != None: 	#Failsafe to prevent a crash of the scrip as if the word is in a <formatted-text> tag and runs though this par of the script it will return a NoneType object which crashes the Script if you request its text value
				text_2 = mtext.find('caption').text 	#Searches thought the current <metadata-record> tag for any text in a <caption> tag
				if text_2 == search_term: 	#checks if the found text matches the searched word
					found = True 	#sets the variable found to true to make sure the if statement at the end that shows that nothing has been found does not bot return as possitive

					#print(text_2) 	#DEBUGGING ONLY Prints the word found
					#print("replace_text_"+str(counter)) 	#DEBUGGING ONLY Prints the placeholder the world will be replaced by

					if text_2 in replaced_text:
						index_number=replaced_text.index(text_2)
						mtext.find('caption').text = str("replace_text_"+str(index_number)) 	#Replaces the word with the placeholder
					else:
						mtext.find('caption').text = str("replace_text_"+str(counter)) 	#Replaces the word with the placeholder
						counter += 1 	#Counter varaible increased by one as one placeholder was used
						replaced_text.append(text_2) 	#Replaced word gets appended to array of replaced words

		for srule in xml_file.iter('style-rule'): 	#For every tag of <style-rule> run the indented lines of code bellow
			if srule.find('format') != None: 	#Failsafe to prevent a crash of the scrip as if the word is in a differnt tag and runs though this par of the script it will return a NoneType object which crashes the Script if you request its text value

				for form in srule.iter('format'):

					text_3 = form.attrib['value']

					if text_3 == search_term: 	#checks if the found text matches the searched word
						found = True 	#sets the variable found to true to make sure the if statement at the end that shows that nothing has been found does not bot return as possitive

						#print(text_3) 	#DEBUGGING ONLY Prints the word found
						#print("replace_text_"+str(counter)) 	#DEBUGGING ONLY Prints the placeholder the world will be replaced by

						if text_3 in replaced_text:
							index_number=replaced_text.index(text_3)
							form.attrib['value'] = str("replace_text_"+str(index_number)) 	#Replaces the word with the placeholder
						else:
							form.attrib['value'] = str("replace_text_"+str(counter)) 	#Replaces the word with the placeholder
							counter += 1 	#Counter varaible increased by one as one placeholder was used
							replaced_text.append(text_3) 	#Replaced word gets appended to array of replaced words

		for aliases in xml_file.iter('aliases'): 	#For every tag of <aliases> run the indented lines of code bellow
			if aliases.find('alias') != None: 	#Failsafe to prevent a crash of the scrip as if the word is in a differnt tag and runs though this par of the script it will return a NoneType object which crashes the Script if you request its text value
				#text_4 = aliases.findall('alias').attrib['value'] 	#Searches thought the current <aliases> tag for any text in a <alias> tag

				for alias in aliases.iter('alias'):

					text_4 = alias.attrib['value']

					if text_4 == search_term: 	#checks if the found text matches the searched word
						found = True 	#sets the variable found to true to make sure the if statement at the end that shows that nothing has been found does not bot return as possitive

						#print(text_4) 	#DEBUGGING ONLY Prints the word found
						#print("replace_text_"+str(counter)) 	#DEBUGGING ONLY Prints the placeholder the world will be replaced by

						if text_4 in replaced_text:
							index_number=replaced_text.index(text_4)
							alias.attrib['value'] = str("replace_text_"+str(index_number)) 	#Replaces the word with the placeholder
						else:
							alias.attrib['value'] = str("replace_text_"+str(counter)) 	#Replaces the word with the placeholder
							counter += 1 	#Counter varaible increased by one as one placeholder was used
							replaced_text.append(text_4) 	#Replaced word gets appended to array of replaced words

		for mems in xml_file.iter('members'): 	#For every tag of <members> run the indented lines of code bellow
			if mems.find('member') != None: 	#Failsafe to prevent a crash of the scrip as if the word is in a differnt tag and runs though this par of the script it will return a NoneType object which crashes the Script if you request its text value
				#text_5 = mems.findall('member').attrib['value'] 	#Searches thought the current <members> tag for any text in a <member> tag

				for mem in mems.iter('member'):

					if 'alias' in mem.attrib:
						text_5 = mem.attrib['alias']

						if text_5 == search_term: 	#checks if the found text matches the searched word
							found = True 	#sets the variable found to true to make sure the if statement at the end that shows that nothing has been found does not bot return as possitive

							#print(text_5) 	#DEBUGGING ONLY Prints the word found
							#print("replace_text_"+str(counter)) 	#DEBUGGING ONLY Prints the placeholder the world will be replaced by

							if text_5 in replaced_text:
								index_number=replaced_text.index(text_5)
								mem.attrib['alias'] = str("replace_text_"+str(index_number)) 	#Replaces the word with the placeholder
							else:
								mem.attrib['alias'] = str("replace_text_"+str(counter)) 	#Replaces the word with the placeholder
								counter += 1 	#Counter varaible increased by one as one placeholder was used
								replaced_text.append(text_5) 	#Replaced word gets appended to array of replaced words


		if found == False: 	#If the word has not been found the indented lines of code will be executed
			print("Not Found") 	#Displays to the user that no word matching the search has been found
		else:
			print("Word Found")



if counter == 0: 	#If no words where changed the script will execute the indented lines of code
	print("Script will now terminate") 	#The user will be notified that the script will close and then the program will end

else: 	#If one or more words have been replaced the indented lines of code will execute


	replaced_amount=counter 	#copies the value of counter into replaced amount
	print("Amount of words Replaced: " +str(replaced_amount)) 	#Displays how many words where replaced in total

	print("You have replaced thses words: ") 	#Prints to the user the list of words that have been replaced
	print(', '.join(replaced_text)) 	#Prints array as joined list


	print("Creating new XML file with placeholders present.") 	#Lets the user know that the changes are being written to a new XML file with placeholers present.
	o_tree.write('output/Report with placeholders.twb', xml_declaration=True, encoding='utf-8') 	#writes all changes to a new XML file called 'Report with placeholders.twb' with XML declaration at the top in UFT-8 encoding

	table_name=input("Please enter a name for the table in the Database: ") 	#Asks user for name of Table in the database that he would like the placeholders to be stored in.

	print("Writing Changes to Database.") 	#Notifies the user that the placehoders are being added to the database.

	c.execute("""CREATE TABLE """+table_name+"""(id, e, g)""") 	#Creates a table with the name the user entered with three columns. 

	counter=0 	#sets the variable counter to 0

	while counter < replaced_amount: 	#while the counter is lower than the amount of replaced words this loop will run

		print("Inserting record") 	#Lets the user know a record is being inserte into the table

		placeholder_name="replace_text_"+str(counter) 	#Creates a variable with the name of the placeholder

		english_text=replaced_text[counter] 	#Creates a variable with the word that was replaced

		sql ="INSERT INTO "+table_name+" (id, e, g) VALUES(?, ?, ?)" 	#creates a variable and stores an SQL statement into it, this will pace create a record of one repaced word into the table

		c.execute(sql, (placeholder_name, english_text, None)) 	#This will execute the SQL statement stored in the variable sql 
	
		db.commit() 	#Write changes to Database

		print(c.rowcount, "record inserted.") 	#Notifies user that racord has been inserted

		counter += 1 	#Increases value of counter by 1

