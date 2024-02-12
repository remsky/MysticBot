import os
from discord import File
from discord.commands import Option
from discord.ext import commands
from jira import JIRA
from helper.tables import issues_to_image

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

JIRA_SERVER_URL = os.environ['JIRA_URL']
JIRA_EMAIL = os.environ['JIRA_EMAIL']
JIRA_API_KEY = os.environ['JIRA_API_KEY']
JIRA_PROJECT_KEY = os.environ['JIRA_PROJECT_KEY']


class JiraCog(commands.Cog, name="Jira"):

  def __init__(self, bot):
    self.bot = bot
    self.jira = JIRA(server=JIRA_SERVER_URL,
                     basic_auth=(JIRA_EMAIL, JIRA_API_KEY))

  @commands.slash_command(name="listopen", help="List all open Jira tickets")
  async def list_open_issues(self, ctx):
    await ctx.defer()
    try:
      issues = self.jira.search_issues(f'project={JIRA_PROJECT_KEY}')
      image_buffer = issues_to_image(issues)
      await ctx.respond(file=File(fp=image_buffer, filename="issues.png"))
    except Exception as e:
      await ctx.respond(f"Error: {str(e)}")

  @commands.slash_command(name="addticket",
                          help="Add a new Jira ticket",
                          guild_ids=SERVER_IDS)
  async def add_ticket(
      self,
      ctx,
      summary: str,
      description: str = Option(description="Description of the issue",
                                default="TODO"),
      issuetype: str = Option(description="Type of the issue",
                              choices=["Task", "Bug", "Story", "Epic"],
                              default="Task")):
    try:
      new_issue = self.jira.create_issue(project=JIRA_PROJECT_KEY,
                                         summary=summary,
                                         description=description,
                                         issuetype={'name': issuetype})
      await ctx.respond(
          f"New issue created: {new_issue.key}: {new_issue.fields.summary}")
    except Exception as e:
      await ctx.respond(f"Error: {str(e)}")


def setup(bot):
  bot.add_cog(JiraCog(bot))
