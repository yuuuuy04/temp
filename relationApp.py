from datetime import timedelta
from urllib.parse import urlencode
from flask import Flask, jsonify,request, send_from_directory
from flask_cors import CORS
from static.TikTok import *
from static.DataFetcher import startLoadData
from static.checkFile import *
from static.sendData import startSend
from static.checkData import startCheckCoolaborated
from static.filterData1 import start_filter_excel_data
import os
import sys
import pandas as pd
import webbrowser
import threading
def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# 使用resource_path函数来引用seleniumwire的证书文件
ca_crt_path = resource_path(os.path.join('seleniumwire', 'ca.crt'))
ca_key_path = resource_path(os.path.join('seleniumwire', 'ca.key'))
# if getattr(sys, 'frozen', False):
#     # 如果是打包后的exe文件，返回exe所在的目录
#     application_path = os.path.dirname(sys.executable)
# else:
#     # 如果是普通的脚本文件，返回脚本所在的目录
#     application_path = os.path.dirname(os.path.abspath(__file__))

# # 使用application_path而不是直接使用__file__
# current_dir = application_path
# print(current_dir)  # 打印当前的工作目录
# os.chdir(application_path)  # 修改工作目录到应用所在的位置
app = Flask(__name__,template_folder='static', static_url_path='')
# app = Flask(__name__,template_folder='static', static_url_path='',root_path=application_path)
app.secret_key = 'gdufe'

CORS(app)  # 允许所有来源的跨域请求，也可以指定特定源
mylogin=TikTokShop_Loginer(arg_path_driver_chrome=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
email_global=None
# email_global="tiger1689999@163.com"
@app.route('/login',methods=['POST','GET'])
def login():
    single=None
    file_path = "data/headers.json"
    # 确保目录存在
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # 创建所有需要的父级目录
        print(f"已创建目录: {directory}")
    
    # 确保文件存在
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)  # 初始化为空列表
            print(f"已创建新文件: {file_path}")
    # 假设这是从请求中获取的email和password
    global email_global
    email = request.get_json().get('email')
    email_global = email
    password = request.get_json().get('password')
    with open(file_path, 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []  # 如果文件为空或者不是有效的JSON格式，则从空列表开始
        account_entry = next((item for item in data if item.get('account') == email), None)
        if account_entry:
            last_detail = account_entry['details'][-1]
            if 'cookie1' not in last_detail:
                if 'update' not in last_detail:
                    account_check = "notExit"
                    print(f"账号没有cookie且无update: {email}")
                else:
                    account_check = "准备写入"
                    print(f"账号没有cookie但有update: {email}")
            else:
                # 获取最后一个update的时间
                last_update_str = last_detail['update']
                last_update = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")
                if datetime.now() - last_update > timedelta(days=3):
                    # 如果距离上次更新超过3天，添加新的更新时间
                    account_entry['details'].append({"update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    account_check = "账号过期"
                    print(f"账号过期，更新了email账户: {email}")
                else:
                    account_check = "exit"
                    print(f"Email账户已存在且未过期: {email}")
        else:
            # 添加新的email账户及当前时间到details
            data.append({
                "account": email,
                "details": [{"update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
            })
            account_check = "notExit"
            print(f"添加了新的email账户: {email}")
        
        # 回到文件开头，写入更新后的数据并截断原文件长度
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(email, password)
    if account_check!="exit":
        result = mylogin.login(email, password)
        print(result)
        single = "登录请求超时" if result.get('is_timeout_send_request_login_by_email') else ""
        single = "用户不存在" if result["body_response_login_by_email"]["data"]["description"]=="用户不存在" else ""
        single = "账号或密码错误，请重试。" if result["body_response_login_by_email"]["data"]["description"][:7]=="账号或密码错误" else ""
        if single!="":
            mylogin.quit()
        # print(result)
    else:
        print("已有账号且不用更新")
    return jsonify({'single': single, 'account': email, 'status': account_check})

@app.route('/verify',methods=['POST','GET'])
def verify():
    # 文件路径
    file_path = "data/headers.json"
    print(f"user_email:{email_global}")
    verify_input = request.get_json().get('verify')
    region=request.get_json().get('region')
    print(region)
    # mylogin.set_homepage_url(f"https://seller.tiktokglobalshop.com/homepage?shop_region={region}")
    print(mylogin)
    print(verify_input)
    result_verify = mylogin.verify_by_email(verify_input)
    print(result_verify)
    try:
        if result_verify["body_response_verify_by_email"]["message"]!='success':
            return jsonify({'status': "请重试"})
    except Exception as e:
        print(e)
    mylogin.change_region(region_code=region)
    # cookie = mylogin.get_cookies_homepage()
    is_timeout, cookie = mylogin.get_cookies_homepage()
    print("1")
    print(is_timeout)
    print(cookie)
    # for index in range(10):
        
    #     is_timeout, cookie = mylogin.get_cookies_homepage()
    #     if not is_timeout:
    #         print("完整 Cookies:", cookie)
    #         break
    #     else:
    #         print(index)
    #         print("获取 Cookies 超时")
    if is_timeout:
        mylogin.refresh()
        is_timeout, cookie = mylogin.get_cookies_homepage()
        print(cookie)
    try:
        is_timeout, seller_id = mylogin.get_seller_id()
        print(f"seller_id{seller_id}")
    except Exception as e:
        print(e)
    img_src = mylogin.get_headshot()
    print(f"img_src:{img_src}")
    mylogin.quit()
    # 读取现有数据
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    account_found = False
    for item in data:
        if item["account"] == email_global:  # 假设account对应于user_email
            account_found = True
            # 更新或设置"src"和"seller_id"
            item["src"] = img_src
            item["seller_id"] = seller_id
            
            # 如果details存在，则在最后一个detail中添加或更新cookie
            if "details" in item and len(item["details"]) > 0:
                last_detail = item["details"][-1]
                last_detail["cookie"] = cookie  # 更新或添加cookie键值对
            break
    # 如果找到了对应的account，则将更新的数据写回到文件中
    if account_found:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    account_check = 'success' if account_found else 'fail'
    return jsonify({'status': account_check})

@app.route('/loadData',methods=['POST','GET'])
def myLoadData():
    file_path = "data/headers.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item["account"] == email_global: 
            cookies_str=item['details'][-1]['cookie']
            shop_id=item['seller_id']
            break
    headers = {
    'path': '/api/v1/oec/affiliate/creator/marketplace/find?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m5z3kj3u_5IrLVhnI_rbyW_4PzT_AW9a_WyqHSuXALryM&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F131.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id=7495839077177002076&shop_region=MY&msToken=mncDPr3yLt3R-gcrA8RiLp-_O7HxcWEhQMUaEeHB1Qlrkv3THOLRZSma-LokVxumueiLq7AQkWYdCmd0DGRIthC4y2ugtmSOWeAvSGQr0_ODs1lxvDW-_dDsPAz1e2MhJwqMgxil&X-Bogus=DFSzswVYbt-0OEactpj1hcTQh4tl&_signature=_02B4Z6wo00001t6geJQAAIDDAfuL2vnCxqLeoHwAANAt42',
    'content-type': 'application/json',
    'cookie': cookies_str,
    'referer': 'https://affiliate.tiktokglobalshop.com/connection/creator?shop_region=MY',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0'
}
    region=request.get_json().get('region')
    select_time=request.get_json().get('update')
    params = {
        'user_language': 'zh-CN',
        'aid': '6556',
        'app_name': 'i18n_ecom_alliance',
        'device_id': '0',
        'fp': 'verify_m6093t7z_9SDrPxRV_BiaM_4TEK_BBIK_ZRIXcgw9DvxP',
        'device_platform': 'web',
        'cookie_enabled': 'true',
        'screen_width': '475',
        'screen_height': '622',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Mozilla',
        'browser_version': '5.0+(Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F131.0.0.0+Mobile+Safari%2F537.36+Edg%2F131.0.0.0',
        'browser_online': 'true',
        'timezone_name': 'Asia%2FShanghai',
        'oec_seller_id': f'{shop_id}',
        'shop_region': f'{region}',
        # 'msToken': 'S6iysZXnpqvtpUmkV-uuXE3H3XUY_3pwecA8IM272SUrhH1MXCJI6tFTjbdFdP9hnX0ifE9v2-1_Lnm9FoQiclrcujN5APmXUBgGwdCVBE098ZiW1DPGLyJm6pydT-v3unpdEHJ0Hco=',
        # 'X-Bogus': 'DFSzKwVO49G4JIVftpcIZOTQh4Cs',
        # '_signature': '_02B4Z6wo00001XNrUZQAAIDArDCi23NZjHFze1UAADtU5f'
    }

    # 构建查询字符串
    query_string = urlencode(params)
    details_url=f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/profile?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m7g9hi5s_6ovVNPzE_w6yB_4u9G_9FOF_EEWcpRs7BnaX&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F133.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id={shop_id}&shop_region={region}&msToken=A8_Dkys1oqImNwD0QD4I4M1g_UxMsEtv1sZpeE1RhZbt2scejKNCcqOxYCwxlvpjB6B6R-zPPopH5rqmM3wWm_GHcROKJbz6V3RLo6hJ3rimBAnt9p5VIraxTw7N-2Q1GrQji9Lq&X-Bogus=DFSzswVuw9zCkQ4ktDy3vcTQh4CI&_signature=_02B4Z6wo00001TKqungAAIDA7fFJNl0tIy0yqr7AACsW47"
    # 构建完整的URL
    url = f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/find?{query_string}"
    timeFlag=check_file_in_data('creator.csv','mytime')
    if select_time=='none-day':
        startLoadData(url=url,headers=headers,cookies_str=cookies_str,region=region,details_url=details_url)
    elif select_time=='three-day':
        if timeFlag=='notExist'or timeFlag>3:
            startLoadData(url=url,headers=headers,cookies_str=cookies_str,region=region,details_url=details_url)
            
    elif select_time=='week':
        if timeFlag=='notExist'or timeFlag>7:
            startLoadData(url=url,headers=headers,cookies_str=cookies_str,region=region,details_url=details_url)
            
    elif select_time=='month':
        if timeFlag=='notExist'or timeFlag>30:
            startLoadData(url=url,headers=headers,cookies_str=cookies_str,region=region,details_url=details_url)
            
    return jsonify({'status':'success_load'})

@app.route('/filterData',methods=['POST','GET'])
def filterData():
    file_path = "data/merged_data.csv"

    filter_condition=request.get_json().get('filterCondition')
    need_smart_sort = ('sortBy' in request.json and request.json['sortBy'] == 'smart')
    
    # 添加智能排序标识
    filter_condition['need_smart_rank'] = need_smart_sort
    filter_df=start_filter_excel_data(file_path=file_path,filter_conditions=filter_condition)
    filter_df['达人ID'] = filter_df['达人ID'].astype(str)
    print(filter_df)
    # 将筛选后的DataFrame转换为JSON格式
    result = filter_df.to_json(orient='records', force_ascii=False)
    
    # 返回JSON响应
    return jsonify({'filter_data': result,'ranking_field': '综合得分' if need_smart_sort else None})

def load_or_create_json(json_file_path):
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
    with open(json_file_path, 'r', encoding='utf-8') as file:  # 指定encoding='utf-8'
        return json.load(file)

def save_json(data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as file:  # 指定encoding='utf-8'
        json.dump(data, file, ensure_ascii=False, indent=4)

@app.route('/sendData',methods=['POST','GET'])
def sendData(): 
    csv_file_path = 'data/merged_data.csv'
    json_file_path = 'data/data.json'
    info=request.get_json().get('info')
    creator_id_list=request.get_json().get('creator_list')
    region=request.get_json().get('region')
    df = pd.read_csv(csv_file_path)
    df['达人ID'] = df['达人ID'].astype(str)
    file_path = "data/headers.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item["account"] == email_global: 
            cookies_str=item['details'][-1]['cookie']
            shop_id=item['seller_id']
            break
    print("开始发送信息给达人")
    print(cookies_str)
    startSend(mycookies=cookies_str,info=info,creator_list=creator_id_list,shop_id=shop_id,region=region)
    # df = pd.read_csv(csv_file_path)
    data = load_or_create_json(json_file_path)
    for creator_id in creator_id_list:
        row = df[df['达人ID'] == creator_id]
        nickname = str(row['达人用户名'].values[0]) if not row.empty else ""
        has_collaborated = str(row['是否有过合作'].values[0]) if not row.empty else "False"
        
        # 查找是否已有该ID
        existing_entry = next((item for item in data if item["id"] == creator_id), None)
        new_detail = {
            "has_collaborated": has_collaborated,
            "update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": info
        }
        if existing_entry:
            # ID已存在，仅插入到details列表中
            existing_entry["details"].append(new_detail)
        else:
            # ID不存在，追加一个新的结构
            data.append({
                "id": creator_id,
                "nickname": nickname,
                "details": [new_detail]
            })
    
    save_json(data, json_file_path)
    print(info,creator_id_list,region)
    return jsonify({'status':'success'})

@app.route('/loadSrc',methods=['POST','GET'])
def loadSrc():   
    json_file_path = 'data/headers.json'
    # 打开并读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        account_entry = next((item for item in data if item.get('account') == email_global), None)
    # 返回JSON数据
    print(data)
    print(email_global)
    print(account_entry)
    single=True
    return jsonify({"data":account_entry,"single":single})


@app.route('/checkCoolaborated',methods=['POST','GET'])
def checkCoolaborated():   
    json_file_path = 'data/data.json'
    file_path = "data/headers.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item["account"] == email_global: 
            cookies_str=item['details'][-1]['cookie']
            shop_id=item['seller_id']
            break
    region=request.get_json().get("region")
    check_json_data=startCheckCoolaborated(cookie=cookies_str,shop_id=shop_id,region=region,data_json_file_path=json_file_path)
    # with open()
    # 返回JSON数据
    single=True
    return jsonify({"data":check_json_data,"single":single})

@app.route('/')
def home():
    static_folder = resource_path('static')
    return send_from_directory(static_folder, 'login.html')

# 测试使用的
# @app.route('/')
# def home():
#     # return send_from_directory('static', 'relationMain.html')
#     return send_from_directory('static', 'login.html')

if __name__ == '__main__':
    
    thread_app = threading.Thread(target=app.run, kwargs={'port':5000})
    thread_app.start()
    webbrowser.open("http://127.0.0.1:5000/")

    thread_app.join()