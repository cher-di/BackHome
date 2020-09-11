import subprocess
import re

MAC_REGEXP = re.compile('([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')


def scan():
    result = subprocess.run(['hcitool', 'scan'],
                            capture_output=True,
                            text=True,
                            check=True)

    addrs = dict()
    for line in result.stdout.split('\n')[1:-1]:
        # skip first line, because it is "Scanning..."
        # skip last line, because it is empty line
        mac = re.search(MAC_REGEXP, line).group()
        name = line.replace(mac, '').replace('\t', '')
        addrs[mac] = name

    return addrs
