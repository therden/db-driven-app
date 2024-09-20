import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def add_entry(entry_dict, user_time):
  current_user = anvil.users.get_user()
  if current_user is not None:
    entry_dict['content'] = encrypt(entry_dict['content'])
    app_tables.entries.add_row(
      created=user_time,
      updated=user_time,
      user = current_user,
      **entry_dict
  )

@anvil.server.callable
def get_entries():
  current_user = anvil.users.get_user()
  # Get a list of entries from the Data Table, sorted by 'created' column, in descending order
  if current_user is not None:
    results = app_tables.entries.search(
      tables.order_by("created", ascending=False),
      user = current_user
    )
    for row in results:
      row['content'] = decrypt(row['content'])
    return results

@anvil.server.callable
def update_entry(entry, entry_dict):
  # check that the entry given is really a row in the ‘entries’ table
  if app_tables.entries.has_row(entry):
    entry_dict['content'] = encrypt(entry_dict['content'])
    entry.update(**entry_dict)
  else:
    raise Exception("Note does not exist")

@anvil.server.callable
def delete_entry(entry):
  # check that the entry being deleted exists in the Data Table
  if app_tables.entries.has_row(entry):
    entry.delete()
  else:
    raise Exception("Note does not exist")

@anvil.server.callable
def keep_alive():
  pass

@anvil.server.callable
def programmatic_logout():
  anvil.users.logout()

def encrypt(plaintext):
  return anvil.secrets.encrypt_with_key('cryptkeeper', plaintext)

def decrypt(ciphertext):
  try:
    return anvil.secrets.decrypt_with_key('cryptkeeper', ciphertext)
  except anvil.secrets.SecretError:
    return ciphertext