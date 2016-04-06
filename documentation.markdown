Syntax
------

* Arbitrary whitespace is allowed. This includes leading whitespace and whitespace between an open parenthesis and the operator token. For example, the following are valid expressions.

```
>                      (+ 1 2)
> (    + 1     2)
```

* Only integer numeric values are allowed.
* A complete expression is defined as either (1) a parentheses-matched expression or (2) a single whitespace-delimited token with no parentheses.
* Once a complete expression has been parsed, the rest of the input will be ignored. This can be used to create comments.

```
> () This is a comment.
```
* An operation cannot be introduced without parentheses. For example, this would not work.

```
> +
```
