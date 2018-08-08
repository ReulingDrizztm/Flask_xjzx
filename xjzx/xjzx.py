import app
from config import DevelopConfig
from flask_script import Manager
from models import db
from flask_migrate import Migrate, MigrateCommand
from my_command import CreateAdmin, LoginTest
# 创建app对象
# 这里的DevelopConfig是一个配置，创建的对象没有实际意义，所以用app去创建这个对象
develop_app = app.create_app(DevelopConfig)
# 创建扩展命令对象
manager = Manager(develop_app)
# 添加迁移命令
Migrate(develop_app, db)
manager.add_command("db", MigrateCommand)

# 添加管理员命令
manager.add_command("createadmin", CreateAdmin())
manager.add_command("logintest", LoginTest())

if __name__ == '__main__':
    manager.run()
