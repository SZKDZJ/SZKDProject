package com.neu.edu.his;

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.HospitalBed;
import com.neu.edu.his.model.Line;
import com.neu.edu.his.view.EmergencyWiringView;
import com.neu.edu.his.view.RegistrationView;
import com.neu.edu.his.view.InPatientView;

import java.util.ArrayList;
import java.util.Scanner;

/**
 * 程序的主入口
 * @date: 0723
 */
public class MainEntry {
    //成员变量
    private static Scanner scanner = new Scanner(System.in);
    //创建挂号员窗口对象(不在下面case 1中创建，避免每循环到那就创建对象，节省内存空间)
    private static RegistrationView registrationView = new RegistrationView();
    //住院部
    private static InPatientView inPatientView = new InPatientView();
    //救护接线
    private static EmergencyWiringView emergencyWiringView = new EmergencyWiringView();
    /**
     * 主方法，程序唯一入口
     * @param args
     */
    public static void main(String[] args) {

        System.out.println("----------------------------");
        System.out.println("|     欢迎进入HIS云医院系统     |");
        System.out.println(" |        Version:1.0       |");
        //调用主菜单
        MainEntry entry = new MainEntry();
        //退出总系统前，可一直重复运行
        while(true) {
            //调用主菜单
            entry.mainMenu();
        }
    }
    public static void mainMenu(){
        //登录操作
        System.out.println("-------------------------------");
        System.out.println("          请选择您的身份     ");
        System.out.println("          1、挂号收费员     ");
        System.out.println("          2、门诊医生     ");
        System.out.println("          3、住院部    ");
        System.out.println("          4、救护接线    ");
        System.out.println("          0、退出系统     ");
        System.out.println("------------------------------");
        System.out.println("|-----请输入您的身份：");

        /**
         *
         */
        try {
            int choose = scanner.nextInt();
            switch (choose) {
                case 1://挂号员登录
                    //处理业务逻辑
                    registrationView.login();
                    break;
                case 2://门诊医生登录
                    break;
                case 3:
                    //住院部
                    inPatientView.showInPatientMenu();
                    break;
                case 4:
                    //救护接线
                    emergencyWiringView.login();
                    break;
                case 0://退出
                    System.out.println("--------祝您身体健康，再见！----------");
                    //退出总系统
                    System.exit(0);
                    break;
                default:
                    System.out.println("---您当前输入菜单不存在，请重新选择---");
                    break;
            }
        }catch(Exception e){//Exception e所有异常都会转到这里
                            //Exception 异常父类 e类名
            e.printStackTrace();//会转到具体错误
            scanner.nextLine();//清空上次的输入，避免死循环
            System.out.println("---您当前非法输入，请重新选择---");
        }
    }
}
