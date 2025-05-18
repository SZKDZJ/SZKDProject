package com.neu.edu.his.view;
/**
 * 作者：张子琪
 * 救护接线界面
 */

import com.neu.edu.his.MainEntry;
import com.neu.edu.his.controller.EmergencyWiringController;

import java.util.Scanner;

public class EmergencyWiringView {
    private Scanner scanner = new Scanner(System.in);
    private EmergencyWiringController emergencyWiringController = new EmergencyWiringController();
    private MainEntry mainEntry = new MainEntry();

    public void login(){
        System.out.println("|---请输入救护接线员的账号：|");
        //获取账号
        String account = scanner.next();
        System.out.println("|---请输入救护接线员的密码：|");
        //获取密码
        String password = scanner.next();
        //将账号和密码作为参数传入controller层，让他去进行对比和处理
        int result = emergencyWiringController.login(account,password);
        if(result==-1||result==-2){
            System.out.println("----【警告】账号和密码为非法输入-----");
        }else if(result==200){
            //继续向下流程：显示挂号科室
            System.out.println("-------------------------------");
            System.out.println("--------【提示】登录成功------------");
            showEmergencyWiringView();
        }else{
            //登录不成功
            System.out.println("---------【警告】登录失败----------");
            InPatientView inPatientView = new InPatientView();
            inPatientView.showInPatientMenu();
        }
    }
    private void showEmergencyWiringView(){
        System.out.println("----------救护接线员：功能菜单--------");
        System.out.println("          1、接线救护");
        System.out.println("          2、完善报告");
        System.out.println("          3、查询报告");
        System.out.println("          0、退出到主菜单");
        System.out.println("          9、任意键退出系统");
        System.out.println("|---------请输入您的选择：");

        //获取输入内容
        String input = scanner.next();
        switch (input){
            case "1":
                //接线
                emergencyWiringController.contact();
                showEmergencyWiringView();
                break;
            case "2":
                //完善
                emergencyWiringController.writing();
                showEmergencyWiringView();
                break;
            case "3":
                //查询
                emergencyWiringController.consult();
                showEmergencyWiringView();
                break;
            case "0":
                //到主菜单
                mainEntry.mainMenu();
                break;
            default:
                //退出系统
                System.out.println("--------祝您身体健康，再见！----------");
                System.exit(0);
                break;
        }
    }
}
