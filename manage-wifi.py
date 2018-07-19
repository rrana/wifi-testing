#!/usr/bin/env python

import sys
import json
from argparse import ArgumentParser

import wifi


def scan_ssid(interface_name):
    wifi_network_details = {}

    try:
        ssid_list = wifi.Cell.all(interface_name)
    except wifi.exceptions.InterfaceError as err:
        print "%s - is not a valid wifi interface. Or, %s" % (interface_name, err)
        sys.exit(1)

    for ssid in ssid_list:
        ssid_details = []

        ssid_details.append({'SSID': ssid.ssid,
                            'Address': ssid.address,
                            'Encrypted': ssid.encrypted,
                            'Encryption_type' : ssid.encryption_type,
                            'Frequency': ssid.frequency,
                            'Channel': ssid.channel,
                            'Mode': ssid.mode,
                            'Quality': ssid.quality,
                            'Signal': ssid.signal,
                            'Noise': ssid.noise,
                            'Bitrates': ssid.bitrates
                            })
        wifi_network_details[ssid.ssid] = sorted(ssid_details)

    return wifi_network_details


def main(interface_name, report=False, insecure_networks=False):
    ssid_list = scan_ssid(interface_name)

    if report:
        print json.dumps(ssid_list, indent=2, sort_keys=True)

    if insecure_networks:
        insecure_network_list = []
        for ssid in ssid_list:
            if not ssid_list[ssid][0]['Encrypted']:
                insecure_network_list.append(ssid)
        if not insecure_network_list:
            print "All available wifi networks are encrypted!"
        else:
            print "List of unencrypted wifi networks: " + ', '.join([str(item) for item in insecure_network_list])


if __name__ == '__main__':
    parser = ArgumentParser(description='List available wifi networks')
    parser.add_argument('--interface', '-i', default='wlp3s0', help="Wifi interface name i.e. wlan0", type=str)
    parser.add_argument('--report', '-r', dest='report', action='store_true', help="Print detailed wifi scan report")
    parser.add_argument('--list-insecure-networks', dest='insecure_networks', action='store_true', help="Print list of networks without encryption")
    args = parser.parse_args()

    main(args.interface, args.report, args.insecure_networks)
