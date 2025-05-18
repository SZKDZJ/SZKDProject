package com.test;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			ServerSocket server = new ServerSocket(9999);
			while(true) {
				//监听端口，无访问时阻塞，有访问返回客户端的socket对象
				System.out.println("服务端等待请求……");
				Socket socket = server.accept();
				InputStream is = socket.getInputStream();//得到输入流
				OutputStream os = socket.getOutputStream();//得到输出流
				byte[] b = new byte[100];
				b[0] = (byte)is.read();
				for(int i=1; i<is.available(); i++) {
					b[i] = (byte)is.read();
				}
				System.out.println("服务端接收到："+new String(b));
				os.write("byebye".getBytes());
				os.flush();
				is.close();
				os.close();

			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
