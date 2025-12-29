#!/usr/bin/env python3
"""
Build script to convert Markdown files to HTML articles.
Reads .md files from writing/src/ and generates HTML files in writing/
"""

import os
import re
from pathlib import Path
import markdown
import frontmatter

# Get project root (parent of scripts directory, or current dir if run from root)
SCRIPT_DIR = Path(__file__).parent.absolute()
if SCRIPT_DIR.name == "scripts":
    PROJECT_ROOT = SCRIPT_DIR.parent
else:
    PROJECT_ROOT = Path.cwd()

# Paths relative to project root
SRC_DIR = PROJECT_ROOT / "writing" / "src"
OUTPUT_DIR = PROJECT_ROOT / "writing"

# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Ayush Gupta</title>
    <link rel="icon" href="data:,">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }}
    }};
    </script>
</head>
<body>
    <header>
        <nav>
            <div class="nav-container">
                <a href="/" class="nav-brand">Ayush Gupta</a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/pages/writing.html">Writing</a>
                    <a href="/pages/projects.html">Projects</a>
                    <a href="/pages/timeline.html">Timeline</a>
                </div>
            </div>
        </nav>
    </header>

    <aside class="sidebar">
        <div class="sidebar-profile">
            <h1 class="profile-name">Ayush Gupta</h1>
            <p class="profile-title">Quantitative Researcher</p>
        </div>
        
        <div class="sidebar-section">
            <h2>Navigation</h2>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/pages/writing.html">Writing</a></li>
                <li><a href="/pages/projects.html">Projects</a></li>
                <li><a href="/pages/timeline.html">Timeline</a></li>
            </ul>
        </div>
        
        <div class="sidebar-section">
            <h2>Social</h2>
            <div class="social-links">
                <a href="https://github.com/7ayushgupta" target="_blank" rel="noopener" aria-label="GitHub">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                </a>
                <a href="https://linkedin.com/in/7ayushgupta" target="_blank" rel="noopener" aria-label="LinkedIn">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                </a>
                <a href="https://x.com/ayushGup7" target="_blank" rel="noopener" aria-label="Twitter">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                    </svg>
                </a>
            </div>
        </div>
    </aside>

    <main>
        <div class="container">
            <div class="main-content">
                <article class="article-content">
                    <div class="article-header">
                        <h1 class="article-title">{title}</h1>
                        <div class="article-meta">{date}</div>
                    </div>

                    <div class="article-content">
{content}
                    </div>
                </article>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 Ayush Gupta</p>
        </div>
    </footer>
</body>
</html>'''


def preserve_mathjax(text):
    """Preserve MathJax delimiters during markdown processing."""
    # Replace $$...$$ with placeholders before markdown conversion
    math_blocks = []
    placeholder_pattern = r'\$\$([^\$]+)\$\$'
    
    def replace_math(match):
        math_blocks.append(match.group(0))
        return f"MATHJAX_PLACEHOLDER_{len(math_blocks) - 1}"
    
    text = re.sub(placeholder_pattern, replace_math, text)
    return text, math_blocks


def restore_mathjax(html, math_blocks):
    """Restore MathJax delimiters after markdown conversion."""
    for i, math_block in enumerate(math_blocks):
        placeholder = f"MATHJAX_PLACEHOLDER_{i}"
        html = html.replace(placeholder, math_block)
    return html


def convert_markdown_to_html(content):
    """Convert markdown content to HTML, preserving MathJax."""
    # Preserve MathJax blocks
    content_with_placeholders, math_blocks = preserve_mathjax(content)
    
    # Configure markdown with extensions
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'tables',
        'nl2br'
    ])
    
    # Convert markdown to HTML
    html = md.convert(content_with_placeholders)
    
    # Restore MathJax blocks
    html = restore_mathjax(html, math_blocks)
    
    # Add target="_blank" rel="noopener" to external links
    # Match links that start with http:// or https://
    html = re.sub(
        r'<a href="(https?://[^"]+)">',
        r'<a href="\1" target="_blank" rel="noopener">',
        html
    )
    
    return html


def build_article(md_file):
    """Build a single article from a markdown file."""
    print(f"Processing: {md_file.name}")
    
    # Read and parse frontmatter
    with open(md_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    # Extract metadata
    title = post.metadata.get('title', md_file.stem.replace('-', ' ').title())
    date = post.metadata.get('date', '')
    
    # Convert markdown content to HTML
    html_content = convert_markdown_to_html(post.content)
    
    # Format HTML content with proper indentation
    indented_html = '\n'.join('                    ' + line if line.strip() else line 
                              for line in html_content.split('\n'))
    
    # Fill template
    html_output = HTML_TEMPLATE.format(
        title=title,
        date=date,
        content=indented_html
    )
    
    # Write output file
    output_file = OUTPUT_DIR / f"{md_file.stem}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"  -> Generated: {output_file}")
    return output_file


def main():
    """Main build function."""
    # Ensure directories exist
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all markdown files
    md_files = list(SRC_DIR.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {SRC_DIR}")
        print(f"Create .md files in {SRC_DIR} with frontmatter:")
        print("---")
        print("title: Your Article Title")
        print("date: Jan 2024")
        print("---")
        print("\nYour content here...")
        return
    
    print(f"Found {len(md_files)} markdown file(s)")
    print()
    
    # Build each article
    for md_file in md_files:
        try:
            build_article(md_file)
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("Build complete!")


if __name__ == "__main__":
    main()

