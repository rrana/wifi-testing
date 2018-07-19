#!/usr/bin/env python

import wifi


interface_name = 'wlp3s0'

def scan_ssid(interface_name):
	ssid_list = wifi.scan.Cell.all(interface_name)
	return ssid_list


if __name__ == '__main__':
	for ssid in scan_ssid(interface_name):
		print ssid
