package com.neu.edu.his.controller;

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Department;

import java.util.ArrayList;

/**
 * 科室操作类
 */
public class DepartmentController {
    /**
     * 查询所有科室信息
     */
    public ArrayList<Department> findAllDepartment(){
        return DateBase.departmentTable;
    }
}
