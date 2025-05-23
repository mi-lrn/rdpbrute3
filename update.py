import os
import sys
script_name = "rdpbrute3.py"
if os.getuid() != 0:
    print("You must be an administrator to update this utility.")
    sys.exit(1)
print("Updating...")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name} https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/{script_name}")
os.system(f"sudo chmod +x /usr/local/bin/{script_name}")
os.system(f"sudo mv -f /usr/local/bin/{script_name} /usr/local/bin/{script_name[:-3]}")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts/LICENSE")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts/README.md")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts/exceptions.py")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts/threadpool.py")
os.system(f"sudo rm -rf /usr/local/bin/{script_name[:-3]}_scripts/uninstall.py")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/LICENSE https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/LICENSE")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/README.md https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/README.md")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/exceptions.py https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/exceptions.py")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/threadpool.py https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/threadpool.py")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/uninstall.py https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/uninstall.py")
os.system(f"sudo curl --create-dirs -o /usr/local/bin/{script_name[:-3]}_scripts/update.py https://raw.githubusercontent.com/mi-lrn/rdpbrute3/master/update.py")
