package com.neu.edu.his.controller;
/**
 * 作者：张子琪
 * 住院护士操作类：对患者增删改
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.InPatientDoctor;
import com.neu.edu.his.model.InPatientNurse;
import com.neu.edu.his.model.Line;
import com.neu.edu.his.model.Patient;
import com.neu.edu.his.utils.ContactUtils;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Scanner;

public class InPatientNurseController {
    private Scanner scanner = new Scanner(System.in);
    private HospitalBedController hospitalBedController = new HospitalBedController();
    String category01;

    public int login(String account,String password) {
        //附加功能：
        //判断输入的字符串是否为空,获取是否都是空格
        if (!ContactUtils.isNull(account) || !ContactUtils.isNull(password)) {
            //不合法，结束该方法
            return -1;
        }
        //判断是否是字母以及数字组成，并且长度是4-8
        if (!ContactUtils.validate(account)||!ContactUtils.validate(password)) {
            //不合法，结束该方法
            return -2;
        }
        //与数据库对比账号密码是否正确
        for(InPatientNurse inPatientNurse : DateBase.inPatientNurseTable){
            //对比账号和密码
            if(inPatientNurse.getAccount().equals(account)&& inPatientNurse.getPassword().equals(password)){
                //成功
                return 200;
            }
        }
        //登录不成功
        return 0;
    }
    //增加患者信息
    public void increaseMenu(){
        //查询患者住院证明,显示患者信息
        System.out.println("|----请输入患者ID：");
        String id = scanner.next();
        int Did ;
        int sign = 1;
        for(Patient patient: DateBase.patientTable) {
            if(patient.getId().equals(id)) {
                System.out.print("|---是否住院：");
                System.out.println(patient.getMsgByDoctor().get("住院证明"));
                String proof = patient.getMsgByDoctor().get("住院证明");
                sign = 0;
                //显示对应科室病房数量
                if(proof.equals("是")) {
                    System.out.println("|---患者科室："+patient.getDepartmentId());
                    hospitalBedController.showHopitalBed(patient.getMsgByDoctor().get("病房类型"),patient.getDepartmentId());
                    System.out.println("----是否办理住院----");
                    System.out.println("     1、是");
                    System.out.println("     2、否");
                    int choose1 = scanner.nextInt();
                    Did = patient.getDepartmentId();
                    if(choose1==1) {
                        System.out.println("------请选择病房类别-----");
                        System.out.println("      1、普通病房");
                        System.out.println("      2、ICU病房");

                        for (InPatientDoctor inPatientDoctor:DateBase.inPatientDoctorTable) {
                            if(patient.getDepartmentId()==inPatientDoctor.getDepartment().getDid()) {
                                patient.setDoctorId(inPatientDoctor.getId());
                            }
                        }


                        int choose2 = scanner.nextInt();
                        if (choose2 == 1) {
                            category01 = "普通";
                            hospitalBedController.reduceHospitalBed("普通", patient.getDepartmentId());
                            if(hospitalBedController.sign==0) {
                                System.out.println("|---请输入患者的床号：");
                                int bed = scanner.nextInt();
                                patient.setBed(bed);

                                Date date = new Date();
                                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
                                String dateString = format.format(date);
                                System.out.println("住院日期：" + dateString);
                                System.out.println("-------【提示】办理住院成功-------");
                                //每个病人排队人数-1
                                for(Patient patient1:DateBase.patientTable) {
                                    if(patient1.getDepartmentId()==patient.getDepartmentId()
                                        &&patient1.getMsgByDoctor().get("病房类型").equals(patient.getMsgByDoctor().get("病房类型"))) {
                                        if (patient1.getLineid() > 0) {
                                            int x = patient.getLineid();
                                            patient1.setLineid(x-1);
                                        }
                                    }
                                }
                                //排队类减去已新增的患者
                                for(Line line:DateBase.lineTable){
                                    if(line.getHospitalBed().getDepartment().getDid()==patient.getDepartmentId()
                                            &&line.getRoom().equals(category01)) {
                                        if (line.getId() != null && !line.getId().isEmpty()) {
                                            //list不为空
                                            //hospitalBedController.ID.remove(0);
                                            line.getId().remove(id);
                                            int x = line.getHospitalBed().getCategory().get(category01);
                                            line.getHospitalBed().getCategory().put(category01,x-1);
                                        }
                                    }
                                }
                            }else{
                                System.out.println("------- 请选择：--------");
                                System.out.println("        1、排队等候");
                                System.out.println("        2、转院");
                                lineMenu(id,"普通",Did);
                            }
                        }
                        if (choose2 == 2) {
                            category01 = "ICU";
                            hospitalBedController.reduceHospitalBed("ICU", patient.getDepartmentId());
                            if(hospitalBedController.sign==0) {
                                System.out.println("|---请输入患者的床号：");
                                int bed = scanner.nextInt();
                                patient.setBed(bed);

                                Date date = new Date();
                                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
                                String dateString = format.format(date);
                                System.out.println("住院日期：" + dateString);
                                System.out.println("-------【提示】办理住院成功-------");
                                //每个病人排队人数-1
                                for(Patient patient1:DateBase.patientTable) {
                                    if(patient1.getDepartmentId()==patient.getDepartmentId()
                                            &&patient1.getMsgByDoctor().get("病房类型").equals(category01)) {
                                        if (patient1.getLineid() > 0) {
                                            int x = patient.getLineid();
                                            patient1.setLineid(x-1);
                                        }
                                    }
                                }
                                //排队类减去已新增的患者
                                for(Line line:DateBase.lineTable){
                                    if(line.getHospitalBed().getDepartment().getDid()==patient.getDepartmentId()
                                            &&line.getRoom().equals(category01)) {
                                        if (line.getId() != null && !line.getId().isEmpty()) {
                                            //list不为空
                                            line.getId().remove(id);
                                            //hospitalBedController.ID.remove(0);
                                            int x = line.getHospitalBed().getCategory().get(category01);
                                            line.getHospitalBed().getCategory().put(category01,x-1);
                                        }
                                    }
                                }
                            }else{
                                System.out.println("------- 请选择：--------");
                                System.out.println("        1、排队等候");
                                System.out.println("        2、转院");
                                lineMenu(id,"ICU",Did);
                            }
                        }
                    }
                }
            }
        }
        if(sign==1){
            System.out.println("-----找不到该患者-----");

        }
    }
    //转院或排队等候
    private void lineMenu(String id,String category, int Did){
        int choose = scanner.nextInt();
        if(choose == 1){
            hospitalBedController.lineBed(id,category, Did);
        }
        if(choose == 2){
            System.out.println("-------请选择要转入的医院-----");
            System.out.println("       1、A附院");
            System.out.println("       2、B院");
            System.out.println("       3、C院");

            String input = scanner.next();
            switch (input) {
                case "1":
                    for (Patient patient : DateBase.patientTable) {
                        if (patient.getId().equals(id)) {
                            patient.setHospital("A附院");
                        }
                    }
                    System.out.println("--------【提示】转院成功-------");
                    break;
                case "2":
                    for (Patient patient : DateBase.patientTable) {
                        if (patient.getId().equals(id)) {
                            patient.setHospital("B院");
                        }
                    }
                    System.out.println("--------【提示】转院成功-------");
                    break;
                case "3":
                    for (Patient patient : DateBase.patientTable) {
                        if (patient.getId().equals(id)) {
                            patient.setHospital("C院");
                        }
                    }
                    System.out.println("--------【提示】转院成功-------");
                    break;
            }
        }
    }
    //改变患者信息
    public void changeMenu(){
        System.out.println("|----请输入患者ID：");
        String id = scanner.next();
        for(Patient patient: DateBase.patientTable) {
            if(patient.getId().equals(id)) {
                System.out.println("|---请输入患者更改的科室：");
                int depaetmentId = scanner.nextInt();
                patient.setDepartmentId(depaetmentId);
                System.out.println("|---请输入患者对应的医生：");
                String doctorId = scanner.next();
                patient.setDoctorId(doctorId);
                System.out.println("|---请输入患者更改的床号：");
                int bed = scanner.nextInt();
                patient.setBed(bed);
            }
        }
    }
    //删除患者信息
    public void deleteMenu(){
        System.out.println("|----请输入患者ID：");
        String id = scanner.next();
        for(Patient patient: DateBase.patientTable) {
            if(patient.getId().equals(id)) {
                //删除人员
                int departmentId = patient.getDepartmentId();
                HashMap<String,String> map = new HashMap<>();
                map.put("住院证明","否");
                map.put("病房类型",category01);
                patient.setMsgByDoctor(map);
                patient.setBed(0);

                Date date = new Date();
                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
                String dateString2 = format.format(date);
                System.out.println("出院日期："+dateString2);
                System.out.println("---------【提示】办理出院成功--------");
                hospitalBedController.increaseHospitalBed(category01,departmentId);
                HashMap<String,String> map1 = new HashMap<>();
                map1.put("住院证明","否");
                map1.put("病房类型","无");
                patient.setMsgByDoctor(map1);
            }
        }
    }
}
