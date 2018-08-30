import lxml.etree as ET
import sqlite3


language=input("What language would you like e or g? ")

tree = ET.parse('New.twb')
xml_file = tree.getroot()

db = sqlite3.connect('Database.db')
c = db.cursor()

c.execute("SELECT e FROM Trans WHERE id LIKE 'replace_text_%'")
array=c.fetchall()

print(len(array))


number=0
while number < len(array):
	print(*array[number])
	number += 1

i = 0

while i < len(array):

	for text in xml_file.iter('run'):
		var_name = "replace_text_"+str(i)
		print(var_name)
		if text.text == var_name:
			output = text.text
			print(output)

			c.execute("SELECT "+language+" FROM Trans WHERE id = '"+(str(var_name))+"'")

			translation = c.fetchone()[0]

			print("New text is "+translation)

			text.text = str(translation)

			i += 1

tree.write('file-after-edits.twb', xml_declaration=True, encoding='UTF-8')
