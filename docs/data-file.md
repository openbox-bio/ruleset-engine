# Data File

The **data file** is the actual table being validated against your rules file.

### Accepted formats

`ruleset-engine` accepts `.csv`, `.tsv`, and `.xls`/`.xlsx` format data files. Data files are expected to be tabular with column headers included in the first row.

### Example data file

The table below (`top_15_squash_players.csv`) is what the rules file in [Section 3](rules-file.md) validates against:

| Rank | PSA_ID  | First_Name | Last_Name   | Country | Year_of_Birth | Address                         | Zip_Code |
|------|---------|------------|-------------|---------|----------------|----------------------------------|----------|
| 1    | PSA9057 | Mostafa    | Asal        | EGY     | 2001           | 18 High St, Alexandria           | 11574    |
| 2    | PSA9086 | Ali        | Farag       | EGY     | 1993           | 411 High St, Giza                | 11772    |
| 3    | PSA6447 | Diego      | Elias       | PER     | 2004           | 235 Oak Dr, Cusco                | 15441    |
| 4    | PSA1932 | Paul       | Coll        | NZL     | 1992           | 99 Beach Rd, Auckland            | 1010     |
| 5    | PSA3884 | Marwan     | ElShorbagy  | EGY     | 1993           | 55 Nile Ave, Cairo               | 11311    |
| 6    | PSA7765 | Tarek      | Momen       | EGY     | 1988           | 12 Lotus St, Maadi               | 11431    |
| 7    | PSA8820 | Victor     | Crouin      | FRA     | 1999           | 45 Rue de Lyon, Paris            | 75012    |
| 8    | PSA1399 | Joel       | Makin       | WAL     | 1994           | 73 Cardiff Rd, Newport           | NP10 8XG |
| 9    | PSA6233 | Mazen      | Hesham      | EGY     | 1994           | 31 Zamalek St, Cairo             | 11211    |
| 10   | PSA5431 | Youssef    | Ibrahim     | EGY     | 1999           | 23 Freedom Rd, Alexandria        | 11432    |
| 11   | PSA4738 | Nicolas    | Mueller     | SUI     | 1989           | 90 Lake View, Zurich             | 8004     |
| 12   | PSA3186 | Saurav     | Ghosal      | IND     | 1986           | 77 Residency Rd, Kolkata         | 700025   |
| 13   | PSA2567 | Mohamed    | ElShorbagy  | ENG     | 1991           | 19 Queen's Walk, Bristol         | BS8 1SB  |
| 14   | PSA9012 | Baptiste   | Masotti     | FRA     | 1995           | 12 Place du Marché, Marseille    | 13001    |
| 15   | PSA8777 | Eain Yow   | Ng          | MAS     | 1998           | 38 Jalan Ampang, Kuala Lumpur    | 50450    |

Running `ruleset-engine` with this data file against the rules file in [Section 3](rules-file.md) produces a clean log, since every row satisfies every rule — see [Section 5.6](syntax/log-file.md) for that output in full.

### What happens if the format is incorrect

If `ruleset-engine` cannot read the data file at all — an unsupported file type, a corrupted file, or a path that doesn't resolve — it writes an error to the log file explaining what went wrong (e.g. `Error: could not read data file. <underlying error>`) and exits without attempting any validation. It does not partially validate a file it couldn't fully parse, and it never modifies or attempts to repair the data file itself.

This is distinct from a data file that parses successfully but *fails* individual rules (a wrong value type, a null in a required column, and so on) — those are reported per-column as validation errors in the log, not as a file-format error. See [Section 5.6](syntax/log-file.md) for how each case is logged.

---
