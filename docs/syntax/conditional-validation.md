# Conditional Validation

Apply a rule only when a condition (`if`) is met. The consequent (`then`) can include multiple atomic rules, each applied to a separate column. Multiple `if`/`then` rules can be specified in one rules file. Each conditional rule needs a rule tag (a quoted string identifying it).

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
column: 'state' in ['MD', 'NY', 'DE', 'VA']
```

The worked example in [Section 3](../rules-file.md) uses two conditional rules together (`WalesEnglandZipCodeRule` and `NotWalesEnglandZipCodeRule`) to apply different `Zip_Code` type rules depending on `Country`.

---
