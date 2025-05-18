package com.neu.edu.his.view;
/**
 * 住院部界面
 * 作者：张子琪
 */

import com.neu.edu.his.MainEntry;
import com.neu.edu.his.view.InPatientNurseView;

import java.util.Scanner;

public class InPatientView {
    private Scanner scanner = new Scanner(System.in);
    private MainEntry mainEntry = new MainEntry();

    public void showInPatientMenu(){
        System.out.println("----------选择身份--------");
        System.out.println("          1、住院护士");
        System.out.println("          2、住院医生");
        System.out.println("          0、退出到主菜单");
        System.out.println("          9、任意键退出系统");
        System.out.println("|---------请输入您的选择：");

        String input = scanner.next();
        switch (input){
            case "1":
                //住院护士
                InPatientNurseView inPatientNurseView = new InPatientNurseView();
                inPatientNurseView.login();
                break;
            case "2":
                //住院医生
                InPatientDoctorView inPatientDoctorView = new InPatientDoctorView();
                inPatientDoctorView.login();
                break;
            case "0":
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
