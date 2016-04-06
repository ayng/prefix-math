import fileinput
from sys import stdin, stdout
from operator import add, sub, mul, div

ops = {'+': add, '-': sub, '*': mul, '/': div, '\\': div}
special_tokens = ('(', ')')

def main():
    if stdin.isatty():
        run_interactively()
    else:
        run_from_stdin()

def run_from_stdin():
    '''Read from stdin all at once.'''
    for line in stdin:
        line = line.rstrip('\n')
        try:
            print format_output(evaluate(line))
        except EvalException as e:
            print "Error: {}".format(e)


def run_interactively():
    '''Start a prompt which the user can type into.'''
    while True:
        try:
            line = raw_input('> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break

        try:
            print format_output(evaluate(line))
        except EvalException as e:
            print e
    print '\nBye!'

def evaluate(expr):
    '''Evaluates expression and returns result.
    
    Raises EvalException upon error.

    Returns either a Python list or integer.
    '''

    def evaluate_helper(expr, i):
        '''Evaluate prefix notation math expression.
        
        Returns tuple of the form (evaluate_helperd expression, index i after evaluation).
        '''
        token, i = parse_token(expr, i)

        # Handle case of expression enclosed in parentheses.
        if token == '(':
            # If there is an operator, set the OPERATION variable.
            operation = None
            next_token = peek_token(expr, i)
            if next_token in ops.keys():
                token, i = parse_token(expr, i)
                operation = ops[token]

            # Recursively call evaluate_helper on the rest of the tokens.
            arguments = list()
            next_token = peek_token(expr, i)
            while next_token != ')':
                evaluated_expr, i = evaluate_helper(expr, i)
                # Result of recursive call could be list or number.
                if type(evaluated_expr) is list:
                    arguments += evaluated_expr
                elif type(evaluated_expr) is int:
                    arguments.append(evaluated_expr)

                if i >= len(expr):
                    raise EvalException('Missing ")".')
                next_token = peek_token(expr, i)

            # Skip next token, which we peeked and found to be ')'.
            token, i = parse_token(expr, i)

            if operation and len(arguments) > 0:
                return reduce(operation, arguments), i
            elif operation and len(arguments) == 0:
                raise EvalException('Found operation with no arguments.')
            else:
                return arguments, i

        # Handle bare expression not enclosed in parentheses.
        elif token == ')':
            raise EvalException('Unexpected ")".')
        else:
            try:
                value = int(token)
                return (value, i)
            except ValueError:
                raise EvalException('"{}" could not be parsed.'\
                        .format(token))
    
    # End of function definition for evaluate_helper

    # An empty string will cause tokenizer to fail
    if expr == '':
        return None
    result, _ = evaluate_helper(expr, 0)
    return result

def format_output(obj):
    if obj is None:
        return ''
    elif type(obj) is list:
        if len(obj) == 0:
            return ''
        obj = map(str, obj)
        return '({})'.format(' '.join(obj))
    elif type(obj) is int:
        return str(obj)
        
def peek_token(expr, i):
    token, _ = parse_token(expr, i)
    return token

def parse_token(expr, i):
    '''Reads the next token in EXPR after index I, ignoring leading whitespace.
    Special tokens such as '(' and ')' do not have to be whitespace-delimited
    to be considered tokens.
    
    Returns tuple of the form (token, index i after token).
    '''
    # Skip leading whitespace.
    while expr[i].isspace():
        i += 1
    
    # Handle special tokens, which halts parsing before finding whitespace.
    if expr[i] in special_tokens:
        return (expr[i], i + 1)

    # For the rest, tokenize by whitespace or by special character.
    token_begin = i
    while i < len(expr) and not expr[i].isspace() \
            and expr[i] not in special_tokens:
        i += 1
    token_end = i

    return (expr[token_begin:token_end], token_end)


class EvalException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

if __name__ == '__main__':
    main()
