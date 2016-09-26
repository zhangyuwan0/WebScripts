import requests
import json
import os
from selenium import webdriver

# 汉王OCR在线识别 URL
targetURL = r"http://rc.hanvon.com/rc/rapid"
# 汉王上传文件URL
uploadURL = r"http://rc.hanvon.com/file/single/upload"
recognitionURL = r"http://rc.hanvon.com/file/rapid/recog"

# 通过get的方式获取cookie
def getCookieWithGET(url):
    # 使用 phantomJs(无前台的浏览器)作为驱动
    driver = webdriver.PhantomJS(executable_path= r"D:\program Files\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    # get 汉王URL
    driver.get(targetURL)
    # 设置等待 使得javascript脚本得以执行完毕
    driver.implicitly_wait(1)
    # 获取cookie list
    cookies = driver.get_cookies()
    # 关闭驱动
    driver.close()
    return cookies

# 将cookie 换换成字典
def convertCookie(list_cookies):
    cookies = {}
    for s in list_cookies:
        cookies[s["name"]] = s["value"]

# 上传文件到汉王
def uploadFile(url,filePath,cookies):
    target_file = open(filePath, "rb")
    file ={"file": target_file}
    # 之前报http 400错误
    #　解决过程：
    """ 1.查看 Http 400错误的含义
        2.查看description内容并搜索相关问题解决方案
        3.发现是参数post参数与服务器参数不对称的问题
        4.查看FileService.singleUploadFile函数中的XHR代码段
        发现参数名不是"uploadFile"而是"file" 
        5.改变参数重试,问题解决！"""
    r = requests.post(url=url, files=file, cookies=cookies)
    print(r.text)
    # 关闭文件流
    target_file.close()
    # 转换返回的json
    return json.loads(r.text)

# 请求API识别该图片
def recognitionPicture(url, result_dict, cookies, docType = "txt"):
    """
        url: 请求识别的url
        result_dict: 上传文件回传参数字典
        cookies: page cookie
        docType: 识别后返回文件类型
            txt - 文本文件
            pdf - 可复制的PDF文档
            rtf - mircosoft word 文档
            xls - microsoft excel 文档
    """
    # check 文件是否上传成功
    if result_dict["result"] != "success":
        print("recognitionPicture method: the result was" + result_dict["result"])
        raise ValueError
        
    headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type":"application/json;charset=utf-8",
        "Host":"rc.hanvon.com",
        "Referer":"http://rc.hanvon.com/rc/rapid",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    }
    # 填写文件请求
    """ 之前BUG -> HTTP 415 
        问题原因：post参数填写错误,没有将json_data填入到data
        解决方法: 将填写在json参数的json_data改为填入到data参数中
    """
    json_content = {"fileType":docType,"fid":result_dict["inFid"],"fileName":result_dict["fileName"]}
    json_data = json.dumps(json_content)
    # psot 识别请求
    r = requests.post(url, headers=headers, data=json_data, cookies=cookies)
    print(r.text)
    return json.loads(r.text)
    # 将返回结果转换为json

# 下载识别后文件
def downloadResult(downloadFolder,result_dict, docType="txt"):
    downloadURL = r"http://rc.hanvon.com/file/download?outFid={0}&flag=rapidRecog".format(result_dict["fid"])
    print(downloadURL)
    local_filename = result_dict["fileName"].split(".")[0] + "." + docType
    r = requests.get(downloadURL) # here we need to set stream = True parameter  
    print(r.text)
    if not os.path.exists(downloadFolder):
        os.makedirs(downloadFolder)
    with open(downloadFolder + local_filename, 'wb') as f:
        # 之前错误 -> GBK 不能解码 r.text 
        # 解决方案 -> 直接写入二进制 然后以txt文件读取
        f.write(r.content)
    return local_filename 

# 识别文件
def convertPDFpicture(filePath, convertedFolder="results\\", docType="txt"):
    # 第一步将PDF按页分解成多个图片
    
    # 第二步循环识别文件 并拼接到结果文档
#     for xx in xx :
    # 第一步：获取cookie 以便之后的操作
    cookies = convertCookie(getCookieWithGET(targetURL))
    # 第二步：向汉王服务器上传图片
    result_dict = uploadFile(uploadURL, filePath, cookies)
    # 第三步: 请求API识别该图片
    result = recognitionPicture(recognitionURL,result_dict,cookies,docType)
    # 第四步：下载文件
    downloadResult(convertedFolder, result, docType)

convertPDFpicture(r"C:\Users\Administrator\Desktop\12.jpg")