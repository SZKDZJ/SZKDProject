package com.neu.edu.his.controller;

/**
 * 作者：张子琪
 * 患者操作类：展示患者信息
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.HospitalBed;
import com.neu.edu.his.model.Patient;

import java.awt.image.PackedColorModel;

public class PatientController {
    public void addPatient(String id,String name,String sex,String doctorID,int age,int departmentId){
        Patient patient = new Patient();
        patient.setId(id);
        patient.setName(name);
        patient.setSex(sex);
        patient.setAge(age);
        patient.setDoctorId(doctorID);
        patient.setDepartmentId(departmentId);
        patient.setType(true);//就诊中
        //将患者放入数据库
        DateBase.patientTable.add(patient);
    }
    public void showPatient(String id){
        for(Patient patient:DateBase.patientTable){
            if(patient.getId().equals(id)) {
                System.out.print("患者ID：" + patient.getId() + "\t 患者姓名：" + patient.getName()
                        + "\t 患者科室：" + patient.getDepartmentId()
                        + "\t 患者医生：" + patient.getDoctorId());
                if (patient.getBed() != 0) {
                    System.out.println("\t 患者床号：" + patient.getBed());
                }else{
                    if(patient.getHospital().equals("A院")) {
                        System.out.println("\t 排队中");
                    }else{
                        System.out.println("\t 转入"+patient.getHospital());
                    }
                }
            }
        }
    }
    public void showAllPatient(String id){
        for(Patient patient:DateBase.patientTable){
            if(patient.getId().equals(id)) {
                System.out.println("患者ID：" + patient.getId() + "\t 患者姓名：" + patient.getName()
                        + "\t 患者科室：" + patient.getDepartmentId()
                        + "\t 患者医生：" + patient.getDoctorId()
                        + "\t 患者床号：" + patient.getBed()
                        + "\t 患者病例：" + patient.getMsgByDoctor());
            }
        }
    }
}
