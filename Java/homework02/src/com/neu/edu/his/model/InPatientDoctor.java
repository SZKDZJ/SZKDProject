package com.neu.edu.his.model;
/**
 * 作者：张子琪
 * 住院护士模型
 */
import java.util.HashMap;

public class InPatientDoctor extends BaseUser{
    private Department department;
    private HashMap<Integer,String> workplan;

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    public HashMap<Integer, String> getWorkplan() {
        return workplan;
    }

    public void setWorkplan(HashMap<Integer, String> workplan) {
        this.workplan = workplan;
    }

    @Override
    public String toString() {
        return "InPatientDoctor{" +
                "department=" + department +
                ", workplan=" + workplan +
                '}';
    }
}
