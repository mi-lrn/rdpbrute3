import os
import sys
script_name = "rdpbrute3.py"
if os.getuid() != 0:
    print("You must be an administrator to install this utility.")
    sys.exit(1)
print("Installing...")
os.system(f"sudo chmod +x {script_name}")
os.system(f"mv -f {script_name} {script_name[:-3]}")
os.system(f"sudo mv -f {script_name[:-3]} /usr/local/bin/{script_name[:-3]}")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts")
os.system(f"sudo mkdir -p /usr/local/bin/{script_name[:-3]}_scripts")
os.system(f"sudo mv -f uninstall.py /usr/local/bin/{script_name[:-3]}_scripts/uninstall.py")
os.system(f"sudo mv -f update.py /usr/local/bin/{script_name[:-3]}_scripts/update.py")
os.system(f"sudo mv -f threadpool.py /usr/local/bin/{script_name[:-3]}_scripts/threadpool.py")
os.system(f"sudo mv -f exceptions.py /usr/local/bin/{script_name[:-3]}_scripts/exceptions.py")
os.system(f"sudo mv -f LICENSE /usr/local/bin/{script_name[:-3]}_scripts/LICENSE")
os.system(f"sudo mv -f README.md /usr/local/bin/{script_name[:-3]}_scripts/README.md")
os.system(f"sudo rm -rf install.py")
print(f"IMPORTANT: uninstall.py and update.py have been relocated to /usr/local/bin/{script_name[:-3]}_scripts")
