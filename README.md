# omni-post

CLI tool for publishing content to multiple platforms at once.

## Features

- Parse Markdown files with frontmatter support
- Convert content to platform-specific formats
- Publish to Medium, Dev.to, Hashnode, Reddit, Discord
- Batch publishing to multiple platforms
- Dry-run mode for testing
- Rich CLI output with status tables

## Installation


## Configuration

1. Copy the example config:

2. Edit `config.yaml` with your platform credentials

## Usage

Publish to all configured platforms:

Publish to specific platforms:

Dry run (preview without publishing):

Use custom config file:

## Markdown Format

Your markdown file can include frontmatter:


## Platform Setup

### Medium
1. Get integration token from https://medium.com/me/settings
2. Get user ID from API: `https://api.medium.com/v1/me`

### Dev.to
1. Get API key from https://dev.to/settings/extensions

### Hashnode
1. Get personal access token from https://hashnode.com/settings/developer
2. Get publication ID from your publication settings

### Reddit
1. Create OAuth app at https://www.reddit.com/prefs/apps
2. Get access token via OAuth flow

### Discord
1. Create webhook in channel settings
2. Copy webhook URL

## License

MIT