package com.neu.edu.his.controller;
/**
 * 作者：张子琪
 * 救护接线操作类：具体接线、完善报告、查询报告操作
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Accident;
import com.neu.edu.his.model.Doctor;
import com.neu.edu.his.model.EmergencyWiring;
import com.neu.edu.his.model.Patient;
import com.neu.edu.his.utils.ContactUtils;

import java.util.HashMap;
import java.util.Scanner;

public class EmergencyWiringController {
    private Scanner scanner = new Scanner(System.in);
    public String id;

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
        for(EmergencyWiring emergencyWiring : DateBase.emergencyWiringTable){
            //对比账号和密码
            if(emergencyWiring.getAccount().equals(account)&& emergencyWiring.getPassword().equals(password)){
                //成功
                return 200;
            }
        }
        //登录不成功
        return 0;
    }

    //接线
    public void contact(){
        System.out.println("----------请录入救护基本信息--------");
        Accident accident = new Accident();
        System.out.println("|---1、时间：");
        String Date = scanner.next();
        accident.setDate(Date);
        System.out.println("|---2、地点：");
        String Place = scanner.next();
        accident.setPlace(Place);
        System.out.println("|---3、病人基本情况：");//“时间+病因+部位+情况” “部位+情况+持续时间”
        String Situation =scanner.next();
        accident.setSituation(Situation);
        System.out.println("|---4、有效电话：");
        String Call = scanner.next();
        accident.setCall(Call);
        DateBase.accidentTable.add(accident);
        System.out.println("-------请联系相关医生安排救助-------");
        int i = 1;
        for (Doctor doctor:DateBase.doctorTable){
            System.out.println(i+"、\t 科室："+doctor.getDepartment().getDid()+"\t"+doctor.getDepartment().getName()
                    +"\t 医生姓名："+doctor.getName()+"\t 医生电话："+doctor.getCall());
            i++;
        }
        System.out.println("--------请您输入选择--------");
        int choose = scanner.nextInt();
        int j = 1;
        for (Doctor doctor:DateBase.doctorTable){
            if(j==choose){
                id = doctor.getId();
                HashMap<String,String> map = new HashMap<>();
                map.put("时间",Date);
                map.put("地点",Place);
                map.put("病人基本情况",Situation);
                map.put("有效电话",Call);
                doctor.getMessage().add(map);
                System.out.println("------【提示】已联系成功------");
                break;
            }
            j++;
        }
    }

    //完善
    public void writing(){
        System.out.println("--------请输入救助事件的序号--------");
        int number = scanner.nextInt();
        Patient patient = new Patient();
        System.out.println("|---请输入患者ID:");
        String ID = scanner.next();
        patient.setId(ID);
        System.out.println("|---请输入患者姓名：");
        String name = scanner.next();
        patient.setName(name);
        System.out.println("|---请输入患者性别：");
        String sex = scanner.next();
        patient.setSex(sex);
        System.out.println("|---请输入患者年龄：");
        int age = scanner.nextInt();
        patient.setAge(age);
        patient.setDoctorId(id);
        for(Doctor doctor:DateBase.doctorTable) {
            if(doctor.getId().equals(id)) {
                patient.setDepartmentId(doctor.getDepartment().getDid());
            }
        }
        System.out.println("|---请输入救助结果：");
        String result = scanner.next();
        DateBase.accidentTable.get(number-1).setPatient(patient);
        DateBase.accidentTable.get(number-1).setResult(result);
    }

    //查询
    public void consult(){
        System.out.println("--------请输入需要查询的救助事件序号--------");
        int number = scanner.nextInt();
        System.out.println("|--救助事件序号："+number);
        System.out.println("|--患者ID："+DateBase.accidentTable.get(number-1).getPatient().getId());
        System.out.println("|--患者姓名："+DateBase.accidentTable.get(number-1).getPatient().getName());
        System.out.println("|--患者性别："+DateBase.accidentTable.get(number-1).getPatient().getSex());
        System.out.println("|--患者年龄："+DateBase.accidentTable.get(number-1).getPatient().getAge());
        System.out.println("|--负责科室："+DateBase.accidentTable.get(number-1).getPatient().getDepartmentId());
        for (Doctor doctor:DateBase.doctorTable) {
            if(DateBase.accidentTable.get(number-1).getPatient().getDoctorId().equals(doctor.getId()))
            System.out.println("|--救助医生：" + doctor.getName());
        }
        System.out.println("|--救助结果："+DateBase.accidentTable.get(number-1).getResult());
    }
}
