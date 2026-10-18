# Value Rules

Value rules are the building blocks of a RuleSet data quality schema. Each rule checks exactly one property of a column's values, and you combine rules to describe what valid data looks like for that column. A few ideas shape how they work:

- **One rule, one check.** Rules are atomic. `is unique` checks only uniqueness and `has value type integer` checks only the type. A rule never checks anything you didn't ask for, so each rule is easy to read, and a failure points to one clear cause.
- **Stack rules to build up a schema.** A column can have as many rules as you need, and every rule must pass for the column to be valid. Rules are evaluated independently, so their order does not matter.
- **Develop the schema iteratively.** Start with the checks you are sure about, often just a value type for each column. Run `ruleset-engine`, review the [log file](log-file.md), and add rules as you learn more about the data. Columns that are listed in `column names in [ … ]` but have no value rules yet are flagged with a warning in the log, which gives you a running list of what is still unchecked.
- **Change stringency one line at a time.** To tighten a schema, add a rule. To loosen it, delete one. Because rules don't depend on each other, the rest of the schema is unaffected, and the same rules file can grow from a quick first-pass check into a strict specification.
- **Nothing is implicit.** Data is only checked by the rules you write, and it is never modified.

For example, a first pass at a `Rank` column might only confirm the type:
```
column: 'Rank'
has value type integer
```
Once you know the values should also be positive, add one line:
```
column: 'Rank'
has value type integer
is > 0
```

To apply the same rules to several columns, use [rule blocks](rule-blocks.md). To apply rules only when another column has a particular value, use [conditional validation](conditional-validation.md).

**Block Syntax:**
```
column: <ColumnName>
<ValueRule1>
<ValueRule2>
    …
```
**Example:**
```
column: 'age'
has value type integer
is >= 0
is <= 120
```

#### Data Type & Format

**`has value type <ValueType>`**
```
has value type string
```
Accepted value types:

| Value Type     | Description                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| string         | Text-based data (e.g., names, addresses, categories).                                                       |
| integer        | Whole numbers without decimal points (e.g., 1, 42, -10).                                                    |
| floating point | Decimal numbers (e.g., 3.14, -0.01, 2.718).                                                                 |
| boolean        | True/False values (e.g., true, false).                                                                      |
| date-time      | Date or timestamp values (e.g., 2023-12-25, 2025-03-27T14:00:00). See supported formats below.              |
| scientific     | Numbers expressed in scientific notation (e.g., 1.23e-4).                                                   |
| complex        | Complex numbers with real and imaginary parts (e.g., 3+4j).                                                 |

**`has format <FormatType>`**
```
has format YYYY-MM-DD
```
Applies only to the `date-time` type. Supported date-time formats:

[`HH:mm:ss`, `HH:mm`, `hh:mm:ss AM/PM`, `hh:mm AM/PM`, `HHmmss`, `YYYY-MM-DD HH:mm:ss`,
`YYYY-MM-DDTHH:mm:ss`, `YYYY-MM-DD HH:mm`, `YYYY-MM-DDTHH:mm`, `DD/MM/YYYY HH:mm:ss`,
`MM-DD-YYYY hh:mm:ss AM/PM`, `YYYY/MM/DD HH:mm:ss`, `YYYY-MM-DDTHH:mm:ss.sssZ`,
`YYYY-MM-DDTHH:mm:ss+hh:mm`, `YYYY-MM-DD`, `MM-DD-YYYY`, `DD-MM-YYYY`, `YYYY/MM/DD`,
`MM/DD/YYYY`, `DD/MM/YYYY`, `YYYY.MM.DD`, `MM.DD.YYYY`, `DD.MM.YYYY`, `YYYYMMDD`, `YYYY`]

*Other formats for geolocation and currency data will be added in future.*

#### Presence & Uniqueness

**`is required`**
```
is required
```
**`is unique`**
```
is unique
```
**`is null`** / **`is not null`**
```
is null
is not null
```

#### Pattern & Membership

**`has pattern /…/`**
```
has pattern /^[A-Z]{2}\d{4}$/
```
**`is in [ … ]`** / **`is not in [ … ]`**
```
is in ['Active', 'Pending', 'Closed']
is not in ['Cancelled', 'Deleted']
```

#### Exact Value Comparisons

**`is "<string>"`** / **`is not "<string>"`**
```
is "USA"
is not "N/A"
```
**`is == <NUMBER>`** / **`is != <NUMBER>`**
```
is == 100
is != 0
```

#### Numeric Bounds

**`is > <NUMBER>`** / **`is < <NUMBER>`**
```
is > 0
is < 100
```
**`is >= <NUMBER>`** / **`is <= <NUMBER>`**
```
is >= 0
is <= 120
```

**Local tolerance:** `is ==`, `is !=`, and the bound comparisons above respect tolerance (see [Global Settings](global-settings.md) for how tolerance works). You can set a tolerance local to one column's comparisons, which takes precedence over any specified global tolerance:
```
set tolerance at 0.0000001
set tolerance at 1E-06
```

#### Length Constraints

**`has length <INT>`**
```
has length 5
```
**`has min length <INT>`** / **`has max length <INT>`**
```
has min length 3
has max length 10
```

#### String Affixes & Substrings

**`starts with "<string>"`** / **`ends with "<string>"`**
```
starts with "ABC"
ends with ".csv"
```
**`includes "<string>"`** / **`does not include "<string>"`**
```
includes "urgent"
does not include "spam"
```

#### Precision Rules

**`has <INT> significant digits`**
```
has 3 significant digits
```
**`has <INT> decimal places`**
```
has 2 decimal places
```

---
