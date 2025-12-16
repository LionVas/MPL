from Lexer import Lexer

#s = "int[] a = { 1, 2, 3, 5, 12, ыфв }"
#s = "if (a < b) {  "
strings = []
with open("sample.java", encoding="utf-8") as file:
    for line in file:
        strings.append(Lexer.def_type(line))

with open("translated.py", "w", encoding="utf-8") as file:
    for s in strings:
        #print(s)
        file.write(s + "\n")
print(Lexer.variables)
