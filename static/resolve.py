import time
import tkinter as tk
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import http.cookies
import requests
import json

def check_need_verify(arg_creator_oec_id,arg_url,arg_header):
    data = {
        'creator_oec_id': str(arg_creator_oec_id),  # 将达人ID转换为字符串
        'profile_types': [2]  # 可根据需要更改 profile_types 参数
    }
    json_data = json.dumps(data)
    response = requests.post(url=arg_url, headers=arg_header, data=json_data,timeout=30)
    if len(response.content) != 0 and response.json()['code'] == 0:
        return False
    else:
        return True

def startResolve(mycookies, region, arg_creator_oec_id,arg_url,arg_header,arg_path_chromedriver):
    print("debug: startResolve")
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    url = f"https://affiliate.tiktokglobalshop.com/connection/creator?enter_from=seller_center_entry&shop_region={region}"
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument(f"window-size={screen_width},{screen_height}")
    chrome_options.add_argument('--disable-webrtc')
    service = Service(ChromeDriverManager().install())
    # service = ChromeService(executable_path=arg_path_chromedriver)  # 替换为chromedriver路径
    driver = webdriver.Chrome(options=chrome_options, service=service)
    isSucceed = False
    try:
        print("debug: startResolve -> get")
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        # 添加cookies
        cookies_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in mycookies.split("; ")}
        for name, value in cookies_dict.items():
            driver.add_cookie({
                'name': name,
                'value': value,
                'domain': '.tiktokglobalshop.com',
                'path': '/',
            })
        # 刷新页面使新cookies生效
        driver.refresh()
        time.sleep(3)  # 等待页面加载完成
        driver.get(url=url)
        
        # 定位并使用JavaScript点击指定元素
        element_locator = (By.CSS_SELECTOR, "#content-container .arco-table-body tbody tr:nth-child(1) td .arco-table-cell")
        try:
            target_element = wait.until(EC.presence_of_element_located(element_locator))
            driver.execute_script("arguments[0].click();", target_element)
            
            # time.sleep(30)
            while check_need_verify(arg_creator_oec_id,arg_url,arg_header):
                time.sleep(15)
            isSucceed = True
        
        except Exception as e:
            print(f"Failed to click the target element using JavaScript: {e}")

    except Exception as e:
        print(e)
    finally:
        # 关闭浏览器
        driver.quit()
        return isSucceed
    
if __name__ == '__main__':
    cookies_str="_m4b_theme_=new; i18next=zh-CN; s_v_web_id=verify_m7lfabd3_Jl8J2iPR_y0L8_4PMk_Ap2n_JnCRU5Zr1Bmr; passport_csrf_token=0f6e52fed51e4a3c35e80623888646f0; passport_csrf_token_default=0f6e52fed51e4a3c35e80623888646f0; d_ticket=a43e0c2efa8c25a61db8b25e75ef2d56e64a0; msToken=r1H9zW_qhwaTEn8643Pa3BpHjaxgOOxVP09Fuaam7uhSUJkkgDvZ8TZg7DRFK-RGoSgW-6Han2LT960cCDwy6DL-djy5TdDWvgrSNjjFF6nM; uid_tt=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; uid_tt_ss=975b57e3bd259cb08dacb79f08d041a7eb28b859550287c1ec0eab0b5648eea2; sid_tt=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid=e1cf181f85ecbd62cd8160a9c9bf1c55; sessionid_ss=e1cf181f85ecbd62cd8160a9c9bf1c55; msToken=txPiQ0QirmErpftWIkSaJqSEr6QBNCbXuzbZX_aGy3Gx5sm3_UmKqOIHMMKYYPJjdjQ_q04QPk8pFb3elTu6anhoco_nftfUGSUuIQndmLB2; ttwid=1%7CM2-5BOIM_DRiSUPmadgptgUfqntT-cBGso-4J7ylYko%7C1740544642%7C96f4f8c36572c20a72a9449d6145d9d8da0973c927390a753e16ec33770e4455; sid_guard=e1cf181f85ecbd62cd8160a9c9bf1c55%7C1740544643%7C863992%7CSat%2C+08-Mar-2025+04%3A37%3A15+GMT; sid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; ssid_ucp_v1=1.0.0-KDM3MTgwYjVjOTgzMjI5N2Y0YTIxZTEzOWJkZWJiZGI2ZjA1YWM3NDkKGAiRiJbund7gsGcQg7X6vQYYnDM4AUDrBxADGgJteSIgZTFjZjE4MWY4NWVjYmQ2MmNkODE2MGE5YzliZjFjNTU; lang_type=zh-CN; passport_fe_beating_status=false"
    region='MY'
    startResolve(mycookies=cookies_str,region=region)