# Column Rules

Specify which columns must be included, whether all named columns are required, and whether extra columns are allowed.

#### `column names in [ … ]`
**Description: (Required)** List exactly which columns the table must contain. **This is the only required rule in RuleSet** — every rules file must have a column names list.
**Syntax:**
```
column names in <list of column names>
```
**Example:**
```
column names in ['user_id', 'first_name', 'last_name', 'signup_date']
```

#### `all columns required`
**Description:** Fail if any of the named columns is missing.
**Syntax & Example:**
```
all columns required
```

#### `no extra columns allowed`
**Description:** Fail if the data table contains any column not listed in the rules file.
**Syntax & Example:**
```
no extra columns allowed
```

#### `check column order`
**Description:** Physical column order must match the order listed in the rules file.
**Syntax & Example:**
```
check column order
```

---
