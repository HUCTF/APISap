# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from ScanServer.extensions import bootstrap, db, login_manager
from ScanServer.config import config
from ScanServer.blueprints.user import user_bp
from ScanServer.blueprints.api_v1.api import api_v1 
#from ScanServer.blueprints.admin import admin_bp
from ScanServer.models import User
import os
import click

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('ScanServer')
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    register_commands(app)
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user_bp)
 #   app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(user_bp, url_prefix='/user')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('404.html'), 404

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404




def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        user = User(
            username='admin',
            email='admin@admin.com',
            is_super=True
        )
        user.set_password('admin')
        db.session.add(user)
        click.echo('Initialized database...Success Add admin count.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--email', prompt=True, help='The Email used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, email, password):
        """Building Bluelog, just for you."""

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
