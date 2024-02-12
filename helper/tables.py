import matplotlib.pyplot as plt
import pandas as pd
import io


def issues_to_image(issues):
  """
  Purpose built for Jira tickets
  """
  # Convert issues to a DataFrame
  data = {
      'Key': [issue.key for issue in issues],
      'Summary': [issue.fields.summary for issue in issues],
      'Status': [issue.fields.status.name for issue in issues],
      'Type': [issue.fields.issuetype.name for issue in issues],
  }
  df = pd.DataFrame(data)

  # Determine the figure size required to make the table readable
  # Width can be set to a fixed size or made dynamic as well
  cell_width = 3.0
  cell_height = 0.625
  fig_width = cell_width * len(df.columns)
  fig_height = cell_height * (len(df) + 1)  # +1 for the header

  # Create the figure and axis
  fig, ax = plt.subplots(figsize=(fig_width, fig_height))
  ax.axis('off')

  # Create the table
  table = ax.table(
      cellText=df.values,
      colLabels=df.columns,
      cellLoc='center',
      loc='center',
      bbox=[0, 0, 1, 1]  # Use full area of the axis
  )

  # Style the table, you can fine-tune these parameters as needed
  table.auto_set_font_size(False)
  table.set_fontsize(12)
  table.auto_set_column_width(col=list(range(len(
      df.columns))))  # Adjust to fit the text

  # Convert matplotlib figure to PNG image
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.05)
  buffer.seek(0)
  plt.close(fig)

  return buffer


def dataframe_to_image(df):
  """
  More general function to convert a DataFrame to an image.
  """
  # Determine the figure size required to make the table readable
  cell_width = 3.0
  cell_height = 0.625
  fig_width = cell_width * len(df.columns)
  fig_height = cell_height * (len(df) + 1)  # +1 for the header

  # Create the figure and axis
  fig, ax = plt.subplots(figsize=(fig_width, fig_height))
  ax.axis('off')

  # Create the table
  table = ax.table(
      cellText=df.values,
      colLabels=df.columns,
      cellLoc='center',
      loc='center',
      bbox=[0, 0, 1, 1]  # Use full area of the axis
  )

  # Style the table
  table.auto_set_font_size(False)
  table.set_fontsize(12)
  table.auto_set_column_width(col=list(range(len(
      df.columns))))  # Adjust to fit the text

  # Convert matplotlib figure to PNG image
  buffer = io.BytesIO()
  plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.05)
  buffer.seek(0)
  plt.close(fig)

  return buffer
