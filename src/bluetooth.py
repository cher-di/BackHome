import subprocess
import re
import platform

MAC_REGEXP = re.compile('([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')


def scan():
    if platform.system() == 'Windows':
        return scan_windows()
    elif platform.system() == 'Linux':
        return scan_linux()
    else:
        raise Exception(f'Unsupported OS: {platform.system()}')


def scan_linux():
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


def scan_windows():
    result = subprocess.run(['btdiscovery', '-d', '%a%\\t%n%\\t%r%'],
                            capture_output=True,
                            text=True,
                            check=True)

    addrs = dict()
    for line in result.stdout.split('\n')[:-1]:
        # skip last string because it is empty
        mac, name, remembered = line.split('\t')
        mac = mac[1:-1]  # delete brackets
        if remembered == 'No':
            addrs[mac] = name

    return addrs
