from urllib import request
# 媒体类型
import mimetypes
import os
# id生成器
import uuid

"""
	结果: PostMan 不添加header即可post成功
		  使用requests库同样的方式post 显示HTTP 500 错误
		  使用urllib库 拼接data方式post 显示HTTP 400 错误
	疑问: 为什么传递requests 多传递hm_xxx cookie后就能post成功
		  ulrlib如何将二进制file文件 拼接到字符串中
		  Post添加了什么参数 ？？？

"""

filePath = r"C:\Users\Administrator\Desktop\未命名.jpg"
uploadURL = r"http://rc.hanvon.com/file/single/upload"
url = r"http://rc.hanvon.com/rc/rapid"

boundary = "---------------------------273761636013558"


def uploadWithUrllib(url, filePath):
    req = request.Request(url, getdata("file", filePath))
    # 之前BUG 不添加 这一个行 便不可以
    req.add_header('Content-Type', "multipart/form-data; boundary=" + boundary)
    response = request.urlopen(req)
    print(response.read().decode("utf-8"))


def getdata(fileFieldName, filePath):
    # 随即生成boundary

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

uploadWithUrllib(uploadURL, filePath)
