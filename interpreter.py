import subprocess
import os
import sys
from parser import Parser

pyinstaller_installed = False
try:
    import pyinstaller.__main__
    pyinstaller_installed = True
except:
    pyinstaller_installed = False

class Interpreter(object):
    def run(self,code):

        subprocess.call([sys.executable, "outs.py"])
        if remove:
            os.remove("outs.py")

remove = True

def ArgCheck():
    global remove
    execname = ""
    for x in sys.argv[1:]:
        if x.startswith("-"):
            if x == "-T":
                remove = False
            elif x == "--version":
                print("JaneScript v0.21")
                print(f"Bootstrapped: {os.path.exists('interpreter.jns')}")
                exit(-1)
        else:
            execname = x

    code = open(execname).read()
    print(code)
    parser = Parser(code)
    inter = Interpreter()
    inter.run(parser.code)

if __name__ == "__main__":
    ArgCheck()
