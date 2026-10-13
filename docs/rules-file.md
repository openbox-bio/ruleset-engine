# Rules File

A **rules file** is a plain-text file containing one or more RuleSet rules. It has no required file extension — `.ruleset`, `.dsl`, or no extension at all are all valid, since `ruleset-engine` only cares about the file's contents, not its name.

### Correct format

- Lines starting with `//` are comments and are ignored; comments may appear anywhere in the file.
- Every rules file must contain exactly one `column names in [ … ]` rule — this is the **only required rule** in RuleSet (see [Section 5.2](syntax/column-rules.md)).
- Beyond that, rules are composed from the building blocks in [Section 5](syntax/index.md): **global settings, column rules, value rules, rule blocks, and conditional rules — combined in that order.**
- Rule order does not affect the validation outcome (see Rule Stacking, [Section 1](index.md)).

### Example

Here's a complete, valid rules file. It validates a table of squash players: every column has a declared type, `PSA_ID` must be unique and start with `'PSA'`, `Country` must be one of nine listed values, and a conditional rule handles the fact that UK postal codes (Wales, England) are alphanumeric while other countries' zip codes are numeric.

```
//Rules to validate top_15_squash_players.csv
//Column ID should be unique; each value should start with 'PSA'; PSA0000 is not a valid value.
//Column Country can have only one of the following values:
//'EGY', 'PER', 'NZL', 'IND', 'MAS', 'WAL', 'ENG', 'FRA', 'SUI'.
//Column Year_of_Birth should have the format 'YYYY'.
//Column Zip_Code is not null.
//Conditional rules:
//Zip_Code for Wales and England should be of type string.
//Zip_Code for all other countries should be of type integer.
//-------------------------------------

column names in ['Rank', 'PSA_ID', 'First_Name', 'Last_Name', 'Country', 'Year_of_Birth', 'Address', 'Zip_Code']
all columns required
no extra columns allowed

column: 'Rank'
description: "World ranking of the player. Must be a positive whole number."
has value type integer
is > 0

column: 'PSA_ID'
description: "Unique player identifier. Must start with PSA; PSA0000 is not a valid value."
has value type string
is unique
starts with 'PSA'
is not 'PSA0000'

column: 'First_Name'
description: "First name of the player."
has value type string

column: 'Last_Name'
description: "Last name of the player."
has value type string

column: 'Country'
description: "Three-letter country code of the player. Must be one of the nine codes listed."
has value type string
is in ['EGY', 'PER', 'NZL', 'IND', 'MAS', 'WAL', 'ENG', 'FRA', 'SUI']

column: 'Year_of_Birth'
description: "Four-digit year of birth, in YYYY format."
has value type date-time
has format YYYY

column: 'Address'
description: "Street address and city of the player."
has value type string

column: 'Zip_Code'
description: "Postal code of the player's address. Must not be empty. Its type depends on Country; see the conditional rules below."
is not null

"WalesEnglandZipCodeRule"
if
column: 'Country' is in ['WAL', 'ENG']
then
column: 'Zip_Code' has value type string

"NotWalesEnglandZipCodeRule"
if
column: 'Country' is not in ['WAL', 'ENG']
then
column: 'Zip_Code' has value type integer
```

This same example is referenced throughout [Section 5](syntax/index.md) when individual syntax features are explained.

---
