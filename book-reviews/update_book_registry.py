#!/usr/bin/env python3
"""
Convert books.txt file to update book-registry.html.
Usage: python update_book_registry.py
"""

import sys
import html
import re
from pathlib import Path
from datetime import datetime

# Path to the books text file
BOOKS_FILE = Path(__file__).parent / 'books.txt'
REGISTRY_HTML = Path(__file__).parent.parent / 'book-registry.html'


def parse_book_line(line):
    """
    Parse a line from books.txt.
    Format: rating (stars) - date read - book title - author name - description
    
    Returns a dict with: rating, date, title, author, description
    """
    line = line.strip()
    if not line:
        return None
    
    # Split by " - " delimiter
    parts = [p.strip() for p in line.split(' - ')]
    
    if len(parts) < 5:
        print(f"Warning: Invalid format in line: {line}")
        print("Expected format: rating - date - title - author - description")
        return None
    
    rating = parts[0]
    date_read = parts[1]
    title = parts[2]
    author = parts[3]
    description = ' - '.join(parts[4:])  # Join in case description contains " - "
    
    return {
        'rating': rating,
        'date_read': date_read,
        'title': title,
        'author': author,
        'description': description
    }


def format_date(date_str):
    """
    Keep date in YYYY-MM-DD format (no formatting).
    """
    return date_str


def generate_book_html(books):
    """
    Generate HTML for two sections:
    1. Summary list: rating, date, title + author
    2. Details list: title, author, description
    """
    if not books:
        return '', ''
    
    # Section 1: Summary list (rating, date, title + author)
    summary_items = []
    for book in books:
        title_escaped = html.escape(book['title'])
        author_escaped = html.escape(book['author'])
        rating_escaped = html.escape(book['rating'])
        date_escaped = html.escape(format_date(book['date_read']))
        
        summary_items.append(
            f'                <li>{rating_escaped} — {date_escaped} — <strong>{title_escaped}</strong> by {author_escaped}</li>'
        )
    
    summary_html = '\n'.join(summary_items)
    
    # Section 2: Details list (title, author, description)
    detail_items = []
    for book in books:
        title_escaped = html.escape(book['title'])
        author_escaped = html.escape(book['author'])
        description_escaped = html.escape(book['description'])
        
        detail_items.append(
            f'                <li>\n                    <span class="book-title-author"><strong>{title_escaped}</strong> by {author_escaped}</span>\n                    <div class="book-description">{description_escaped}</div>\n                </li>'
        )
    
    detail_html = '\n'.join(detail_items)
    
    return summary_html, detail_html


def update_book_registry():
    """
    Read books.txt, parse it, and update book-registry.html
    """
    # Read books file
    if not BOOKS_FILE.exists():
        print(f"Error: Books file not found at '{BOOKS_FILE}'")
        return False
    
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading books file: {e}")
        return False
    
    # Parse all books
    books = []
    for line_num, line in enumerate(lines, 1):
        if line.strip() and not line.strip().startswith('#'):  # Skip empty lines and comments
            book = parse_book_line(line)
            if book:
                books.append(book)
    
    if not books:
        print("Warning: No books found in books.txt")
        return False
    
    print(f"Found {len(books)} book(s)")
    
    # Read the HTML template
    if not REGISTRY_HTML.exists():
        print(f"Error: book-registry.html not found at '{REGISTRY_HTML}'")
        return False
    
    try:
        with open(REGISTRY_HTML, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading book-registry.html: {e}")
        return False
    
    # Generate HTML for the two sections
    summary_html, detail_html = generate_book_html(books)
    
    # Find and replace the content between books-list and the closing main tag
    # Pattern matches from books-list div through books-details div (or just books-list if details don't exist yet)
    pattern = r'(<div class="books-list">.*?</ul>\s*</div>)(?:\s*<div class="books-separator">.*?</div>)?(?:\s*<div class="books-details">.*?</ul>\s*</div>)?(\s*</main>)'
    
    replacement = f'''<div class="books-list">
            <ul>
{summary_html}
            </ul>
        </div>

        <div class="books-separator"></div>

        <div class="books-details">
            <ul>
{detail_html}
            </ul>
        </div>\\2'''
    
    # Try to replace the content
    new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # If that didn't work, try matching just the books-list section
    if new_html == html_content:
        pattern_simple = r'(<div class="books-list">\s*<ul>)(.*?)(</ul>\s*</div>)(\s*</main>)'
        replacement_simple = f'''<div class="books-list">
            <ul>
{summary_html}
            </ul>
        </div>

        <div class="books-separator"></div>

        <div class="books-details">
            <ul>
{detail_html}
            </ul>
        </div>\\4'''
        
        new_html = re.sub(pattern_simple, replacement_simple, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    try:
        with open(REGISTRY_HTML, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"✓ Updated {REGISTRY_HTML.name} with {len(books)} book(s)")
        return True
    except Exception as e:
        print(f"Error writing book-registry.html: {e}")
        return False


def main():
    """Main entry point for the script."""
    if update_book_registry():
        print("✓ Book registry updated successfully!")
        return 0
    else:
        print("✗ Failed to update book registry")
        return 1


if __name__ == '__main__':
    sys.exit(main())

