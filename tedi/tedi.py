import click


@click.group()
def cli():
    pass


@cli.command()
def render(help='Render all the templates'):
    print('Consider them rendered.')
