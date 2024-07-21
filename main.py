import argparse
import fnmatch
import sys
import os


def read_patterns(file_path: str) -> list[str]:
    """
    Read patterns from the file.
    :param file_path: path to the file
    :return: list of patterns
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def match_any_pattern(name: str, patterns: list[str]) -> bool:
    """
    Check if the name matches any of the patterns.
    :param name: name to check
    :param patterns: patterns to match
    :return: true if the name matches any of the patterns, false otherwise
    """
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def print_tree(current_path: str,
               omit_patterns: list[str],
               prefix: str = "",
               output=sys.stdout) -> None:
    """
    Print directory tree structure, omitting specified directories.
    :param current_path: current directory path
    :param omit_patterns: omit patterns
    :param prefix: prefix to print
    :param output: output stream (stdout by default)
    :return: None
    """
    entries = sorted(os.listdir(current_path))
    entries = [e for e in entries if not match_any_pattern(e, omit_patterns)]

    entries_count = len(entries)

    for i, entry in enumerate(entries):
        entry_path = os.path.join(current_path, entry)
        if i == entries_count - 1:
            print(f"{prefix}+-- {entry}", file=output)
            new_prefix = f"{prefix}    "
        else:
            print(f"{prefix}|-- {entry}", file=output)
            new_prefix = f"{prefix}|   "

        if os.path.isdir(entry_path):
            print_tree(entry_path, omit_patterns, new_prefix, output)


def tree(dir_path: str, omit_file: str) -> None:
    """
    Print directory tree structure, omitting specified directories.
    :param dir_path: path to the root directory
    :param omit_file: file containing glob patterns to omit
    :return: None
    """
    omit_patterns = read_patterns(omit_file)
    print(dir_path)
    print_tree(dir_path, omit_patterns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print directory tree structure, omitting specified directories.")
    parser.add_argument("dir_path", type=str, help="The root directory to start the tree structure.")
    parser.add_argument("omit_file", type=str, help="Path to the file containing glob patterns to omit.")
    args = parser.parse_args()
    tree(args.dir_path, args.omit_file)
