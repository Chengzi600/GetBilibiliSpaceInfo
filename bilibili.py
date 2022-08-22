import datetime
import time
import json
import os
import sys
# import shutil

import requests

version = '2.1.0'
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
}


def read_config():
    try:
        os.makedirs('./bilibili/images/', exist_ok=True)
        os.makedirs('./bilibili/data/', exist_ok=True)
        file_dir = r'./bilibili/config.json'
        config_v = {'sb': 'nmsl', 'fuckyou': 114514}
        try:
            with open(file_dir) as config_file:
                config = json.load(config_file)
                config_d = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))
                # print(config_d)

        except FileNotFoundError:
            with open(file_dir, 'w+') as config_file:
                # config_w = json.dumps(config_v, sort_keys=True, indent=4, separators=(',', ': '))
                json.dump(config_v, config_file)
            with open(file_dir) as config_file_r:
                config = json.load(config_file_r)
                config_d = json.dumps(config, sort_keys=True, indent=4, separators=(',', ': '))
        return config_d
    except:
            os.system('cls')
            print('=======================')
            print('配置文件或数据读写错误，请尝试以管理员身份运行或不要放在C盘或C盘根目录')
            print('如果你无意间修改时损坏了配置文件，请删除配置文件')
            print('请检查程序目录下是否创建bilibili文件夹')
            print('为防止崩溃，程序无法继续运行 ，请检查后重试')
            print('=======================')
            input('按回车退出程序...')
            sys.exit('FAILED_TO_LOAD_CONFIG')


# python删除文件的方法 os.remove(path)path指的是文件的绝对路径,如：
def del_file(path_data):
    for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + i  # 当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:  # os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
            print('已成功删除:' + str(file_data))
        else:
            del_file(file_data)

def get_info(i_uid, rt=0, rb=0, rc=''):
    url = 'https://api.bilibili.com/x/space/acc/info?mid='
    # 个人信息API
    url_b = 'https://api.bilibili.com/x/relation/stat?vmid='
    # UP主统计信息API(无需COOKIE版)
    url_c = 'https://api.bilibili.com/x/web-interface/archive/stat?bvid='
    # 视频查询API(BVID)
    uid = str(i_uid)
    bvid = str(rc)
    if rb != 0:
        r = requests.get(url_b + uid, headers=headers)
        response_dict_f = r.json()
    elif rc != '':
        r = requests.get(url_c + rc, headers=headers)
        response_dict_f = r.json()
    else:
        r = requests.get(url + uid, headers=headers)
        response_dict_f = r.json()
    if rt == 0:
        return response_dict_f
    else:
        return r

def api_test(r, r2, r3, response_dict):
    if response_dict['code'] == 0:
        print('B站API解析正常(0)')
    else:
        print('B站API解析异常' + '(' + str(response_dict['code']) + ')')

    if r.status_code == 200:
        print('个人信息API响应正常(200)')
    else:
        print('个人信息API响应异常' + '(' + str(r.status_code) + ')')

    if r2.status_code == 200:
        print('UP主信息API响应正常(200)')
    else:
        print('UP主信息API响应异常' + '(' + str(r2.status_code) + ')')

    if r3.status_code == 200:
        print('视频信息API响应正常(200)')
    else:
        print('视频信息API响应异常' + '(' + str(r3.status_code) + ')')

def output_info(response_dict, response_dict_b):
    os.system("cls")
    print('=========[API]=========')

    if response_dict['code'] == 0 and response_dict_b['code'] == 0:
        print('API返回状态码:' + '正常' + '(' + str(response_dict['code']) + ')(' + str(
            response_dict['message']) + ')' + '(' + str(response_dict_b['code']) + ')(' + str(
            response_dict_b['message']) + ')')
    else:
        print('API返回状态码:' + '异常' + '(' + str(response_dict['code']) + ')(' + str(
            response_dict['message']) + ')' + '(' + str(response_dict_b['code']) + ')(' + str(
            response_dict_b['message']) + ')')
        print('TTL:' + str(response_dict['ttl']) + '/' + str(response_dict_b['ttl']))
        print('====================')
        print('API返回状态码异常，获取失败')
        print('请检查网络或根据错误码寻找错误原因')
        return

    print('TTL:' + str(response_dict['ttl']))

    repo_dicts = response_dict['data']
    repo_dicts_b = response_dict_b['data']

    try:
        os.makedirs('./bilibili/images/', exist_ok=True)
        os.makedirs('./bilibili/data/', exist_ok=True)
        file_dir = r'./bilibili/images/' + repo_dicts['name'] + '-' + datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S") + '.jpg'
        file_dir_da = r'./bilibili/data/' + repo_dicts['name'] + '-data-' + datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S") + '.json'
        file_dir_db = r'./bilibili/data/' + repo_dicts['name'] + '-datab-' + datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S") + '.json'
        image = requests.get(repo_dicts['face'], headers=headers)
        with open(file_dir_da, 'w+') as da_file:
            json.dump(response_dict, da_file)
        with open(file_dir_db, 'w+') as db_file:
            json.dump(response_dict_b, db_file)
        with open(file_dir, 'wb') as image_file:
            image_file.write(image.content)
        os.system(r'start ' + file_dir)
    except:
        print('=======================')
        print('警告:数据下载或写入失败，请尝试管理员身份运行或检查网络')

    print('=======[基本信息]=======')
    repo_dicts_school_name = repo_dicts['school']['name']
    repo_dicts_profession_name = repo_dicts['profession']['name']
    print('UID:' + str(repo_dicts['mid']))
    print('昵称:' + str(repo_dicts['name']))
    print('性别:' + str(repo_dicts['sex']))
    print('头像:' + str(repo_dicts['face']))
    print('生日:' + str(repo_dicts['birthday']))
    print('学校:' + str(repo_dicts_school_name))
    print('职业:' + str(repo_dicts_profession_name))
    print('签名:' + str(repo_dicts['sign']))
    print('等级:Lv' + str(repo_dicts['level']))

    print('关注数:' + str(repo_dicts_b['following']))
    print('粉丝数:' + str(repo_dicts_b['follower']))
    print('私密数:' + str(repo_dicts_b['whisper']))
    print('拉黑数:' + str(repo_dicts_b['black']))

    print('主页图:' + str(repo_dicts['top_photo']))
    print('MCN机构:' + str(repo_dicts['mcn_info']))
    print('=======[粉丝勋章]=======')
    repo_dicts_medal = repo_dicts['fans_medal']
    print('是否展示:' + str(repo_dicts_medal['show']))
    print('是否佩戴:' + str(repo_dicts_medal['wear']))
    repo_dicts_medal_data = repo_dicts_medal['medal']
    if repo_dicts_medal['medal']:
        print('徽章名称:' + str(repo_dicts_medal_data['medal_name']))
        print('勋章UP主UID:' + str(repo_dicts_medal_data['target_id']))
        print('勋章编号:' + str(repo_dicts_medal_data['medal_id']))
        print('勋章等级:' + str(repo_dicts_medal_data['level']))
        print('亲密度(勋章经验):' + str(repo_dicts_medal_data['intimacy']))
        print('升级所需经验:' + str(repo_dicts_medal_data['next_intimacy']))

    else:
        print('徽章数据:无')

    print('=======[大会员信息]=======')
    repo_dicts_vip = repo_dicts['vip']
    if repo_dicts_vip['type'] == 0:
        print('大会员状态:从未开通(0)')
    elif repo_dicts_vip['type'] == 1:
        print('大会员状态:已过期(1)')
    elif repo_dicts_vip['type'] == 2:
        print('大会员状态:已开通(2)')
    else:
        print('大会员状态:未知(' + str(repo_dicts_vip['type']) + ')')

    due_date = int(repo_dicts_vip['due_date']) / 1000
    localtime = time.localtime(due_date)
    out_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    print('大会员到期时间:' + out_time)

    if repo_dicts_vip['status'] == 0:
        print('是否生效:False(0)')
    elif repo_dicts_vip['status'] == 1:
        print('是否生效:True(1)')
    else:
        print('是否生效:' + repo_dicts_vip['status'])

    repo_dicts_vip_label = repo_dicts_vip['label']
    print('大会员头衔:' + str(repo_dicts_vip_label['text']))

    print('=======[认证信息]=======')
    repo_dicts_official = repo_dicts['official']
    if repo_dicts_official['role'] != 0:
        if repo_dicts_official['role'] == 1:
            print('认证类型:知名UP主认证(1)')
        elif repo_dicts_official['role'] == 3:
            print('认证类型:企业认证(3)')
        elif repo_dicts_official['role'] == 4:
            print('认证类型:机构(国家机关)认证(4)')
        elif repo_dicts_official['role'] == 5:
            print('认证类型:机构(媒体)认证(5)')
        elif repo_dicts_official['role'] == 6:
            print('认证类型:机构(高校)认证(6)')
        elif repo_dicts_official['role'] == 9:
            print('认证类型:名人认证(9)')
        else:
            print('认证类型:其他(' + str(repo_dicts_official['role']) + ')')

        if repo_dicts_official['type'] == 1:
            print('认证颜色:蓝色小闪电(1)')
        else:
            print('认证颜色:黄色小闪电(' + str(repo_dicts_official['type']) + ')')

        print('认证信息:' + str(repo_dicts_official['title']))
        print('认证说明:' + str(repo_dicts_official['desc']))
    else:
        print('【该用户当前无任何认证】')

    print('=======[直播间信息]=======')
    repo_dicts_liveroom = repo_dicts['live_room']
    if repo_dicts_liveroom['roomStatus']:
        if repo_dicts_liveroom['roomStatus'] == 1:
            print('房间状态:已开通(1)')
        else:
            print('直播状态:(' + str(repo_dicts_liveroom['liveStatus']) + ')')
        if repo_dicts_liveroom['liveStatus'] == 1:
            print('开播状态:正在直播(1)')
        else:
            print('开播状态:未开播(' + str(repo_dicts_liveroom['liveStatus']) + ')')
        print('房间号:' + str(repo_dicts_liveroom['roomid']))
        print('标题:' + str(repo_dicts_liveroom['title']))
        print('直播间链接:' + str(repo_dicts_liveroom['url']))
        print('直播间封面:' + str(repo_dicts_liveroom['cover']))
        print('当前热度:' + str(repo_dicts_liveroom['watched_show']['text_large']))

    else:
        print('【此用户当前未开通直播间】')

    print('=======[头像框]=======')
    repo_dicts_pendant = repo_dicts['pendant']
    if repo_dicts_pendant['pid'] == 0:
        print('【此用户当前无头像框/挂件】')
    else:
        print('装扮ID:' + str(repo_dicts_pendant['pid']))
        print('装扮名称:' + str(repo_dicts_pendant['name']))
        print('图片:' + str(repo_dicts_pendant['image']))

    print('=======[名牌]=======')
    repo_dicts_nameplate = repo_dicts['nameplate']
    if repo_dicts_nameplate['nid'] == 0:
        print('【此用户当前无名牌】')
    else:
        print('装扮ID:' + str(repo_dicts_nameplate['nid']))
        print('装扮名称:' + str(repo_dicts_nameplate['name']))
        print('图片:' + str(repo_dicts_nameplate['image']))

    print('=======[荣誉]=======')
    repo_dicts_honour = repo_dicts['user_honour_info']
    if repo_dicts_honour['mid'] == 0:
        print('【此用户当前无荣誉】')
    else:
        print('ID:' + str(repo_dicts_honour['mid']))
        print('颜色:' + str(repo_dicts_honour['colour']))
        print('数量:' + str(len(repo_dicts_honour['tags'])))

def output_info_bv(response_dict_c):
    os.system("cls")
    print('=========[API]=========')

    if response_dict_c['code'] == 0:
        print('API返回状态码:' + '正常' + '(' + str(response_dict_c['code']) + ')(' + str(
            response_dict_c['message']) + ')')
    else:
        print('API返回状态码:' + '异常' + '(' + str(response_dict_c['code']) + ')(' + str(
            response_dict_c['message']) + ')')
        print('TTL:' + str(response_dict_c['ttl']))
        print('====================')
        print('API返回状态码异常，获取失败')
        print('请检查网络或根据错误码寻找错误原因')
        return

    print('TTL:' + str(response_dict_c['ttl']))

    repo_dicts = response_dict_c['data']
    try:
        os.makedirs('./bilibili/images/', exist_ok=True)
        os.makedirs('./bilibili/data/', exist_ok=True)
        file_dir_d = r'./bilibili/data/' + repo_dicts['bvid'] + '-bvdata-' + datetime.datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S") + '.json'
        with open(file_dir_d, 'w+') as d_file:
            json.dump(response_dict_c, d_file)
    except:
        print('=======================')
        print('警告:数据下载或写入失败，请尝试管理员身份运行或检查网络')

    print('=======[基础信息]=======')
    print('AV号:' + str(repo_dicts['aid']))
    print('BV号:' + str(repo_dicts['bvid']))
    print('=======[基础数据]=======')
    print('播放量:' + str(repo_dicts['view']))
    print('点赞数:' + str(repo_dicts['like']))
    print('投币数:' + str(repo_dicts['coin']))
    print('收藏数:' + str(repo_dicts['favorite']))
    print('转发数:' + str(repo_dicts['share']))
    print('弹幕数:' + str(repo_dicts['danmaku']))
    print('评论数:' + str(repo_dicts['reply']))
    print('=======[统计数据]========')
    try:
        print('点赞率:' + str('{:.2%}'.format(repo_dicts['like'] / repo_dicts['view'])))
        print('投币率:' + str('{:.2%}'.format(repo_dicts['coin'] / repo_dicts['view'])))
        print('收藏率:' + str('{:.2%}'.format(repo_dicts['favorite'] / repo_dicts['view'])))
        print('转发率:' + str('{:.2%}'.format(repo_dicts['share'] / repo_dicts['view'])))
        print('评论率:' + str('{:.2%}'.format(repo_dicts['reply'] / repo_dicts['view'])))
    except ZeroDivisionError:
        print('哎呀!有数值是0呢!无法计算统计数据啦!')

    print('=======[高级信息]========')
    print('当前排名:' + str(repo_dicts['now_rank']))
    print('最高排名:' + str(repo_dicts['his_rank']))
    if repo_dicts['no_reprint'] == 1:
        print('转载或自制:自制')
    else:
        print('转载或自制:转载')
    # 版权忽略
    print('争议信息(如有):' + str(repo_dicts['argue_msg']))
    print('评价(如有):' + str(repo_dicts['evaluation']))

try:
    r = get_info(114514, 1)
    response_dict = get_info(114514)
    r_b = get_info(114514, 1, 1)
    response_dict_b = get_info(114514, 0, 1)
    r_c = get_info(114514, 1, 0, 'BV17x411w7KC')
except:
    print('====================')
    print('网络通信错误，请检查网络连接')
    print('这可能是程序模块无法上网导致的，为防止崩溃，程序已停止运行')
    print('请检查网络连接后重试')
    print('====================')
    input('按回车退出程序...')
    sys.exit('CANNOT_CONNECT_API')

print('欢迎使用bilibili用户查询系统！version=' + version)
print('====================')
read_config()
api_test(r, r_b, r_c, response_dict)

while True:
    print('====================')
    print('命令列表:')
    print('[Q]退出程序 [S]设置 [X]清空下载的数据')
    print('[A]通过UID查询个人信息 [B]通过视频BVID查询视频信息')
    print('请输入命令后按下回车键')
    print('====================')
    i = input('>>>')
    if i == 'Q' or i == 'q' or i == '退出':
        break
    elif i == 'S' or i == 's' or i == '设置':
        print('====================')
        print('当前配置项如下(该功能还没有完成，无法配置)')
        print(read_config())
    elif i == 'X' or i == 'x' or i == '删除':
        os.system('cls')
        print('====================')
        print('确定要删除下载的头像和响应数据吗?')
        print('此操作将会清空程序文件夹bilibili下的data和images文件夹中的数据')
        print('确认请输入Y，否则直接按回车取消')
        print('====================')
        u = input('>>>')
        if u == 'Y' or u == 'y' or u == 'yes':
            try:
                del_file('./bilibili/images/')
                del_file('./bilibili/data/')
                print('====================')
                print('已成功清空所有数据!')
                print('====================')
                input('按回车返回主页面...')
                os.system('cls')
            except:
                print('====================')
                print('删除失败!请尝试删除整个程序文件夹bilibili，或手动删除')
                print('====================')

    elif i == 'A' or i == 'a' or i == '用户':
        os.system('cls')
        print('====================')
        print('请输入你要查询的用户UID，然后按下回车键')
        print('====================')
        u = input('>>>')
        try:
            r = get_info(int(u), 1)
            r_b = get_info(int(u), 0, 1)
            response_dict = get_info(int(u))
            response_dict_b = get_info(int(u), 0, 1)
            output_info(response_dict, response_dict_b)
        except:
            print('====================')
            print('一个或多个部分解析失败，请检查输入或网络')
            print('为防止程序崩溃，解析已结束')
            print('这也有可能是API或者程序的问题，如果别人也这样，请通知开发者')

    elif i == 'B' or i == 'b' or i == '视频':
        os.system('cls')
        print('====================')
        print('请输入你要查询的BV号，然后按下回车键')
        print('====================')
        u = input('>>>')

        try:
            r_c = get_info(114514, 0, 0, str(u))
            response_dict_c = get_info(114514, 0, 0, str(u))
            output_info_bv(response_dict_c)
        except:
            print('====================')
            print('一个或多个部分解析失败，请检查输入或网络')
            print('为防止程序崩溃，解析已结束')
            print('这也有可能是API或者程序的问题，如果别人也这样，请通知开发者')
    else:
        print('====================')
        print('命令有误，请检查后重试')
