# Rule Blocks

If a group of columns share the same rules, RuleSet lets you define those rules once and apply them to the entire group, rather than repeating the same value rules under separate `column:` blocks. Multiple rule blocks may be specified in one rules file, and columns can still have additional rules defined individually elsewhere.

**Syntax:**
```
ruleblock: [<ColumnName_1>, <ColumnName_2>...<ColumnName_n>]
<ValueRule1>
<ValueRule2>
...
```
**Example:**
```
ruleblock: [ "First_Name", "Last_Name", "City" ]
has value type string
has min length 3
is required
```

---
