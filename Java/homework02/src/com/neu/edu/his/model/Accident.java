package com.neu.edu.his.model;

import java.util.ArrayList;

public class Accident {
//    private ArrayList<Integer> aid = new ArrayList<>();
    private String Date;
    private String Place;
    private String Situation;
    private String Call;
    private Patient patient;
    private String result;

//    public ArrayList<Integer> getAid() {
//        return aid;
//    }
//
//    public void setAid(ArrayList<Integer> aid) {
//        this.aid = aid;
//    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public Patient getPatient() {
        return patient;
    }

    public void setPatient(Patient patient) {
        this.patient = patient;
    }

    public String getDate() {
        return Date;
    }

    public void setDate(String date) {
        Date = date;
    }

    public String getPlace() {
        return Place;
    }

    public void setPlace(String place) {
        Place = place;
    }

    public String getSituation() {
        return Situation;
    }

    public void setSituation(String situation) {
        Situation = situation;
    }

    public String getCall() {
        return Call;
    }

    public void setCall(String call) {
        Call = call;
    }

    @Override
    public String toString() {
        return "Accident{" +
                "Date='" + Date + '\'' +
                ", Place='" + Place + '\'' +
                ", Situation='" + Situation + '\'' +
                ", Call='" + Call + '\'' +
                ", patient=" + patient +
                ", result='" + result + '\'' +
                '}';
    }
}
