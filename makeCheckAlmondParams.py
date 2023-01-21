#!/usr/bin/env python3
from pathlib import Path
home = str(Path.home())
email_address_from = input("Email address from: ")
email_address_to = input("Email address to: ")
email_password = input("Gmail App password: ")
parameters = {
    'email_address_from': email_address_from,
    'email_address_to': [email_address_from,email_address_to],
    'email_password': email_password
  }

import pickle
import stat
import os
file_name = home + '/checkAlmond.pickled'

with open(file_name, 'wb') as out_file:
  pickle.dump(parameters, out_file)
  st = os.stat(file_name)
  os.chmod(file_name, st.st_mode )
