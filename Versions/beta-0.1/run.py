import lexer, parser, optimizer, interpreter, os


file_name = "index.qs"
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        tokens = lexer.run(content)
        ast = parser.parse(tokens)
        interpreter_result = interpreter.interpret(ast)
        # # for code in content:
        # #     print(f"{code}", end="")
        # # for token in tokens: print(token)\
        print("parser:")
        for node in ast: print(node)
        print("Output:")
        for result in interpreter_result:
            print(result)

