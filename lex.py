# terminals attach themselves since they were already constructed by the lexer
def main():
        self = None
        match self.tokens:
                case [a]: 
                        current_node.add_child(a)
                        tokens.remove(a)
                        return
                case [a, b, c]:
                        current_node.add_child(a)
                        current_node.add_child(b)
                        current_node.add_child(c)
                        self._pop_tokens([a,b,c])
                        return
                case [a, b, *rest]:
                        current_node.add_child(a)
                        current_node.add_child(b)
                        self._pop_tokens([a,b])
                        self.A_EXPR(current_node)
                case _:
                        raise ParseError("A_EXPR fell through")