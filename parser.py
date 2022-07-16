import textwrap


class Parser:
    def __init__(self, code):
        self.code = code
        self.parse(self.code)

    def ParseKeywords(self, code):
        for TT in ("iterate", "fn", "public static object"):
            for line in code.splitlines():
                if TT in line and not self.StrContains(TT, line):
                    if TT == "fn":
                        code = code.replace(line, line.replace("fn", "def"))
                    elif TT == "iterate":
                        code = code.replace(line, line.replace("iterate", "for"))
                    elif TT == "public static object":
                        code = code.replace(line, line.replace(TT, "class"))
    
        return code

    def parse(self, code, ret=False):
        code = self.ParseComments(code)
        code = self.ParseImports(code)
        code = self.ParseKeywords(code)
        code = self.ParseBraces(code)
        if ret:
            return code
        code = self.Enter(code)
        with open("outs.py", "w") as f:
            f.write(code)

    def ParseBraces(self, code):
        leftBraceCounter = 0
        rightBraceCounter = 0
        for x in code.splitlines():
            words = x.split()
            for wordNo, word in enumerate(words):
                for char in word:
                    if char == "{" and not self.StrContains("{",x):
                        leftBraceCounter += 1
                    elif char == "}" and not self.StrContains("}",x):
                        rightBraceCounter += 1
        
        assert leftBraceCounter == rightBraceCounter, "Unmatched Braces"
        indent = 0
        for line in code.splitlines():
            words = line.split()
            for wordNo, word in enumerate(words):
                for char in word:
                    if char == "{" and not self.StrContains("{", line):
                        indent += 1
                        code = code.replace(line, line.replace("{",":"))
                        for x in code.splitlines()[code.index(line.replace("{",":")):]:
                        
                            while not ("}" in x and not self.StrContains("}",x)):
                                print("f")
                                code = code.replace(x,(" "*4*indent) + x)
                            indent -= 1
        return code

    def ParseComments(self, code):
        newcode = ""
        for l in code.splitlines():
            if "//" in l and not self.StrContains("//", l):
                ...
            else:
                newcode += l + "\n"

        return newcode

    def ParseImports(self, code):
        for x in code.splitlines():
            words = x.split()
            for wordNo, word in enumerate(words):
                if word == "#include" and not self.StrContains("#include", x):
                    if words[wordNo+1] == "native":

                        importName = words[2].strip("<>")
                        code = code.replace(x, f"from {importName} import *")
                    else:
                        importName = words[wordNo+1].strip("<>")
                        with open(importName+".jns","r") as f:
                            nc = self.parse(f.read(), True)
                            
                            code = code.replace(x, nc)
                elif word == "#reference" and not self.StrContains("#reference", x):
                    if words[wordNo+1] == "native":
                        ref = words[wordNo+2].strip("<>")
                        code = code.replace(f"#reference native <{ref}>",f"import {ref}")

        return code


    def Enter(self, code):
            code += """
if __name__ == "__main__":
    m = Main()
    m.Main()
    exit(0)
            """
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
