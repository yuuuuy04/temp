import requests
from datetime import datetime
import json
from static.resolve import *

def startCheckCoolaborated(cookie,shop_id,region,data_json_file_path):
    headers = {
    'path': '/api/v1/oec/affiliate/creator/marketplace/find?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m5z3kj3u_5IrLVhnI_rbyW_4PzT_AW9a_WyqHSuXALryM&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F131.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id=7495839077177002076&shop_region=MY&msToken=mncDPr3yLt3R-gcrA8RiLp-_O7HxcWEhQMUaEeHB1Qlrkv3THOLRZSma-LokVxumueiLq7AQkWYdCmd0DGRIthC4y2ugtmSOWeAvSGQr0_ODs1lxvDW-_dDsPAz1e2MhJwqMgxil&X-Bogus=DFSzswVYbt-0OEactpj1hcTQh4tl&_signature=_02B4Z6wo00001t6geJQAAIDDAfuL2vnCxqLeoHwAANAt42',
    'content-type': 'application/json',
    'cookie': cookie,
    'referer': 'https://affiliate.tiktokglobalshop.com/connection/creator?shop_region=MY',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0'
}
    details_url=f"https://affiliate.tiktokglobalshop.com/api/v1/oec/affiliate/creator/marketplace/profile?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m7g9hi5s_6ovVNPzE_w6yB_4u9G_9FOF_EEWcpRs7BnaX&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F133.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id={shop_id}&shop_region={region}&msToken=A8_Dkys1oqImNwD0QD4I4M1g_UxMsEtv1sZpeE1RhZbt2scejKNCcqOxYCwxlvpjB6B6R-zPPopH5rqmM3wWm_GHcROKJbz6V3RLo6hJ3rimBAnt9p5VIraxTw7N-2Q1GrQji9Lq&X-Bogus=DFSzswVuw9zCkQ4ktDy3vcTQh4CI&_signature=_02B4Z6wo00001TKqungAAIDA7fFJNl0tIy0yqr7AACsW47"
    # 打开并读取JSON文件
    with open(data_json_file_path, 'r', encoding='utf-8') as file:
        creator_data = json.load(file)
    # print(data)
    # creator_list=[]
    for creator_index in range(len(creator_data)):
        while True:
            data = {
                'creator_oec_id': str(creator_data[creator_index]["id"]),  # 将达人ID转换为字符串
                'profile_types': [1]  
            }
            json_data = json.dumps(data)
            # 发起POST请求
            response = requests.post(url=details_url, headers=headers, data=json_data,timeout=30)
            if len(response.content) != 0 and response.json()['code'] == 0:
                response_data = response.json()  # 获取 JSON 数据
                has_collaborated=response_data['creator_profile']['has_collaborated']['value']
                if "check" in creator_data[creator_index]:
                    print(f"{str(creator_data[creator_index]['id'])}--exist check")
                    creator_data[creator_index]["check"].append({"update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"has_collaborated":str(has_collaborated)})
                    break
                else:
                    creator_data[creator_index]["check"]=[{"update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"has_collaborated":str(has_collaborated)}] 
                    break
            else:
                print(f"API 请求失败，状态码: {response.status_code} - {creator_data[creator_index]['id']}")
                startResolve(mycookies=cookie,region=region)
    # 使用with语句打开文件，这确保了文件会在with语句块结束时正确关闭
    with open(data_json_file_path, 'w', encoding='utf-8') as f:
        # 使用json.dump将数据写入文件
        json.dump(creator_data, f, ensure_ascii=False, indent=4)

    print(f"数据已保存到 {data_json_file_path}")
    return creator_data
        

if __name__=="__main__":
    cookies_str='_m4b_theme_=new; i18next=zh-CN; s_v_web_id=verify_m7lfabd3_Jl8J2iPR_y0L8_4PMk_Ap2n_JnCRU5Zr1Bmr; passport_csrf_token=0f6e52fed51e4a3c35e80623888646f0; passport_csrf_token_default=0f6e52fed51e4a3c35e80623888646f0; d_ticket=a43e0c2efa8c25a61db8b25e75ef2d56e64a0; msToken=r1H9zW_qhwaTEn8643Pa3BpHjaxgOOxVP09Fuaam7uhSUJkkgDvZ8TZg7DRFK-RGoSgW-6Han2LT960cCDwy6DL-djy5TdDWvgrSNjjFF6nM; uid_tt=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; uid_tt_ss=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; sid_tt=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid_ss=e1cf181f85ecbd62cd8160a9c9bf1c55; msToken=txPiQ0QirmErpftWIkSaJqSEr6QBNCbXuzbZX_aGy3Gx5sm3_UmKqOIHMMKYYPJjdjQ_q04QPk8pFb3elTu6anhoco_nftfUGSUuIQndmLB2; ttwid=1%7CM2-5BOIM_DRiSUPmadgptgUfqntT-cBGso-4J7ylYko%7C1740544642%7C96f4f8c36572c20a72a9449d6145d9d8da0973c927390a753e16ec33770e4455; sid_guard=e1cf181f85ecbd62cd8160a9c9bf1c55%7C1740544643%7C863992%7CSat%2C+08-Mar-2025+04%3A37%3A15+GMT; sid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; ssid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; lang_type=zh-CN; passport_fe_beating_status=false'
    headers = {
    'path': '/api/v1/oec/affiliate/creator/marketplace/find?user_language=zh-CN&aid=6556&app_name=i18n_ecom_alliance&device_id=0&fp=verify_m5z3kj3u_5IrLVhnI_rbyW_4PzT_AW9a_WyqHSuXALryM&device_platform=web&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F131.0.0.0+Safari%2F537.36&browser_online=true&timezone_name=Asia%2FShanghai&oec_seller_id=7495839077177002076&shop_region=MY&msToken=mncDPr3yLt3R-gcrA8RiLp-_O7HxcWEhQMUaEeHB1Qlrkv3THOLRZSma-LokVxumueiLq7AQkWYdCmd0DGRIthC4y2ugtmSOWeAvSGQr0_ODs1lxvDW-_dDsPAz1e2MhJwqMgxil&X-Bogus=DFSzswVYbt-0OEactpj1hcTQh4tl&_signature=_02B4Z6wo00001t6geJQAAIDDAfuL2vnCxqLeoHwAANAt42',
    'content-type': 'application/json',
    'cookie': cookies_str,
    'referer': 'https://affiliate.tiktokglobalshop.com/connection/creator?shop_region=MY',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0'
}
    region='MY'
    shop_id="7495839077177002076"
    json_path=r'D:\python experiment\爬虫\代码\智能建联\workapp\static\data.json'
    print(startCheckCoolaborated(cookie=cookies_str,shop_id=shop_id,region=region,data_json_file_path=json_path))