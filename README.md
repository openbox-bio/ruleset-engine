# ruleset-engine

**A data validation language non-coders can read, write, and maintain.**

[![PyPI version](https://img.shields.io/pypi/v/ruleset-engine.svg)](https://pypi.org/project/ruleset-engine/)
[![CI](https://github.com/openbox-bio/ruleset-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/openbox-bio/ruleset-engine/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/openbox-bio/ruleset-engine.svg)](LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/ruleset-engine.svg)](pyproject.toml)
<!--
  The PyPI badge above will 404 until the package is actually published --
  remove it until then, or it'll render as a broken badge on the repo page.
-->

RuleSet is a data validation language that domain experts can use to develop, maintain, and communicate data validation rules — without writing code. `ruleset-engine` is the command-line tool that validates a data table against rules written in RuleSet.

## Quick Start

### Install

```bash
pip install ruleset-engine
```

### Write a rules file

```dsl
// squash_rules.rules
column names in ['PSA_ID', 'First_Name', 'Last_Name', 'Country', 'Zip_Code']
all columns required
no extra columns allowed

column: 'PSA_ID'
has value type string
is unique
starts with 'PSA'

column: 'Country'
has value type string
is in ['EGY', 'FRA', 'ENG', 'WAL']

column: 'Zip_Code'
is not null
```

### Validate your data

```bash
ruleset-engine --rules-file squash_rules.rules --data-file players.csv
```

`ruleset-engine` checks `players.csv` against every rule in `squash_rules.rules` and writes a timestamped log file reporting what passed and what didn't — no Python required to read or write the rules themselves.

## Key Features

- **Atomic Rules** — each rule checks exactly one thing (presence, type, format, range, ...), so rules stay simple to read and debug in isolation.
- **Rule Stacking** — apply multiple rules to a column; all must pass, and order doesn't affect the outcome.
- **Rule Blocks** — define a set of rules once and apply them across a group of columns that share the same requirements.
- **Conditional Validation** — express rules like *"if column A is X, then column B must be Y,"* including multiple consequent rules per condition.
- **No implicit evaluation** — nothing is checked unless a rule explicitly says so.
- **No data modification** — validation never changes your data, ever.

See [`docs/RuleSet_DSL_Full.md`](docs/RuleSet_DSL_Full.md) for the complete language reference, including all supported value types, date/time formats, and a full worked example.

## Why RuleSet?

Most data validation tools — [Pandera](https://github.com/unionai-oss/pandera), [Great Expectations](https://github.com/great-expectations/great_expectations) — are built for programmers and data scientists. That's the right choice for engineering teams, but it puts validation out of reach for the domain experts who often understand the data best: the biologist who knows disease terminology, the analyst who knows which countries are even valid.

RuleSet is built the other way around: rules are short, declarative, English-like statements that a non-coder can write, read back, and trust — while `ruleset-engine` still gives engineering teams a real, scriptable CLI to run those same rules in a data engineering pipeline.


## Installation Options

| Method | Command | Requires Python? |
|---|---|---|
| pip | `pip install ruleset-engine` | Yes |
| pipx | `pipx install ruleset-engine` | Yes (isolated automatically) |

## Contributing

```bash
git clone https://github.com/openbox-bio/ruleset-engine.git
cd ruleset-engine
pip install -e ".[test]"
pytest
```

Contributions, bug reports, and feature requests are welcome — please open an issue before starting work on anything substantial.

## License

MIT — see [`LICENSE`](LICENSE) for details.
