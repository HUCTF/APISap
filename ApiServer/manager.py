from ApiServer import create_app
from ApiServer.extensions import db
from ApiServer.models import User

from flask_script import Manager, Server, Shell
import click
app = create_app()

banner = r"""
"""

manager = Manager(app)


def make_shell_context():
    return {
        "app": app,
    }


manager.add_command("runserver", Server(host="0.0.0.0", port=5000, use_debugger=True))
manager.add_command("shell", Shell(banner=banner, make_context=make_shell_context))


@manager.command
def reset_db():
    """Initialize the database."""
        
    click.confirm('This operation will delete the database, do you want to continue?', abort=True)
    db.drop_all()
    click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_super=True,
    )
    admin.set_id(str(admin.id))
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def init_db():
    db.create_all()
    click.echo('Initialized database.')
    admin = User(
        username='admin',
        email='admin@admin.com',
        is_super=True,
    )
    admin.set_id(str(admin.id))
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Success Add Admin Count.')

@manager.command
def set_user(username, email, password):
    """Add A New User."""

    click.echo('Initializing the database...')
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('The useristrator already exists, updating...')
        user.username = username
        user.email = email
        user.set_password(password)
    else:
        click.echo('Creating the temporary useristrator account...')
        user = User(
            username=username,
            email=email,
            is_super=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    manager.run()

