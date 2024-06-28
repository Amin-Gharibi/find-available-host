import platform  # For getting the operating system name
import subprocess  # For executing a shell command
from concurrent.futures import ThreadPoolExecutor, as_completed  # For multi thread pinging


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def check_hosts(prefix, domain, start, end):
    """
    Finds the target host with PREFIX{i}.DOMAIN which i starts with START and ends with END
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_host = {executor.submit(ping, f'{prefix}{i}.{domain}'): i for i in range(start, end + 1)}
        for future in as_completed(future_to_host):
            host_index = future_to_host[future]
            try:
                is_up = future.result()
                if is_up:
                    print(f'{prefix}{host_index}.{domain} is up :)')
                    break
                else:
                    print(f'{prefix}{host_index}.{domain} is down :(')
            except Exception as exc:
                print(f'{prefix}{host_index}.{domain} generated an exception: {exc}')


if __name__ == '__main__':
    _prefix = input('Enter Prefix: ')
    _domain = input('Enter Domain: ')
    _start = int(input('Enter Starting Point: '))
    _end = int(input('Enter Ending Point: '))
    check_hosts(prefix=_prefix, domain=_domain, start=_start, end=_end)
