# Blog Conversion Script

This directory includes a Python script to automatically convert markdown files to HTML blog posts.

## Folder Structure

- `drafts/` - Contains all markdown (`.md`) files for articles
- `posts/` - Contains all generated HTML article files
- `md_to_html.py` - Conversion script (in main folder)
- `article-template.html` - HTML template for articles (in main folder)

## Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install markdown python-frontmatter
```

## Usage

Convert a markdown file from `drafts/` to HTML in `posts/`:
```bash
python md_to_html.py drafts/<markdown_file.md>
```

Or use a shorter path (script will look in `drafts/` automatically):
```bash
python md_to_html.py <markdown_file.md>
```

Examples:
```bash
python md_to_html.py drafts/first-blog-post.md
python md_to_html.py first-blog-post.md  # Will look in drafts/
```

This will create an HTML file named `article-<slugified-title>.html` in the `posts/` folder.

## Markdown File Format

Your markdown files should have YAML frontmatter at the top:

```markdown
---
title: My Blog Post Title
date: 2025-01-04
---

Your markdown content goes here...

You can use **bold**, *italic*, [links](https://example.com), and more.
```

### Date Formats

The script accepts dates in these formats:
- ISO format: `2025-01-04` (will be formatted as "January 4, 2025")
- Already formatted: `April 17, 2021` (will be used as-is)

## Output

The script generates an HTML file that:
- Matches your site's styling
- Includes navigation
- Has proper meta tags
- Is mobile responsive
- Includes a "Back to Blog" link

## Notes

- The output filename is generated from the title (slugified)
- Existing HTML files will be overwritten
- Make sure to add the new article to `blog.html` manually (for now)

