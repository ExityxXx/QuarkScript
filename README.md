# QuarkScript 🖥 - Programming Language in Python
## Description ✏
- QuarkScript is a low-level, interpreted programming language for solving various information-processing tasks and for helping to learn the process of creating programming languages.

# Technologies used 🛠
## Python 🐍
- We didn't use any helper libraries, creating flexibility
- We wrote a lexer, a parser and an interpreter
- In general, a sufficient amount for its programming language

# Stages of creating a programming language 👨‍💻
## Lexer 🔡
- A lexer reads the source code and breaks it down into tokens.
- The lexer generates strings, numbers, operator signs, etc.
- In general, I can say that this is the easiest stage in developing your own programming language.
## Parser 📜
- The parser reads the tokens received by the lexer and generates future syntax from them.
- The parser creates arithmetic expressions, taking into account the priorities of operators and parentheses.
- The parser is the most complex stage in development, because it generates the syntax tree, AST for short.
## Interpreter 🖨
- An interpreter is a command executor.
- The interpreter receives a list of nodes from the parser and performs the final computation.
- The interpreter outputs the value

# Syntax 📖
## Version beta-0.1
```
stdout 'Hello, World!
var value : Int = 50;
stdout value, type(value); // 50 Int
var name : String = "Alexandr";
stdout name, length(name), name.split(0, 4); // Alexandr 8 Alex
stdout type(50.5); // Float
var float_val : Float = 34.5;
var boolean : Bool = True;
var auto := "Hi";
```

# IDE ✒
- ## Our programming language has its own code editor, you can check it out in the repository
  - ### Link : TODO LINK
- ## Developed on tkinter
  - ### Link : TODO LINK 
