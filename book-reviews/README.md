# Book Registry Automation

This folder contains the files needed to automatically update `book-registry.html` from a simple text file.

## Files

- `books.txt` - Text file containing all book reviews
- `update_book_registry.py` - Python script that converts books.txt to HTML
- `README.md` - This file

## Format

Each book entry in `books.txt` should follow this format on a single line:

```
rating - date read - book title - author name - description
```

**Example:**
```
★★★★☆ - 2024-12-15 - Stranger in a Strange Land - Robert A. Heinlein - Interesting and different POV on metaphysics, religion and bonding as human.
```

### Format Details

- **Rating**: Use star symbols (e.g., ★★★★☆ for 4 out of 5 stars)
- **Date read**: Format as YYYY-MM-DD (e.g., 2024-12-15)
- **Book title**: The title of the book
- **Author name**: The author's name
- **Description**: Your personal thoughts and description (can contain " - " if needed)

**Note:** Each field is separated by " - " (space-dash-space). If your description contains " - ", that's okay - the script will handle it correctly.

## Usage

1. Add your book entries to `books.txt`, one per line
2. Run the script from the main blog directory:

```bash
python book-reviews/update_book_registry.py
```

Or from the book-reviews folder:

```bash
cd book-reviews
python update_book_registry.py
```

3. The script will automatically update `book-registry.html` with:
   - **Section 1**: Summary list showing rating, date read, and title + author
   - **Section 2**: Details list showing title, author, and description
   - A separator line between the two sections

## Output

The generated `book-registry.html` will have two sections:

1. **Summary List**: Quick reference with rating, date, title, and author
   - Example: `★★★★☆ — December 15, 2024 — **Stranger in a Strange Land** by Robert A. Heinlein`

2. **Book Details**: Full information with title, author, and description
   - Example: `**Stranger in a Strange Land** by Robert A. Heinlein — Interesting and different POV on metaphysics, religion and bonding as human.`

## Tips

- Empty lines are ignored
- Lines starting with `#` are treated as comments and ignored
- Dates are automatically formatted from YYYY-MM-DD to "Month Day, Year" format
- All text is HTML-escaped for safety

