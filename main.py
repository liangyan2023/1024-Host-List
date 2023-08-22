import json
import requests
import sys

def loadHosts() -> list:
    hostList = []
    try:
        with open("1024_hosts.json", "r", encoding='utf8') as file:hostList = json.load(file)
    except:print("加载失败")
    return hostList

def saveHosts(hostList):
    with open("1024_hosts.json", "w+", encoding='utf8') as file:json.dump(hostList, file, ensure_ascii=False, indent = 4)

def saveREADME(hostList):
    content = f'''# 1024 Host List
最新域名：

| {" | ".join(hostList[-3:])} |
| ---- | ---- | ---- |

1024社区域名列表

| {" | ".join(hostList[:3])} |
| :---: | :---: | :---: |
'''

    for i in range(3, len(hostList), 3):
        content += f"| {' | '.join(['**' + i + '**' for i in hostList[i:i+3]])} |\n"
    with open("README.md", "w+", encoding='utf8') as file:file.write(content)

def getHosts() -> list:
    url = sys.argv[1]
    data = json.loads(sys.argv[2])
    response = requests.post(url,data=data)
    response = json.loads(response.text)
    hostList = []
    hostList.append(response['url1'])
    hostList.append(response['url2'])
    hostList.append(response['url3'])
    return hostList

def checkHost(host):
    headers  = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
    try:
        response = requests.get(f'https://{host}/index.php', headers=headers)
        if '歡迎新會員' in response.text:return True
        else:return False
    except requests.exceptions.ConnectionError:return False

def main():
    hostList = loadHosts()
    old_hostList = hostList.copy()
    lastestHostList = getHosts()
    for i in lastestHostList:
        if i not in hostList:hostList.append(i)
    for i in hostList:
        if checkHost(i):continue
        else:hostList.remove(i)
    if old_hostList == hostList:print("false")
    else:print("true")
    saveHosts(hostList)
    saveREADME(hostList)

if __name__ == '__main__':
    main()