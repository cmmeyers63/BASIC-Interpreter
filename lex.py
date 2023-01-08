import re
from ast_types import *

class Lexer():
        def __init__(self, filename : str) -> None:
                self._filename = filename
                self._integer_re = re.compile("\d")
                self._identifer_re = re.compile("^[a-zA-Z]+$")

                self._line_num = 0
                self._column_num = 0
                self._current_line = []

        def __del__()

        def _build_token(self, str_tok : str) -> Token:
                match str_tok:
                        case '(':
                                return Token(TokenType.L_PAREN)
                        case ')':
                                return Token(TokenType.R_PAREN)
                        case '=':
                                return Token(TokenType.EQUALS)
                        case '+':
                                return Token(TokenType.PLUS)
                        case '-':
                                return Token(TokenType.MINUS)
                        case '*':
                                return Token(TokenType.TIMES)
                        case '/':
                                return Token(TokenType.DIVIDE)
                        case ';':
                                return Token(TokenType.END_OF_STMT)
                        case '**':
                                return Token(TokenType.POW)

                # integer test
                match = self._integer_re.match(str_tok)
                if match is not None:
                        return Token(TokenType.VALUE, value=int(str_tok))
                
                match = self._identifer_re.match(str_tok)
                if match is not None:
                        return Token(TokenType.IDENTIFIER, value=str_tok)
                
                raise ValueError(f"Unexpected token : {str_tok}")

        def lex(input : list[str]) -> list[Token]:
                user_in = [x for x in user_in if x != "" or x != " "]

                print(f"start build token")
                tokens = []
                for char in user_in:
                        print(f"\t in : {char}")
                        token = build_token(char)
                        print(f"\t out: {token}")
                        tokens.append(token)
                print("end build token")
                return tokens


        def peek(self, token_type_list : list[TokenType]) -> bool:
                for tok in token_type_list:
                        result : bool = self._peek(tok)
                        if not result:
                                return result
                return True

        def peek(self, token_type : TokenType) -> bool:
                pass