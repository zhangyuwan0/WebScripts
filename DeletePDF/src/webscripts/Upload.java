package webscripts;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;



public class Upload {
	public static void main(String[] args) {
		// 文件地址
		String filePath = "C:\\Users\\Administrator\\Desktop\\未命名.jpg";
		// 上传url
		String uploadUrl = "http://rc.hanvon.com/file/single/upload";
		Upload upload = new Upload();
		// 打印返回结果
		System.out.println(upload.uploadFile(uploadUrl, filePath));
		
		
	}
	// 上传文件
	public String uploadFile(String urlStr,String filePath){
		String result = null;
			
		HttpURLConnection conn = null;
		// 分割线
		String BOUNDARY = "---------------------------"+ hashCode();
		// 回车换行符
		String CRLF = "\r\n";
		try{
			URL url = new URL(urlStr);
			// 开启连接
			conn = (HttpURLConnection) url.openConnection();
			// 设置超时等待
			conn.setConnectTimeout(5000);
			// 设置读取等待
			conn.setReadTimeout(30000);
			// 未知
			conn.setDoOutput(true);  
            conn.setDoInput(true);  
            // 禁用缓存
            conn.setUseCaches(false);
            // 使用Post请求
            conn.setRequestMethod("POST");  
            // 添加headers
            conn.setRequestProperty("Connection", "Keep-Alive");  
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.6)");  
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + BOUNDARY);  
            // 输出流
            OutputStream out = new DataOutputStream(conn.getOutputStream());
            
            // file
            File file = new File(filePath);
            // 如果文件不存在结束程序
            if(!file.exists()){
            	System.out.println("文件不存在!");
            }
            // Mime类型
            String contentType = "image/png";
            String fileName = file.getName();
            StringBuffer strBuff = new StringBuffer();
            // 添加分割头
            strBuff.append("--").append(BOUNDARY).append(CRLF);
            // 添加文件描述
            strBuff.append("Content-Disposition: form-data; name=\"")
            	   .append("file")
            	   .append("\";")
            	   .append(" filename=\"")
            	   .append(fileName)
            	   .append("\"")
            	   .append(CRLF);
            // 添加内容类型
            strBuff.append("Content-Type: ")
            	   .append(contentType)
            	   .append(CRLF+CRLF);
            // 写入输出流
            out.write(strBuff.toString().getBytes());
            
            DataInputStream in = new DataInputStream(new FileInputStream(file));
            int bytes= 0;
            byte[] bufferOut = new byte[1024];
            while((bytes = in.read(bufferOut))!= -1){
            	out.write(bufferOut, 0, bytes);
            }
            
            in.close();
            // 写入结尾
            byte[] endData = ("\r\n--" + BOUNDARY + "--\r\n").getBytes();  
            out.write(endData);  
            out.flush();  
            out.close();  
            // 读取返回数据    
            StringBuffer strBuf = new StringBuffer();  
            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));  
            String line = null; 
            while ((line = reader.readLine()) != null) {  
                strBuf.append(line).append("\n");  
            }  
            result = strBuf.toString();  
            reader.close();  
            reader = null;  
		}catch(Exception e){
			System.out.println("发送POST请求出错。" + urlStr);  
            e.printStackTrace();  
		}finally{
			if (conn != null) {  
                conn.disconnect();  
                conn = null;  
            }  
		}
		return result;
	}
	
}
