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
  - Null values in columns and non-numeric values used in numeric comparisons.
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
#### Example: a run with errors
Let us introduce some errors into the `top15_squash_players_full.csv` file. We introduce the following errors:

- **Row 1, `PSA_ID`:** `9057` does not start with `PSA`. Also, `9057` will be parsed as an integer and not as a string.
- **Row 2, `Year_of_Birth`:** `10-02-2004` is not in the required `YYYY` format.
- **Row 3, `Country`:** the value is empty (null).
- **Row 4, `Rank`:** `A4` is not an integer.
- **Row 11, `Zip_Code`:** `SX0476` is not an integer. `Country` is `SUI`, so the conditional rule `Country-Zip2` requires an integer.

| Rank | PSA_ID  | First_Name | Last_Name  | Country | Year_of_Birth | Address                       | Zip_Code |
|------|---------|------------|------------|---------|---------------|-------------------------------|----------|
| 1    | 9057    | Mostafa    | Asal       | EGY     | 2001          | 18 High St, Alexandria        | 11574    |
| 2    | PSA9086 | Ali        | Farag      | EGY     | 10-02-2004    | 411 High St, Giza             | 11772    |
| 3    | PSA6447 | Diego      | Elias      |         | 2004          | 235 Oak Dr, Cusco             | 15441    |
| A4   | PSA1932 | Paul       | Coll       | NZL     | 1992          | 99 Beach Rd, Auckland         | 1010     |
| 5    | PSA3884 | Marwan     | ElShorbagy | EGY     | 1993          | 55 Nile Ave, Cairo            | 11311    |
| 6    | PSA7765 | Tarek      | Momen      | EGY     | 1988          | 12 Lotus St, Maadi            | 11431    |
| 7    | PSA8820 | Victor     | Crouin     | FRA     | 1999          | 45 Rue de Lyon, Paris         | 75012    |
| 8    | PSA1399 | Joel       | Makin      | WAL     | 1994          | 73 Cardiff Rd, Newport        | NP10 8XG |
| 9    | PSA6233 | Mazen      | Hesham     | EGY     | 1994          | 31 Zamalek St, Cairo          | 11211    |
| 10   | PSA5431 | Youssef    | Ibrahim    | EGY     | 1999          | 23 Freedom Rd, Alexandria     | 11432    |
| 11   | PSA4738 | Nicolas    | Mueller    | SUI     | 1989          | 90 Lake View, Zurich          | SX0476   |
| 12   | PSA3186 | Saurav     | Ghosal     | IND     | 1986          | 77 Residency Rd, Kolkata      | 700025   |
| 13   | PSA2567 | Mohamed    | ElShorbagy | ENG     | 1991          | 19 Queen's Walk, Bristol      | BS8 1SB  |
| 14   | PSA9012 | Baptiste   | Masotti    | FRA     | 1995          | 12 Place du Marché, Marseille | 13001    |
| 15   | PSA8777 | Eain Yow   | Ng         | MAS     | 1998          | 38 Jalan Ampang, Kuala Lumpur | 50450    |

This file is stored as `top_15_squash_players_full_with_errors.csv` in the [examples](https://github.com/openbox-bio/ruleset-engine/tree/main/examples) folder.

Here's the log produced by validating the table above against the same rules file:

```
Info: Rules File squash_rules.ruleset is OK.
Info: Data file top_15_squash_players_full_with_errors.csv parsed as csv.
Info: Rows:15
Info: Columns:8
Info: Missing Values:
Info: Missing value count for Rank: 0
Info: Missing value count for PSA_ID: 0
Info: Missing value count for First_Name: 0
Info: Missing value count for Last_Name: 0
Info: Missing value count for Country: 1
Info: Missing value count for Year_of_Birth: 0
Info: Missing value count for Address: 0
Info: Missing value count for Zip_Code: 0
Info: All columns in columns list have associated value rules.
Info: All columns with at least one value rule are included in the columns list.
Info: All columns present in data file.
Info: All required columns found in data file.
Info: No extra columns included in data file.
Error: column Rank, row 4: value A4 is not an integer.
Warning: column Rank, row 4: value A4 is not numeric.
Error: column PSA_ID, row 1: value 9057 is not a string.
Error: column PSA_ID, row 1: value 9057 does not start with PSA.
Info: Column: First_Name all OK.
Info: Column: Last_Name all OK.
Warning: column Country, row 3: value nan is null.
Error: column Year_of_Birth, row 2: value 10-02-2004 is not in the correct format.
Info: Column: Address all OK.
Info: Column: Zip_Code all OK.
Info: For conditional rule Country-Zip1: Country, Zip_Code is OK.
Error: Conditional rule Country-Zip2 fails for columns: Country, Zip_Code, row 11.
```