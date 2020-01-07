from functools import reduce
from lark import *
import copy
import enum

'''All tree type from AST tree'''
class Tree_type(enum.Enum):
    program = "program"
    plus = "plus"
    minus = "minus"
    multiply = "multiply"
    divide = "divide"
    modulus = "modulus"
    greater = "greater"
    smaller = "smaller"
    equal = "equal"
    def_stmt = "def_stmt"
    variable = "variable"
    fun_exp = "fun_exp"
    fun_call = "fun_call"
    fun_name = "fun_name"
    fun_ids = "fun_ids"
    fun_body = "fun_body"
    and_op = "and_op"
    or_op = "or_op"
    not_op = "not_op"
    if_exp = "if_exp"
    print_num = "print_num"
    print_bool = "print_bool"

'''All token type from AST tree'''
class Token_type(enum.Enum):
    NOT_TOKEN = "NOT_TOKEN"
    NUMBER = "NUMBER"
    BOOL_VAL = "BOOL_VAL"
    ID = "ID"

'''Error type for error handling'''
class Error_type(enum.Enum):
    NOT_NUMBER = 0
    NOT_BOOL = 1
    FUNC_NOT_EXIST = 2
    VAR_NOT_EXIST = 3
    ARGS_LEN_NOT_MATCH = 4
    SYNTAX_ERROR = 5

'''Class type for function define'''
class Def_function(object):
    def __init__(self, args, body, def_var, def_func):
        self.args, self.body, self.def_var, self.def_func = args, body, def_var, def_func
    def __call__(self, *params):
        '''argument length check'''
        if len(params) != len(self.args):
            error_handle(Error_type.ARGS_LEN_NOT_MATCH)

        '''new var, func map to this function'''
        new_def_var, new_def_func = copy.deepcopy(self.def_var), copy.deepcopy(self.def_func)
        for (arg, param) in zip(self.args, params):
            if isinstance(param, Def_function):
                new_def_func[arg] = param
            else:
                new_def_var[arg] = param

        '''execute all function code'''
        for def_stmt in self.body[:-1]:
            traverse(def_stmt, new_def_var, new_def_func)
        return traverse(self.body[-1], new_def_var, new_def_func)

def error_handle(error_type, arg="NULL"):
    if error_type == Error_type.NOT_NUMBER:
        print("Type Error: Expect 'number' but got 'boolean'")
    if error_type == Error_type.NOT_BOOL:
        print("Type Error: Expect 'boolean' but got 'number'")
    if error_type == Error_type.FUNC_NOT_EXIST:
        print("Error: Unknown function name {}".format(arg))
    if error_type == Error_type.VAR_NOT_EXIST:
        print("Error: Unknown variable name {}".format(arg))
    if error_type == Error_type.VAR_NOT_EXIST:
        print("Error: Length of argment not match")
    if error_type == Error_type.SYNTAX_ERROR:
        print("syntax error")
    exit(1)

def visit_all_child(tree, def_var, def_func, type_check=Token_type.NOT_TOKEN):
    # print("VISIT_ALL_CHILD", tree)
    childs = []
    for el in tree.children:
        if not isinstance(tree, Token):
            el = traverse(el, def_var, def_func)
        childs.append(el)
    
    if type_check != Token_type.NOT_TOKEN:
        # print(childs)
        if not all( Token_type(el.type) == type_check for el in childs ):
            if type_check == Token_type.NUMBER:
                error_handle(Error_type.NOT_NUMBER)
            elif type_check == Token_type.BOOL_VAL:
                error_handle(Error_type.NOT_BOOL)

    return childs

def traverse(tree, def_var={}, def_func={}):
    # print("[TRAVERSE]", tree)

    # token
    if isinstance(tree, Token):
        if Token_type(tree.type) == Token_type.ID:
            if tree in def_var:
                return def_var[tree]
        return tree

    # _stmt
    elif Tree_type(tree.data) == Tree_type.program:
        return visit_all_child(tree, def_var, def_func)

    # plus
    elif Tree_type(tree.data) == Tree_type.plus:
        return Token(Token_type.NUMBER.value, reduce((lambda a, b : a + b), [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]))
    # minus
    elif Tree_type(tree.data) == Tree_type.minus:
        return Token(Token_type.NUMBER.value, reduce((lambda a, b : a - b), [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]))
    # multiply
    elif Tree_type(tree.data) == Tree_type.multiply:
        return Token(Token_type.NUMBER.value, reduce((lambda a, b : a * b), [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]))    
    # divide
    elif Tree_type(tree.data) == Tree_type.divide:
        return Token(Token_type.NUMBER.value, reduce((lambda a, b : a // b), [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]))
    # modulus
    elif Tree_type(tree.data) == Tree_type.modulus:
        return Token(Token_type.NUMBER.value, reduce((lambda a, b : a % b), [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]))
    # greater
    elif Tree_type(tree.data) == Tree_type.greater:
        args = [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]
        return Token(Token_type.BOOL_VAL.value, "#t" if args[0] > args[1] else "#f")
    # smaller
    elif Tree_type(tree.data) == Tree_type.smaller:
        args = [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]
        return Token(Token_type.BOOL_VAL.value, "#t" if args[0] < args[1] else "#f")
    # equal
    elif Tree_type(tree.data) == Tree_type.equal:
        args = [int(el) for el in visit_all_child(tree, def_var, def_func, Token_type.NUMBER)]
        return Token(Token_type.BOOL_VAL.value, "#t" if all(el == args[0] for el in args) else "#f")

    # def_stmt
    elif Tree_type(tree.data) == Tree_type.def_stmt:
        [var, exp] = tree.children
        if isinstance(exp, Tree) and (Tree_type(exp.data) == Tree_type.fun_exp or Tree_type(exp.data) == Tree_type.fun_call):
            def_func[var] = traverse(exp, def_var, def_func)
        else:
            def_var[var] = traverse(exp, def_var, def_func)
        
    # fun_exp
    elif Tree_type(tree.data) == Tree_type.fun_exp:
        [fun_ids, fun_body] = visit_all_child(tree, def_var, def_func)
        return Def_function(fun_ids, fun_body, def_var, def_func)
    # fun_ids
    elif Tree_type(tree.data) == Tree_type.fun_ids:
        return tree.children
    # fun_body
    elif Tree_type(tree.data) == Tree_type.fun_body:
        return tree.children
    # fun_call
    elif Tree_type(tree.data) == Tree_type.fun_call:
        func = traverse(tree.children[0], def_var, def_func)
        params = [traverse(el, def_var, def_func) for el in tree.children[1:]]
        return func(*params)

    # fun_name
    elif Tree_type(tree.data) == Tree_type.fun_name:
        if tree.children[0] not in def_func:
            error_handle(Error_type.FUNC_NOT_EXIST, tree.children[0])
        else:
            return def_func[tree.children[0]]

    # and_op
    elif Tree_type(tree.data) == Tree_type.and_op:
        args = [el for el in visit_all_child(tree, def_var, def_func, Token_type.BOOL_VAL)]
        return Token(Token_type.BOOL_VAL.value, "#t" if all(el == "#t" for el in args) else "#f")
    # or_op
    elif Tree_type(tree.data) == Tree_type.or_op:
        args = [el for el in visit_all_child(tree, def_var, def_func, Token_type.BOOL_VAL)]
        return Token(Token_type.BOOL_VAL.value, "#f" if all(el == "#f" for el in args) else "#t")
    # not_op
    elif Tree_type(tree.data) == Tree_type.not_op:
        args = [el for el in visit_all_child(tree, def_var, def_func, Token_type.BOOL_VAL)]
        return Token(Token_type.BOOL_VAL.value, "#f" if args[0] == "#t" else "#t")

    # if_exp
    elif Tree_type(tree.data) == Tree_type.if_exp:
        test_exp = traverse(tree.children[0], def_var, def_func)
        if Token_type(test_exp.type) != Token_type.BOOL_VAL:
            error_handle(Error_type.NOT_BOOL)

        return traverse(tree.children[1 if test_exp == "#t" else 2], def_var, def_func)
            
    # print_num
    elif Tree_type(tree.data) == Tree_type.print_num:
        print_data = visit_all_child(tree, def_var, def_func, Token_type.NUMBER)[0]
        print(print_data)
        return print_data
        
    # print_bool
    elif Tree_type(tree.data) == Tree_type.print_bool:
        print_data = visit_all_child(tree, def_var, def_func, Token_type.BOOL_VAL)[0]
        print(print_data)
        return print_data

def main():
    '''grammer'''
    with open("./grammer/grammer.lark") as f:
        gram = f.read()
    lark = Lark(gram, start='program', parser='lalr')

    '''input lisp code'''
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    lisp_text = '\n'.join(lines)

    '''parse'''
    try:
        tree = lark.parse(lisp_text)
    except(UnexpectedInput, UnexpectedToken, UnexpectedCharacters) as e:
        error_handle(Error_type.SYNTAX_ERROR)

    '''traversal'''
    # print(tree)
    traverse(tree)

if __name__ == "__main__":
    main()