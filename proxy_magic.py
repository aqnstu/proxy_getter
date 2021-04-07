# -*- coding: utf-8 -*-
from proxyscrape import create_collector
import requests as r
import time


# TODO: комментарии, ускорить
# только для HTTP, HTTPS
def get_valid_proxies(iso_codes: tuple = ('ru'), anonymous: bool = True,
                type_proxy: str = 'https', all: bool = False, number_of_checks:int = 100,
                check_timeout: int = 0.5) -> list:
    collector = create_collector(
        name='default_collector',
        resource_types=type_proxy,
        refresh_interval=3600,
    )
    filter_dict = {
        'anonymous': anonymous,
        'type': type_proxy
    }
    if iso_codes != ():
        filter_dict['code'] = iso_codes
    collector.apply_filter(filter_dict)
    proxies, valid_proxies, i = [], [], 0
    while True:
        p = collector.get_proxy()
        print(p)
        if p and i < number_of_checks:
            p_str =  f'{p.host}:{p.port}'
            if p_str not in proxies:
                print('-', p_str)
                proxies.append(p_str)
                try:
                    if type_proxy == 'http':
                        req = r.get('http://api.ipify.org?fromat=json', proxies={'http': p_str}, timeout=check_timeout)
                    else:
                        req = r.get('https://api.ipify.org?fromat=json', proxies={'https': p_str}, timeout=check_timeout)
                    if req.text == p.host:
                        print('--', p_str)
                        if not all:
                            return [p_str]
                        valid_proxies.append(p_str)
                        collector.remove_proxy(p)
                except:
                    collector.remove_proxy(p)
                    continue
            else:
                collector.remove_proxy(p)
        else:
            break
        i += 1
    return valid_proxies


def main():
    l = get_valid_proxies(
        iso_codes=(),
        type_proxy='https',
        all=True,
        number_of_checks=30,
    )
    print(l)
    

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Time: {time.time() - start_time} sec")
    