import re

def convert_content(content: dict, platform: str) -> dict:
    """Convert content format for specific platform"""
    
    converters = {
        'medium': _convert_medium,
        'devto': _convert_devto,
        'hashnode': _convert_hashnode,
        'reddit': _convert_reddit,
        'discord': _convert_discord
    }
    
    converter = converters.get(platform.lower(), _convert_default)
    return converter(content)

def _convert_medium(content: dict) -> dict:
    """Convert to Medium format (HTML)"""
    return {
        'title': content['title'],
        'content': content['html'],
        'contentFormat': 'html'
    }

def _convert_devto(content: dict) -> dict:
    """Convert to Dev.to format (Markdown)"""
    tags = content['frontmatter'].get('tags', '').split(',')
    return {
        'title': content['title'],
        'body_markdown': content['markdown'],
        'published': False,
        'tags': [tag.strip() for tag in tags if tag.strip()][:4]
    }

def _convert_hashnode(content: dict) -> dict:
    """Convert to Hashnode format (Markdown)"""
    tags = content['frontmatter'].get('tags', '').split(',')
    return {
        'title': content['title'],
        'contentMarkdown': content['markdown'],
        'tags': [{'name': tag.strip()} for tag in tags if tag.strip()]
    }

def _convert_reddit(content: dict) -> dict:
    """Convert to Reddit format (Markdown)"""
    # Reddit has character limits, truncate if needed
    body = content['markdown']
    if len(body) > 40000:
        body = body[:39900] + "\n\n[Content truncated...]"
    
    return {
        'title': content['title'][:300],  # Reddit title limit
        'text': body,
        'kind': 'self'
    }

def _convert_discord(content: dict) -> dict:
    """Convert to Discord webhook format"""
    # Discord has 2000 char limit per message
    body = content['markdown']
    if len(body) > 1900:
        body = body[:1900] + "..."
    
    return {
        'content': f"**{content['title']}**\n\n{body}",
        'username': 'Content Publisher'
    }

def _convert_default(content: dict) -> dict:
    """Default converter"""
    return {
        'title': content['title'],
        'content': content['markdown']
    }
