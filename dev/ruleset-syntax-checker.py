#!/usr/bin/env python3
"""
ruleset_checker.py
-------------------
A syntax checker for documents written in the RuleSet DSL, implemented
directly from the RuleSet.tx grammar (a textX grammar file).

No external dependencies are required (pure Python 3 standard library),
so this works in environments where the `textX` package cannot be
installed.

Usage:
    python3 ruleset_checker.py path/to/rules_file.dsl [more_files ...]
    python3 ruleset_checker.py --no-warnings path/to/rules_file.dsl

Exit code is 0 if every file is syntactically valid, 1 otherwise.

Design notes
------------
This is a hand-written recursive-descent (PEG-style) parser that mirrors
the rule definitions in RuleSet.tx one-for-one:

    RuleSet -> SetValueRule* ColumnRule+ BlockInColumnValueRule*
               InColumnValueRule* ConditionalRule*

Alternatives within a grammar rule (e.g. `HasValueTypeRule | HasValueFormatRule
| ...`) are tried in the exact order they appear in the .tx file. If a
rule's leading keyword doesn't match at all, we backtrack silently and try
the next alternative (a "soft fail"). Once a rule's leading keyword HAS
matched (so we're confident about the author's intent), any further
failure to complete that rule raises a hard syntax error with a precise
line/column, instead of silently backtracking -- this gives far more
useful error messages than a generic "no alternative matched" would.

One deliberate leniency: the grammar's `FormatType` rule is a bare
(unquoted) literal match rule, but every example in the RuleSet
documentation writes format strings in quotes, e.g. `has format "YYYY-MM-DD"`.
To stay useful against real-world documents, `has format` accepts the
format literal with or without surrounding quotes.
"""

import argparse
import re
import sys


# --------------------------------------------------------------------------
# Terminals
# --------------------------------------------------------------------------

STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"' + r"|'(?:\\.|[^'\\])*'")
NUMBER_RE = re.compile(r'[+-]?\d+(\.\d+)?([eE][+-]?\d+)?')
INT_RE = re.compile(r'[+-]?\d+')
WS_RE = re.compile(r'\s+')
REGEX_LITERAL_RE = re.compile(r'/.*/')

VALUE_TYPES = ['string', 'integer', 'floating point', 'boolean',
               'date-time', 'scientific', 'complex']

FORMAT_TYPES = [
    'HH:mm:ss', 'HH:mm', 'hh:mm:ss AM/PM', 'hh:mm AM/PM', 'HHmmss',
    'YYYY-MM-DDTHH:mm:ss+hh:mm', 'YYYY-MM-DDTHH:mm:ss.sssZ',
    'YYYY-MM-DDTHH:mm:ss', 'YYYY-MM-DD HH:mm:ss', 'YYYY-MM-DD HH:mm',
    'YYYY-MM-DDTHH:mm', 'DD/MM/YYYY HH:mm:ss', 'MM-DD-YYYY hh:mm:ss AM/PM',
    'YYYY/MM/DD HH:mm:ss', 'YYYY-MM-DD', 'MM-DD-YYYY', 'DD-MM-YYYY',
    'YYYY/MM/DD', 'MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY.MM.DD', 'MM.DD.YYYY',
    'DD.MM.YYYY', 'YYYYMMDD', 'YYYY',
    '[N,S]DD.DDDD', '[E,W]DD.DDDD',
]
# Try longest literals first so e.g. 'YYYY-MM-DD' isn't shadowed by 'YYYY'.
FORMAT_TYPES_BY_LEN = sorted(FORMAT_TYPES, key=len, reverse=True)


class RuleSetSyntaxError(Exception):
    def __init__(self, line, col, message, line_text=""):
        self.line = line
        self.col = col
        self.message = message
        self.line_text = line_text
        super().__init__(f"line {line}, col {col}: {message}")


def strip_comments(text):
    """Replace // line comments and /* */ block comments with spaces,
    preserving newlines and string literal contents, so that character
    positions (and therefore line numbers) stay accurate."""
    out = []
    i, n = 0, len(text)
    in_string = None
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == in_string:
                in_string = None
            i += 1
            continue
        if c in ('"', "'"):
            in_string = c
            out.append(c)
            i += 1
            continue
        if text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j == -1 else j
            out.append(' ' * (j - i))
            i = j
            continue
        if text.startswith('/*', i):
            j = text.find('*/', i + 2)
            end = n if j == -1 else j + 2
            out.append(''.join(ch if ch == '\n' else ' ' for ch in text[i:end]))
            i = end
            continue
        out.append(c)
        i += 1
    return ''.join(out)


class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.n = len(text)

    # -- low level -------------------------------------------------------

    def skip_ws(self):
        m = WS_RE.match(self.text, self.pos)
        if m:
            self.pos = m.end()

    def literal(self, lit):
        save = self.pos
        self.skip_ws()
        if self.text.startswith(lit, self.pos):
            end = self.pos + len(lit)
            if lit[-1].isalnum() and end < self.n and \
                    (self.text[end].isalnum() or self.text[end] == '_'):
                self.pos = save
                return False
            self.pos = end
            return True
        self.pos = save
        return False

    def regex(self, pattern):
        save = self.pos
        self.skip_ws()
        m = pattern.match(self.text, self.pos)
        if m:
            self.pos = m.end()
            return m
        self.pos = save
        return None

    def _line_col(self, pos):
        line = self.text.count('\n', 0, pos) + 1
        last_nl = self.text.rfind('\n', 0, pos)
        col = pos - last_nl
        return line, col

    def _line_text(self, line_no):
        lines = self.text.split('\n')
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1].strip()
        return ""

    def error(self, msg, pos=None):
        pos = self.pos if pos is None else pos
        line, col = self._line_col(pos)
        raise RuleSetSyntaxError(line, col, msg, self._line_text(line))

    # -- terminals ---------------------------------------------------------

    def p_string(self):
        m = self.regex(STRING_RE)
        return m.group(0) if m else None

    def p_number(self):
        m = self.regex(NUMBER_RE)
        return m.group(0) if m else None

    def p_int(self):
        m = self.regex(INT_RE)
        return m.group(0) if m else None

    def p_value(self):
        v = self.p_string()
        if v is not None:
            return v
        return self.p_number()

    def p_column_name(self):
        return self.p_string()

    def p_value_type(self):
        for lit in VALUE_TYPES:
            save = self.pos
            if self.literal(lit):
                return lit
            self.pos = save
        return None

    def p_format_type(self):
        # Lenient: accept an optional matching pair of quotes around the
        # literal, since documentation examples quote format strings even
        # though the grammar's FormatType rule is unquoted.
        save = self.pos
        self.skip_ws()
        quote = None
        if self.pos < self.n and self.text[self.pos] in ('"', "'"):
            quote = self.text[self.pos]
            self.pos += 1
        for lit in FORMAT_TYPES_BY_LEN:
            save2 = self.pos
            if self.text.startswith(lit, self.pos):
                self.pos += len(lit)
                if quote:
                    if self.pos < self.n and self.text[self.pos] == quote:
                        self.pos += 1
                        return lit
                    else:
                        self.pos = save2
                        continue
                return lit
            self.pos = save2
        self.pos = save
        return None

    def p_regex_literal(self):
        m = self.regex(REGEX_LITERAL_RE)
        return m.group(0) if m else None

    def p_string_or_int(self):
        v = self.p_string()
        if v is not None:
            return v
        return self.p_int()

    def p_list(self, item_fn, ctx_name):
        """Parse '[' item (',' item)* ']'. Caller must have already
        confirmed the '[' is expected (i.e. we're committed)."""
        if not self.literal('['):
            self.error(f"Expected '[' to start the {ctx_name} list")
        items = []
        it = item_fn()
        if it is not None:
            items.append(it)
            while True:
                save = self.pos
                if self.literal(','):
                    it2 = item_fn()
                    if it2 is None:
                        self.error(f"Expected another value after ',' in the {ctx_name} list")
                    items.append(it2)
                else:
                    self.pos = save
                    break
        if not self.literal(']'):
            self.error(
                f"Expected ']' to close the {ctx_name} list "
                f"(check for a missing comma between items, or an unquoted value)"
            )
        return items

    # -- SetValueRule --------------------------------------------------

    def try_set_null_values_rule(self):
        save = self.pos
        if self.literal('allowed null values in'):
            vals = self.p_list(self.p_value, "allowed null values")
            return ('SetNullValuesRule', vals)
        self.pos = save
        return None

    def try_set_locale_rule(self):
        save = self.pos
        if self.literal('set locale as'):
            v = self.p_string()
            if v is None:
                self.error("Expected a quoted string after 'set locale as'")
            return ('SetLocaleRule', v)
        self.pos = save
        return None

    def try_thousands_separator_rule(self):
        save = self.pos
        if self.literal('thousands separator is'):
            v = self.p_string()
            if v is None:
                self.error("Expected a quoted string after 'thousands separator is'")
            return ('ThousandsSeparatorRule', v)
        self.pos = save
        return None

    def try_set_global_tolerance_rule(self):
        save = self.pos
        if self.literal('set tolerance at'):
            v = self.p_value()
            if v is None:
                self.error("Expected a number after 'set tolerance at'")
            return ('SetGlobalToleranceRule', v)
        self.pos = save
        return None

    def try_ignore_null_warnings_rule(self):
        save = self.pos
        if self.literal('ignore null warnings'):
            return ('IgnoreNullWarningsRule', True)
        self.pos = save
        return None

    def try_set_value_rule(self):
        for fn in (self.try_set_null_values_rule, self.try_set_locale_rule,
                   self.try_thousands_separator_rule,
                   self.try_set_global_tolerance_rule,
                   self.try_ignore_null_warnings_rule):
            r = fn()
            if r is not None:
                return r
        return None

    # -- ColumnRule ------------------------------------------------------

    def try_column_list_rule(self):
        save = self.pos
        if self.literal('column names in'):
            names = self.p_list(self.p_column_name, "column names")
            return ('ColumnListRule', names)
        self.pos = save
        return None

    def try_required_columns_rule(self):
        save = self.pos
        if self.literal('all columns required'):
            return ('RequiredColumnsRule', True)
        self.pos = save
        return None

    def try_extra_columns_rule(self):
        save = self.pos
        if self.literal('no extra columns allowed'):
            return ('ExtraColumnsRule', True)
        self.pos = save
        return None

    def try_column_order_rule(self):
        save = self.pos
        if self.literal('check column order'):
            return ('ColumnOrderRule', True)
        self.pos = save
        return None

    def try_column_rule(self):
        for fn in (self.try_column_list_rule, self.try_required_columns_rule,
                   self.try_extra_columns_rule, self.try_column_order_rule):
            r = fn()
            if r is not None:
                return r
        return None

    # -- ColumnValueRule (order matches the .tx file exactly) -----------

    def try_has_value_type_rule(self):
        save = self.pos
        if self.literal('has value type'):
            vt = self.p_value_type()
            if vt is None:
                # soft fail: could be 'has value type in [...]' instead
                self.pos = save
                return None
            return ('HasValueTypeRule', vt)
        self.pos = save
        return None

    def try_has_value_format_rule(self):
        save = self.pos
        if self.literal('has format'):
            ft = self.p_format_type()
            if ft is None:
                self.error(
                    "Expected a recognized date/time format after 'has format' "
                    "(see Appendix B for the list of supported formats)"
                )
            return ('HasValueFormatRule', ft)
        self.pos = save
        return None

    def try_has_value_type_in_rule(self):
        save = self.pos
        if self.literal('has value type in'):
            vts = self.p_list(self.p_value_type, "value types")
            return ('HasValueTypeInRule', vts)
        self.pos = save
        return None

    def try_is_unique_rule(self):
        save = self.pos
        if self.literal('is unique'):
            return ('IsUniqueRule', True)
        self.pos = save
        return None

    def try_is_required_rule(self):
        save = self.pos
        if self.literal('is required'):
            return ('IsRequiredRule', True)
        self.pos = save
        return None

    def try_is_null_rule(self):
        save = self.pos
        if self.literal('is null'):
            return ('IsNullRule', True)
        self.pos = save
        return None

    def try_is_not_null_rule(self):
        save = self.pos
        if self.literal('is not null'):
            return ('IsNotNullRule', True)
        self.pos = save
        return None

    def try_value_in_rule(self):
        save = self.pos
        if self.literal('is in'):
            vals = self.p_list(self.p_value, "'is in'")
            return ('ValueInRule', vals)
        self.pos = save
        return None

    def try_value_not_in_rule(self):
        save = self.pos
        if self.literal('is not in'):
            vals = self.p_list(self.p_value, "'is not in'")
            return ('ValueNotInRule', vals)
        self.pos = save
        return None

    def try_has_value_rule(self):
        save = self.pos
        if self.literal('is'):
            v = self.p_string()
            if v is None:
                self.pos = save  # soft fail (e.g. 'is ==' / 'is >' etc.)
                return None
            return ('HasValueRule', v)
        self.pos = save
        return None

    def try_not_has_value_rule(self):
        save = self.pos
        if self.literal('is not'):
            v = self.p_string()
            if v is None:
                self.pos = save
                return None
            return ('NotHasValueRule', v)
        self.pos = save
        return None

    def try_is_equal_to_rule(self):
        save = self.pos
        if self.literal('is =='):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is =='")
            return ('IsEqualToRule', v)
        self.pos = save
        return None

    def try_is_not_equal_to_rule(self):
        save = self.pos
        if self.literal('is !='):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is !='")
            return ('IsNotEqualToRule', v)
        self.pos = save
        return None

    def try_is_greater_than_rule(self):
        save = self.pos
        if self.literal('is >') and not self.text.startswith('=', self.pos):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is >'")
            return ('IsGreaterThanRule', v)
        self.pos = save
        return None

    def try_is_less_than_rule(self):
        save = self.pos
        if self.literal('is <') and not self.text.startswith('=', self.pos):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is <'")
            return ('IsLessThanRule', v)
        self.pos = save
        return None

    def try_is_gte_rule(self):
        save = self.pos
        if self.literal('is >='):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is >='")
            return ('IsGreaterThanOrEqualToRule', v)
        self.pos = save
        return None

    def try_is_lte_rule(self):
        save = self.pos
        if self.literal('is <='):
            v = self.p_number()
            if v is None:
                self.error("Expected a number after 'is <='")
            return ('IsLessThanOrEqualToRule', v)
        self.pos = save
        return None

    def try_has_length_rule(self):
        save = self.pos
        if self.literal('has length'):
            v = self.p_int()
            if v is None:
                self.error("Expected an integer after 'has length'")
            return ('HasLengthRule', v)
        self.pos = save
        return None

    def try_has_min_length_rule(self):
        save = self.pos
        if self.literal('has min length'):
            v = self.p_int()
            if v is None:
                self.error("Expected an integer after 'has min length'")
            return ('HasMinLengthRule', v)
        self.pos = save
        return None

    def try_has_max_length_rule(self):
        save = self.pos
        if self.literal('has max length'):
            v = self.p_int()
            if v is None:
                self.error("Expected an integer after 'has max length'")
            return ('HasMaxLengthRule', v)
        self.pos = save
        return None

    def try_starts_with_rule(self):
        save = self.pos
        if self.literal('starts with'):
            v = self.p_string_or_int()
            if v is None:
                self.error("Expected a quoted string or integer after 'starts with'")
            return ('StartsWithRule', v)
        self.pos = save
        return None

    def try_ends_with_rule(self):
        save = self.pos
        if self.literal('ends with'):
            v = self.p_string_or_int()
            if v is None:
                self.error("Expected a quoted string or integer after 'ends with'")
            return ('EndsWithRule', v)
        self.pos = save
        return None

    def try_includes_rule(self):
        save = self.pos
        if self.literal('includes'):
            v = self.p_string_or_int()
            if v is None:
                self.error("Expected a quoted string or integer after 'includes'")
            return ('IncludesRule', v)
        self.pos = save
        return None

    def try_does_not_include_rule(self):
        save = self.pos
        if self.literal('does not include'):
            v = self.p_string_or_int()
            if v is None:
                self.error("Expected a quoted string or integer after 'does not include'")
            return ('DoesNotIncludeRule', v)
        self.pos = save
        return None

    def try_has_significant_digits_rule(self):
        save = self.pos
        if self.literal('has'):
            v = self.p_int()
            if v is None:
                self.pos = save
                return None
            if self.literal('significant digits') or self.literal('significant digit'):
                return ('HasSignificantDigitsRule', v)
            self.pos = save
            return None
        self.pos = save
        return None

    def try_has_decimal_places_rule(self):
        save = self.pos
        if self.literal('has'):
            v = self.p_int()
            if v is None:
                self.pos = save
                return None
            if self.literal('decimal places') or self.literal('decimal place'):
                return ('HasDecimalPlacesRule', v)
            self.pos = save
            return None
        self.pos = save
        return None

    def try_has_pattern_rule(self):
        save = self.pos
        if self.literal('has pattern'):
            v = self.p_regex_literal()
            if v is None:
                self.error(
                    "Expected a regular expression between slashes after 'has pattern', "
                    "e.g. /^[A-Z]{2}\\d{4}$/"
                )
            return ('HasPatternRule', v)
        self.pos = save
        return None

    def try_column_value_rule(self):
        for fn in (
            self.try_has_value_type_rule,
            self.try_has_value_format_rule,
            self.try_has_value_type_in_rule,
            self.try_is_unique_rule,
            self.try_is_required_rule,
            self.try_is_null_rule,
            self.try_is_not_null_rule,
            self.try_value_in_rule,
            self.try_value_not_in_rule,
            self.try_has_value_rule,
            self.try_not_has_value_rule,
            self.try_is_equal_to_rule,
            self.try_is_not_equal_to_rule,
            self.try_is_greater_than_rule,
            self.try_is_less_than_rule,
            self.try_is_gte_rule,
            self.try_is_lte_rule,
            self.try_has_length_rule,
            self.try_has_min_length_rule,
            self.try_has_max_length_rule,
            self.try_starts_with_rule,
            self.try_ends_with_rule,
            self.try_includes_rule,
            self.try_does_not_include_rule,
            self.try_has_significant_digits_rule,
            self.try_has_decimal_places_rule,
            self.try_has_pattern_rule,
        ):
            r = fn()
            if r is not None:
                return r
        return None

    def try_set_local_tolerance_rule(self):
        save = self.pos
        if self.literal('set tolerance at'):
            v = self.p_value()
            if v is None:
                self.error("Expected a number after 'set tolerance at'")
            return ('SetLocalToleranceRule', v)
        self.pos = save
        return None

    def _error_no_value_rules(self, ctx_label):
        """Called when a column:/ruleblock: block matched zero value rules.
        If there's leftover, unrecognized text before the next known
        delimiter, point at that text specifically (much more useful than
        a generic 'no value rules' message, e.g. for a typo'd keyword)."""
        save = self.pos
        self.skip_ws()
        if self.pos < self.n:
            nxt = self.text[self.pos:]
            looks_like_new_block = (
                nxt.startswith('column:') or nxt.startswith('ruleblock:')
            )
            if not looks_like_new_block:
                snippet = nxt.split('\n')[0].strip()
                if snippet:
                    self.error(
                        f"Could not parse '{snippet}' as a valid value rule "
                        f"(check for typos in the keyword or value)"
                    )
        self.pos = save
        self.error(
            f"{ctx_label} has no value rules -- every block needs at least "
            f"one rule (e.g. 'has value type ...', 'is required', ...)"
        )

    # -- InColumnValueRule / BlockInColumnValueRule ----------------------

    def parse_in_column_value_rule(self):
        save = self.pos
        if not self.literal('column:'):
            self.pos = save
            return None
        name_pos = self.pos
        name = self.p_column_name()
        if name is None:
            self.error("Expected a quoted column name after 'column:'", name_pos)
        local_rules = []
        while True:
            save2 = self.pos
            r = self.try_set_local_tolerance_rule()
            if r is None:
                self.pos = save2
                break
            local_rules.append(r)
        value_rules = []
        while True:
            save3 = self.pos
            r = self.try_column_value_rule()
            if r is None:
                self.pos = save3
                break
            value_rules.append(r)
        if not value_rules:
            self._error_no_value_rules(f"Column block for {name}")
        return {'type': 'InColumnValueRule', 'column': name,
                'local_rules': local_rules, 'value_rules': value_rules,
                'line': self._line_col(save)[0]}

    def parse_block_rule(self):
        save = self.pos
        if not self.literal('ruleblock:'):
            self.pos = save
            return None
        names = self.p_list(self.p_column_name, "ruleblock column names")
        local_rules = []
        while True:
            save2 = self.pos
            r = self.try_set_local_tolerance_rule()
            if r is None:
                self.pos = save2
                break
            local_rules.append(r)
        value_rules = []
        while True:
            save3 = self.pos
            r = self.try_column_value_rule()
            if r is None:
                self.pos = save3
                break
            value_rules.append(r)
        if not value_rules:
            self._error_no_value_rules("Rule block")
        return {'type': 'BlockInColumnValueRule', 'columns': names,
                'local_rules': local_rules, 'value_rules': value_rules,
                'line': self._line_col(save)[0]}

    # -- ConditionalRule ---------------------------------------------------

    def parse_conditional_rule(self):
        save = self.pos
        tag_pos = self.pos
        tag = self.p_string()
        if tag is None:
            self.pos = save
            return None
        if not self.literal('if'):
            # Not actually a conditional rule tag (or 'if' is missing/misspelled).
            self.pos = save
            return None
        cond = self.parse_in_column_value_rule()
        if cond is None:
            self.error(
                f"Expected a 'column: ...' condition block after 'if' in "
                f"conditional rule {tag}"
            )
        if not self.literal('then'):
            self.error(
                f"Expected 'then' after the 'if' condition in conditional rule {tag}"
            )
        consequences = []
        while True:
            save2 = self.pos
            r = self.parse_in_column_value_rule()
            if r is None:
                self.pos = save2
                break
            consequences.append(r)
        if not consequences:
            self.error(
                f"Expected at least one 'column: ...' block after 'then' in "
                f"conditional rule {tag}"
            )
        return {'type': 'ConditionalRule', 'tag': tag, 'if': cond,
                'then': consequences, 'line': self._line_col(tag_pos)[0]}

    # -- top level ---------------------------------------------------------

    def parse(self):
        set_value_rules = []
        while True:
            save = self.pos
            r = self.try_set_value_rule()
            if r is None:
                self.pos = save
                break
            set_value_rules.append(r)

        column_rules = []
        while True:
            save = self.pos
            r = self.try_column_rule()
            if r is None:
                self.pos = save
                break
            column_rules.append(r)
        if not column_rules:
            self.error(
                "Expected at least one column rule -- every RuleSet file must "
                "contain a 'column names in [...]' rule"
            )

        block_rules = []
        while True:
            save = self.pos
            r = self.parse_block_rule()
            if r is None:
                self.pos = save
                break
            block_rules.append(r)

        column_value_rules = []
        while True:
            save = self.pos
            r = self.parse_in_column_value_rule()
            if r is None:
                self.pos = save
                break
            column_value_rules.append(r)

        conditional_rules = []
        while True:
            save = self.pos
            r = self.parse_conditional_rule()
            if r is None:
                self.pos = save
                break
            conditional_rules.append(r)

        self.skip_ws()
        if self.pos < self.n:
            snippet = self.text[self.pos:self.pos + 50].split('\n')[0].strip()
            self.error(
                f"Unexpected content -- could not parse this as any valid "
                f"RuleSet rule: '{snippet}'"
            )

        return {
            'set_value_rules': set_value_rules,
            'column_rules': column_rules,
            'block_rules': block_rules,
            'column_value_rules': column_value_rules,
            'conditional_rules': conditional_rules,
        }


# --------------------------------------------------------------------------
# Semantic checks (beyond pure grammar syntax, but cheap & high-value)
# --------------------------------------------------------------------------

def semantic_warnings(ast):
    warnings = []

    column_names = []
    has_column_list = False
    for kind, val in ast['column_rules']:
        if kind == 'ColumnListRule':
            has_column_list = True
            column_names = [v.strip('"\'') for v in val]

    if not has_column_list:
        warnings.append(
            "No 'column names in [...]' rule found. This is the one required "
            "rule in every RuleSet file."
        )

    referenced = set()
    for block in ast['block_rules']:
        for cname_raw in block['columns']:
            cname = cname_raw.strip('"\'')
            referenced.add(cname)
            if column_names and cname not in column_names:
                warnings.append(
                    f"Line {block['line']}: 'ruleblock:' refers to column "
                    f"{cname_raw} which is not listed in 'column names in [...]'"
                )
    for block in ast['column_value_rules']:
        cname = block['column'].strip('"\'')
        referenced.add(cname)
        if column_names and cname not in column_names:
            warnings.append(
                f"Line {block['line']}: 'column: {block['column']}' refers to a "
                f"column not listed in 'column names in [...]'"
            )
    for cond in ast['conditional_rules']:
        for block in [cond['if']] + cond['then']:
            cname = block['column'].strip('"\'')
            referenced.add(cname)
            if column_names and cname not in column_names:
                warnings.append(
                    f"Line {block['line']}: 'column: {block['column']}' (in "
                    f"conditional rule {cond['tag']}) refers to a column not "
                    f"listed in 'column names in [...]'"
                )

    for cname in column_names:
        if cname not in referenced:
            warnings.append(
                f"Column {cname!r} is listed but has no associated value rules "
                f"(no 'column:' block for it)."
            )

    return warnings


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def check_file(path, show_warnings=True):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw = f.read()
    except OSError as e:
        print(f"{path}: ERROR could not read file ({e})")
        return False

    text = strip_comments(raw)
    parser = Parser(text)
    try:
        ast = parser.parse()
    except RuleSetSyntaxError as e:
        print(f"{path}: INVALID")
        print(f"  Syntax error at line {e.line}, column {e.col}:")
        print(f"    {e.message}")
        if e.line_text:
            print(f"  >>> {e.line_text}")
        return False

    print(f"{path}: OK (syntactically valid RuleSet document)")
    if show_warnings:
        for w in semantic_warnings(ast):
            print(f"  Warning: {w}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Check RuleSet DSL files for syntax errors.")
    ap.add_argument('files', nargs='+', help="One or more RuleSet rule files to check")
    ap.add_argument('--no-warnings', action='store_true',
                     help="Suppress semantic warnings (e.g. unreferenced columns)")
    args = ap.parse_args()

    all_ok = True
    for path in args.files:
        ok = check_file(path, show_warnings=not args.no_warnings)
        all_ok = all_ok and ok

    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()