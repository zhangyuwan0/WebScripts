import requests
# 媒体类型
import mimetypes
import json
import os


# 汉王OCR在线识别 URL
targetURL = r"http://rc.hanvon.com/rc/rapid"
# 汉王上传文件URL
uploadURL = r"http://rc.hanvon.com/file/single/upload"
recognitionURL = r"http://rc.hanvon.com/file/rapid/recog"
# 允许上传的文件类型
uploadType = ["jpg", "png", "tif", "bmp"]
# 固定随即分割串
boundary = "---------------------------273761636013558"


def getFileBytes(fileFieldName, filePath):
    file = open(filePath, "rb")
    # 1.获取文件名
    fileName = os.path.basename(filePath)
    # 2.猜测媒体类型
    fileType = mimetypes.guess_type(fileName)[0]
    # 3.判断该类型是否已经被识别
    #   如果未被识别 则赋值为默认媒体类型
    if not fileType:
        fileType = "text/plain; charset=utf-8"
    # 拼接开头
    CRLF = "\r\n"
    # 拼接body
    head = ""
    head += "--" + boundary + CRLF
    head += 'Content-Disposition: form-data; name="' + \
        fileFieldName + '"; filename="' + fileName + '"' + CRLF
    head += 'Content-Type: ' + fileType + CRLF
    head += CRLF
    tail = CRLF + "--" + boundary + "--" + CRLF
    return head.encode("utf-8") + file.read() + tail.encode("utf-8")


def getdata(boundary, fileFieldName, filePath):
    # 获取文件名
    fileName = os.path.basename(filePath)
    # 获取文件类型
    fileType = mimetypes.guess_type(fileName)[0]
    # 如果没有该类型 则按文本类型处理
    if fileType == None:
        fileType = "text/plain; charset=utf-8"
    # 读取文件
    fileData = open(filePath, "rb").read()
    CRLF = "\r\n"
    # 拼接body
    head = ""
    head += "--" + boundary + CRLF
    head += 'Content-Disposition: form-data; name="' + \
        fileFieldName + '"; filename="' + fileName + '"' + CRLF
    head += 'Content-Type: ' + fileType + CRLF
    head += CRLF
    body = head.encode("utf-8") + fileData
    tail = CRLF + "--" + boundary + "--" + CRLF
    body += tail.encode("utf-8")
    print(head, end="这是data")
    print(tail)
    return body


def uploadFile(url, filePath):
    # 上传文件到汉王
    try:
        # 判断文件是否是jpg,png,tif,bmp中的一种
        fileName = os.path.basename(filePath)
        #　如果该文件不在允许上传的文件类型内
        """
            BUG--
            大意的把split的()写成了[]
            导致报出错误
        """
        if fileName.split(".")[-1] not in uploadType:
            # 抛出文件类型错误异常
            raise ValueError("The upload file type must in jpg,png,tif,bmp!")
    except Exception as e:
        print(e)
        #　文件无扩展名
        raise ValueError("this file have not suffix!")
    headers = {
        "Content-Type": "multipart/form-data; boundary=" + boundary
    }
    file = {"file": getFileBytes("file", filePath)}
    r = requests.post(url, files=file, headers=headers)
    result = r.text
    try:
        result = json.loads(result)
        # check 文件是否上传成功
        if result["inFid"] == None:
            # 不存在inFid键 文件不能被识别
            raise ValueError("File can not be identified.")
    except Exception as e:
        # 抛出HTTP 错误代码
        raise e
    # 转换成 返回json
    return result

# 请求API识别该图片


def recognitionPicture(url, result_dict, docType="txt"):
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
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Content-Type": "application/json;charset=utf-8",
        "Host": "rc.hanvon.com",
        "Referer": "http://rc.hanvon.com/rc/rapid",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"
    }
    # 填写文件请求
    """ 
        之前BUG -> HTTP 415
        问题原因：post参数填写错误,没有将json_data填入到data
        解决方法: 将填写在json参数的json_data改为填入到data参数中
    """
    json_content = {"fileType": docType, "fid": result_dict[
        "inFid"], "fileName": result_dict["fileName"]}
    json_data = json.dumps(json_content)
    # psot 识别请求
    r = requests.post(url, headers=headers, data=json_data)
    result = json.loads(r.text)
    return json.loads(r.text)
    # 将返回结果转换为json

# 下载识别后文件


def downloadResult(downloadFolder, fileName, result_dict, docType="txt"):
    downloadURL = r"http://rc.hanvon.com/file/download?outFid={0}&flag=rapidRecog".format(
        result_dict["fid"])
    print(downloadURL)
    if not fileName:
        fileName = result_dict["fileName"].split(".")[
            0].encode("utf-8").decode("utf-8") + "." + docType
    else:
        fileName = fileName.split(".")[0] + "." + docType
    # here we need to set stream = True parameter
    r = requests.get(downloadURL)
    if not os.path.exists(downloadFolder):
        os.makedirs(downloadFolder)
    with open(downloadFolder + fileName, 'wb') as f:
        # 之前错误 -> GBK 不能解码 r.text
        # 解决方案 -> 直接写入二进制 然后以txt文件读取
        f.write(r.content)
    return downloadFolder + fileName

# 文件未找到异常


class FileNotFound(Exception):
    """docstring for FileNotFound"""

    def __init__(self, arg):
        self.arg = arg

# 识别文件


def convertPDFpicture(filePath, reusltFolder="results\\", docType="txt"):
    # 判断文件路径是否存在
    if not os.path.exists(filePath):
        raise FileNotFound("this path is not exists!")
    # 暂存fileName 用于之后保存文件
    fileName = os.path.basename(filePath)
    # 第1步：向汉王服务器上传图片
    result_dict = uploadFile(uploadURL, filePath)
    # 第2步: 请求API识别该图片
    result = recognitionPicture(recognitionURL, result_dict, docType)
    # 第3步：下载文件
    downloadResult(reusltFolder, fileName, result, docType)

if __name__ == '__main__':
    convertPDFpicture(r"C:\Users\Administrator\Desktop\未命名.jpg")
