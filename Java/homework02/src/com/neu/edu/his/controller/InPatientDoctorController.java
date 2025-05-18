package com.neu.edu.his.controller;

/**
 * 作者：张子琪
 * 住院医生操作类：查询值班信息
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Doctor;
import com.neu.edu.his.model.InPatientDoctor;
import com.neu.edu.his.utils.ContactUtils;

import java.util.Scanner;

public class InPatientDoctorController {
    private Scanner scanner = new Scanner(System.in);
    private InPatientDoctor inPatientDoctor = new InPatientDoctor();

    public int login(String account, String password) {
        //附加功能：
        //判断输入的字符串是否为空,获取是否都是空格
        if (!ContactUtils.isNull(account) || !ContactUtils.isNull(password)) {
            //不合法，结束该方法
            return -1;
        }
        //判断是否是字母以及数字组成，并且长度是4-8
        if (!ContactUtils.validate(account) || !ContactUtils.validate(password)) {
            //不合法，结束该方法
            return -2;
        }
        //与数据库对比账号密码是否正确
        for (InPatientDoctor inPatientDoctor : DateBase.inPatientDoctorTable) {
            //对比账号和密码
            if (inPatientDoctor.getAccount().equals(account) && inPatientDoctor.getPassword().equals(password)) {
                //成功
                return 200;
            }
        }
        //登录不成功
        return 0;
    }

    //查看信息
    public void consultWorkPlan(String id) {
        for (Doctor doctor : DateBase.doctorTable) {
            if (doctor.getId().equals(id)) {
                System.out.println(doctor.getMessage());
            }
        }
        for (InPatientDoctor inPatientDoctor : DateBase.inPatientDoctorTable) {
            if (inPatientDoctor.getId().equals(id)) {
                System.out.println("周一：" + inPatientDoctor.getWorkplan().get(1));
                System.out.println("周二：" + inPatientDoctor.getWorkplan().get(2));
                System.out.println("周三：" + inPatientDoctor.getWorkplan().get(3));
                System.out.println("周四：" + inPatientDoctor.getWorkplan().get(4));
                System.out.println("周五：" + inPatientDoctor.getWorkplan().get(5));
                System.out.println("周六：" + inPatientDoctor.getWorkplan().get(6));
                System.out.println("周日：" + inPatientDoctor.getWorkplan().get(7));
            }
        }
    }
}
    //开单检查
//    public void insept(){
//        System.out.println("-------请选择需要检查的项目--------");
//        System.out.println("       1、血检");
//        System.out.println("       2、X光");
//        System.out.println("       3、CT");
//        System.out.println("       0、退出到主菜单");
//        System.out.println("       9、任意键退出系统");
//        System.out.println("|---------请输入您的选择：");
//
//        //获取输入内容
//        String input = scanner.next();
//        switch (input){
//            case "1":
//                ；
//                break;
//            case "2":
//
//                break;
//            case "3":
//                //开处方
//
//                break;
//            case "0":
//                //到主菜单
//
//                break;
//            default:
//                //退出系统
//                System.out.println("--------祝您身体健康，再见！----------");
//                System.exit(0);
//                break;
//        }
//    }
