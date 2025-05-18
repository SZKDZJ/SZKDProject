package com.neu.edu.his.controller;
/**
 * 排队操作类：查询排队信息
 * 作者：张子琪
 */

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Line;

public class LineController {
    public void consultLine(){
        for (Line line: DateBase.lineTable) {
            if(line.getRoom().equals("ICU")) {
                System.out.println("|---科室：" + line.getHospitalBed().getDepartment().getDid()
                        + "\t" + line.getHospitalBed().getDepartment().getName()
                        + "\t病房类型：ICU病房 \t 排队人数：" + line.getHospitalBed().getCategory().get("ICU"));
                if (line.getHospitalBed().getCategory().get("ICU") != 0) {
                    System.out.println("|---排队的患者ID：" + line.getId());
                }
            }
            if(line.getRoom().equals("普通")) {
                System.out.println("|---科室：" + line.getHospitalBed().getDepartment().getDid()
                        + "\t" + line.getHospitalBed().getDepartment().getName()
                        + "\t病房类型：普通病房 \t 排队人数：" + line.getHospitalBed().getCategory().get("普通"));
                if (line.getHospitalBed().getCategory().get("普通") != 0) {
                    System.out.println("|---排队的患者ID：" + line.getId());
                }
            }
        }
    }

}
