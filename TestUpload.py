# from urllib import request, parse
# # 媒体类型
# import mimetypes
# import os
# # id生成器
# import uuid
import requests

"""
	结果: PostMan 不添加header即可post成功
		  使用requests库同样的方式post 显示HTTP 500 错误
		  使用urllib库 拼接data方式post 显示HTTP 400 错误
	疑问: 为什么传递requests 多传递hm_xxx cookie后就能post成功
		  ulrlib如何将二进制file文件 拼接到字符串中
		  Post添加了什么参数 ？？？

"""

filePath = r"C:\Users\Administrator\Desktop\测试.png"
uploadURL = r"http://rc.hanvon.com/file/single/upload"
url = r"http://rc.hanvon.com/rc/rapid"

# def uploadWithUrllib(url,filePath):
# 	with request.urlopen(url=uploadURL,data=getdata("file",filePath).encode("utf-8")) as page:
# 		page.read().decode("utf-8")

def upload(url,filePath):
	cookies = {
		"JSESSIONID":"DFC2729024CB6D75C4FAC86FB60E7B14",
		"Hm_lvt_4c8be966697649d1191e0cfabcb9ea64":"1474852818,1474879212,1474951731,1475030808",
		"Hm_lpvt_4c8be966697649d1191e0cfabcb9ea64":"1475032556"
	}

	files = {"file": open(filePath, "rb")}
	r = requests.post(url=uploadURL,files=files,cookies=cookies)
	print(r.text)

upload(url,filePath)


# def getdata(fileFieldName,filePath):
# 	# 随即生成boundary
# 	boundary = "--------sgc" + uuid.uuid4().hex;
# 	# 获取文件名
# 	fileName = os.path.basename(filePath)
# 	# 解码为utf-8
# 	# fileName = fileName.encode("utf-8")
# 	# 获取文件类型
# 	fileType = mimetypes.guess_type(fileName)[0]
# 	# 如果没有该类型 则按文本类型处理
# 	if fileType==None:
# 		fileType = "text/plain; charset=utf-8"

# 	print(fileType)
# 	print(fileName)
# 	# 读取文件
# 	fileData = open(filePath, "rb").read()
# 	CRLF = "\r\n"
# 	# 拼接body
# 	body = ""
# 	body += "--" + boundary + CRLF;
# 	body += 'Content-Disposition: form-data; name="' + fileFieldName +'"; filename="' + fileName + '"'
# 	body += 'Content-Type:' + fileType + CRLF
# 	body += CRLF;
# 	body += str(fileData) + CRLF
# 	body += "--" + boundary + "--" + CRLF
# 	print("body size:{0}".format(len(body)))
# 	return body

# uploadWithUrllib(url,filePath)
