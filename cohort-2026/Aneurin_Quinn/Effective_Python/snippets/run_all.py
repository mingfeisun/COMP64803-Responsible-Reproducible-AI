"""Run every demo in order -- the default command of the Docker image."""

import item_01_python_version
import item_04_fstrings
import item_06_unpacking
import item_08_zip
import item_10_walrus

for module in (item_01_python_version, item_04_fstrings, item_06_unpacking,
               item_08_zip, item_10_walrus):
    module.main()
    print()
