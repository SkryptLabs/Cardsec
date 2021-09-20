import typer
import psutil
import subprocess
import distro

GOOD=50
OK=75

def num_colour(start:str,num:int):
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
    Cardsec for SPOs
    """

@app.command()
def system():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent(2)
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    try:
        node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
    except: node="Not found."
    try:
        wallet=subprocess.check_output(['cardano-wallet','version']).decode().split()[0]
    except: wallet="Not found."
    
    typer.secho("\n-------System Info---------",fg=typer.colors.MAGENTA)
    
    typer.echo(num_colour("CPU usage: ",cpu_load))
    typer.echo(num_colour("RAM usage: ",ram_load))
    typer.echo(num_colour("Disk usage: ",disk_load[3])+'\n')
    typer.echo("Distro: "+distro.id()+' '+distro.version())
    typer.echo("Cardano-Node: "+node)
    typer.echo("Cardano-Wallet: "+wallet)
    typer.echo('\n')