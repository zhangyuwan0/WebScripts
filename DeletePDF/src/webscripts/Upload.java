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
		// �ļ���ַ
		String filePath = "C:\\Users\\Administrator\\Desktop\\δ����.jpg";
		// �ϴ�url
		String uploadUrl = "http://rc.hanvon.com/file/single/upload";
		Upload upload = new Upload();
		// ��ӡ���ؽ��
		System.out.println(upload.uploadFile(uploadUrl, filePath));
		
		
	}
	// �ϴ��ļ�
	public String uploadFile(String urlStr,String filePath){
		String result = null;
			
		HttpURLConnection conn = null;
		// �ָ���
		String BOUNDARY = "---------------------------"+ hashCode();
		// �س����з�
		String CRLF = "\r\n";
		try{
			URL url = new URL(urlStr);
			// ��������
			conn = (HttpURLConnection) url.openConnection();
			// ���ó�ʱ�ȴ�
			conn.setConnectTimeout(5000);
			// ���ö�ȡ�ȴ�
			conn.setReadTimeout(30000);
			// δ֪
			conn.setDoOutput(true);  
            conn.setDoInput(true);  
            // ���û���
            conn.setUseCaches(false);
            // ʹ��Post����
            conn.setRequestMethod("POST");  
            // ���headers
            conn.setRequestProperty("Connection", "Keep-Alive");  
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.6)");  
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + BOUNDARY);  
            // �����
            OutputStream out = new DataOutputStream(conn.getOutputStream());
            
            // file
            File file = new File(filePath);
            // ����ļ������ڽ�������
            if(!file.exists()){
            	System.out.println("�ļ�������!");
            }
            // Mime����
            String contentType = "image/png";
            String fileName = file.getName();
            StringBuffer strBuff = new StringBuffer();
            // ��ӷָ�ͷ
            strBuff.append("--").append(BOUNDARY).append(CRLF);
            // ����ļ�����
            strBuff.append("Content-Disposition: form-data; name=\"")
            	   .append("file")
            	   .append("\";")
            	   .append(" filename=\"")
            	   .append(fileName)
            	   .append("\"")
            	   .append(CRLF);
            // �����������
            strBuff.append("Content-Type: ")
            	   .append(contentType)
            	   .append(CRLF+CRLF);
            // д�������
            out.write(strBuff.toString().getBytes());
            
            DataInputStream in = new DataInputStream(new FileInputStream(file));
            int bytes= 0;
            byte[] bufferOut = new byte[1024];
            while((bytes = in.read(bufferOut))!= -1){
            	out.write(bufferOut, 0, bytes);
            }
            
            in.close();
            // д���β
            byte[] endData = ("\r\n--" + BOUNDARY + "--\r\n").getBytes();  
            out.write(endData);  
            out.flush();  
            out.close();  
            // ��ȡ��������    
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
			System.out.println("����POST�������" + urlStr);  
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
