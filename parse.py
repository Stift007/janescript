import os
from base64 import b16decode


class Parser:
    def __init__(self, code, fn=os.path.abspath(__file__)):
        self.code = code
        self.path = [os.getcwd(), os.path.dirname(
            os.path.abspath(__file__))+"/include"]
        self.parse(self.code, False, fn)
#        print (f"{os.path.dirname(os.path.abspath(__file__))}/outs.py")

    def parse(self, code, ret=False, fn=None):
        code = self.ParsePragmas(code)
        self.fn = fn
        # if not hasattr(self, "NI_BUILTINS"):
        #    code = "#include <__builtins__>"+"\n"+code
        code = self.ParseComments(code)
        code = self.ParseEOL(code)
        code = self.ParseImports(code)
        code = self.ParseBraces(code)
        code = self.ParseKeywords(code)
        code = self.ParseIndents(code)
        code = self.ParseEscapeChars(code)
        code = self.CleanupCode(code)
        if ret:
            return code

        with open(f"{os.path.dirname(os.path.abspath(__file__))}/outs.py", "w+") as f:
            f.write(code)
        # exit(0)

    def ParseComments(self, code):
        for line in code.splitlines():
            if line.startswith("//"):
                code = code.replace(line, "\n")
            if "//" in line and not self.StrContains("//", line):
                code = code.replace(line, line.split("//")[0])

        return code

    def ParseKeywords(self, code):
        """
        Changing `fn` to `def`
        """
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                code = code.replace(line, line.replace("else if", "elif"))
                if word == "fn" and not self.StrContains("fn", line):
                    code = code.replace(line, line.replace("fn", "def"))
                if word == "structure" and not self.StrContains("structure", line):
                    code = code.replace(
                        line,  line.replace("structure", "class"))

                if word == "for" and not self.StrContains("for", line) and not "#transpiled" in line:
                    _, var, kw, fn, stp, step = line.split()  # Syntax: `for _=0 until 5 step 1`
                    step = step.partition(":")[0]
                    try:
                        varname, initial = var.split("=")
                        indents = line.count("\t")
                        ind = "\t"*indents
                        code = code.replace(
                            line, f'for {varname} in range({initial}, {fn}, {step}): #transpiled')
                    except:
                        raise SyntaxError(
                            f"Malformed For Loop ({self.fn}:{idx}")
                if word == "const" and not self.StrContains("const", line):
                    varname = words[idx+1]

                    code = code.replace(line, line.replace(
                        f"const {varname}", varname.upper()))
                    for l in code.splitlines():
                        if varname in l and not self.StrContains(varname, l):
                            code = code.replace(
                                l, l.replace(varname, varname.upper()))
        return code

    def ParsePragmas(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word == "#pragma" and not self.StrContains("#pragma", line):

                    name, val = line[len(word):].split(",")
                    setattr(self, name, val)
        return code

    def ParseImports(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word == "from" and not self.StrContains("from", line):
                    if words[idx+1] == "native":
                        if words[idx+2] == "import":
                            import_name = words[idx+3]
                            code = code.replace(
                                line, f"from {import_name} import *")

                        elif words[idx+2] == "reference":
                            import_name = words[idx+3]
                            code = code.replace(line, f"import {import_name}")

                elif word == "#include" and not self.StrContains("#include", line):
                    importName = words[idx+1].strip("<>")
                    for i in self.path:
                        if os.path.exists(i+"/"+importName+".jns"):
                            with open(i+"/"+importName+".jns", "r") as f:
                                nc = self.parse(
                                    f.read(), True, importName+".jns")
                                code = nc+"\n"+code
        return code

    def ParseEscapeChars(self, code):
        code = code.splitlines()
        for i, line in enumerate(code):
            if "\\{" in line and not self.isAssignment(line) and not self.StrContains("\\{", line):
                code[i] = (line.replace("\\{", "{"))
            if "\\}" in line and not self.isAssignment(line) and not self.StrContains("\\}", line):
                code[i] = (line.replace("\\}", "}"))
        return "\n".join(code)

    def ParseEOL(self, code):
        for i, line in enumerate(code.splitlines()):
            if not line.strip("\t \n\r"):
                continue
            if line.startswith("#") or ("{" in line) or ("}" in line) or not line or line.strip("\t").replace(" ", "").startswith("@"):
                continue
            if line.rstrip("\t \n")[-1] == ";":
                code = code.replace(line, line[:-1])
            else:

                raise SyntaxError(
                    f"Missing Semicolon in {self.fn} on line #{i+1} - {line} (Expected ;, found {line[-1]}!")
        return code

    def ParseBraces(self, code):
        lbraces = 0
        rbraces = 0
        code = code.splitlines()
        for i, line in enumerate(code):
            if ("{" in line and not "\\{" in line) and not self.isAssignment(line) and not self.StrContains("{", line):
                lbraces += 1
                code[i] = (line.replace("{", ":"))
#                print(lbraces)
                code.insert(i+1, "#startindent")
            # if lbraces-1==rbraces: print(line+":"+str(i))
            if ("}" in line and not "\\}" in line) and not self.StrContains("}", line):

                rbraces += 1
                code[i] = (line.replace("}", ""))
                code.insert(i+1, "#endindent")
#                print(rbraces)

       # assert lbraces == rbraces, ( f"Opening Brace Count ({lbraces}) does not match Closing Brace count ({rbraces}) in {self.fn} ")
        return "\n".join(code)

    def isAssignment(self, line):
        if "{" in line:
            if self.StrContains("{", line):
                return True
            if ('={' in line.replace(" ", "").replace("\t", "")):
                return True
        return False

    def ParseIndents(self, code):
        indentCount = 0
        code = code.splitlines()
        for i, line in enumerate(code):

            if line == "#startindent":
                indentCount += 1
            if line == "#endindent":
                indentCount -= 1
            # line = line.replace("\t","")
#            print(line+":"+str(indentCount))
            code[i] = (("\t"*(indentCount+1)) +
                       line) if code[i] != (("\t"*indentCount) + line) else line
        return "\n".join(code)

    def CleanupCode(self, code):
        """
        Remove Indentation Placeholders, Import the Builtin Library
        """
        code = code.replace("#startindent", "")
        code = code.replace("#endindent", "")
        return code

    def StrContains(self, pattern, line):
        if not pattern in line:
            return False

        if not "\"" in line:
            return False
        else:
            firstquote = line.find('"')
            qc = 1
            lastquote = -1
            for l in range(len(line[firstquote+1:])):
                if line[l] == '"':
                    lastquote = l

            return pattern in line[firstquote:lastquote]
