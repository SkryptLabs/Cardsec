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


@app.callback()
def callback():
    """
    System and Security Assesment Tool for SPOs
    """

@app.command(short_help="Info about the system")
def system():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent()
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    
    try:
        node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
    except: node="Not found."
    try:
        wallet=subprocess.check_output(['cardano-wallet','version']).decode().split()[0]
    except: wallet="Not found."
    
    typer.secho("\n-------System Info---------",fg=typer.colors.MAGENTA,bold=True)
    
    typer.echo(num_colour("CPU usage: ",cpu_load))
    typer.echo(num_colour("RAM usage: ",ram_load))
    typer.echo(num_colour("Disk usage: ",disk_load[3])+'\n')
    
    typer.echo("Distro: "+distro.id()+' '+distro.version())
    typer.echo("Cardano-Node: "+node)
    typer.echo("Cardano-Wallet: "+wallet+'\n')
    #typer.echo('\n')

@app.command()
def scan(ports: Optional[str] = typer.Argument(None)):
    if ports is None:
        typer.secho("Scan ports by: cardsec scan ports")
    else:
        port_list=scan_ports()
        if port_list:
            typer.secho("The following ports are open:",fg=typer.colors.BRIGHT_MAGENTA)
            for i in port_list:
                typer.echo(i)
            typer.secho("Note: Only keep 2 outgoing ports open. (SSH & Node port) \n",fg=typer.colors.WHITE)
        else: typer.secho("No ports open!",fg=typer.colors.RED)
