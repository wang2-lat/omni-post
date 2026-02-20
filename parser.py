import markdown
from pathlib import Path
import re

def parse_markdown(file_path: Path) -> dict:
    """Parse markdown file and extract metadata"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter if exists
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()
            
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
    
    # Extract title from first heading or frontmatter
    title = frontmatter.get('title', '')
    if not title:
        title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    
    return {
        'title': title or 'Untitled',
        'markdown': body,
        'html': html_content,
        'frontmatter': frontmatter
    }
