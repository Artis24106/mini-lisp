# MiniLisp Interpreter

## Feature
### Basic Feature
| Feature              | Description                                      | Points |
| -------------------- | ------------------------------------------------ | ------ |
| Syntax Validation    | Print "syntax error" when parsing invalid syntax | 10     |
| Print                | Implement `print-num` statement                  | 10     |
| Numerical Operations | Implement all numerical operations               | 25     |
| Logical Operations   | Implement all logical operations                 | 25     |
| `if` Expression      | Implement `if` expression                        | 8      |
| Variable Definition  | Able to define a variable                        | 8      |
| Function             | Able to declare and call an anonymoux function   | 8      |
| Named Function       | Able declare and call a named function           | 6      |

### Bonus Feature
| Feature              | Description                             | Points |
| -------------------- | --------------------------------------- | ------ |
| Recursion            | Support recursive function call         | 5      |
| Type Checking        | Print error messages for type errors    | 5      |
| Nested Function      | Nested function (static scope)          | 5      |
| First-class Function | Able to pass functions, support closure | 5      |

## Dependencies
- python3
- [ark-parser/lark](https://github.com/lark-parser/lark)

## Usage
### set up
```bash=1
git clone https://github.com/Artis24106/mini-lisp.git
cd mini-lisp
```
### run it!
```bash=1
python3 miniLisp.py
# and input lisp code
```
### or you can just redirect .lsp file as input
```bash=1
python3 miniLisp.py < myLisp.lsp
```

## Operations
### Numerical Operators

| Name     | Symbol | Example     | Example Output | Parameter Type | Output Type |
| -------- | ------ | ----------- | -------------- | -------------- | ----------- |
| Plus     | `+`    | `(+ 1 2)`   | `3`            | Number(s)      | Number      |
| Minus    | `-`    | `(- 1 2)`   | `-1`           | Number(s)      | Number      |
| Multiply | `*`    | `(* 1 2)`   | `2`            | Number(s)      | Number      |
| Divide   | `/`    | `(/ 8 4)`   | `2`            | Number(s)      | Number      |
| Modulus  | `mod`  | `(mod 8 4)` | `0`            | Number(s)      | Number      |
| Greater  | `>`    | `(> 1 2)`   | `#f`           | Number(s)      | Boolean     |
| Smaller  | `<`    | `(< 1 2)`   | `#t`           | Number(s)      | Boolean     |
| Equal    | `=`    | `(= 1 2)`   | `#f`           | Number(s)      | Boolean     |

### Logical Operators

| Name | Symbol | Example       | Example Output | Parameter Type | Output Type |
| ---- | ------ | ------------- | -------------- | -------------- | ----------- |
| And  | `and`  | `(and #t #f)` | `#f`           | Boolean(s)     | Boolean     |
| Or   | `or`   | `(or #t #f)`  | `#t`           | Boolean(s)     | Boolean     |
| Not  | `not`  | `(not #t)`    | `#f`           | Boolean        | Boolean     |

### Other Operators
| Symbol   | Parameter Type | Output Type                         |
| -------- | -------------- | ----------------------------------- |
| `define` | Boolean(s)     | no output                           |
| `fun`    | Any            | Depend on function                  |
| `if`     | Any            | Depend on `then-exp` and `else-exp` |