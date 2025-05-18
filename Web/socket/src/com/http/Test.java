package com.http;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			ServerSocket ss = new ServerSocket(9999);
			while(true) {
				System.out.println("waiting......");
				Socket socket = ss.accept();
				Thread t = new Thread(new HttpServer(socket));
				t.start();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
