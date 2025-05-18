package com.neu.edu.his.view;

import com.neu.edu.his.controller.DepartmentController;
import com.neu.edu.his.controller.DoctorController;
import com.neu.edu.his.controller.PatientController;
import com.neu.edu.his.controller.RegistrationController;
import com.neu.edu.his.model.Department;
import com.neu.edu.his.model.Doctor;
import com.neu.edu.his.model.Patient;

import java.util.ArrayList;
import java.util.Scanner;

/**
 * 挂号员登录
 * @date: 0723
 */
public class RegistrationView {
    private Scanner scanner = new Scanner(System.in);
    private RegistrationController registrationController = new RegistrationController();
    /**
     * 挂号员的登录页面
     */
    public void login(){
        System.out.println("|---请输入挂号护士的账号：|");
        //获取账号
        String account = scanner.next();
        System.out.println("|---请输入挂号护士的密码：|");
        //获取密码
        String password = scanner.next();
        //将账号和密码作为参数传入controller层，让他去进行对比和处理
        int result = registrationController.login(account,password);
        if(result==-1||result==-2){
            System.out.println("----【警告】账号和密码为非法输入-----");
        }else if(result==200){
            //继续向下流程：显示挂号科室
            System.out.println("-------------------------------");
            System.out.println("--------【提示】登录成功------------");
            showRegistraMenu();
        }else{
            //登录不成功
            System.out.println("---------【警告】登录失败----------");
        }
    }
    private void showRegistraMenu(){
        System.out.println("----------挂号人员：功能菜单--------");
        System.out.println("          1、挂号操作");
        System.out.println("          0、退出到主菜单");
        System.out.println("          9、任意键退出系统");
        System.out.println("|---------请输入您的选择：");

        //获取输入内容
        String input = scanner.next();
        switch (input){
            case "1":
                //挂号流程
                registrationMenu();
                break;
            case "0":
                //到主菜单
                break;
            default:
                //退出系统
                System.out.println("--------祝您身体健康，再见！----------");
                System.exit(0);
                break;
        }
    }

    /**
     * 挂号的菜单
     */
    private void registrationMenu(){
        //显示科室
        System.out.println("--------科室如下：--------");
        //通过科室controller,查询所有科室信息
        DepartmentController departmentController = new DepartmentController();
        ArrayList<Department> departList = departmentController.findAllDepartment();
        //显示科室信息
        for(Department department: departList){
            System.out.println("|---科室编号："+department.getDid()+"\t 科室名字："+department.getName()+"---|");
        }
        //提示用户选择科室
        System.out.println("|----请输入您选择的科室：");
        int departChoose = scanner.nextInt();

        //根据科室、坐诊时间，显示坐诊医生
        DoctorController doctorController = new DoctorController();
        ArrayList<Doctor> doctorList = doctorController.findDoctorsByDid(departChoose);
        for (Doctor doctor:doctorList){
            System.out.println("|---医生编号："+doctor.getId()
                    + "\t 医生名字："+doctor.getName()
                    + "\t 医生等级："+doctor.getGrade()
                    +"\t 医生科室："+doctor.getDepartment().getName()+"---|");
        }
        System.out.println("---请输入您要挂号的门诊医生编号：");
        String doctorID = scanner.next().trim();
        //录入患者信息
        System.out.println("|---请输入当日患者ID：");
        String id = scanner.next();
        System.out.println("|--请输入患者姓名：");
        String name = scanner.next();
        System.out.println("|--请输入患者性别：");
        String sex = scanner.next();
        System.out.println("|--请输入患者年龄：");
        int age = scanner.nextInt();

        //提示成功或失败
        PatientController patientController = new PatientController();
        patientController.addPatient(id,name,sex,doctorID,age,departChoose);
        System.out.println("|---【提示】恭喜您添加成功！");

        showRegistraMenu();
    }
}
