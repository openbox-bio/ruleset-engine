# Conditional Validation
Apply a rule only when a condition (`if`) is met. The `if` condition is a single column with a single atomic rule. The consequent (`then`) can include multiple columns, but each column can have only one atomic rule. Multiple `if`/`then` rules can be specified in one rules file. Each conditional rule needs a rule tag (a quoted string identifying it).

**Syntax:**
```
<Rule Tag> if
column: <ColumnA> <ValueRuleA>
then
column: <ColumnB> <ValueRuleB>
column: <ColumnC> <ValueRuleC>
```
**Example:**
```
'USAStateZipRule' if
column: 'country' is "USA"
then
column: 'zipcode' has pattern /^\d{5}(-\d{4})?$/
column: 'state' is in ['MD', 'NY', 'DE', 'VA']
```

**One rule per column:** Each column in the consequent takes exactly one atomic rule. A column block with two or more rules is not valid in a conditional rule:
```
then
column: 'zipcode' is not null
has value type string
```
To require several rules on the same column, write a separate conditional rule for each one and repeat the `if` condition:
```
'ZipRequired' if
column: 'country' is "USA"
then
column: 'zipcode' is not null

'ZipIsString' if
column: 'country' is "USA"
then
column: 'zipcode' has value type string
```

The worked example in [Rules File](../rules-file.md) uses two conditional rules together (`Country-Zip1` and `Country-Zip2`) to apply different `Zip_Code` type rules depending on `Country`.

---
