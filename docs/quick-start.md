# Quick Start

### Install

```bash
pip install ruleset-engine
```

### Run

```bash
ruleset-engine --rules-file RULES_FILE --data-file DATA_FILE [--logfile-path LOGFILE_PATH]
```

**Required Arguments:**
- `--rules-file RULES_FILE` — Path to the file containing the data validation rules (see [Rules File](rules-file.md)).
- `--data-file DATA_FILE` — Path to the data file to be validated (see [Data File](data-file.md)).

**Optional Arguments:**
- `--logfile-path LOGFILE_PATH` — Directory path where the log file will be stored. If not specified, the current working directory is used.
- `-h`, `--help` — Display the help message and exit.

**Notes:**
- Ensure the `ruleset-engine` command is on your system's `PATH` (a standard `pip install` handles this automatically).
- Logfile names include a timestamp: `YYYY_MM_DD_HH_MM_SS_ruleset.log`.
- See [Log File](syntax/log-file.md) for a full explanation of log output, with examples.

### A minimal end-to-end example

```bash
ruleset-engine --rules-file squash_rules.ruleset --data-file top_15_squash_players.csv
```

The [Rules File](rules-file.md) and [Data File](data-file.md) pages build out exactly this `squash_rules.ruleset` / `top_15_squash_players.csv` pair in detail.

---
