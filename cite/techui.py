import click
from cmd_view import *


@click.group()
def cli():
    pass


@click.command()
@click.argument('login')
def profile(login: str):
    click.echo(CmdUsersView.profile(login))
cli.add_command(profile)


@click.command()
@click.argument('login')
def approveacc(login: str):
    click.echo(CmdUsersView.approve(login))
cli.add_command(approveacc)


@click.command()
def allprofiles():
    click.echo(CmdUsersView.get_all())
cli.add_command(allprofiles)


@click.command()
def unverprofiles():
    click.echo(CmdUsersView.get_unverified())
cli.add_command(unverprofiles)


@click.command()
def dutydrivers():
    click.echo(CmdDutyView.get_drivers())
cli.add_command(dutydrivers)


@click.command()
def dutyguards():
    click.echo(CmdDutyView.get_guards())
cli.add_command(dutyguards)


@click.command()
def trucks():
    click.echo(CmdEntityView.get_trucks())
cli.add_command(trucks)


@click.command()
def checkpoints():
    click.echo(CmdEntityView.get_checkpoints())
cli.add_command(checkpoints)


@click.command()
def delivery():
    click.echo(CmdEntityView.get_delivery())
cli.add_command(delivery)


@click.command()
def passrecords():
    click.echo(CmdEntityView.get_pass_records())
cli.add_command(passrecords)


@click.command()
@click.argument('id')
def deliverypage(id: int):
    click.echo(CmdEntityView.delivery_page(id))
cli.add_command(deliverypage)


if __name__ == '__main__':
    cli()
