#!/usr/bin/env python3
import os
import sys
import time
import re
import requests
import itertools

RANK = 'SAB'
TEMPLATE_URL = 'https://db.kcwiki.org/drop/map/{mapId}/{pointId}-{rank}.json'
TEMPLATE_EVENT_URL = 'https://db.kcwiki.org/drop/map/{mapId}/{difficult}/{pointId}-{rank}.json'

# data source https://github.com/kcwikizh/poi-statistics/blob/master/models/KanColleConstant_map.rb
# const boss = {}
# for (let key in json) { boss[key] = json[key].cells.filter(a => a.boss).map(a => a.point) }
# const MAP_BOSS = JSON.stringify(boss).replace(/"/g, "'").replace(/:/g, ": ").replace(/,/g, ", ")
MAP_BOSS = {'11': ['C'], '12': ['E'], '13': ['J'], '14': ['L'], '15': ['J'], '16': [], '21': ['H'], '22': ['K'], '23': ['N'], '24': ['P'], '25': ['O'], '31': ['G'], '32': ['L'], '33': ['M'], '34': ['P'], '35': ['K'], '41': ['J'], '42': ['L'], '43': ['N'], '44': ['K'], '45': ['T'], '51': ['J'], '52': ['O'], '53': ['Q'], '54': ['P'], '55': ['S'], '61': ['K'], '62': ['K'], '63': ['J'], '64': ['N'], '65': ['M'], '71': ['K'], '311': ['Z'], '312': ['Z'], '313': ['Z'], '314': ['Z'], '315': ['Z'], '316': ['Z'], '317': ['Z'], '321': ['J'], '322': ['K'], '323': ['K'], '324': ['O'], '325': ['N'], '331': ['J'], '332': ['O'], '333': ['S', 'T'], '341': ['J'], '342': ['J'], '343': ['K'], '344': ['K'], '345': ['M'], '346': ['N'], '347': ['N'], '351': ['I'], '352': ['M'], '353': ['J'], '354': ['Q'], '361': ['L'], '362': ['O'], '363': ['Q'], '364': ['V'], '365': ['T'], '371': [], '372': ['M'], '373': ['U'], '381': ['M'], '382': ['T'], '383': ['W'], '384': ['I'], '385': ['T'], '391': ['P'], '392': ['O'], '393': ['Q'], '394': ['N'], '395': ['M'], '396': ['S'], '397': ['U'], '401': ['S'], '402': ['P'], '403': ['S'], '404': ['ZZ3'], '411': ['O'], '412': ['Z'], '413': ['U'], '414': ['X'], '415': ['T'], '416': ['W'], '417': ['X'], '421': ['I'], '422': ['O'], '423': ['Q'], '424': ['U'], '425': ['Z2']}
# const mapPoint = {}
# for (var key in json) { mapPoint[key] = json[key].cells.map(a => a.point) }
# const MAP_INFO = JSON.stringify(mapPoint).replace(/"/g, "'").replace(/:/g, ": ").replace(/,/g, ", ").replace(/],/g, "],\n   ")
MAP_INFO = {
   '11': ['A', 'B', 'C'],
   '12': ['A', 'B', 'C', 'D', 'E'],
   '13': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
   '14': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
   '15': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
   '16': ['A', 'C', 'E', 'G', 'H', 'K', 'M', 'L', 'J', 'I', 'D', 'F', 'B', 'N'],
   '21': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
   '22': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
   '23': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'],
   '24': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
   '25': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
   '31': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
   '32': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
   '33': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'],
   '34': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
   '35': ['B', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'K'],
   '41': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
   '42': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
   '43': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'],
   '44': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
   '45': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'],
   '51': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
   '52': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
   '53': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'],
   '54': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
   '55': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S'],
   '61': ['B', 'A', 'C', 'D', 'F', 'G', 'I', 'H', 'E', 'J', 'K'],
   '62': ['B', 'C', 'A', 'D', 'F', 'E', 'H', 'G', 'I', 'J', 'K'],
   '63': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
   '64': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'],
   '65': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'],
   '71': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
   '311': ['A', 'B', 'C', 'E', 'F', 'Z'],
   '312': ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'Z'],
   '313': ['B', 'C', 'D', 'E', 'G', 'H', 'I', 'X', 'Z'],
   '314': ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'J', 'Z'],
   '315': ['A', 'C', 'E', 'F', 'G', 'H', 'J', 'K', 'Z'],
   '316': ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'K', 'L', 'M', 'Z'],
   '317': ['B', 'C', 'E', 'F', 'I', 'J', 'K', 'L', 'M', 'X', 'Y', 'Z'],
   '321': ['A', 'C', 'E', 'F', 'H', 'J'],
   '322': ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'K'],
   '323': ['B', 'C', 'D', 'E', 'F', 'H', 'K'],
   '324': ['B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'M', 'N', 'O'],
   '325': ['B', 'D', 'F', 'G', 'H', 'I', 'J', 'L', 'N'],
   '331': ['A', 'B', 'D', 'F', 'G', 'H', 'I', 'J'],
   '332': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
   '333': ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'S', 'T'],
   '341': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J'],
   '342': ['A', 'B', 'E', 'F', 'G', 'I', 'J'],
   '343': ['A', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K'],
   '344': ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
   '345': ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M'],
   '346': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'N'],
   '347': ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N'],
   '351': ['A', 'B', 'C', 'E', 'F', 'G', 'I'],
   '352': ['A', 'D', 'E', 'F', 'G', 'H', 'I', 'M'],
   '353': ['A', 'B', 'C', 'D', 'G', 'H', 'J'],
   '354': ['A', 'C', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'Q'],
   '361': ['B', 'C', 'D', 'E', 'F', 'J', 'L'],
   '362': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'O'],
   '363': ['A', 'B', 'C', 'D', 'F', 'H', 'I', 'J', 'K', 'L', 'Q'],
   '364': ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'J', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'V'],
   '365': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'O', 'P', 'T', 'U'],
   '371': ['A', 'B', 'D', 'I', 'L', 'M'],
   '372': ['A', 'B', 'E', 'F', 'G', 'H', 'I', 'J', 'M'],
   '373': ['A', 'B', 'C', 'D', 'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'Q', 'T', 'V', 'W', 'X', 'U'],
   '381': ['A', 'B', 'D', 'F', 'I', 'J', 'K', 'L', 'M'],
   '382': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'K', 'M', 'N', 'O', 'Q', 'R', 'T'],
   '383': ['A', 'F', 'G', 'K', 'P', 'R', 'S', 'I', 'L', 'O', 'Q', 'V', 'W'],
   '384': ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'K', 'L', 'N', 'O', 'P', 'Q'],
   '385': ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'O', 'R', 'N', 'T'],
   '391': ['C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'N', 'P', 'R', 'S'],
   '392': ['B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'O', 'P', 'Q'],
   '393': ['B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'Q'],
   '394': ['A', 'B', 'C', 'D', 'I', 'J', 'K', 'L', 'M', 'N'],
   '395': ['A', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'M'],
   '396': ['B', 'C', 'D', 'E', 'G', 'H', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S'],
   '397': ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'T', 'U'],
   '401': ['B', 'D', 'E', 'H', 'J', 'K', 'L', 'N', 'O', 'Q', 'S'],
   '402': ['A', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M', 'P', 'Q'],
   '403': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'J', 'K', 'L', 'N', 'O', 'P', 'Q', 'R', 'S'],
   '404': ['A', 'B', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z1', 'Z2', 'Z3', 'Z4', 'Z6', 'Z7', 'Z8', 'Z9', 'ZZ1', 'ZZ2', 'ZZ3'],
   '411': ['A', 'B', 'F', 'G', 'H', 'I', 'J', 'K', 'N', 'O'],
   '412': ['A', 'C', 'E', 'F', 'G', 'H', 'I', 'K', 'M', 'N', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
   '413': ['A', 'B', 'C', 'D', 'F', 'G', 'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q', 'S', 'U'],
   '414': ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'V', 'W', 'X'],
   '415': ['A', 'B', 'D', 'F', 'H', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'T'],
   '416': ['C', 'G', 'H', 'I', 'J', 'K', 'L', 'O', 'P', 'U', 'Q', 'V', 'R', 'W'],
   '417': ['A', 'C', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'Q', 'S', 'T', 'U', 'V', 'W', 'X'],
   # 抜錨！連合艦隊、西へ！
   '421':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
   '422':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'],
   '423':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q'],
   '424':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W'],
   '425':['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Z2', 'Z3'],
}

def printHelp():
    print('''kcwiki敌舰配置信息转换脚本

从 {url} 查询对应地图点敌舰配置信息，并转换为 wikitext 输出
活动地图编号可在 https://db.kcwiki.org/ 查询
活动地图难度编号： 1 丁 2 丙 3 乙 4 甲

用法:
    python {file} [difficult] [mapId]

命令:
    python {file} 11        # 转换 1-1 所有战斗点敌舰配置信息
    python {file} 61 C      # 转换 6-1 C 点敌舰配置信息
    python {file} 61 C D    # 转换 6-1 C D点敌舰配置信息
    python {file} 421 1     # 转换 425（2018秋活E1）丁难度敌舰配置信息

使用 "python {file} --help" 查看帮助。
'''.format(file=os.path.basename(__file__), url=TEMPLATE_URL))

def isNumber(s) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def isChar(s) -> bool:
    try:
        chr(s)
        return True
    except ValueError:
        return False

def isBoss(mapId, pointId) -> bool:
    return True if pointId.upper() in MAP_BOSS.get(mapId, []) else False

def convert2Wikitext(data, pointId, nodeType='') -> str:
    '''
    @param data: [
        {
            'formation': '単縦陣',
            'group': [1551, 1551]
        }
    ]
    @return:
        |nodetype =
        |海域点 =B
        |海域点原名 =
        |海域点译名 =
        |阵型 =複縦陣
        |敌方 ={{深海横幅|1522}}{{深海横幅|1529}}
        |阵型 =複縦陣
        |敌方 ={{深海横幅|1527}}{{深海横幅|1529}}
    '''
    if not data:
        return ''
    head = '''{{敌方配置表
|nodetype ={nodeType}
|海域点 ={pointId}
|海域点原名 =
|海域点译名 =
'''.format(nodeType=nodeType, pointId=pointId)

    enemies = []
    for conf in data:
        formation = '|阵型 ={formation}\n'.format(formation=conf.get('formation', ''))
        prefix = '|敌方 ={{深海横幅|'
        group = '}}{{深海横幅|'.join(conf.get('group', ''))
        suffix = '}}'
        res = ''.join([formation, prefix, group, suffix])
        enemies.append(res)

    return ''.join([head, '\n'.join(enemies)])

def saveFile(filename, data):
    if not data:
        return
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    return True

def handle(json) -> list:
    '''
    @return: [
        {
            'group': [1551, 1551],
            'formation': '単縦陣'
        }
    ]
    '''
    if not json or not json.get('data', None):
        return
    enemies = []
    for item in json.get('data', {}):
        enemy = json['data'][item].get('enemy')
        enemies.append(enemy.keys())
    enemies = list(itertools.chain.from_iterable(enemies)) # spread out
    enemies = list(set(enemies)) # uniq
    if len(enemies) <= 0:
        return

    enemyTable = []
    for enemy in enemies:
        # "潜水新棲姫 バカンスmode(1807)/潜水カ級(1532)/潜水カ級(1532)/駆逐イ級後期型(1575)(梯形陣)"
        group = re.findall(r'(?<=\().+?(?=\))', enemy) # 潜水カ級(1532)/潜水カ級(1532)(梯形陣) -> ['1532', '1532', '梯形陣']
        formation = group.pop() # ['1532', '1532', '1575', '梯形陣'] -> 梯形陣
        # 阵型合并
        if len(enemyTable) > 0 and enemyTable[-1]['group'] == group:
            enemyTable[-1]['formation'] += '<br>' + formation
            continue
        enemyConfig = {
            'group': sorted(group),
            'formation': formation
        }
        enemyTable.append(enemyConfig)
    return enemyTable

def getData(mapId, pointId, difficult=None):
    # difficult 地图难度 仅活动地图 1 丁 2 丙 3 乙 4 甲
    if difficult:
        url = TEMPLATE_EVENT_URL.format(mapId=mapId, pointId=pointId, rank=RANK, difficult=difficult)
    else:
        url = TEMPLATE_URL.format(mapId=mapId, pointId=pointId, rank=RANK)
    try:
        resp = requests.get(url)
        status = resp.status_code
        if status != 200:
            print('fail status', status)
            return
    except Exception  as e:
        print('error in request', e)
        return

    try:
        json = resp.json()
    except ValueError:
        print('json parse fail')
        return
    return json

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['h', 'help', '-h', '--help']:
        printHelp()
        return

    mapId = sys.argv[1]
    if not isNumber(mapId) or not 2 <= len(mapId) <= 3:
        print('参数 mapId 必须为 2-3 位地图编号数字')
        printHelp()
        return

    mapList = sys.argv[2:]
    difficult = None
    if isNumber(sys.argv[2]):
        difficult = sys.argv[2]
        mapList = sys.argv[3:] # reset mapList

    if len(mapList) <= 0:
        mapList = MAP_INFO.get(mapId, [])
    if len(mapList) <= 0:
        print('找不到地图 {} 的战斗点信息，请检查 mapId'.format(mapId))
        return

    res = []
    for i in range(0, len(mapList)):
        pointId = mapList[i].upper()
        print('starting download data {mapId}-{pointId} ...'.format(mapId=mapId, pointId=pointId))
        json = getData(mapId, pointId, difficult)
        enemyTable = handle(json)
        if not enemyTable:
          print('该点无敌人数据，可能不是战斗点')
          continue
        wikitext = convert2Wikitext(enemyTable, pointId, 'boss' if isBoss(mapId, pointId) else '')
        res.append(wikitext.strip('\n'))
    print('downloaded completed')
    if difficult:
        filename = '{mapId}-{difficult}.txt'.format(mapId=mapId, difficult=difficult)
    else:
        filename = mapId + '.txt'

    saveFile(filename, '\n'.join(res))
    print('save in', filename)
    print('finish')


if __name__ == '__main__':
    main()
