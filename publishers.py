import requests
from typing import Tuple

def publish_to_platforms(platform: str, content: dict, config: dict) -> Tuple[str, str]:
    """Publish content to specific platform"""
    
    publishers = {
        'medium': _publish_medium,
        'devto': _publish_devto,
        'hashnode': _publish_hashnode,
        'reddit': _publish_reddit,
        'discord': _publish_discord
    }
    
    publisher = publishers.get(platform.lower(), _publish_generic)
    return publisher(content, config)

def _publish_medium(content: dict, config: dict) -> Tuple[str, str]:
    """Publish to Medium via API"""
    url = f"https://api.medium.com/v1/users/{config['user_id']}/posts"
    headers = {
        'Authorization': f"Bearer {config['token']}",
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=content, headers=headers, timeout=30)
        if response.status_code in [200, 201]:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return "error", str(e)

def _publish_devto(content: dict, config: dict) -> Tuple[str, str]:
    """Publish to Dev.to via API"""
    url = "https://dev.to/api/articles"
    headers = {
        'api-key': config['api_key'],
        'Content-Type': 'application/json'
    }
    
    payload = {'article': content}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code in [200, 201]:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return "error", str(e)

def _publish_hashnode(content: dict, config: dict) -> Tuple[str, str]:
    """Publish to Hashnode via GraphQL API"""
    url = "https://api.hashnode.com"
    headers = {
        'Authorization': config['token'],
        'Content-Type': 'application/json'
    }
    
    mutation = """
    mutation CreatePost($input: CreateStoryInput!) {
        createPublicationStory(input: $input) {
            code
            success
        }
    }
    """
    
    variables = {
        'input': {
            'title': content['title'],
            'contentMarkdown': content['contentMarkdown'],
            'tags': content.get('tags', []),
            'publicationId': config['publication_id']
        }
    }
    
    try:
        response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers, timeout=30)
        if response.status_code == 200:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return "error", str(e)

def _publish_reddit(content: dict, config: dict) -> Tuple[str, str]:
    """Publish to Reddit via API"""
    url = f"https://oauth.reddit.com/api/submit"
    headers = {
        'Authorization': f"Bearer {config['access_token']}",
        'User-Agent': 'omni-post/1.0'
    }
    
    data = {
        'sr': config['subreddit'],
        'kind': content['kind'],
        'title': content['title'],
        'text': content['text']
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        if response.status_code == 200:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return "error", str(e)

def _publish_discord(content: dict, config: dict) -> Tuple[str, str]:
    """Publish to Discord via Webhook"""
    url = config['webhook_url']
    
    try:
        response = requests.post(url, json=content, timeout=30)
        if response.status_code in [200, 204]:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return "error", str(e)

def _publish_generic(content: dict, config: dict) -> Tuple[str, str]:
    """Generic webhook publisher"""
    if 'webhook_url' not in config:
        return "error", "No webhook_url configured"
    
    try:
        response = requests.post(config['webhook_url'], json=content, timeout=30)
        if response.status_code in [200, 201, 204]:
            return "success", "Published successfully"
        return "error", f"HTTP {response.status_code}"
    except Exception as e:
        return "error", str(e)
