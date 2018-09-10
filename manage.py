import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import db, create_app

app = create_app(os.getenv('CONFIGURATION_SETTING') or 'dev')

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()


if __name__ == '__main__':
    app.run()
