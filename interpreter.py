from b_types import *


class Interpreter():
    def __init__(self, ast_root : Node) -> None:
        self.ast_root: Node = ast_root

    def visit_a_expr(self):
        pass

    def visit_b_expr(self):
        pass

    def visit_i_expr(self):
        pass

    def call_coresp_visitor_func(self, node : Node):
        match node.type:
            case TokenType.I_EXPR:
                return self.visit_i_expr()
            case TokenType.B_EXPR:
                return self.visit_b_expr()
            case TokenType.A_EXPR:
                return self.visit_a_expr()
            case _:
                raise RuntimeError(f"No visitor function exists with node of type {node.type}")

    def run(self):
        for node in self.ast_root.children:
            self.call_coresp_visitor_func(node)