import typer
import psutil


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
    typer.echo("CPU usage: "+ str(cpu_load)+'%')
    typer.echo("RAM usage: "+ str(ram_load)+'%')
    typer.echo("Disk usage: "+ str(disk_load[3])+'%')
