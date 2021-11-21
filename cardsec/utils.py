import xml.etree.ElementTree as treant
from termcolor import colored

def parser(f):
    tree = treant.parse(f)
    root = tree.getroot()

    for child in root.findall('host'):
        for k in child.findall('address'):
            host = k.attrib['addr']
            for y in child.findall('ports/port'):
                current_port = y.attrib['portid']
                for m in y.findall('script'):
                        output = m.attrib['output']
                        print (colored("CVE Detection - Cardsec", "red"))
                        print("")
                        print (colored("Port Number:", "magenta") + current_port )
                        print (colored("cve detected:", "magenta") + output)
                        print("")
