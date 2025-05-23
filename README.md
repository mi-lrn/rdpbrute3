## rdpbrute3

### What is rdpbrute3?

**rdpbrute3** is a brute forcing tool for remote desktop protocol (forked from crowbar) that can be used during penetration tests. It supports xfreerdp3 which is the new default on kali linux.

To get latest version from GitHub:

```
# git clone https://github.com/mi-lrn/rdpbrute3
# cd rdpbrute3/
# sudo python3 install.py
```

### Brute Forcing - Remote Desktop Protocol (RDP)

RDP brute forcing a host using a single username and a single password:

```
# rdpbrute3 -ho 192.168.2.182 -u admin -p Aa123456
```
- - -

RDP brute forcing a host using username list file and a single password:

```
# rdpbrute3 -ho 192.168.2.211 -U ~/Desktop/userlist -p passw0rd
```
- - -

RDP brute forcing a host using a single username and a password list:

```
# rdpbrute3 -ho 192.168.2.250 -u localuser -P ~/Desktop/passlist
```
- - -

RDP brute forcing multiple hosts using a username list and a password list:

```
# rdpbrute3 -H ~/Desktop/hostslist -U ~/Desktop/userlist -P ~/Desktop/passlist
```
- - -
