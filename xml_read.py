import xml.etree.ElementTree as et
import os

database_filename = "database.xml"
database_fullpath = os.path.join(os.path.abspath(os.path.curdir), database_filename)
print(database_fullpath)
database_xml = et.parse(database_fullpath)
db_root = database_xml.getroot()

for entry in db_root:
    print(entry.attrib)
