#!/usr/bin/env python3
"""
README Link Checker

This script checks the online status of links in a README.md file. It extracts all URLs from the file using Markdown link syntax and sends a HEAD request to each URL.

Usage:
    1. Save this script as check_markdown_links.py.
    2. Ensure Python 3 is installed on your system.
    3. Install the required module using:
           pip install requests
    4. Run the script from the command line by providing the path to your README.md file:
           python check_markdown_links.py path/to/README.md
    5. The script will output the status of each link found in the README file.
    
Inspired by: Brandon Himpfen - himpfen.xyz
"""

import requests
import re
import argparse
from typing import List, Optional


def extract_urls(contents: str) -> List[str]:
    """
    Extracts all URLs from a markdown file using Markdown link syntax.
    """
    return re.findall(r"\[.*?\]\((http[s]?://.*?)\)", contents)


def check_link(url: str, session: requests.Session) -> Optional[int]:
    """
    Checks a single URL using a HEAD request.

    Returns:
        The HTTP status code if the request was successful, or None if an error occurred.
    """
    try:
        response = session.head(url, allow_redirects=True, timeout=5)
        return response.status_code
    except requests.RequestException:
        return None


def check_links(file_path: str) -> None:
    """
    Reads a Markdown file, extracts URLs, and checks their online status.
    Prints the status for each link. Broken links are highlighted in red.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()

    urls = extract_urls(contents)
    if not urls:
        print("No links found in the file.")
        return

    with requests.Session() as session:
        for url in urls:
            status = check_link(url, session)
            if status == 200:
                # Green text for online links
                print(f"\033[92mLink {url} is online.\033[0m")
            elif status is not None:
                # Red text for links that return an error code
                print(f"\033[91mLink {url} returned status code {status}.\033[0m")
            else:
                # Red text for links where an error occurred
                print(f"\033[91mError occurred while checking link {url}.\033[0m")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check the online status of links in a README.md file."
    )
    parser.add_argument("filepath", help="Path to the README.md file")
    args = parser.parse_args()

    check_links(args.filepath)


if __name__ == "__main__":
    main()
