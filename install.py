import typer
from venv import create
import sys
import os
import subprocess

def main(preinstall:bool=typer.Option(False,"--preinstall"), mkenv:bool=typer.Option(False,"--make-env"),install_dir:str = typer.Option(os.path.join(os.path.expanduser("~"),".jns"), "--venv-dir")):
    if mkenv:
            print("e")
            if not os.path.exists(install_dir):
                for i in os.path.split(install_dir):
                    if not os.path.exists(i): os.mkdir(i)
                    os.chdir(i)
            os.chdir(os.path.dirname(__file__))
            print("Entering Directory: "+os.getcwd())
            create(os.path.join(install_dir, "venv"), True, with_pip=True)
            print("Created (1) Virtual Environment!")
            if preinstall:
                print("Installing Libraries...")
                subprocess.run([os.path.join(install_dir, "venv","bin", "pip"), "install","requests","jinja2", "aiohttp"], cwd=os.getcwd())


typer.run(main)