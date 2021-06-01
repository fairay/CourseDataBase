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


if __name__ == '__main__':
    cli()
