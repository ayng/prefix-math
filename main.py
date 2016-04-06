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
        stdout.write('> ' + line)
        try:
            print evaluate(line)
        except EvalException as e:
            print e


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
            print evaluate(line)
        except EvalException as e:
            print e
    print '\nBye!'

def evaluate(expr):
    if expr == '':
        return ''
    result, _ = evaluate_helper(expr, 0)
    return result

def evaluate_helper(expr, i):
    '''Evaluate prefix notation math expression.
    
    Returns tuple of the form (evaluate_helperd expression, index i after evaluation).
    '''
    token, i = parse_token(expr, i)

    # Handle case of expression enclosed in parentheses.
    if token == '(':
        # Ensure first token after '(' is operator.
        token, i = parse_token(expr, i)
        if token not in ops.keys():
            raise EvalException('Operator {} expected. Found \'{}\'.'\
                                .format(ops.keys(), token))

        operation = ops[token]
        # Recursively call evaluate_helper on the rest of the tokens.
        arguments = list()
        next_token = token
        while next_token != ')':
            evaluated_expr, i = evaluate_helper(expr, i)
            arguments.append(evaluated_expr)
            next_token, _ = parse_token(expr, i)

        token, i = parse_token(expr, i)

        return reduce(operation, arguments), i

    # Handle bare expression not enclosed in parentheses.
    elif token == ')':
        raise EvalException('Unexpected ")".')
    else:
        try:
            value = int(token)
            return (value, i)
        except ValueError:
            raise EvalException('Token "{}" could not be parsed as integer.'\
                    .format(token))




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
