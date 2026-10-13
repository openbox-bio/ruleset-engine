# Introduction and RuleSet Features

RuleSet is a data validation language that non-coding domain experts can use to develop, maintain, and communicate data validation rules. The accompanying data validation program, `ruleset-engine`, validates a data table against rules written in RuleSet.

### Key Features

- **Atomic Rules** — Each rule in RuleSet targets a single feature of your dataset. For instance, applying an "is not null" rule to a column will solely check for the presence of null values, without performing any type or format validations.

- **Rule Stacking** — You can specify multiple atomic rules for a data column. Rules are evaluated independently, and their order does not affect the outcome. A data column must pass all applicable rules to be considered valid. Successful validations are recorded with an "all OK" message in the log file.

- **Rule Blocks** — If a group of columns share the same rules, RuleSet allows you to define those rules once and apply them to the entire group. Rules that are specific to individual columns can still be defined separately.

- **Conditional Validation** — RuleSet supports conditional validations, which let you apply validation rules only when a condition is met. For example: `if column A contains "John Doe," then column B must contain "1970-12-22."` You may specify multiple consequent rules, e.g. `if column country is "USA" then column State must be in ["CO", "NY", "FL"]; column Zip Code must be an integer and have 5 digits.`

- **No implicit evaluation** — Data is never evaluated implicitly. All validation rules must be explicitly defined to be applied.

- **No data modification** — Data is never modified during the validation process.

With these features, RuleSet lets you specify data validation rules at different levels of stringency — from a quick type check on every column, to fully conditional, cross-column business rules. The [Rules File](rules-file.md) and [Data File](data-file.md) pages walk through a complete worked example.

---
