# Global Settings

Global dataset settings that apply across the whole rules file (not to any one column).

#### `allowed null values in [ … ]`
**Description:** Treat the listed literals as null/missing values.
**Syntax:**
```
allowed null values in <list of literals to be treated as null>
```
**Example:**
```
allowed null values in ["Not Measured", "Not Collected", "Not Included", "-"]
```

#### `thousands separator is "…"`
**Description:** Specify the character used to separate thousands in numeric fields.
**Syntax:**
```
thousands separator is <seperator>
```
**Example:**
```
thousands separator is "."
```

#### `set tolerance at <NUMBER>`
**Description:** Specify the tolerance level used for numeric comparisons. The default is `0.001` — two values are considered equal if they differ by no more than that. Setting tolerance at this level applies it globally to all numeric comparisons in the rules file. You can also specify tolerance for an individual comparison (see [Section 5.3](value-rules.md)); when both a global and a local tolerance are defined, the **local tolerance takes precedence**.
**Syntax:**
```
set tolerance at <tolerance level>
```
**Example:**
```
set tolerance at 0.00001
set tolerance at 1E-6
```

**Understanding tolerance:** In many real-world datasets, numeric values that should be equal differ slightly because of rounding, measurement error, or floating-point representation. RuleSet uses tolerance to determine whether two numbers are *close enough* to be treated as equal — two values are equal when the absolute difference between them is less than or equal to the specified tolerance:

```
               reference value
                     │
                     ▼
───────────────┬─────●─────┬───────────────
               │           │
     reference - t     reference + t

          <------ tolerance ------>

              ▲
         test value

If the test value lies anywhere inside the interval,
the comparison succeeds.

abs(test - reference) <= tolerance
```

#### `ignore warnings`
**Description:** Suppress the warnings that value rules write to the log for null values and for non-numeric values in numeric comparisons. Errors are never suppressed.
**Syntax & Example:**
```
ignore warnings
```

**Warnings suppressed by this setting**

| Warning message | Reported by |
|---|---|
| `value … is null.` | `has value type`, `has format`, `is ==`, `is !=`, `is >`, `is >=`, `is <`, `is <=` |
| `value … is not numeric.` | `is ==`, `is !=`, `is >`, `is >=`, `is <`, `is <=` |

**What does not change**

- Errors are still reported. A numeric value that fails a comparison, or a non-null value of the wrong type, is logged as an error with or without this setting.
- `is required`, `is not null` and `is null` report violations as errors, so this setting does not hide them.
- Values listed in `allowed null values in [ … ]` count as null, so they are no longer warned about either.
- Rules that never produce null or non-numeric warnings (for example `is in`, `starts with`, `has pattern`) behave the same with or without the setting.

---
