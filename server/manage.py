from flask.cli import FlaskGroup, run_command

from wsgi import app

cli = FlaskGroup(app)


@cli.command("runserver")
def runserver():
    run_command()


if __name__ == "__main__":
    cli()
