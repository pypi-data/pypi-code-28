# -*- coding: utf-8 -*-
"""
Description for ES5 unparser.
"""

from __future__ import unicode_literals
from calmjs.parse.lexers.es5 import Lexer

from calmjs.parse.ruletypes import (
    OpenBlock,
    CloseBlock,
    EndStatement,
    Space,
    RequiredSpace,
    OptionalSpace,
    Newline,
    OptionalNewline,
    Indent,
    Dedent,
    PushScope,
    PopScope,
    PushCatch,
    PopCatch,
)
from calmjs.parse.ruletypes import (
    Attr,
    Text,
    Optional,
    JoinAttr,
    Operator,
    ElisionToken,
    ElisionJoinAttr,
)
from calmjs.parse.ruletypes import (
    Literal,
    Declare,
    Resolve,
    ResolveFuncName,
)
from calmjs.parse.ruletypes import (
    children_newline,
    children_comma,
)
from calmjs.parse.unparsers.base import BaseUnparser
from calmjs.parse import rules

value = (
    Attr('value'),
)

# definitions of all the rules for all the types for an ES5 program.
definitions = {
    'ES5Program': (
        children_newline,
        OptionalNewline,
    ),
    'Block': (
        OpenBlock,
        Indent, Newline,
        children_newline,
        Dedent, OptionalNewline,
        CloseBlock,
    ),
    'VarStatement': (
        Text(value='var'), Space, children_comma, EndStatement,
    ),
    'VarDecl': (
        Attr(Declare('identifier')), Optional('initializer', (
            Space, Operator(value='='), Space, Attr('initializer'),),),
    ),
    'VarDeclNoIn': (
        Text(value='var '), Attr(Declare('identifier')),
        Optional('initializer', (
            Space, Operator(value='='), Space, Attr('initializer'),),),
    ),
    'GroupingOp': (
        Text(value='('), Attr('expr'), Text(value=')'),
    ),
    'Identifier': (Attr(Resolve()),),
    'PropIdentifier': value,
    'Assign': (
        Attr('left'), OptionalSpace, Attr('op'), Space, Attr('right'),
    ),
    'GetPropAssign': (
        Text(value='get'), Space, Attr('prop_name'),
        PushScope,
        Text(value='('), Text(value=')'), Space,
        OpenBlock,
        Indent, Newline,
        JoinAttr(attr='elements', value=(Newline,)),
        Dedent, OptionalNewline,
        CloseBlock,
        PopScope,
    ),
    'SetPropAssign': (
        Text(value='set'), Space, Attr('prop_name'), Text(value='('),
        PushScope,
        Attr(Declare('parameter')), Text(value=')'), Space,
        OpenBlock,
        Indent, Newline,
        JoinAttr(attr='elements', value=(Newline,)),
        Dedent, OptionalNewline,
        CloseBlock,
        PopScope,
    ),
    'Number': value,
    'Comma': (
        Attr('left'), Text(value=','), Space, Attr('right'),
    ),
    'EmptyStatement': (EndStatement,),
    'If': (
        Text(value='if'), Space,
        Text(value='('), Attr('predicate'), Text(value=')'), Space,
        Attr('consequent'),
        Optional('alternative', (
            Newline, Text(value='else'), Space, Attr('alternative'),)),
    ),
    'Boolean': value,
    'For': (
        Text(value='for'), Space, Text(value='('),
        Attr('init'),
        OptionalSpace, Attr('cond'),
        OptionalSpace, Attr('count'),
        Text(value=')'), Space, Attr('statement'),
    ),
    'ForIn': (
        Text(value='for'), Space, Text(value='('),
        Attr('item'),
        Space, Text(value='in'), Space,
        Attr('iterable'), Text(value=')'), Space, Attr('statement'),
    ),
    'BinOp': (
        Attr('left'), Space, Operator(attr='op'), Space, Attr('right'),
    ),
    'UnaryExpr': (
        Operator(attr='op'), OptionalSpace, Attr('value'),
    ),
    'PostfixExpr': (
        Operator(attr='value'), Attr('op'),
    ),
    'ExprStatement': (
        Attr('expr'), EndStatement,
    ),
    'DoWhile': (
        Text(value='do'), Space, Attr('statement'), Space,
        Text(value='while'), Space, Text(value='('),
        Attr('predicate'), Text(value=')'), EndStatement,
    ),
    'While': (
        Text(value='while'), Space,
        Text(value='('), Attr('predicate'), Text(value=')'), OptionalSpace,
        Attr('statement'),
    ),
    'Null': (
        Text(value='null'),
    ),
    'String': (
        Attr(Literal()),
    ),
    'Continue': (
        Text(value='continue'), Optional('identifier', (
            Space, Attr(attr='identifier'))), EndStatement,
    ),
    'Break': (
        Text(value='break'), OptionalSpace, Optional('identifier', (
            Attr(attr='identifier'),)), EndStatement,
    ),
    'Return': (
        Text(value='return'), Optional('expr', (
            Space, Attr(attr='expr'))), EndStatement,
    ),
    'With': (
        Text(value='with'), Space,
        # should _really_ have a token for logging a warning
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/
        #   Reference/Statements/with
        Text(value='('), Attr('expr'), Text(value=')'), Space,
        Attr('statement'),
    ),
    'Label': (
        Attr('identifier'), Text(value=':'), Space, Attr('statement'),
    ),
    'Switch': (
        Text(value='switch'), Space,
        Text(value='('), Attr('expr'), Text(value=')'), Space,
        Attr('case_block'),
    ),
    'CaseBlock': (
        OpenBlock,
        Indent, Newline,
        children_newline,
        Dedent, OptionalNewline,
        CloseBlock,
    ),
    'Case': (
        Text(value='case'), Space, Attr('expr'), Text(value=':'),
        Indent, Newline,
        JoinAttr('elements', value=(Newline,)),
        Dedent,
    ),
    'Default': (
        Text(value='default'), Text(value=':'),
        Indent, Newline,
        JoinAttr('elements', value=(Newline,)),
        Dedent,
    ),
    'Throw': (
        Text(value='throw'), Space, Attr('expr'), EndStatement,
    ),
    'Debugger': (
        Text(value='debugger'), EndStatement,
    ),
    'Try': (
        Text(value='try'), Space, Attr('statements'),
        Optional('catch', (Newline, Attr('catch'),)),
        Optional('fin', (Newline, Attr('fin'),)),
    ),
    'Catch': (
        Text(value='catch'), Space,
        PushCatch,
        Text(value='('), Attr('identifier'), Text(value=')'), Space,
        Attr('elements'),
        PopCatch,
    ),
    'Finally': (
        Text(value='finally'), Space, Attr('elements'),
    ),
    'FuncDecl': (
        Text(value='function'), Optional('identifier', (RequiredSpace,)),
        Attr(Declare('identifier')), Text(value='('),
        PushScope, Optional('identifier', (ResolveFuncName,)),
        JoinAttr(Declare('parameters'), value=(Text(value=','), Space)),
        Text(value=')'), Space,
        OpenBlock,
        Indent, Newline,
        JoinAttr('elements', value=(Newline,)),
        Dedent, OptionalNewline,
        CloseBlock,
        PopScope,
    ),
    'FuncExpr': (
        Text(value='function'), Optional('identifier', (RequiredSpace,)),
        Attr(Declare('identifier')), Text(value='('),
        PushScope, Optional('identifier', (ResolveFuncName,)),
        JoinAttr(Declare('parameters'), value=(Text(value=','), Space,)),
        Text(value=')'), Space,
        OpenBlock,
        Indent, Newline,
        JoinAttr('elements', value=(Newline,)),
        Dedent, OptionalNewline,
        CloseBlock,
        PopScope,
    ),
    'Conditional': (
        Attr('predicate'), Space, Text(value='?'), Space,
        Attr('consequent'), Space, Text(value=':'), Space,
        Attr('alternative'),
    ),
    'Regex': value,
    'NewExpr': (
        Text(value='new'), Space, Attr('identifier'), Attr('args'),
    ),
    'DotAccessor': (
        Attr('node'), Text(value='.'), Attr('identifier'),
    ),
    'BracketAccessor': (
        Attr('node'), Text(value='['), Attr('expr'), Text(value=']'),
    ),
    'FunctionCall': (
        Attr('identifier'), Attr('args'),
    ),
    'Arguments': (
        Text(value='('),
        JoinAttr('items', value=(Text(value=','), Space)),
        Text(value=')'),
    ),
    'Object': (
        Text(value='{'),
        Optional('properties', (
            Indent, Newline,
            JoinAttr('properties', value=(Text(value=','), Newline,)),
            Dedent, Newline,
        )),
        Text(value='}'),
    ),
    'Array': (
        Text(value='['),
        ElisionJoinAttr('items', value=(Space,)),
        Text(value=']'),
    ),
    'Elision': (
        ElisionToken(attr='value', value=','),
    ),
    'This': (
        Text(value='this'),
    ),
}


class Unparser(BaseUnparser):

    def __init__(
            self,
            definitions=definitions,
            token_handler=None,
            rules=(rules.default(),),
            layout_handlers=None,
            deferrable_handlers=None,
            prewalk_hooks=()):

        super(Unparser, self).__init__(
            definitions=definitions,
            token_handler=token_handler,
            rules=rules,
            layout_handlers=layout_handlers,
            deferrable_handlers=deferrable_handlers,
            prewalk_hooks=prewalk_hooks,
        )


def pretty_printer(indent_str='    '):
    """
    Construct a pretty printing unparser
    """

    return Unparser(rules=(rules.indent(indent_str=indent_str),))


def pretty_print(ast, indent_str='  '):
    """
    Simple pretty print function; returns a string rendering of an input
    AST of an ES5 Program.

    arguments

    ast
        The AST to pretty print
    indent_str
        The string used for indentations.  Defaults to two spaces.
    """

    return ''.join(chunk.text for chunk in pretty_printer(indent_str)(ast))


def minify_printer(
        obfuscate=False,
        obfuscate_globals=False,
        shadow_funcname=False,
        drop_semi=False):
    """
    Construct a minimum printer.

    Arguments

    obfuscate
        If True, obfuscate identifiers nested in each scope with a
        shortened identifier name to further reduce output size.

        Defaults to False.
    obfuscate_globals
        Also do the same to identifiers nested on the global scope; do
        not enable unless the renaming of global variables in a not
        fully deterministic manner into something else is guaranteed to
        not cause problems with the generated code and other code that
        in the same environment that it will be executed in.

        Defaults to False for the reason above.
    drop_semi
        Drop semicolons whenever possible (e.g. the final semicolons of
        a given block).
    """

    active_rules = [rules.minify(drop_semi=drop_semi)]
    if obfuscate:
        active_rules.append(rules.obfuscate(
            obfuscate_globals=obfuscate_globals,
            shadow_funcname=shadow_funcname,
            reserved_keywords=(Lexer.keywords_dict.keys())
        ))
    return Unparser(rules=active_rules)


def minify_print(
        ast,
        obfuscate=False,
        obfuscate_globals=False,
        shadow_funcname=False,
        drop_semi=False):
    """
    Simple minify print function; returns a string rendering of an input
    AST of an ES5 program

    Arguments

    ast
        The AST to minify print
    obfuscate
        If True, obfuscate identifiers nested in each scope with a
        shortened identifier name to further reduce output size.

        Defaults to False.
    obfuscate_globals
        Also do the same to identifiers nested on the global scope; do
        not enable unless the renaming of global variables in a not
        fully deterministic manner into something else is guaranteed to
        not cause problems with the generated code and other code that
        in the same environment that it will be executed in.

        Defaults to False for the reason above.
    drop_semi
        Drop semicolons whenever possible (e.g. the final semicolons of
        a given block).
    """

    return ''.join(chunk.text for chunk in minify_printer(
        obfuscate, obfuscate_globals, shadow_funcname, drop_semi)(ast))
