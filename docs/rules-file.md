# Rules File

A **rules file** is a plain-text file containing one or more RuleSet rules. It has no required file extension — `.ruleset`, `.dsl`, or no extension at all are all valid, since `ruleset-engine` only cares about the file's contents, not its name.

### Correct format

- Lines starting with `//` are comments and are ignored; comments may appear anywhere in the file.
- Every rules file must contain exactly one `column names in [ … ]` rule — this is the **only required rule** in RuleSet (see [Column Rules](syntax/column-rules.md)).
- Beyond that, rules are composed from the building blocks in [RuleSet Syntax](syntax/index.md): **global settings, column rules, value rules, rule blocks, and conditional rules — combined in that order.**
- Rule order does not affect the validation outcome.

### Example

Here's a complete, valid rules file. It validates a table of squash players- `top15_squash_players_full.csv`.
<br>Every column has a declared type, `PSA_ID` must be unique and start with `'PSA'`, `Country` must be one of nine listed values, and a conditional rule handles the fact that UK postal codes (Wales, England) are alphanumeric while other countries' zip codes are numeric. Both the rules file and data file can be found in the [examples](https://github.com/openbox-bio/ruleset-engine/tree/main/examples) folder.

```
//Rules to validate top15_squash_players_full.csv and top15_squash_players_full_with_errors.csv.
// Column ID should be unique, each value should start with 'PSA'; PSA0000 is not a valid value.
// Column Country can have only one of the following values: 
//'EGY', 'PER', 'NZL', 'IND', 'MAS', 'WAL', 'ENG', 'FRA', 'SUI'.
//Column Year_of_Birth should have the format YYYY
//Conditional rules:
//Zip for Wales should start with 'NP'
//Zip for Egypt should be 5 characters long.
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

'Country-Zip1'
if
column: 'Country' is in ['WAL', 'ENG']
then
column: 'Zip_Code' has value type string

'Country-Zip2'
if
column: 'Country' is not in ['WAL', 'ENG']
then
column: 'Zip_Code' has value type integer
```
---
