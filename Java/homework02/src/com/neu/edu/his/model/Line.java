package com.neu.edu.his.model;
/**
 * 作者：张子琪
 * 排队模型
 */

import java.util.ArrayList;

public class Line {
    private ArrayList<String> id;
    private HospitalBed hospitalBed;
    private String room;

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public ArrayList<String> getId() {
        return id;
    }

    public void setId(ArrayList<String> id) {
        this.id = id;
    }

    public HospitalBed getHospitalBed() {
        return hospitalBed;
    }

    public void setHospitalBed(HospitalBed hospitalBed) {
        this.hospitalBed = hospitalBed;
    }

    @Override
    public String toString() {
        return "Line{" +
                "id=" + id +
                ", hospitalBed=" + hospitalBed +
                ", room='" + room + '\'' +
                '}';
    }
}
