from b_types import *


class Interpreter():
    def __init__(self, ast_root : Node) -> None:
        self.ast_root: Node = ast_root

        self.program_counter = 0
        self.symbol_table: dict[str, object] = {}


    def eval_expr(self, node : Node) -> object:
        children = node.children
        
        if node.type is TokenType.A_EXPR or node.type is TokenType.B_EXPR:
            # should be some form of left op right
            if len(children) == 3:
                l_val = self.eval_expr(children[0])
                r_val = self.eval_expr(children[2])
                
                # I'm pretty sure Python's semantics for addition of strings and ints
                # is pretty much the same as BASICS, this makes things a lot easier 
                match children[1].value:
                    case '+':
                        return l_val + r_val
                    case '-':
                            # right associativity
                            # this works, but I should spend some time and figure out the best way to mangle the tree
                            # so that I don't have to flip the order of evaluation to something that really doesn't make sense
                            return r_val - l_val
                    case '/' if r_val > 0:
                            return l_val / r_val
                    case '/':
                            raise ZeroDivisionError(f"Division by zero in {l_val}/{r_val} near line={children[1].line} col={children[1].col}")
                    case '*':
                            return l_val * r_val
                    case _:
                            raise RuntimeError(f"Fell through on {children[1].value}")
            # node with a singular child, just need get the value of the child
            else:
                return self.eval_expr(children[0])
        # I_EXPRs may hold values, simple expressions that can be evluated without recursion
        # or a nested A_EXPR
        elif node.type is TokenType.I_EXPR:     
            
            # (expr)
            if len(children) == 3 and \
            children[0].type is TokenType.L_PAREN and children[2].type is TokenType.R_PAREN:
                return self.eval_expr(children[1])
            # value
            elif len(children) == 1:
                match children[0].type:
                    case TokenType.NUMBER:
                        return int(children[0].value)
                    case TokenType.IDENT:
                        if children[0].value in self.symbol_table:
                            return self.symbol_table[children[0].value]
                        else:
                            raise RuntimeError(f"token={children[0].value} is undefined at row={children[0].line} col={children[0].col}")
                    case _:
                        return (children[0].value)
            elif len(children) == 4 and \
                children[1].type is TokenType.L_PAREN and children[3].type is TokenType.R_PAREN:
                 return -1 * self.eval_expr(children[2])
            