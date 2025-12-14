class Lexer:

    variables = set() # сюда короч буду класть все переменные которые объявляются
    types = ["int", "float", "String", "boolean", "double","int[]", "float[]", "String[]", "boolean[]", "double[]"]
    conditions = ["if", "else"]
    braces = ["{", "}"]
    loops = ["for", "while", "do"]
    statements = ["continue;", "break;"]
    tabs_counter= 0
    loop_mode = 0 # 0- for/while, 1 - do while
    @staticmethod
    def  def_type(s):  # s - типа string, а функция выдает тип строки(условие цикл выражение и тд)

        parts = s.split();
        print(str(parts) + "/" + str(Lexer.tabs_counter))
        if len(parts) > 0:
            type = parts[0];
        else:
            print("Неизвестная строка")
            return " ";
        if type in Lexer.types:
            return Lexer.process_variable(parts)
        elif type in Lexer.conditions:
            return Lexer.process_condition(parts)
        elif type in Lexer.braces:
            if (Lexer.loop_mode == 0):
                #print( Lexer.loop_mode)
                Lexer.check_braces(parts)
                return ""
            else:
                return Lexer.process_loops(parts)
        elif type in Lexer.variables:
            return Lexer.process_expression(parts)
        elif type in Lexer.loops:
            return Lexer.process_loops(parts)
        elif type in Lexer.statements:
            return Lexer.process_statement(type)
        else:
            print("Неизвесная строка: " + s)
            return "\n"


    def process_variable(parts):
        parts = [p.replace(";", " ") for p in parts]
        Lexer.variables.add(parts[1].strip())
        if "[]" in parts[0]:
            if len(parts) == 2 or parts[3] == 'new':
                result = Lexer.tabs_counter * "\t" + parts[1] + " = []"
                return result
            elif parts[3] == "{":
                variables_list = []
                for x in parts[4:]:
                    if x != "}":
                        variables_list.append(x)
                result = parts[1] + " = [ "
                for x in variables_list:
                    result += x
                    result += " "
                result += "]"
                result = Lexer.tabs_counter*"\t" + result
                return result
        else:
            if len(parts) == 2:

                return Lexer.tabs_counter*"\t" + parts[1] + " = None"
            else:

                return Lexer.tabs_counter*"\t" + parts[1] + " = " + parts[3]



    def process_condition(parts):
        if parts[0] == "else":
            if parts[1] =="if":
                result = Lexer.tabs_counter*"\t" + "elif"
                result += " ".join(parts[2:])
                Lexer.check_braces(parts)
                result.replace("{", ":")
                return result
            else:
                result = Lexer.tabs_counter*"\t" +"else: \n"
                Lexer.check_braces(parts)
                return result
        elif parts[0] == "if":
            result = Lexer.tabs_counter * "\t" + "if "
            result += " ".join(parts[1:])
            Lexer.check_braces(parts)
            result = result.replace("{", ":")
            return result
    def process_expression(parts):
        result = Lexer.tabs_counter*"\t" + " ".join(parts)
        result = result.replace(";", "")
        return result



    def check_braces(parts):
        for p in parts:
            if "{" in p:
                Lexer.tabs_counter += 1
            elif "}" in p:
                Lexer.tabs_counter -= 1

    def process_loops(parts):
        if parts[0] == "do":
            Lexer.loop_mode = 1
            result = Lexer.tabs_counter * "\t" + "while True:"
            Lexer.check_braces(parts)
            return result
        elif parts[1] =="while" :
            result = Lexer.tabs_counter * "\t" + "if not "
            result += " ".join(parts[2:]) + ":"
            result = result.replace(";", "")
            result += "\n" +(Lexer.tabs_counter+1) * "\t" + "break"
            Lexer.check_braces(parts)
            Lexer.loop_mode = 0
            return result
        elif parts[0] =="while":
            result = Lexer.tabs_counter * "\t" + "while "
            result += " ".join(parts[1:])
            Lexer.check_braces(parts)
            result = result.replace("{", ":")
            return result
        elif parts[0] == "for":
            condition = " ".join(parts[1:-1])
            condition = condition.split(";")
            arg1 = condition[0].split("=")
            var = arg1[0]
            var = var.split(" ")[1]
            arg1 = int(arg1[1].strip())
            arg2 = condition[1]
            for i in arg2:
                try:
                    x = int(i)
                    arg2=x
                    break
                except:
                    continue
            arg3 = condition[2]
            for i in arg3:
                if ("++" in i) :
                    x = "+1"
                    arg3=x
                    break
                elif("--" in i):
                    x = "-1"
                    arg3=x
                    break
                else:
                    arg3= "+0"
            result = Lexer.tabs_counter * "\t" + "for " + var + " in range (" + str(arg1) + "," + str(arg2) + ", " + str(arg3) + "):"
            Lexer.check_braces(parts)
            return result


    def process_statement(type):
        if (type == "break;"):
            return "break"
        elif (type == "continue;"):
            return "continue"