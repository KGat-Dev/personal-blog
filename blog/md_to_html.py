#!/usr/bin/env python3
"""
Convert markdown files with YAML frontmatter to HTML blog posts.
Usage: python md_to_html.py <markdown_file.md>
"""

import sys
import re
import html
from datetime import datetime
from pathlib import Path

# Try to import markdown and frontmatter, provide helpful error if missing
try:
    import markdown
    import frontmatter
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install them with: pip install markdown python-frontmatter")
    sys.exit(1)


# CSS styles (extracted from article template)
CSS_STYLES = """        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #F5F5F5;
            color: #000000;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Navigation */
        nav {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: rgba(245, 245, 245, 0.95);
            backdrop-filter: blur(10px);
            padding: 1.5rem 2rem;
            z-index: 1000;
            border-bottom: 1px solid #e0e0e0;
        }

        nav ul {
            list-style: none;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }

        nav li:first-child {
            margin-right: auto;
        }

        nav li:nth-child(2) {
            margin-left: auto;
        }

        nav a {
            color: #666666;
            text-decoration: none;
            font-size: 0.95rem;
            transition: color 0.3s ease;
            position: relative;
        }

        nav li:first-child a {
            font-size: 1.2rem;
            font-weight: 700;
        }

        nav a:hover {
            color: #000000;
        }

        nav a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background-color: #000000;
            transition: width 0.3s ease;
        }

        nav a:hover::after {
            width: 100%;
        }

        /* Main Content */
        main {
            margin-top: 80px;
            padding: 3rem 2rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .article-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 3rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .article-header {
            margin-bottom: 2.5rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #e0e0e0;
        }

        .article-header h1 {
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
            color: #000000;
            line-height: 1.2;
        }

        .article-meta {
            font-size: 0.95rem;
            color: #666666;
        }

        .article-content {
            color: #333333;
            font-size: 1.1rem;
            line-height: 1.8;
        }

        .article-content p {
            margin-bottom: 1.5rem;
        }

        .article-content h2 {
            font-size: clamp(1.75rem, 3vw, 2.25rem);
            font-weight: 700;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: #000000;
        }

        .article-content h3 {
            font-size: clamp(1.5rem, 2.5vw, 1.875rem);
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #000000;
        }

        .article-content strong {
            font-weight: 600;
            color: #000000;
        }

        .article-content em {
            font-style: italic;
        }

        .article-content a {
            color: #000000;
            text-decoration: underline;
            text-decoration-color: #999999;
            text-underline-offset: 3px;
            transition: text-decoration-color 0.3s ease;
        }

        .article-content a:hover {
            text-decoration-color: #000000;
        }

        .article-content ul,
        .article-content ol {
            margin-left: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .article-content li {
            margin-bottom: 0.5rem;
        }

        .back-to-blog {
            display: inline-block;
            margin-top: 3rem;
            color: #666666;
            text-decoration: none;
            font-size: 0.95rem;
            transition: color 0.3s ease;
            position: relative;
            padding-left: 1.5rem;
        }

        .back-to-blog::before {
            content: '←';
            position: absolute;
            left: 0;
            transition: transform 0.3s ease;
        }

        .back-to-blog:hover {
            color: #000000;
        }

        .back-to-blog:hover::before {
            transform: translateX(-4px);
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 2rem;
            color: #666666;
            font-size: 0.9rem;
            border-top: 1px solid #e0e0e0;
            margin-top: 4rem;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            nav {
                padding: 1rem;
            }

            nav ul {
                gap: 1rem;
                font-size: 0.9rem;
            }

            main {
                padding: 2rem 1.5rem;
            }

            .article-container {
                padding: 2rem 1.5rem;
            }

            .article-header {
                margin-bottom: 2rem;
                padding-bottom: 1.5rem;
            }
        }

        @media (max-width: 480px) {
            nav {
                padding: 0.75rem 1rem;
            }

            nav ul {
                gap: 0.5rem;
                font-size: 0.8rem;
            }

            nav a {
                padding: 0.25rem 0.5rem;
            }

            main {
                padding: 1.5rem 1.25rem;
                margin-top: 60px;
            }

            .article-container {
                padding: 1.5rem 1.25rem;
            }
        }

        /* Smooth fade-in animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .article-container {
            animation: fadeIn 0.6s ease-out;
        }"""


NAVIGATION = """            <li><a href="../../index.html"><strong>Ken</strong></a></li>
                   <li><a href="../../blog.html">Blog</a></li>
                   <li><a href="../../now.html">Now</a></li>
                   <li><a href="../../quotes.html">Quotes</a></li>
                   <li><a href="../../book-registry.html">Book Registry</a></li>"""


def format_date(date_input):
    """
    Format date from various formats to a readable format.
    Accepts: datetime object, date string (YYYY-MM-DD), or formatted string.
    """
    if isinstance(date_input, datetime):
        return date_input.strftime("%B %d, %Y")
    
    if isinstance(date_input, str):
        # Try parsing ISO format (YYYY-MM-DD)
        try:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            # If it's already formatted, return as-is
            return date_input
    
    return str(date_input)


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_html_template(title, date, content_html):
    """
    Generate HTML template for a blog post.
    
    Args:
        title: Article title (will be HTML escaped)
        date: Formatted date string
        content_html: Converted markdown content as HTML
    """
    # Escape HTML in title for safe insertion
    title_escaped = html.escape(title)
    date_escaped = html.escape(date) if date else ''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_escaped} - Ken Gatera</title>
    <style>
{CSS_STYLES}
    </style>
</head>
<body>
    <nav>
        <ul>
{NAVIGATION}
        </ul>
    </nav>

    <main>
        <article class="article-container">
            <header class="article-header">
                <h1>{title_escaped}</h1>
                <div class="article-meta">{date_escaped}</div>
            </header>

            <div class="article-content">
{content_html}
            </div>

            <a href="../../blog.html" class="back-to-blog">Back to Blog</a>
        </article>
    </main>

    <footer>
        <p>&copy; 2025 Ken Gatera. All rights reserved.</p>
    </footer>
</body>
</html>
"""


def convert_markdown_to_html(md_file_path, output_dir=None):
    """
    Convert a markdown file with frontmatter to an HTML blog post.
    
    Args:
        md_file_path: Path to the markdown file (defaults to drafts/ if relative path)
        output_dir: Directory to save HTML file (default: posts/)
    
    Returns:
        Path to the generated HTML file, or None if error
    """
    md_path = Path(md_file_path)
    
    # If path doesn't exist and is relative, try drafts/ folder
    if not md_path.exists() and not md_path.is_absolute():
        drafts_path = Path('drafts') / md_path
        if drafts_path.exists():
            md_path = drafts_path
    
    if not md_path.exists():
        print(f"Error: File '{md_file_path}' not found.")
        return None
    
    try:
        # Read and parse the markdown file with frontmatter
        with open(md_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
    except Exception as e:
        print(f"Error reading file '{md_file_path}': {e}")
        return None
    
    # Extract metadata (using .metadata attribute as frontmatter returns an object)
    title = post.metadata.get('title', 'Untitled')
    date = post.metadata.get('date', '')
    
    # Format the date
    formatted_date = format_date(date) if date else ''
    
    # Convert markdown content to HTML
    md = markdown.Markdown(extensions=['extra', 'nl2br'])
    html_content = md.convert(post.content)
    
    # Generate output filename - default to posts/ folder
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path('posts')
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from title
    html_filename = f"article-{slugify(title)}.html"
    html_file_path = output_path / html_filename
    
    # Generate HTML using template function
    html_output = generate_html_template(title, formatted_date, html_content)
    
    # Write HTML file
    try:
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"✓ Converted '{md_path.name}' to 'posts/{html_filename}'")
        return html_file_path
    except Exception as e:
        print(f"Error writing file '{html_file_path}': {e}")
        return None


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <markdown_file.md> [output_dir]")
        print("\nExample:")
        print("  python md_to_html.py drafts/first-blog-post.md")
        print("  python md_to_html.py first-blog-post.md  (will look in drafts/)")
        print("  python md_to_html.py drafts/my-post.md output/  (custom output)")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_markdown_to_html(md_file, output_dir)


if __name__ == '__main__':
    main()

