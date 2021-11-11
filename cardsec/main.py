import typer
import psutil
import subprocess
import distro
from os import system
from termcolor import colored
from cardsec.port_scanner import scan_ports


GOOD=50
OK=75


def num_colour(start:str,num:int):
    start=typer.style(start,fg=typer.colors.BRIGHT_WHITE)
    if num<=GOOD:
        end=typer.style(str(num)+'%', fg=typer.colors.GREEN, bold=True)
    elif num<=OK:
        end=typer.style(str(num)+'%', fg=typer.colors.YELLOW, bold=True)
    else: typer.style(str(num)+'%', fg=typer.colors.RED, bold=True)

    return start+end


def banner():
	print("                                                                      ")
	print("                                                                      ")
	print(colored("          █████╗  █████╗ ██████╗ ██████╗  ██████╗███████╗ █████╗         ", "white"))
	print(colored("         ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════ ██╔════╝██╔══██╗        ", "white"))
	print(colored("         ██║  ╚═╝███████║██████╔╝██║  ██║╚█████╗ █████╗  ██║  ╚═╝        ", "white"))
	print(colored("         ██║  ██╗██╔══██║██╔══██╗██║  ██║ ╚═══██╗██╔══╝  ██║  ██╗        ", "white"))
	print(colored("         ╚█████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗╚█████╔╝        ", "white"))
	print(colored("          ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚════╝        ", "white"))
	print("                                                                      ")
	print(colored("                        Developed by: SkryptLabs                              ", "blue"))
	print(colored("                         twitter.com/skryptlabs             				   ", "red"))
	print("                                                                         ")


def info():
    try:
        node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
    except: node="Not found."

    typer.secho("\n-------System Info---------",fg=typer.colors.MAGENTA,bold=True)

    typer.echo("Distro: "+distro.id()+' '+distro.version())
    typer.echo("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
    typer.echo("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
    typer.echo("Cardano-Node: " +node)


def load():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent()
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    
    typer.secho("\n-------System Load---------",fg=typer.colors.MAGENTA,bold=True)
    
    typer.echo(num_colour("CPU usage: ",cpu_load))
    typer.echo(num_colour("RAM usage: ",ram_load))
    typer.echo(num_colour("Disk usage: ",disk_load[3])+'\n')


def scanner(port_range):
	port_list=scan_ports(port_range)
	if port_list:
		print(colored("The following ports were found open:", "magenta"))
		for i in port_list:
			print(i)
		print(colored("Note: Only keep 2 outgoing ports open. (SSH & Node port)", "red"))
		print("")
	else: print(colored("No ports open!", "red"))


def scan():
	print(colored("-------Port Scanner---------", "magenta"))
	def submenu():
		print("[1] Light Scan - 6000 ports")
		print("[2] Exhaustive Scan - 64000 ports")
		print("[3] Exit to Main Menu")

	while 1:
		print('')
		submenu()
		try:
			suboption = int(input(colored("Select your option: ", "yellow")))
		except: return

		if suboption == 1:
			port_range=6000
			print(f"Scanning {port_range} ports...")
			scanner(port_range)			
		      
		elif suboption == 2:
				port_range=6000
				print("Scanning", 6000, "ports...")
				scanner(port_range)

		elif suboption == 3:
			break
	
		else:
			print("Invalid Option!")		
		

def menu():
		print("[1] System Info")
		print("[2] System Load")
		print("[3] Port Scanner")
		print("[4] Vulnerability Scanner")
		print("[5] Exit Cardsec")


def select(option):
	print("")
	if option == 1:
		info()	
	elif option == 2:
		load()
	elif option == 3:
		scan()
	elif option == 4:
		print("Coming Soon....")
	elif option == 5:
		print("Happy Minting!")
		exit()	
	else:
		print("Invalid option.")
	
	print("")


app=typer.Typer(invoke_without_command=True)
system("clear")
banner()
while 1:
	menu()
	try:
		option = int(input(colored("Select your option: ", "yellow")))
	except: exit()
	system("clear")
	banner()
	select(option)
