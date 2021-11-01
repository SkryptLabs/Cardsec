import typer
import psutil
import subprocess
import distro
from typing import Optional
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

app = typer.Typer()
system = typer.Typer()
app.add_typer(system, name="system",help="System Details")


@app.callback()
def callback():
    """
    System and Security Assesment Tool for SPOs
    """

@system.command("info",short_help="System Information")
def info():
    try:
        node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
    except: node="Not found."

    typer.secho("\n-------System Info---------",fg=typer.colors.MAGENTA,bold=True)

    typer.echo("Distro: "+distro.id()+' '+distro.version())
    typer.echo("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
    typer.echo("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
    typer.echo("Cardano-Node: " +node)

@system.command("load",short_help="System Load")
def load():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent()
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    
    typer.secho("\n-------System Load---------",fg=typer.colors.MAGENTA,bold=True)
    
    typer.echo(num_colour("CPU usage: ",cpu_load))
    typer.echo(num_colour("RAM usage: ",ram_load))
    typer.echo(num_colour("Disk usage: ",disk_load[3])+'\n')

@app.command(short_help="Port scanner")
def scan(all:bool = typer.Option(False, help="Exhaustive Full scan")):
    
    if all:
        port_range=64000
    else:
        port_range=6000
    
    typer.echo(f"Scanning {port_range} ports...")

    port_list=scan_ports(port_range)
    if port_list:
        typer.secho("The following ports were found open:",fg=typer.colors.BRIGHT_MAGENTA)
        for i in port_list:
            typer.echo(i)
        typer.secho("Note: Only keep 2 outgoing ports open. (SSH & Node port) \n",fg=typer.colors.WHITE)
    else: typer.secho("No ports open!",fg=typer.colors.RED)
