#!/usr/bin/env python
from flask_script import Manager
from flask_script.commands import Server, Shell, ShowUrls, Clean

from flask_application import app
from flask_application.script import ResetDB
from flask_application.tests.script import RunTests


manager = Manager(app)
manager.add_command("shell", Shell(use_ipython=True))
manager.add_command("runserver", Server(use_reloader=True))
manager.add_command("show_urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("reset_db", ResetDB())
manager.add_command('run_tests', RunTests())


if __name__ == "__main__":
    manager.run()
