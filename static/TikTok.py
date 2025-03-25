'''
1. 使用登录函数 login
    - 如果登录不通过，可以重复调用

2. 登录通过后，调用验证函数 verify_by_email 进行验证
    - 如果验证不通过，可以重复调用 
    - 如果验证码超时，可以调用 send_captcha_by_email 重新获取验证码

3. 验证通过后，进入到homepage，可以调用 get_cookies_homepage, get_seller_id, get_headshot 获取对应数据

...

end. 调用 quit 函数结束使用
'''
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
from time import sleep, time
import gzip

# from LoggerManager import loggerManager
# loggerRegistrar = loggerManager(__file__)

'''
关于 LoggerManager
@QYQTexas: 
    LoggerManager 预留功能，自用日志，如果需要，可以使用，本次实现没有用到，如果无需使用，后续可以删除或无需理会.
'''
'''
@QYQTexas:
    类 TikTokShop_Loginer 内不处理任何报错，请在类外实现报错处理。
'''

# @loggerRegistrar     
class TikTokShop_Loginer:
    by_email = 'email'
    by_mobile = 'mobile'

    def __init__(
            self, 
            arg_path_driver_chrome, 
            arg_timeout = 30
            ):
        
        self.__path_config = './config_TikTokShop_Loginer.json' 
        self.__config = dict()
        self.__init_config()
        self.__update_config_hot()
        '''
        关于 config 
        @QYQTexas: 
            self.__path_config 配置文件的路径。
            self.__config 配置对象。
            self.__init_config() 初始化配置。
            self.__update_config_hot() 配置热更新，预留功能，暂未实现，后续如若需要，可以追加实现
        '''

        self.__timeout = arg_timeout

        self.__functionLoginBy = {
            TikTokShop_Loginer.by_email: self.__login_by_email,
            TikTokShop_Loginer.by_mobile: self.__login_by_mobile
        }

        self.__chrome_options = {
            'addr': self.__config['options_driver_chrome']['addr'], 
            'port': self.__config['options_driver_chrome']['port'], 
            'options': Options()
        }
        self.__chrome_options['options'].add_argument("--incognito")   
        self.__chrome_options['options'].add_argument("--headless")
        # 驱动器初始化
        self.__path_driver_chrome = arg_path_driver_chrome
        # self.__service_chrome = Service(executable_path=self.__path_driver_chrome)
        # self.__driver_chorme = webdriver.Chrome(service=self.__service_chrome,seleniumwire_options=self.__chrome_options)
        # self.__driver_chorme.get(self.__config['url_TikTokShop_login'])

    def close(self):
        self.__driver_chorme.close()

    def quit(self):
        self.__driver_chorme.quit()
        
    def __init_config(self):
        self.__config['options_driver_chrome'] = {
            'addr': '127.0.0.1', # 如果需要指定代理地址，请根据实际情况调整
            'port': 0, # 随机端口
        }

        self.__config['class_nameContainer'] = 'nameContainer-kJbXUk'
        # self.__config['class_nameContainer'] = 'nameContainer-ym20eH'

        self.__config['id_button_change_to_login_by_email'] = 'TikTok_Ads_SSO_Login_Email_Panel_Button'
        self.__config['id_input_account_by_email'] = 'TikTok_Ads_SSO_Login_Email_Input'
        self.__config['id_input_password_by_email'] = 'TikTok_Ads_SSO_Login_Pwd_Input'
        self.__config['id_button_login_by_email'] = 'TikTok_Ads_SSO_Login_Btn'
        self.__config['id_input_captcha_by_email'] = 'TikTok_Ads_SSO_Login_Code_Input'
        self.__config['id_button_verify_by_email'] = 'TikTok_Ads_SSO_Login_Code_Btn'
        self.__config['id_button_send_captcha_by_email'] = 'TikTok_Ads_SSO_Login_Code_Resend_Email_Btn'

        self.__config['url_TikTokShop_login'] = r'https://seller.tiktokglobalshop.com/account/login'
        self.__config['url_login_base_by_email'] = 'https://seller.tiktokglobalshop.com/passport/web/user/login/'
        self.__config['url_verify_base_by_email'] = 'https://seller.tiktokglobalshop.com/passport/web/email/code_login/'
        self.__config['url_include_seller_id'] = 'https://api16-normal-sg.tiktokglobalshop.com/api/v1/seller/tasks/notify'
        self.__config['url_homepage'] = 'https://seller.tiktokglobalshop.com/homepage'

        # self.__config['selector_src_headshot'] = r'#WB-GEC-nav-bar > div > div.flex.flex-row.justify-center.items-center.ml-auto > div.container-YJs71P > div > div > div.theme-m4b-avatar.theme-m4b-avatar-circle.avatar2-MZqy0z.mr-8 > span > img'
        self.__config['selector_src_headshot'] =".theme-m4b-avatar-image img"

        self.__config['selector_region_target'] = r'#WB-GEC-nav-bar > div:nth-child(2) > span > div.theme-arco-popover-content.theme-arco-popover-content-br > div > div > div > div > div > div > div.regionSelect-fZNqcy > div.theme-arco-radio-group.theme-arco-radio-size-small.theme-arco-radio-mode-outline.theme-arco-radio-group-direction-vertical.theme-m4b-radio-group.w-full.theme-m4b-radio-group-gap-size-small > label:nth-child(1) > span.theme-arco-radio-text > div > div > div'
        self.__config['key_seller_id'] = 'oec_seller_id'
        
        
        # self.__config['selector_region_base'] = r'#WB-GEC-nav-bar > div:nth-child(2) > span > div.theme-arco-popover-content.theme-arco-popover-content-br > div > div > div > div > div > div > div.regionSelect-fZNqcy > div.theme-arco-radio-group.theme-arco-radio-size-small.theme-arco-radio-mode-outline.theme-arco-radio-group-direction-vertical.theme-m4b-radio-group.w-full.theme-m4b-radio-group-gap-size-small > label'
        # self.__config['selector_region_target_template'] = './label/input[@value="{region}"]/following-sibling::span'
        # 修改为更简洁的CSS选择器
        self.__config['selector_region_base'] = 'div.theme-arco-radio-group'
        # self.__config['selector_region_base'] = 'div.regionSelect-fZNqcy div.theme-arco-radio-group'
        # 修改为直接通过input的value属性定位
        self.__config['selector_region_target_template'] = './/input[@value="{region}"]/following-sibling::span'
        with open(self.__path_config,'w',encoding='utf-8') as file:
            json.dump(self.__config, file, ensure_ascii=False, indent=4, sort_keys=True)

    def __update_config_hot(self):
        '''
        暂时保留, 万一TikTokShop的元素id改了, 或许会有热更新的需求?
        '''
        pass
    

    def set_homepage_url(self, new_url):
        self.__config['url_homepage'] = new_url
    # 登录
    def login(self, arg_account, arg_password, arg_by = by_email):
        '''
        # param:  
        - arg_account: 账号, 根据选择的登陆方式而定, 可以是邮箱也可以是手机号码.(暂时只支持邮箱)
        - arg_password: 密码  
        - arg_by: 选择登录方式, 有以下两种选择
            -- TikTokShop_Loginer.by_email: 邮箱登录
            -- TikTokShop_Loginer.by_mobile: 手机号码登录(仅保留, 暂未实现)

        # return:  
        1. by_email: 以dict形式返回，键值: 
            - is_timeout_send_request_login_by_email: 是否找到登录请求的标记.  
                - True: 表示寻找登录请求超时, 即在规定时间内没有找到登录请求, 未找到登录请求的原因是不可知的, 可能是发送请求阶段出现某些错误导致没有发送登录请求, 
                也有可能是发送请求的时间点超过了规定时间.  
                - False: 表示寻找登录请求没有超时, 即在规定时间内找到了登录请求.    

            - is_timeout_response_login_by_email: 登录请求是否超时.  
                - None: 当 is_timeout_send_request 为 True 时, 标记为 None.
                - True: 当 is_timeout_send_request 为 False 时, 登录请求超时.
                - False: 当 is_timeout_send_request 为 False 时, 登录请求没有超时.  

            - request_login_by_email: 登录时, 发送的post请求, 类型为 selenium wire 的 Request  

            - body_response_login_by_email: 如果响应了，这里面存储点击登录按钮后的状态信息：登录失败，登录成功，登录需要验证等等, 类型为dict.  
        
        2. by_mobile: ?  
            ?
        '''
        return self.__functionLoginBy[arg_by](arg_account, arg_password)
    
    def __get_element(self,arg_key):
        return WebDriverWait(
            driver=self.__driver_chorme,
            timeout=self.__timeout).until(EC.presence_of_element_located((By.ID,self.__config[arg_key])))
    
    # 通过 arg_by 获取元素，arg_value 是其对应的值，例如 button 的 id 是 'button_0', 则可以通过 find_element(By.ID, 'button_0') 获取相应元素
    # By 是selenium wire中类似枚举体的一个类，详情请查文档
    def find_element(self,arg_by, arg_value):
        return WebDriverWait(
            driver=self.__driver_chorme,
            timeout=self.__timeout).until(EC.presence_of_element_located((arg_by,arg_value)))

    # 邮箱方式登录
    def __login_by_email(self, arg_account, arg_password):

        # self.__service_chrome = Service(executable_path=self.__path_driver_chrome)
        self.__service_chrome = Service(ChromeDriverManager().install())
        self.__driver_chorme = webdriver.Chrome(service=self.__service_chrome,seleniumwire_options=self.__chrome_options)
        self.__driver_chorme.get(self.__config['url_TikTokShop_login'])
        # 获取元素
        self.__button_change_to_login_by_email = self.__get_element('id_button_change_to_login_by_email')
        self.__input_account_by_email = self.__get_element('id_input_account_by_email')
        self.__input_password_by_email = self.__get_element('id_input_password_by_email')
        self.__button_login_by_email = self.__get_element('id_button_login_by_email')
        
        # 如果当前登陆方式不是邮箱，则点击“切换邮箱登录”按钮
        if self.__button_change_to_login_by_email.get_attribute('class') == 'panel-item ':
            self.__button_change_to_login_by_email.click()

        # 输入邮箱
        self.__input_account_by_email.clear()
        self.__input_account_by_email.send_keys(arg_account)

        # 输入密码
        self.__input_password_by_email.clear()
        self.__input_password_by_email.send_keys(arg_password)

        # 清空请求列表，方便捕获登录请求，也避免重新登录时捕获到旧的登录请求
        print(len(self.__driver_chorme.requests))
        del self.__driver_chorme.requests
        print(len(self.__driver_chorme.requests))

        # 点击登录
        self.__button_login_by_email.click()

        # 捕获登录请求
        is_timeout_send_request_login_by_email, request_login_by_email = self.find_request_login_by_email()

        # 判断登录请求是否响应
        is_timeout_response_login_by_email = None
        body_response_login_by_email = None
        if not is_timeout_send_request_login_by_email:
            time_start = time()
            is_timeout_response_login_by_email = True
            while time() - time_start < self.__timeout:
                is_timeout_send_request_login_by_email, request_login_by_email = self.find_request_login_by_email()
                if request_login_by_email.response:
                    is_timeout_response_login_by_email = False
                    body_response_login_by_email = json.loads(gzip.decompress(request_login_by_email.response.body))
                    break
                sleep(1)
        
        return {
            'is_timeout_send_request_login_by_email': is_timeout_send_request_login_by_email,
            'is_timeout_response_login_by_email': is_timeout_response_login_by_email,
            'request_login_by_email': request_login_by_email,
            'body_response_login_by_email': body_response_login_by_email,
        }
    
    # 通过指定url前缀捕获请求体
    def find_request_by_startwith(self, arg_startwith):
        time_start = time()
        is_timeout = True
        request_target = None
        while time() - time_start < self.__timeout:
            for request in self.__driver_chorme.requests:
                if request.url.startswith(arg_startwith):
                    request_target = request
                    is_timeout = False
                    break
                
        return is_timeout, request_target
    
    # 捕获登录post请求
    def find_request_login_by_email(self):
        return self.find_request_by_startwith(self.__config['url_login_base_by_email'])
    
    # 捕获验证post请求
    def find_request_verify_by_email(self):
        return self.find_request_by_startwith(self.__config['url_verify_base_by_email'])

    # 登陆后的邮箱验证
    def verify_by_email(self, arg_captcha):
        '''
        # param:  
        - arg_captcha: 验证码

        # return:  
            以dict形式返回，键值: 
            - is_timeout_send_request_verify_by_email: 是否找到验证请求的标记.  
                - True: 表示寻找验证请求超时, 即在规定时间内没有找到验证请求, 未找到验证请求的原因是不可知的, 可能是发送请求阶段出现某些错误导致没有发送验证请求, 
                也有可能是发送请求的时间点超过了规定时间.  
                - False: 表示寻找验证请求没有超时, 即在规定时间内找到了验证请求.    

            - is_timeout_response_verify_by_email: 登录验证请求是否超时.  
                - None: 当 is_timeout_send_request 为 True 时, 标记为 None.
                - True: 当 is_timeout_send_request 为 False 时, 验证请求超时.
                - False: 当 is_timeout_send_request 为 False 时, 验证请求没有超时.  

            - request_verify_by_email: 验证时, 发送的post请求, 类型为 selenium wire 的 Request  

            - body_response_verify_by_email: 如果响应了，这里面存储点击验证按钮后的状态信息：验证失败，验证成功等等, 类型为dict.  
        '''

        # 获取元素
        self.__input_captcha_by_email = self.__get_element('id_input_captcha_by_email')
        self.__button_verify_by_email = self.__get_element('id_button_verify_by_email')

        # 输入验证码
        self.__input_captcha_by_email.clear()
        self.__input_captcha_by_email.send_keys(arg_captcha)

        # 点击验证
        del self.__driver_chorme.requests
        self.__button_verify_by_email.click()

        # 捕获验证请求
        is_timeout_send_request_verify_by_email, request_verify_by_email = self.find_request_verify_by_email()

        # 判断验证请求是否响应
        is_timeout_response_verify_by_email = None
        body_response_verify_by_email = None
        if not is_timeout_send_request_verify_by_email:
            time_start = time()
            is_timeout_response_verify_by_email = True
            while time() - time_start < self.__timeout:
                is_timeout_send_request_verify_by_email, request_verify_by_email = self.find_request_verify_by_email()
                if request_verify_by_email.response:
                    is_timeout_response_verify_by_email = False
                    body_response_verify_by_email = json.loads(gzip.decompress(request_verify_by_email.response.body))
                    break
                sleep(1)
        print('headers:',request_verify_by_email.headers)   # request_verify_by_email.headers.get('Cookie', 'No Cookie')
        return {
            'is_timeout_send_request_verify_by_email': is_timeout_send_request_verify_by_email,
            'is_timeout_response_verify_by_email': is_timeout_response_verify_by_email,
            'request_verify_by_email': request_verify_by_email,
            'body_response_verify_by_email': body_response_verify_by_email,
        }
        
    # 点击“发送验证码”，验证码将从tiktokshop发送给客户邮箱
    def send_captcha_by_email(self):
        try:
            self.__button_send_captcha_by_email = self.__get_element('id_button_send_captcha_by_email')
            self.__button_send_captcha_by_email.click()
            return True,None
        except Exception as e:
            return False,e
        
    # 手机号码登录 (未实现，预留)
    def __login_by_mobile(self, arg_account, arg_password):
        pass
    
    # 切换地区
    # def change_region_to_MY(self,region_code):
    # def change_region(self,region_code):
    #     del self.__driver_chorme.requests
    #     # 点击框
    #     nameContainer = self.find_element(arg_by=By.CLASS_NAME,arg_value=self.__config['class_nameContainer'])
    #     nameContainer.click()
    #     sleep(3)
    #     # 选择地区
    #     # region_target = self.find_element(arg_by=By.CSS_SELECTOR,arg_value=self.__config['selector_region_target'])
    #     # region_target.click()

    #     # 构建目标地区的XPath
    #     selector_region_target = self.__config['selector_region_target_template'].format(region=region_code)
        
    #     # 定位到包含所有可选地区的父元素
    #     region_select_base = self.find_element(By.CSS_SELECTOR, self.__config['selector_region_base'])
        
    #     # 查找并点击指定地区的选项
    #     try:
    #         target_region = region_select_base.find_element(By.XPATH, selector_region_target)
    #         target_region.click()
    #     except Exception as e:
    #         print(f"未能找到地区 {region_code}: {e}")

    def change_region(self, region_code):
        del self.__driver_chorme.requests
        # 点击地区选择框
        nameContainer = self.find_element(
            By.CLASS_NAME, 
            self.__config['class_nameContainer']
        )
        # nameContainer.click()
        self.__driver_chorme.execute_script("arguments[0].click();", nameContainer)
        
        # 显式等待地区弹窗加载完成
        WebDriverWait(self.__driver_chorme, self.__timeout).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                self.__config['selector_region_base']
            ))
        )
        
        # 构建目标地区的XPath（修正后的选择器）
        selector_region_target = self.__config['selector_region_target_template'].format(
            region=region_code
        )
        
        # 定位到包含所有地区选项的父元素
        region_select_base = self.find_element(
            By.CSS_SELECTOR, 
            self.__config['selector_region_base']
        )
        
        try:
            # 使用更精确的XPath定位目标地区
            target_region = region_select_base.find_element(
                By.XPATH, 
                f'.//input[@value="{region_code}"]/following-sibling::span'
            )
            self.__driver_chorme.execute_script("arguments[0].click();", target_region)
        except Exception as e:
            print(f"未能找到地区 {region_code}: {e}")
        

    # 刷新页面
    def refresh(self):
        self.__driver_chorme.refresh()

    # https://seller.tiktokglobalshop.com/homepage
    def get_cookies_homepage(self):
        '''
        # return  
        is_timeout, cookie

        - is_timeout: 
            -- True: 查找请求超时，没有找到homepage请求。后续可以通过函数 refresh 刷新页面，再调用一次 get_cookies_homepage 
            -- False: 找到 homepage 请求
        
        - cookie: 
            -- None: 请求超时，cookie为 None
            -- No Cookie: 找到 homepage 请求，但从其请求头中没有找到 Cookie
            -- Cookie 实际值
        '''
        is_timeout, request_homepage = self.find_request_by_startwith(self.__config['url_homepage'])
        cookie = None
        if not is_timeout:
            cookie = request_homepage.headers.get('Cookie','No Cookie')
            # print('*'*100)
            # print(request_homepage.headers)
            # print('*'*100)
            # print(request_homepage.response.headers)
            # print('*'*100)
        return is_timeout, cookie

    # https://api16-normal-sg.tiktokglobalshop.com/api/v1
    def get_seller_id(self):
        '''
        # return  
        is_timeout, cookie

        - is_timeout: 
            -- True: 查找请求超时，没有找到url_include_seller_id请求。后续可以通过函数 refresh 刷新页面，再调用一次 get_seller_id 
            -- False: 找到 url_include_seller_id 请求
        
        - seller_id: 
            -- None: 请求超时，seller_id为 None
            -- No seller_id: 找到 url_include_seller_id 请求，但从其请求头中没有找到 seller_id
            -- seller_id 实际值
        '''
        is_timeout, request_include_seller_id = self.find_request_by_startwith(self.__config['url_include_seller_id'])
        seller_id = None
        if not is_timeout:
            seller_id = request_include_seller_id.params.get(self.__config['key_seller_id'],'No seller_id')
        return is_timeout, seller_id
    
    '''
    #WB-GEC-nav-bar > div > div.flex.flex-row.justify-center.items-center.ml-auto > div.container-YJs71P > div > div > div.theme-m4b-avatar.theme-m4b-avatar-circle.avatar2-MZqy0z.mr-8 > span > img
    '''
    def get_headshot(self):
        src_headshot = self.find_element(By.CSS_SELECTOR,self.__config['selector_src_headshot'])
        self.src_headshot = src_headshot.get_attribute('src')
        return self.src_headshot