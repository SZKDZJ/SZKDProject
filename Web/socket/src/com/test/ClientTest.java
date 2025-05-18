package com.test;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class ClientTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			Socket socket = new Socket("127.0.0.1",9999);
			InputStream is = socket.getInputStream();//输入流
			OutputStream os = socket.getOutputStream();//输出流
			//发送请求到服务端
			os.write("hello".getBytes());//参数byte[]
			os.flush();//立刻写入
			
			byte[] b = new byte[100];
			b[0] = (byte)is.read();
			for(int i=1; i<100; i++) {
				b[i] = (byte)is.read();
			}
			System.out.println("客户端接收到："+new String(b));
			os.close();
			is.close();
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
