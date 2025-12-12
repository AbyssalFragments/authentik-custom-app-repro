from os import makedirs, walk
from shutil import copy, copytree, rmtree
from os.path import exists, dirname, join
from sys import argv
import re

authentik_path = "/authentik"

if "test" in argv:
  print("Running in test mode")
  # copy ./authentik to ./authentik-copy
  if exists("./authentik-copy"):
    rmtree("./authentik-copy")
  copytree("./authentik", "./authentik-copy")
  authentik_path = "./authentik-copy"


print("Forcing yourpackage.apps into TENANT_APPS array")
with open(f'{authentik_path}/root/settings.py', 'r') as f:
  content = f.read()

content = re.sub(r'(\s+)"guardian",', r'\g<0>\g<1>"yourpackage.apps",', content)

print("Adding patched to `Booting authentik` log")

content = re.sub(r'Booting authentik', 'Booting authentik (patched)', content)

with open(f'{authentik_path}/root/settings.py', 'w') as f:
  f.write(content)

print("Applying overrides")
for root, dirs, files in walk("overrides"):
  for file in files:
    if file.endswith(".py"):
      # Get the relative path from overrides directory
      source_path = join(root, file)
      # Remove "overrides" prefix to get relative path
      if root.startswith("overrides"):
        rel_path = root[len("overrides"):].lstrip("/\\")
        rel_path = join(rel_path, file) if rel_path else file
      else:
        rel_path = file
      
      target_path = join(authentik_path, rel_path)
      
      print(f'Overwriting {source_path} -> {target_path}')
      
      # Create parent directory if it doesn't exist
      target_dir = dirname(target_path)
      if target_dir and not exists(target_dir):
        print(f'Creating directory {target_dir}')
        makedirs(target_dir, exist_ok=True)
      
      copy(source_path, target_path)


print('Patching all startswith("authentik") checks')

# recurse all files
for root, dirs, files in walk(authentik_path):
  for file in files:
    if file.endswith(".py"):
      with open(f'{root}/{file}', 'r') as f:
        content = f.read()
      content = re.sub(r'if ([^\s].+)\.startswith\("authentik"\)', r'\g<0> or \g<1>.startswith("yourpackage")', content)
      with open(f'{root}/{file}', 'w') as f:
        f.write(content)
print("Done!")