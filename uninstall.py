import os
import sys
script_name = "rdpbrute3.py"
if os.getuid() != 0:
    print("You must be an administrator to uninstall this utility.")
    sys.exit(1)
print("Uninstalling...")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts")
