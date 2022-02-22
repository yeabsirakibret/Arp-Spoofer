import telnetlib
import time

class RouterUsers:

    def __init__(self):
        pass
        

    def getOnlineUsers(self):
        online_users = {}

        tn = telnetlib.Telnet('192.168.1.1', 23)
        password = ""#your router admin password here
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        tn.write(b"ip arp status\n")

        arps = tn.read_until(b"#", timeout=0.2).decode('utf-8').split("\n")

        for arp in arps:
            if arp.startswith("192.168.1.1"):
                ar = arp.split(" ")
                online_users.setdefault(ar[-5].upper(), {'ip': ar[0], 'mac': ar[-5].upper(), 'name': '-', 'spoofed': False})

        tn.write(b"ip dhcp enif0 status\n")
        time.sleep(0.01)

        tn.write(b"exit\n")

        result = tn.read_until(b"#", timeout=0.2).decode('utf-8')

        lsts = result.split("hostname\r")[1].split("\n")

        for lst in lsts:
            sp = lst.split(" ")[-2:]
            if len(sp) == 2 and len(sp[0].split(":"))>3:
                
                if sp[0].upper() in online_users.keys():
                    online_users[sp[0].upper()]['name'] = sp[1].replace("\r", "") if len(sp[1]) > 1 else "-"
                
        return list(online_users.values())