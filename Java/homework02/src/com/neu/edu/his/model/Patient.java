package com.neu.edu.his.model;
/**
 * 作者：张子琪
 * 病人模型
 */

import java.util.HashMap;

public class Patient {
    private String id;
    private String name;
    private String sex;
    private int age;
    private String doctorId;
    private int departmentId;
    private boolean type;
    private String msgBySelf;
    private HashMap<String,String> msgByDoctor = new HashMap<>();
    private int bed;
    private String hospital;
    private int lineid;

    public int getLineid() {
        return lineid;
    }

    public void setLineid(int lineid) {
        this.lineid = lineid;
    }

    public String getHospital() {
        return hospital;
    }

    public void setHospital(String hospital) {
        this.hospital = hospital;
    }

    public int getBed() {
        return bed;
    }

    public void setBed(int bed) {
        this.bed = bed;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getDoctorId() {
        return doctorId;
    }

    public void setDoctorId(String doctorId) {
        this.doctorId = doctorId;
    }

    public int getDepartmentId() {
        return departmentId;
    }

    public void setDepartmentId(int departmentId) {
        this.departmentId = departmentId;
    }

    public boolean isType() {
        return type;
    }

    public void setType(boolean type) {
        this.type = type;
    }

    public String getMsgBySelf() {
        return msgBySelf;
    }

    public void setMsgBySelf(String msgBySelf) {
        this.msgBySelf = msgBySelf;
    }

    public HashMap<String, String> getMsgByDoctor() {
        return msgByDoctor;
    }

    public void setMsgByDoctor(HashMap<String, String> msgByDoctor) {
        this.msgByDoctor = msgByDoctor;
    }

    @Override
    public String toString() {
        return "Patient{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", sex='" + sex + '\'' +
                ", age=" + age +
                ", doctorId='" + doctorId + '\'' +
                ", departmentId=" + departmentId +
                ", type=" + type +
                ", msgBySelf='" + msgBySelf + '\'' +
                ", msgByDoctor=" + msgByDoctor +
                ", bed=" + bed +
                ", hospital='" + hospital + '\'' +
                ", lineid=" + lineid +
                '}';
    }
}