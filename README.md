# StoryTell

## Digital Journal

This repository now includes a small command line helper that lets you record a
single, freeform entry about your day and automatically separates the text into
feelings, situations, events, health updates, and the people you mention.

The script stores all entries in `data/journal_entries.json` so the information
remains structured and easy to review later.

### Usage

```
python digital_journal.py --entry "I met Alex for coffee and felt really happy."
```

If you omit `--entry`, the script will prompt you to type (or paste) the entry
interactively. You can also provide an ISO timestamp if you want to override
the automatically generated time:

```
python digital_journal.py --entry "Visited the doctor for a checkup." --timestamp 2024-05-22T09:30
```

After saving, the script prints the structured summary of what it detected.

### Reviewing past entries

To revisit what you've logged so far, use the `--history` flag. The script
prints the most recent entries first and echoes both the original text and the
detected categories:

```
python digital_journal.py --history
```

You can limit the output to the latest _N_ entries:

```
python digital_journal.py --history --limit 5
```
