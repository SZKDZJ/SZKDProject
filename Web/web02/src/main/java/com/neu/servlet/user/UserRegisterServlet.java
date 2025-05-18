package com.neu.servlet.user;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Servlet implementation class UserRegisterServlet
 */
@WebServlet(value="/user/register")
public class UserRegisterServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public UserRegisterServlet() {
        super();
        // TODO Auto-generated constructor stub
        System.out.println("创建UserRegisterServlet实例");
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		request.setCharacterEncoding("utf8");//设置请求的字符集
		response.setCharacterEncoding("utf8");//指定响应的字符集
		
		String Id = request.getParameter("loginId");
		String pwd = request.getParameter("loginPassword");
		String ageStr = request.getParameter("loginAge");
		Integer age = null;//包装类型
		if(ageStr != null && !ageStr.trim().equals("")) {
			age = Integer.parseInt(ageStr);
		}
		//int age = Integer.parseInt(ageStr);
//		String sexStr = request.getParameter("sex");
//		Integer sex = null;//包装类型
//		if(sexStr != null && !ageStr.trim().equals("")) {
//			sex = Integer.parseInt(sexStr);
//		}
//		String nationalityStr = request.getParameter("nationality");
//		Integer nationality = null;//包装类型
//		if(nationalityStr != null && !ageStr.trim().equals("")) {
//			nationality = Integer.parseInt(nationalityStr);
//		}
		int sex = Integer.parseInt(request.getParameter("sex"));
		int nationality = Integer.parseInt(request.getParameter("nationality"));
		String[] courseStrs = request.getParameterValues("course");
		int[] courses = null;
		if(courseStrs != null) {
			courses = new int[courseStrs.length];
			for(int i=0;i<courses.length;i++) {
				courses[i]=Integer.parseInt(courseStrs[i]);
			}
		}
		String name = request.getParameter("loginname");
		System.out.println("Id:"+Id);
		System.out.println("Password:"+pwd);
		System.out.println("Age:"+age);
		System.out.println("sex:"+sex);
		System.out.println("nationality："+nationality);
		for(int c : courses) {
			System.out.println("coursrs"+c);
		}
		System.out.println("name:"+name);
		//若表单不填，ageStr空串转成int，会报错
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
