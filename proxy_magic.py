from proxy_checker import ProxyChecker
from proxyscrape import create_collector
import time


def get_proxies(region_codes: tuple = ('ru'), anonymous: bool = True, type: str = 'https', all: bool = False) -> list:
    collector = create_collector(
        name='default_collector',
        resource_types=type,
        refresh_interval=3600,
        resources=None
    )
    collector.apply_filter(
        {
            'code': region_codes,
            'anonymous': anonymous,
            'type': type
        })
    if not all:
        p = collector.get_proxy()
        return [f'{p.host}:{p.port}']
    proxies = []
    while True:
        p = collector.get_proxy()
        if p:
            if p not in proxies:
                proxies.append(f'{p.host}:{p.port}')
                collector.remove_proxy(p)
        else:
            break
    return proxies


def filter_bad_proxies(proxies: list) -> list:
    checker = ProxyChecker()
    return [prx for prx in proxies if checker.check_proxy(proxy=prx, check_country=False, check_address=False) != False]


def main():
    l1 = get_proxies(all=True)
    print(l1)
    l2 = filter_bad_proxies(l1)
    print(l2)
    

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Time: {time.time() - start_time} sec")
    