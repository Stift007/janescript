f = open("jns copy.jns").readlines()
open("jns.jns","w").write("//Unindented")
for line in f:
    open("jns.jns", "a").write(line.strip()+"\n")