package com.neu.edu.his.controller;
/**
 * 病床操作类：展示病床信息、病床排队、出院增加病床
 * 作者：张子琪
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Department;
import com.neu.edu.his.model.HospitalBed;
import com.neu.edu.his.model.Line;
import com.neu.edu.his.model.Patient;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;

public class HospitalBedController {
    public int sign;
    //public ArrayList<String> ID = new ArrayList<>();
    public void showHopitalBed(String category,int departmentId){
        for(HospitalBed hospitalBed: DateBase.hospitalBedTable){
            if(hospitalBed.getDepartment().getDid()==departmentId){
                System.out.println("|---病床类型："+category+"病房"
                        +"\t 目前病床数量：" +hospitalBed.getCategory().get(category));
            }
        }
    }
    public void reduceHospitalBed(String category,int departmentId){
        sign = 1;
        for(HospitalBed hospitalBed: DateBase.hospitalBedTable){
            if(hospitalBed.getDepartment().getDid()==departmentId){
                if(hospitalBed.getCategory().get(category)!=0) {
                    int number = hospitalBed.getCategory().get(category);
                    hospitalBed.getCategory().put(category,number-1);
                    sign = 0;
                }
            }
        }
        if(sign == 1){
            System.out.println("------【提示】病床数量不足------");
        }
    }
    //排队
    public void lineBed(String id,String category, int Did){
        for(Line line:DateBase.lineTable){
            if(line.getHospitalBed().getDepartment().getDid() == Did
                    &&line.getRoom().equals(category)){
                //line.setId(ID);
                line.getId().add(id);
                HospitalBed hospitalBed = new HospitalBed();
                HashMap<String,Integer> map = new HashMap<>();
                int number = line.getHospitalBed().getCategory().get(category) + 1;
                if("ICU".equals(category)) {
                    map.put(category, number);
                    map.put("普通",line.getHospitalBed().getCategory().get("普通"));
                }else{
                    map.put(category, number);
                    map.put("ICU",line.getHospitalBed().getCategory().get("ICU"));
                }
                hospitalBed.setCategory(map);
                Department department = new Department();
                department.setDid(line.getHospitalBed().getDepartment().getDid());
                department.setName(line.getHospitalBed().getDepartment().getName());
                hospitalBed.setDepartment(department);
                line.setHospitalBed(hospitalBed);
                //paitent.lineid
                for (Patient patient:DateBase.patientTable){
                    if(patient.getId().equals(id)){
                        patient.setLineid(number);
                    }
                }
                System.out.println("------【提示】排队成功-------");
                System.out.println("|---科室："+Did+"、\t"+line.getHospitalBed().getDepartment().getName()
                        +"\t 病床类型："+category+"\t 排队人数："+line.getHospitalBed().getCategory().get(category));
            }
        }
    }

    public void increaseHospitalBed(String category,int departmentId){
        for(HospitalBed hospitalBed: DateBase.hospitalBedTable){
            if(hospitalBed.getDepartment().getDid()==departmentId){
                int number = hospitalBed.getCategory().get(category);
                hospitalBed.getCategory().put(category,number+1);
                if (number == 0) {
                    for(Patient patient:DateBase.patientTable) {
                        if(patient.getDepartmentId()==departmentId
                                &&patient.getMsgByDoctor().get("病房类型").equals(category)
                                &&patient.getMsgByDoctor().get("住院证明").equals("是")) {
                            if(patient.getLineid()==1) {
                                System.out.println("|--【提示】该患者已排到:" + patient.getId() + "\t" + patient.getName());
                            }
                        }
                    }
                }
            }
        }
    }
    public void showAllHopitalBed(){
        for(HospitalBed hospitalBed:DateBase.hospitalBedTable){
            System.out.println("科室："+hospitalBed.getDepartment().getDid()
                    +"\t 科室名称："+hospitalBed.getDepartment().getName()
                    +"\t 病床类别："+"ICU病床"
                    +"\t 病床数量："+hospitalBed.getCategory().get("ICU"));
            System.out.println("科室："+hospitalBed.getDepartment().getDid()
                    +"\t 科室名称："+hospitalBed.getDepartment().getName()
                    +"\t 病床类别："+"普通病床"
                    +"\t 病床数量："+hospitalBed.getCategory().get("普通"));
        }
    }
}
