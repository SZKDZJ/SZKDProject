package com.neu.edu.his.model;

/**
 * 科室信息
 * @date 0724
 */
public class Department {
    private int did;
    private String name;

    public int getDid() {
        return did;
    }

    public void setDid(int did) {
        this.did = did;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Department{" +
                "did=" + did +
                ", name='" + name + '\'' +
                '}';
    }
}
