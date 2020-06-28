from flask_script import Manager
from ihome import create_app, db
from flask_migrate import Migrate, MigrateCommand


# 创建flask的应用对象
app = create_app('develop')

manager = Manager(app)

Migrate(app, db)

manager.add_command("db", MigrateCommand)
# manager.add_command('runserver', host='127.0.0.1', port=5000)


if __name__ == "__main__":
    manager.run()
