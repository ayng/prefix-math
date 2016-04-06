Purpose
-------

This program parses and evaluates mathematical expressions in prefix (aka Polish) notation.

How to run
----------

You can either just run it plain,

```
$ python main.py
```

Or pass in a file through stdin, where each line of the file is one expression you would like evaluated.

```
$ python main.py < tests.txt
```

Syntax
------

* Arbitrary whitespace is allowed. This includes leading whitespace and whitespace between an open parenthesis and the operator token. For example, the following are valid expressions.

```
>                      (+ 1 2)
> (    + 1     2)
```

* Only integer numeric values are allowed.
  * To specify negative integers, include a "-" character before the number to be negated, with no whitespace in between. You can also specify positive integers with "+" in the same manner, but integers are positive by default, so this is not necessary.
* A complete expression is defined as either (1) a parentheses-matched expression or (2) a single whitespace-delimited token with no parentheses.
* Once a complete expression has been parsed, the rest of the input will be ignored. This can be used to create comments.

```
> () This is a comment.
> (+ 1 2))))) These rogue close parentheses don't matter!
```

* An expression can either evaluate to a numerical value or a list.

```
> (1 2 3) This evaluates to a list.
> (+ 1 2 3) This evaluates to a numerical value.
```

* An operation cannot be introduced without parentheses. For example, this would cause an error.

```
> +
```

* An operator cannot be introduced without arguments. This would cause an error.

```
> (+)
```
