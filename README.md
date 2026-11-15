# Qaraqalpaq Text Lab ✦

A colorful, dependency-free terminal playground for exploring and transforming text.

## Start it

```bash
python textlab.py
```

Enter a line of text and choose from the interactive tools:

- Analyze character and word counts, unique characters, and a tiny frequency chart
- Sort characters
- Reverse text
- Change to sentence case or uppercase
- Tidy repeated whitespace
- Switch to a new line of text

## Run one tool directly

```bash
python textlab.py "salem dunya" --action analyze
python textlab.py "salem dunya" --action reverse
python textlab.py "  salem   dunya  " --action clean
```

Available actions: `analyze`, `sort`, `reverse`, `capitalize`, `upper`, and `clean`.

Add `--plain` to disable color. The program uses only the Python standard library.
