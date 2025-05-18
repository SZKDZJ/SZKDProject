package com.neu.edu.his.view;
/**
 * 住院医生界面
 * 作者：张子琪
 */

import com.neu.edu.his.controller.EmergencyWiringController;
import com.neu.edu.his.controller.InPatientDoctorController;
import com.neu.edu.his.controller.PatientController;
import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Doctor;

import java.util.Scanner;

public class InPatientDoctorView {
    private Scanner scanner = new Scanner(System.in);
    private InPatientDoctorController inPatientDoctorController = new InPatientDoctorController();
    private PatientController patientController = new PatientController();

    //登录
    public void login(){
        System.out.println("|---请输入住院医生的账号：");
        //获取账号
        String account = scanner.next();
        System.out.println("|---请输入住院医生的密码：");
        //获取密码
        String password = scanner.next();
        //将账号和密码作为参数传入controller层，让他去进行对比和处理
        int result = inPatientDoctorController.login(account,password);
        if(result==-1||result==-2){
            System.out.println("----【警告】账号和密码为非法输入-----");
        }else if(result==200){
            //继续向下流程：显示挂号科室
            System.out.println("-------------------------------");
            System.out.println("--------【提示】登录成功------------");
            showInPatientDoctorMenu();
        }else{
            //登录不成功
            System.out.println("---------【警告】登录失败----------");
            InPatientView inPatientView = new InPatientView();
            inPatientView.showInPatientMenu();
        }
    }
    //住院医生
    private void showInPatientDoctorMenu(){
        System.out.println("----------住院医生：功能菜单--------");
        System.out.println("          1、查询值班时间");
        System.out.println("          2、读取患者信息");
        System.out.println("          0、退出到主菜单");
        System.out.println("          9、任意键退出系统");
        System.out.println("|---------请输入您的选择：");

        //获取输入内容
        String input = scanner.next();
        switch (input){
            case "1":
                //查询值班时间
                consultWorkPlan();
                showInPatientDoctorMenu();
                break;
            case "2":
                //读取患者信息
                readPatient();
                showInPatientDoctorMenu();
                break;
            case "0":
                //到主菜单
                InPatientView inPatientView = new InPatientView();
                inPatientView.showInPatientMenu();
                break;
            default:
                //退出系统
                System.out.println("--------祝您身体健康，再见！----------");
                System.exit(0);
                break;
        }
    }
    //查询
    private void consultWorkPlan(){
        System.out.println("|---请输入您的ID：");
        String id = scanner.next();
        inPatientDoctorController.consultWorkPlan(id);
    }
    //读取患者
    private void readPatient() {
        System.out.println("----------读取患者信息--------");
        System.out.println("|---请输入患者ID：");
        String input = scanner.next();
        patientController.showAllPatient(input);
        operatePatient();
    }
    private void operatePatient(){
        System.out.println("----------请选择进一步操作--------");
        System.out.println("          1、开单检查");
        System.out.println("          2、开处方");
        System.out.println("          3、更新病历");
        System.out.println("          0、退出到主菜单");
        System.out.println("          9、任意键退出系统");
        System.out.println("|---------请输入您的选择：");

        //获取输入内容
        String input = scanner.next();
        switch (input){
            case "1":
                //开单检查
                //inPatientDoctorController.insept();
                operatePatient();
                break;
            case "2":
                //开处方
                //具体操作参考门诊医生
                operatePatient();
                break;
            case "3":
                //更新病例
                //具体操作参考门诊医生
                operatePatient();
                break;
            case "0":
                //到主菜单
                showInPatientDoctorMenu();
                break;
            default:
                //退出系统
                System.out.println("--------祝您身体健康，再见！----------");
                System.exit(0);
                break;
        }
    }
}
