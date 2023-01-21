#!/usr/bin/env python3
parameters = {
    'email_address_from': 'jt2354@gmail.com',
    'email_address_to': ['riveralmondactiongroup@gmail.com','jt2354@gmail.com'],
    'email_password': '<generated Google Gmail App password>'
  }

import pickle
import stat
import os
file_name = '~/checkAlmond.pickled'

with open(file_name, 'wb') as out_file:
  pickle.dump(parameters, out_file)
  st = os.stat(file_name)
  os.chmod(file_name, st.st_mode )
