# Value Rules

Apply one or more value-level constraints to a specific column.

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
```
["HH:mm:ss", "HH:mm", "hh:mm:ss AM/PM", "hh:mm AM/PM", "HHmmss", "YYYY-MM-DD HH:mm:ss",
"YYYY-MM-DDTHH:mm:ss", "YYYY-MM-DD HH:mm", "YYYY-MM-DDTHH:mm", "DD/MM/YYYY HH:mm:ss",
"MM-DD-YYYY hh:mm:ss AM/PM", "YYYY/MM/DD HH:mm:ss", "YYYY-MM-DDTHH:mm:ss.sssZ",
"YYYY-MM-DDTHH:mm:ss+hh:mm", "YYYY-MM-DD", "MM-DD-YYYY", "DD-MM-YYYY", "YYYY/MM/DD",
"MM/DD/YYYY", "DD/MM/YYYY", "YYYY.MM.DD", "MM.DD.YYYY", "DD.MM.YYYY", "YYYYMMDD", "YYYY"]
```
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

**Local tolerance:** `is ==`, `is !=`, and the bound comparisons above respect tolerance (see [Section 5.1](global-settings.md) for how tolerance works). You can set a tolerance local to one column's comparisons, which takes precedence over any global tolerance:
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
