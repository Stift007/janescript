import parse
import json
import typer
import subprocess
import os
import sys
import functools

transpile = False
cwd = os.getcwd()
noexec = False

file = sys.argv[1]
if file == "--version":
    print("JaneScript 0.3.1 (R3)")
    exit(0)
for n,i in enumerate(sys.argv[1:]): 
    if i in ("-T", "--transpile-only"):
        sys.argv.pop(n)
        transpile = True
    if i in ("-cwd", "--workdir","-D"):
        sys.argv.pop(n)
        cwd = sys.argv.pop(n+1)
    
    if i in ("--noexec","--compiler-mode", "-C"):
        sys.argv.pop(n)
        noexec = True
    
additional_args = sys.argv[2:]
def main(file: str, transpile:bool=(False), cwd: str = os.getcwd(), noexec: bool = False):
    os.chdir(cwd)
    with open(file) as f:
        parse.Parser(f.read(), fn=file)
        if not noexec:
            subprocess.call([sys.executable, f"{os.path.dirname(os.path.abspath(__file__))}/outs.py", *additional_args])
        if not transpile:
            os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/outs.py")
    sys.exit(0)
if __name__ == "__main__":
    main(file, transpile, cwd, noexec)