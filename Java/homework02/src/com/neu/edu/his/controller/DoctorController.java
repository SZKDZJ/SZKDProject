package com.neu.edu.his.controller;

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Doctor;
import com.neu.edu.his.utils.ContactUtils;

/**
 * 医生的控制层
 */
import java.util.ArrayList;

public class DoctorController {
    //根据科室，查询医生列表
    public ArrayList<Doctor> findDoctorsByDid(int departmentID){
        ArrayList<Doctor> list = new ArrayList<>();
        for (Doctor doctor:DateBase.doctorTable){
            //显示坐诊是周几
            String workplan = doctor.getWorkplan().get(ContactUtils.getDay());
            if(doctor.getDepartment().getDid()==departmentID&&"坐诊".equals(workplan)){
                //符合要求
                list.add(doctor);
            }
        }
        return list;
    }
}
