# Discord Bot with JIRA Integration

## Introduction
This README provides setup and usage instructions for a Discord bot designed to integrate with JIRA. This bot allows Discord users to interact with JIRA issues directly, enhancing project management and collaboration efficiency.

## Features
- Listing all open JIRA tickets in a Discord channel.
- Creating new JIRA tickets from Discord.
- Converting JIRA ticket lists into images for easy visualization.

## Prerequisites
- A Discord account and administrative access to a server.
- An Atlassian JIRA account with access to your JIRA project.
- Python 3.8 or later.
- Poetry for dependency management.

## Setup Instructions

### Setting Up the Discord Bot
1. **Create a Discord Bot Account**:
   - Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to create a Discord bot account.
   - Note down the bot token for later use.

2. **Clone the Bot Repository**:
   - Use `git clone [repository-url]` to clone the bot's code to your machine.

3. **Install Dependencies with Poetry**:
   - Run `poetry install` to install the required Python packages.

### Configuring Environment Variables
Create a `.env` file in the project directory with the following content:
```bash
JIRA_URL=your_jira_server_url
JIRA_EMAIL=your_jira_email
JIRA_API_KEY=your_jira_api_key
JIRA_PROJECT_KEY=your_jira_project_key
BOT_TOKEN=your_discord_bot_token
SERVER_ID=your_discord_server_id
```
### Setting Up JIRA Integration
1. **Generate a JIRA API Token**:
   - Follow [these instructions](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/) to generate a JIRA API token.
   - Add the generated token and other JIRA details to the `.env` file.

### Running the Bot
Execute the bot using:
```bash
poetry run python bot.py
Usage
With the bot running, use these commands in your Discord server:
```
List Open Issues: /listopen lists all open JIRA tickets in your project.
Add New Ticket: /addticket with summary and description arguments to create a new JIRA ticket.
Contributing
We welcome contributions. Please use the standard fork-and-pull request workflow.

