from ._anvil_designer import HomepageTemplate
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
import anvil.js.window


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    anvil.users.login_with_form()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    # self.refresh_entries()
    self.refresh_data_bindings()
    # Set an event handler on the RepeatingPanel (our 'entries_panel')
    self.entries_panel.set_event_handler("x-refresh_entries", self.refresh_entries)
    self.entries_panel.set_event_handler("x-delete-entry", self.delete_entry)

  def add_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Initialise an empty dictionary to store the user inputs
    new_entry = {}
    # Open an alert displaying the 'EntryEdit' Form
    save_clicked = alert(
      content=EntryEdit(item=new_entry),
      title="Add Note",
      large=True,
      buttons=[("Cancel", False), ("Save", True)],
    )
    # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      user_time = datetime.now(anvil.tz.tzlocal())
      anvil.server.call("add_entry", new_entry, user_time)
      # self.refresh_entries()
      self.refresh_data_bindings()

  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refreshing_data_bindings is called"""
    self.entries_panel.items = anvil.server.call("get_entries")

  def refresh_entries(self, *args, **kwargs):
    # Load and display existing entries from the Data Table
    self.entries_panel.items = anvil.server.call("get_entries")
    # server_entries = anvil.server.call('get_entries')
    # self.tag.local_entries = [dict(each) for each in server_entries]
    # self.entries_panel.items = self.tag.local_entries

  def delete_entry(self, entry, **event_args):
    # Delete the entry
    anvil.server.call("delete_entry", entry)
    # Refresh entry to remove the deleted entry from the Homepage
    # self.refresh_entries()
    self.refresh_data_bindings()

  def keepAlive_timer_tick(self, **event_args):
    """This method is called Every 1380 seconds (23 minutes)."""
    anvil.server.call("keep_alive")

  def logout_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call("programmatic_logout")
    anvil.js.window.location.reload(True)
