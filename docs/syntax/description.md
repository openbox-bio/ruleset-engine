#### `description: "…"`
**Description:** Attach a plain-language explanation to a `column:` block or a `ruleblock:`. Use it to record why the rules exist, such as the business reason or the source of a limit, so that anyone reading the rules file can follow the intent. The description is optional, and it does not change how data are validated.

**Syntax:**
```
column: <ColumnName>
description: "<text>"
<ValueRule1>
<ValueRule2>
...

ruleblock: [<ColumnName_1>, <ColumnName_2>...<ColumnName_n>]
description: "<text>"
<ValueRule1>
...
```

**Example:**
```
column: "Transaction_ID"
description: "Unique identifier assigned by the payment system."
has value type string
is unique

ruleblock: [ "First_Name", "Last_Name", "City" ]
description: "Name and location fields entered by hand.
Must be present and contain at least three characters."
has value type string
has min length 3
is required
```

**Usage notes**

- Place `description:` immediately after the column name (or the `ruleblock:` column list), before any `set tolerance at` line or value rule.
- A column block still needs at least one value rule. A description on its own is not enough.
- The text can be wrapped in single or double quotes and can span several lines. Line breaks inside the quotes are kept as part of the text.
- Use double quotes if the text contains an apostrophe, for example `"Don't leave blank"`. An apostrophe inside a single-quoted string ends the string early and causes a syntax error.
- Make sure every opening quote has a closing quote. A missing closing quote makes the string run on to the next quote in the file, and the syntax error is then reported far from the real mistake.
- In this version of RuleSet a `description:` cannot be added to conditional rules. This will be included in a future version.
- A typed `\n` is not turned into a line break. Use an actual new line instead.
- Unlike a `//` comment, which the parser ignores, a description is part of the rule itself.