#!/usr/bin/env python3
"""A tiny, dependency-free text workshop for the terminal."""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter


VERSION = "1.0.0"


class Style:
    """ANSI colors that gracefully turn off in redirected output."""

    def __init__(self, plain: bool = False) -> None:
        self.enabled = not plain and sys.stdout.isatty() and "NO_COLOR" not in os.environ

    def paint(self, value: str, code: str) -> str:
        if not self.enabled:
            return value
        return f"\033[{code}m{value}\033[0m"

    def title(self, value: str) -> str:
        return self.paint(value, "1;96")

    def accent(self, value: str) -> str:
        return self.paint(value, "1;95")

    def muted(self, value: str) -> str:
        return self.paint(value, "2;37")

    def good(self, value: str) -> str:
        return self.paint(value, "1;92")


def banner(style: Style) -> None:
    print(style.title("""
╭────────────────────────────────────────╮
│          QARAQALPAQ TEXT LAB           │
│       So'zler menen oynap ko'r!        │
╰────────────────────────────────────────╯"""))
    print(style.muted("A small, colorful workshop for your words.\n"))


def analyze(text: str, style: Style) -> None:
    nonspace_chars = [character for character in text if not character.isspace()]
    frequencies = Counter(character.casefold() for character in nonspace_chars)

    print(style.accent("\n✦ Text snapshot"))
    print(f"  Characters : {len(text)}")
    print(f"  Words      : {len(text.split())}")
    print(f"  Unique     : {len(set(nonspace_chars))} (spaces excluded)")

    if not frequencies:
        print(style.muted("  Add a few characters to see the frequency chart."))
        return

    print(style.accent("\n  Most-used characters (case-insensitive)"))
    max_count = frequencies.most_common(1)[0][1]
    for character, count in frequencies.most_common(8):
        bar = "█" * max(1, round(count / max_count * 16))
        print(f"  {character:<8} {style.good(bar)} {count}")


def transform(action: str, text: str) -> str:
    if action == "sort":
        return "".join(sorted(text, key=str.casefold))
    if action == "reverse":
        return text[::-1]
    if action == "capitalize":
        return text.capitalize()
    if action == "upper":
        return text.upper()
    if action == "clean":
        return " ".join(text.split())
    raise ValueError(f"Unknown action: {action}")


def show_menu(style: Style) -> None:
    options = (
        ("1", "Analyze my text"),
        ("2", "Sort characters"),
        ("3", "Reverse text"),
        ("4", "Sentence case"),
        ("5", "UPPERCASE"),
        ("6", "Tidy whitespace"),
        ("7", "Enter different text"),
        ("0", "Exit"),
    )
    print(style.accent("Choose a tool"))
    for number, label in options:
        print(f"  {style.good(number)}  {label}")


def interactive(initial_text: str | None, style: Style) -> None:
    banner(style)
    text = initial_text

    while text is None:
        try:
            answer = input("Matin kiritin (type /q to exit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nSee you next time!")
            return
        if answer.strip().lower() in {"/q", "/quit"}:
            print("See you next time!")
            return
        text = answer

    while True:
        print(style.muted(f"\nCurrent text: {text!r}"))
        show_menu(style)
        try:
            choice = input("\nChoice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSee you next time!")
            return

        if choice == "0":
            print("See you next time!")
            return
        if choice == "1":
            analyze(text, style)
        elif choice in {"2", "3", "4", "5", "6"}:
            action = {"2": "sort", "3": "reverse", "4": "capitalize", "5": "upper", "6": "clean"}[choice]
            text = transform(action, text)
            print(style.good(f"\n→ {text}"))
        elif choice == "7":
            try:
                text = input("Jańa matin kiritin: ")
            except (EOFError, KeyboardInterrupt):
                print("\nSee you next time!")
                return
        else:
            print(style.paint("Pick one of the listed numbers.", "1;91"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Explore, transform, and analyze a piece of text.",
        epilog='Example: python textlab.py "hello world" --action analyze',
    )
    parser.add_argument("text", nargs="?", help="text to work with; omit to enter it interactively")
    parser.add_argument(
        "--action",
        choices=("analyze", "sort", "reverse", "capitalize", "upper", "clean"),
        help="run a single tool and exit",
    )
    parser.add_argument("--plain", action="store_true", help="disable terminal colors")
    parser.add_argument("--version", action="version", version=f"Qaraqalpaq Text Lab {VERSION}")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    style = Style(plain=args.plain)

    if args.action:
        if args.text is None:
            print("Please provide text when using --action.", file=sys.stderr)
            raise SystemExit(2)
        if args.action == "analyze":
            analyze(args.text, style)
        else:
            print(transform(args.action, args.text))
        return

    interactive(args.text, style)


if __name__ == "__main__":
    main()
