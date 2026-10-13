# The Log File

Every `ruleset-engine` run produces a log file (named `YYYY_MM_DD_HH_MM_SS_ruleset.log`) with three levels of output:

- **Info** — Informational messages indicating successful operations and summary details:
  - Confirmation of successful parsing of rules and data files.
  - Summary statistics of the data table, including row and column counts, and counts of missing values.
  - Notifications that all validation rules have passed without issues.
- **Warning** — Potential issues that don't halt execution but could affect validation accuracy:
  - Columns listed in the rules file without associated value rules.
  - Value rules defined for columns not included in the column list.
  - Absence of any value rules in the rules file.
  - Mismatch between column names in the rules file and the data file, preventing evaluation based on column order.
- **Error** — Critical issues that prevent validation from proceeding correctly:
  - Invalid or inaccessible file paths for the rules or data file.
  - Errors encountered while parsing the rules file.
  - Failures during column-level, value-level, or conditional-rule validation (see [Section 4](../data-file.md) for what happens when the data file itself can't be read).

#### Example: a clean run

Here's the log produced by validating the data table from [Section 4](../data-file.md) against the rules file from [Section 3](../rules-file.md) — every rule passes, so every column reports "all OK":

```
Info: Rules File ./squash_rules.ruleset is OK.
Info: All columns in columns list have associated value rules.
Info: All columns with at least one value rule are included in the columns list.
Info: Data file ./top_15_squash_players.csv parsed as csv.
Info: Rows:15
Info: Columns:8
Info: Missing Values:
Info: Missing value count for Rank: 0
Info: Missing value count for PSA_ID: 0
Info: Missing value count for First_Name: 0
Info: Missing value count for Last_Name: 0
Info: Missing value count for Country: 0
Info: Missing value count for Year_of_Birth: 0
Info: Missing value count for Address: 0
Info: Missing value count for Zip_Code: 0
Info: All columns present in data file.
Info: All required columns found in data file.
Info: No extra columns included in data file.
Info: Column: Rank all OK.
Info: Column: PSA_ID all OK.
Info: Column: First_Name all OK.
Info: Column: Last_Name all OK.
Info: Column: Country all OK.
Info: Column: Year_of_Birth all OK.
Info: Column: Address all OK.
Info: Column: Zip_Code all OK.
```
