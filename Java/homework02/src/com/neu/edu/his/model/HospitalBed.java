package com.neu.edu.his.model;

import java.util.HashMap;
/**
 * 作者：张子琪
 * 病床模型
 */
public class HospitalBed {
    private Department department;
    private HashMap<String,Integer> category;

    public HashMap<String, Integer> getCategory() {
        return category;
    }

    public void setCategory(HashMap<String, Integer> category) {
        this.category = category;
    }

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    @Override
    public String toString() {
        return "HospitalBed{" +
                ", department=" + department +
                ", category=" + category +
                '}';
    }
}
