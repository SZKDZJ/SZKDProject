package com.neu.edu.his.model;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * 门诊医生信息表
 */
public class Doctor extends BaseUser{
    //id, account, password, name
    private  Department department;
    private String grade;//初级医师，主治医师，专家
    private HashMap<Integer,String> workplan; //1-7
    private String call;
    private ArrayList <HashMap<String,String>> message = new ArrayList<>();

    public ArrayList<HashMap<String, String>> getMessage() {
        return message;
    }

    public void setMessage(ArrayList<HashMap<String, String>> message) {
        this.message = message;
    }

    public String getCall() {
        return call;
    }

    public void setCall(String call) {
        this.call = call;
    }

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    public String getGrade() {
        return grade;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    public HashMap<Integer, String> getWorkplan() {
        return workplan;
    }

    public void setWorkplan(HashMap<Integer, String> workplan) {
        this.workplan = workplan;
    }

    @Override
    public String toString() {
        return "Doctor{" +
                "department=" + department +
                ", grade='" + grade + '\'' +
                ", workplan=" + workplan +
                ", call='" + call + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
}
