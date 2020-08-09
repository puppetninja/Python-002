#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from concurrent.futures import as_completed
import subprocess
import argparse
import os
import socket
import sys
import time
import json
from netaddr import IPRange


class NetScanner(object):
    def __init__(self, **kwargs):
        self.mode = kwargs['model']
        self.number = kwargs['number']
        self.function = kwargs['function']
        self.save_file = kwargs['write']
        self.verbose = kwargs['verbose']
        self.write = kwargs['write']

        # Convert ip_range into a list ip addrs in string
        ip_range = kwargs['ip_range'].split('-')
        netaddr_ip_range = IPRange(ip_range[0], ip_range[0]) \
            if len(ip_range) == 1 else IPRange(ip_range[0], ip_range[1])
        self.ip_range = [str(ip) for ip in netaddr_ip_range]

    def scan_ping_hosts(self, hosts):
        results = {'host_status': []}

        if self.mode == 'process':
            with ProcessPoolExecutor(max_workers=self.number) as executor:
                host_execs = {executor.submit(self.ping_host, host): host for host in hosts}
                for host_exec in as_completed(host_execs):
                    results['host_status'].append(host_exec.result())

        if self.mode == 'thread':
            with ThreadPoolExecutor(max_workers=self.number) as executor:
                host_execs = {executor.submit(self.ping_host, host): host for host in hosts}
                for host_exec in as_completed(host_execs):
                    results['host_status'].append(host_exec.result())

        return results

    def ping_host(self, host_ip):
        scan_process_id = os.getpid()

        try:
            subprocess.check_call("ping -c 1 %s" % host_ip, shell=True)
            host_status = {
                'host_ip': host_ip,
                'status': 'up',
                'process_id': scan_process_id
            }
        except subprocess.CalledProcessError:
            host_status = {
                'host_ip': host_ip,
                'status': 'down',
                'process_id': scan_process_id
            }

        return host_status

    def scan_tcp_host(self, host_ip):
        port_range = list(range(1, 1025))
        results = {'host_ip': host_ip, 'port_status': []}

        if self.mode == 'process':
            with ProcessPoolExecutor(max_workers=self.number) as executor:
                host_ports = {executor.submit(self.scan_tcp_host_port, host_ip, port): port for port in port_range}
                for port in as_completed(host_ports):
                    results['port_status'].append(port.result())

        if self.mode == 'thread':
            with ThreadPoolExecutor(max_workers=self.number) as executor:
                host_ports = {executor.submit(self.scan_tcp_host_port, host_ip, port): port for port in port_range}
                for port in as_completed(host_ports):
                    results['port_status'].append(port.result())

        return results

    def scan_tcp_host_port(self, host_ip, port):
        scan_process_id = os.getpid()
        s_timeout = 3
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(s_timeout)
        try:
            s.connect((host_ip, port))
            s.shutdown(socket.SHUT_RDWR)
            print("Port %s on %s is open" % (port, host_ip))
            port_status = {
                'number': port,
                'status': 'open',
                'scan_process_id': scan_process_id
            }
        except Exception:
            print("Port %s on %s is closed" % (port, host_ip))
            port_status = {
                'number': port,
                'status': 'closed',
                'scan_process_id': scan_process_id
            }
        finally:
            s.close()

        return port_status

    def save_results(self, results):
        try:
            with open(self.write, 'w') as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            sys.exit("Fail to write results due to %s " % (str(e)))

    def run(self):
        if self.verbose:
            start_time = time.time()

        if self.function == 'tcp':
            results = self.scan_tcp_host(self.ip_range[0])
        elif self.function == 'ping':
            results = self.scan_ping_hosts(self.ip_range)
        else:
            sys.exit("Not a supported funciton,"
                     "it should be either 'ping' or 'tcp'")

        if self.verbose:
            end_time = time.time()
            exec_duration = end_time - start_time
            print("****************Scan Execution Details****************")
            print("Execution time: %s seconds" % exec_duration)

        self.save_results(results)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model",
                        default="thread",
                        help="Model used to run, [process|thread]")
    parser.add_argument("-n", "--number",
                        type=int,
                        default=50,
                        help="Number of threads or processes spawned")
    parser.add_argument("-f", "--function",
                        default="ping",
                        help="Function of the scanning, [ping|tcp]")
    parser.add_argument("-ip", "--ip-range",
                        default="192.168.0.0-192.168.0.255",
                        help="A specific IP or "
                        "IP range like 192.168.0.1-192.168.0.100")
    parser.add_argument("-v", "--verbose",
                        type=bool,
                        default=True,
                        help="Whether to print out execution time.")
    parser.add_argument("-w", "--write",
                        default="results.json",
                        help="File to be save the scanning results.")
    return vars(parser.parse_args())


def main():
    args = parse_args()

    # Create scanner and run it
    ns = NetScanner(**args)
    ns.run()


if __name__ == "__main__":
    main()
