package com.neu.edu.his.view;

import com.neu.edu.his.MainEntry;
import com.neu.edu.his.controller.HospitalBedController;
import com.neu.edu.his.controller.InPatientNurseController;
import com.neu.edu.his.controller.LineController;
import com.neu.edu.his.controller.PatientController;
import com.neu.edu.his.view.InPatientView;
/**
 * 住院护士界面
 * 作者：张子琪
 */
import java.util.Scanner;

public class InPatientNurseView {
        private Scanner scanner = new Scanner(System.in);
        private InPatientNurseController inPatientNurseController = new InPatientNurseController();
        private HospitalBedController hospitalBedController = new HospitalBedController();
        private PatientController patientController = new PatientController();
        private LineController lineController = new LineController();
        //登录
        public void login(){
            System.out.println("|---请输入住院护士的账号：|");
            //获取账号
            String account = scanner.next();
            System.out.println("|---请输入住院护士的密码：|");
            //获取密码
            String password = scanner.next();
            //将账号和密码作为参数传入controller层，让他去进行对比和处理
            int result = inPatientNurseController.login(account,password);
            if(result==-1||result==-2){
                System.out.println("----【警告】账号和密码为非法输入-----");
            }else if(result==200){
                //继续向下流程：显示挂号科室
                System.out.println("-------------------------------");
                System.out.println("--------【提示】登录成功------------");
                showInPatientNurseMenu();
            }else{
                //登录不成功
                System.out.println("---------【警告】登录失败----------");
                InPatientView inPatientView = new InPatientView();
                inPatientView.showInPatientMenu();
            }
        }
        //住院护士
        private void showInPatientNurseMenu(){
            System.out.println("----------住院护士：功能菜单--------");
            System.out.println("          1、办理患者信息");
            System.out.println("          2、查询信息");
            System.out.println("          0、退出到主菜单");
            System.out.println("          9、任意键退出系统");
            System.out.println("|---------请输入您的选择：");

            //获取输入内容
            String input = scanner.next();
            switch (input){
                case "1":
                    //住院信息
                    PatientMenu();
                    showInPatientNurseMenu();
                    break;
                case "2":
                    //查询信息
                    consultMenu();
                    showInPatientNurseMenu();
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
        //办理患者信息
        private void PatientMenu(){
            System.out.println("----------办理患者信息--------");
            System.out.println("          1、新增患者信息");
            System.out.println("          2、修改患者信息");
            System.out.println("          3、删除患者信息");
            System.out.println("          0、退出到主菜单");
            System.out.println("          9、任意键退出系统");
            System.out.println("|---------请输入您的选择：");

            String input = scanner.next();
            switch (input){
                case "1":
                    //新增患者
                    inPatientNurseController.increaseMenu();
                    PatientMenu();
                    break;
                case "2":
                    //修改患者
                    inPatientNurseController.changeMenu();
                    PatientMenu();
                    break;
                case "3":
                    //删除患者
                    inPatientNurseController.deleteMenu();
                    PatientMenu();
                    break;
                case "0":
                    showInPatientNurseMenu();
                    break;
                default:
                    //退出系统
                    System.out.println("--------祝您身体健康，再见！----------");
                    System.exit(0);
                    break;
            }
        }
        //查询患者信息
        private void consultMenu(){
            System.out.println("----------查询信息--------");
            System.out.println("          1、患者");
            System.out.println("          2、病床");
            System.out.println("          3、排队");
            System.out.println("          0、退出到主菜单");
            System.out.println("          9、任意键退出系统");
            System.out.println("|---------请输入您的选择：");

            //获取输入内容
            String input = scanner.next();
            switch (input){
                case "1":
                    //患者
                    System.out.println("------请输入您要查询的患者ID-------");
                    String id = scanner.next();
                    patientController.showPatient(id);
                    consultMenu();
                    break;
                case "2":
                    //病床
                    hospitalBedController.showAllHopitalBed();
                    consultMenu();
                    break;
                case "3":
                    //排队
                    lineController.consultLine();
                    consultMenu();
                    break;
                case "0":
                    //到主菜单
                    showInPatientNurseMenu();
                    break;
                default:
                    //退出系统
                    System.out.println("--------祝您身体健康，再见！----------");
                    System.exit(0);
                    break;
            }
        }
}
