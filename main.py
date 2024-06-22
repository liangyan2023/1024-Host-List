import json
import os
import requests

def getReadmeConfig() -> dict:
    try:return requests.get(os.environ['GET_README_CONFIG']).json()
    except:return {'content1': '','content2': '','table_columns': 6}

def loadHosts() -> list:
    hostList = []
    try:
        with open("1024_hosts.json", "r", encoding='utf8') as file:hostList = json.load(file)
    except:print("加载失败")
    return hostList

def saveHosts(hostList):
    with open("1024_hosts.json", "w+", encoding='utf8') as file:json.dump(hostList, file, ensure_ascii=False, indent = 4)

def saveREADME(hostList):
    readmeConfig = getReadmeConfig()
    table_columns = readmeConfig['table_columns'] # table_columns 控制每行的列数
    content = f'''<h1 align="center">1024 Host List</h1>
<p align="center" class="shields">
    <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2Fpooneyy%2F1024-Host-List.json%3Fshow%3Dunique&style=flat-square&label=%E8%AE%BF%E9%97%AE%E4%BA%BA%E6%95%B0&labelColor=pink&color=default" alt="Visitors"/>
</p>
{readmeConfig['content1']}
最新域名：

| {" | ".join(hostList[-3:])} |
| ---- | ---- | ---- |

1024社区域名列表

| {" | ".join(hostList[:table_columns])} |
{"| :---: " * table_columns}|
'''

    for i in range(table_columns, len(hostList), table_columns):
        content += f"| {' | '.join(['**' + i + '**' for i in hostList[i:i+table_columns]])} |\n"
    content += f'\n{readmeConfig['content2']}'
    with open("README.md", "w+", encoding='utf8') as file:file.write(content)

def getHosts() -> list:
    url = os.environ['GET_HOSTS_API']
    data = json.loads(os.environ['GET_HOSTS_API_PAYLOAD'])
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