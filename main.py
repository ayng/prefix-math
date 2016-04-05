import fileinput
from sys import stdin, stdout

def main():
    if stdin.isatty():
        run_interactively()
    else:
        # Read from stdin
        for line in stdin:
            stdout.write('> ' + line)
            evaluate(line)

def run_interactively():
    '''Start a prompt which the user can type into.'''
    try:
        while True:
            stdout.write('> ')
            line = stdin.readline()
            print line
    except KeyboardInterrupt:
        pass
    finally:
        print '\nBye!'

def evaluate(expr):
    '''Evaluate prefix notation math expression.'''
    print '(answer here)'


if __name__ == '__main__':
    main()
