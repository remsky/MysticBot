import os

import discord
import requests

from discord.ext import commands
from helper.tables import dataframe_to_image

SERVER_IDS = [os.getenv("SERVER_ID")]
# ^add as parameter to command to speed slash command updates if its slow
#  by localizing commands to single server
# -they are added globally by default, and this can take some time
# e.g:
# @commands.slash_command(name="show_tickets",
#                         description="Lists all tickets in the project",
#                         guild_ids=SERVER_IDS)
# async def show_tickets(ctx):
# .....


class GitHubProjectsCog(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.github_token = os.getenv("GITHUB_TOKEN")

    self.headers = {"Authorization": f"Bearer {self.github_token}"}
    self.git_project_username = os.getenv("GIT_PROJECTS_USERNAME")
    self.project_number = 1
    self.project_node_id = None
    self.bot.loop.create_task(self.setup_project())

  async def setup_project(self):
    project_id = await self.get_project_node_id(self.git_project_username,
                                                self.project_number)
    if project_id:
      self.project_node_id = project_id

    print(f"Project Node ID: {self.project_node_id}")

  async def graphql_request(self, query, variables=None):
    response = requests.post('https://api.github.com/graphql',
                             json={
                                 'query': query,
                                 'variables': variables
                             },
                             headers=self.headers)
    if response.status_code == 200:
      return response.json()['data']
    else:
      raise Exception(
          f"GraphQL query failed with response code: {response.status_code}")

  async def get_project_node_id(self, username, project_number):
    query = """
          query($username: String!, $projectNumber: Int!) {
            user(login: $username) {
              projectV2(number: $projectNumber) {
                id
              }
            }
          }
          """
    variables = {"username": username, "projectNumber": project_number}
    result = await self.graphql_request(query, variables)
    return result['user']['projectV2']['id']

  async def add_draft_issue_to_project(self, project_id, title, body):
    mutation = """
          mutation($projectId: ID!, $title: String!, $body: String!) {
            addProjectV2DraftIssue(input: {projectId: $projectId, title: $title, body: $body}) {
              projectItem {
                id
              }
            }
          }
          """
    variables = {"projectId": project_id, "title": title, "body": body}
    result = await self.graphql_request(mutation, variables)
    return result['addProjectV2DraftIssue']['projectItem']['id']

  async def fetch_project_fields(self, project_id):
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2IterationField {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
              }
            }
          }
        }
      }
    }
    """
    variables = {"projectId": project_id}
    result = await self.graphql_request(query, variables)
    fields = result['node']['fields']['nodes']
    return {field['name']: field['id'] for field in fields}

  async def query_project_items(self, project_id):
    query = """
          query($projectID: ID!) {
            node(id: $projectID) {
              ... on ProjectV2 {
                items(first: 20) {
                  nodes {
                    id
                    fieldValues(first: 8) {
                      nodes {
                        ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { name } } }
                        ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2FieldCommon { name } } }
                        ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
                      }
                    }
                    content {
                      ... on DraftIssue { title body }
                      ... on Issue { title assignees(first: 10) { nodes { login } } }
                      ... on PullRequest { title assignees(first: 10) { nodes { login } } }
                    }
                  }
                }
              }
            }
          }
          """
    variables = {"projectID": project_id}
    return await self.graphql_request(query, variables)

  @commands.slash_command(
      name="add_ticket",
      description=
      "Adds a draft ticket to the project, requires title and short decription"
  )
  async def add_draft_issue(self, ctx, title: str, body: str):
    draft_issue_id = await self.add_draft_issue_to_project(
        self.project_node_id, title, body)
    if draft_issue_id:
      await ctx.respond(f"Draft issue added with ID: {draft_issue_id}")
    else:
      await ctx.respond("Failed to add draft issue.")

  @commands.slash_command(name="show_tickets",
                          description="Lists all tickets in the project")
  async def show_project_items(self, ctx):
    await ctx.defer()

    items = await self.query_project_items(self.project_node_id)

    # Create a DataFrame from the items
    data = {
        'Title': [
            item['content'].get('title', 'No Title')
            for item in items['node']['items']['nodes']
        ],
        'Body': [
            item['content'].get('body', 'No Body')
            for item in items['node']['items']['nodes']
        ]
    }
    df = pd.DataFrame(data)

    # Generate the image from the DataFrame
    image_buffer = dataframe_to_image(df)

    # Send the table image
    await ctx.send(
        file=discord.File(fp=image_buffer, filename='project_items.png'))


def setup(bot):
  bot.add_cog(GitHubProjectsCog(bot))
