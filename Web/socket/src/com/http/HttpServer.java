package com.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;

public class HttpServer implements Runnable {
	private Socket socket;
	
	public HttpServer(Socket socket) {
		super();
		this.socket = socket;
	}

	@Override
	public void run() {
		// TODO Auto-generated method stub
		try {
			InputStream is = this.socket.getInputStream();
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			while(reader.ready()) {
				String str = reader.readLine();
				System.out.println(str);
			}
			StringBuffer res = new StringBuffer();
			res.append("http1.1 200 ok").append("\r\n")
			.append("Date: Wed, 07 Jul 2025 02:06:10 GMT").append("\r\n")
			.append("Server: Apache-Coyote/1.1").append("\r\n")
			.append("Content-Type:text/html; charset=UTF-8").append("\r\n")
			.append("\r\n")
			.append("<!DOCTYPE html>")
			.append("<html>")
			.append("<head>")
			.append("<meta charset=\"utf-8\">")
			.append("<title></title>")
			.append("</head>")
			.append("<body>")
			.append("<h1>hello</h1>")
			.append("</body>")
			.append("</html>");
			
			OutputStream os = socket.getOutputStream();
			os.write(res.toString().getBytes());
			os.flush();
			is.close();
			os.close();
			socket.close();
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
