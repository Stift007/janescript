import os


class Parser:
    def __init__(self, code):
        self.code = code
        self.path = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))+"/include"]
        self.parse(self.code)


    def parse(self, code, ret=False):
        code = self.ParseImports(code)
        code = self.ParseKeywords(code)
        if ret:
            return code
        with open("outs.py", "w") as f:
            f.write(code)

    def ParseKeywords(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                code = code.replace(line, line.replace("else if", "elif"))
                if word == "fn" and not self.StrContains("fn", line):
                    code = code.replace(line, line.replace("fn", "def"))
                if word == "structure" and not self.StrContains("structure", line):
                    code = code.replace(line,  line.replace("structure", "class"))
                
                if word == "const" and not self.StrContains("const", line):
                    varname = words[idx+1]

                    code = code.replace(line, line.replace(f"const {varname}", varname.upper()))
                    for l in code.splitlines():
                        if varname in l and not self.StrContains(varname,l):
                            code = code.replace(l, l.replace(varname, varname.upper()))
        return code

    def ParseImports(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word == "from" and not self.StrContains("from", line):
                    if words[idx+1] == "native":
                        if words[idx+2] == "import":
                            import_name = words[idx+3]
                            code = code.replace(line, f"from {import_name} import *")

                        elif words[idx+2] == "reference":
                            import_name = words[idx+3]
                            code = code.replace(line, f"import {import_name}")

                elif word == "#include" and not self.StrContains("#include", line):
                    importName = words[idx+1].strip("<>")
                    for i in self.path:
                        if os.path.exists(i+"/"+importName+".jns"):
                            with open(i+"/"+importName+".jns","r") as f:
                                nc = self.parse(f.read(), True)
                                code = nc+"\n"+code
        return code
    
    
    def StrContains(self, pattern, line):
        if not pattern in line: return False

        if not "\"" in line: return False
        else:
            firstquote = line.find('"')
            qc = 1
            lastquote = -1
            for l in range(len(line[firstquote+1:])):
                if line[l] == '"':
                    lastquote = l

            return pattern in line[firstquote:lastquote]
