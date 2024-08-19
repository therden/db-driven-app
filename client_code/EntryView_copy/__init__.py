from ._anvil_designer import EntryView_copyTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EntryEdit import EntryEdit
from datetime import datetime
import anvil.media


class EntryView_copy(EntryView_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.edit_entry_button.background = app.theme_colors["Green Button"]
    self.delete_entry_button.background = app.theme_colors["Red Button"]

    # Any code you write here will run when the form opens.

  def edit_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Create a copy of the existing entry from the Data Table
    entry_copy = dict(self.item)
    # Open an alert displaying the 'EntryEdit' Form
    # set the `self.item` property of the EntryEdit Form to a copy of the entry to be updated
    save_clicked = alert(
      content=EntryEdit(item=entry_copy),
      title="Update Note",
      large=True,
      buttons=[("Cancel", False), ("Save", True)],
    )
    # Update the entry if the user clicks save
    if save_clicked:
      entry_copy["updated"] = datetime.now(anvil.tz.tzlocal())
      anvil.server.call("update_entry", self.item, entry_copy)

      # Now refresh the page
      self.refresh_data_bindings()

  def delete_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get the user to confirm if they wish to delete the entry
    # If yes, raise the 'x-delete-entry' event on the parent
    # (which is the entries_panel on Homepage)
    # if confirm(f"Are you sure you want to delete {self.item['title']}?"):
    stripped_content = self.item["content"].replace("\n", " ")
    if len(stripped_content) >= 23:
      stripped_content = stripped_content[:20] + "..."
    if confirm(f"Confirm deletion of note '{stripped_content}'"):
      self.parent.raise_event("x-delete-entry", entry=self.item)

  def download_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    file_name = self.item["created"].strftime("%Y%m%d%H%M%S%z")
    file_contents = self.content_label.text.encode()
    text_file = anvil.BlobMedia("text/plain", file_contents, name=f"{file_name}.md")
    anvil.media.download(text_file)
