package com.neu.edu.his.db;

import com.neu.edu.his.model.*;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * 模拟数据库
 */
public class DateBase {
    //模拟表单：挂号员信息表
    public static ArrayList<Register> registerTable = new ArrayList<>();
    //模拟表单：科室信息表
    public static ArrayList<Department> departmentTable = new ArrayList<>();
    //模拟表单：门诊医生信息表
    public static ArrayList<Doctor> doctorTable = new ArrayList<>();
    //模拟表单：患者信息表
    public static ArrayList<Patient> patientTable = new ArrayList<>();
    //住院护士表
    public static ArrayList<InPatientNurse> inPatientNurseTable = new ArrayList<>();
    //病床数量表
    public static ArrayList<HospitalBed> hospitalBedTable = new ArrayList<>();
    //病床排队列表
    public static ArrayList<Line> lineTable = new ArrayList<>();
    //住院医生表
    public static ArrayList<InPatientDoctor> inPatientDoctorTable = new ArrayList<>();
    //救护接线员表
    public static ArrayList<EmergencyWiring> emergencyWiringTable = new ArrayList<>();
    //事件表
    public static ArrayList<Accident> accidentTable = new ArrayList<>();

    static {
        //创建挂号员表
        createRegistorTable();
        createDepartmentTable();
        creatDoctorTable();
        createInPatientTable();
        createHospitalBed();
        createLineTable();
        createInPatientDoctor();
        cteateEmergencyWiring();
        fp();
    }
    //假病人
    public static void fp(){
        Patient patient = new Patient();
        patient.setDepartmentId(1);
        patient.setId("0001");
        patient.setDoctorId("4001");
        patient.setHospital("A院");
        HashMap<String,String> map = new HashMap<>();
        map.put("住院证明","是");
        map.put("病房类型","ICU");//ICU or 普通
        patient.setMsgByDoctor(map);
        patientTable.add(patient);

        Patient patient2 = new Patient();
        patient2.setDepartmentId(1);
        patient2.setId("0002");
        patient2.setDoctorId("4003");
        patient2.setHospital("A院");
        HashMap<String,String> map2 = new HashMap<>();
        map2.put("住院证明","是");
        map2.put("病房类型","ICU");//ICU or 普通
        patient2.setMsgByDoctor(map2);
        patientTable.add(patient2);

        Patient patient3 = new Patient();
        patient3.setDepartmentId(1);
        patient3.setId("0003");
        patient3.setDoctorId("4003");
        patient3.setHospital("A院");
        HashMap<String,String> map3 = new HashMap<>();
        map3.put("住院证明","是");
        map3.put("病房类型","ICU");//ICU or 普通
        patient3.setMsgByDoctor(map3);
        patientTable.add(patient3);
    }
    //初始化救护接线员
    public static void cteateEmergencyWiring(){
        for (int i = 0; i < 5; i++) {
            EmergencyWiring emergencyWiring = new EmergencyWiring();
            emergencyWiring.setId("500"+i);
            emergencyWiring.setAccount("500"+i);
            emergencyWiring.setPassword("500"+i);
            emergencyWiring.setName("迦"+i);
            emergencyWiringTable.add(emergencyWiring);
        }
    }
    //初始化住院医生
    public static void createInPatientDoctor(){
        for (int i=0;i<5;i++){
            InPatientDoctor inPatientDoctor = new InPatientDoctor();
            inPatientDoctor.setId("400"+i);
            inPatientDoctor.setAccount("400"+i);
            inPatientDoctor.setPassword("400"+i);

            inPatientDoctorTable.add(inPatientDoctor);
        }
        //获取第0个数据，赋值
        inPatientDoctorTable.get(0).setName("扁鹊");
        //创建部门
        inPatientDoctorTable.get(0).setDepartment(departmentTable.get(0));
        HashMap<Integer,String> workplanToBianQue = new HashMap<>();
        workplanToBianQue.put(1,"值班");
        workplanToBianQue.put(2,"不值班");
        workplanToBianQue.put(3,"值班");
        workplanToBianQue.put(4,"不值班");
        workplanToBianQue.put(5,"值班");
        workplanToBianQue.put(6,"不值班");
        workplanToBianQue.put(7,"值班");
        inPatientDoctorTable.get(0).setWorkplan(workplanToBianQue);

        //获取第1个数据，赋值
        inPatientDoctorTable.get(1).setName("孙思邈");
        //创建部门
        inPatientDoctorTable.get(1).setDepartment(departmentTable.get(1));
        HashMap<Integer,String> workplanToSunSimiao = new HashMap<>();
        workplanToSunSimiao.put(1,"值班");
        workplanToSunSimiao.put(2,"值班");
        workplanToSunSimiao.put(3,"值班");
        workplanToSunSimiao.put(4,"不值班");
        workplanToSunSimiao.put(5,"值班");
        workplanToSunSimiao.put(6,"不值班");
        workplanToSunSimiao.put(7,"不值班");
        inPatientDoctorTable.get(1).setWorkplan(workplanToSunSimiao);

        //获取第2个数据，赋值
        inPatientDoctorTable.get(2).setName("李时珍");
        //创建部门
        inPatientDoctorTable.get(2).setDepartment(departmentTable.get(2));
        HashMap<Integer,String> workplanLiShizhen = new HashMap<>();
        workplanLiShizhen.put(1,"不值班");
        workplanLiShizhen.put(2,"值班");
        workplanLiShizhen.put(3,"值班");
        workplanLiShizhen.put(4,"不值班");
        workplanLiShizhen.put(5,"值班");
        workplanLiShizhen.put(6,"不值班");
        workplanLiShizhen.put(7,"值班");
        inPatientDoctorTable.get(2).setWorkplan(workplanLiShizhen);


        //获取第3个数据，赋值
        inPatientDoctorTable.get(3).setName("华佗");
        //创建部门
        inPatientDoctorTable.get(3).setDepartment(departmentTable.get(3));
        HashMap<Integer,String> workplanToHuaTuo = new HashMap<>();
        workplanToHuaTuo.put(1,"值班");
        workplanToHuaTuo.put(2,"值班");
        workplanToHuaTuo.put(3,"值班");
        workplanToHuaTuo.put(4,"不值班");
        workplanToHuaTuo.put(5,"不值班");
        workplanToHuaTuo.put(6,"不值班");
        workplanToHuaTuo.put(7,"值班");
        inPatientDoctorTable.get(3).setWorkplan(workplanToHuaTuo);

        //获取第4个数据，赋值
        inPatientDoctorTable.get(4).setName("张仲景");
        //创建部门
        inPatientDoctorTable.get(4).setDepartment(departmentTable.get(4));
        HashMap<Integer,String> workplanToZhangZhongjing = new HashMap<>();
        workplanToZhangZhongjing.put(1,"值班");
        workplanToZhangZhongjing.put(2,"值班");
        workplanToZhangZhongjing.put(3,"不值班");
        workplanToZhangZhongjing.put(4,"值班");
        workplanToZhangZhongjing.put(5,"不值班");
        workplanToZhangZhongjing.put(6,"不值班");
        workplanToZhangZhongjing.put(7,"值班");
        inPatientDoctorTable.get(4).setWorkplan(workplanToZhangZhongjing);

    }
    //初始化病床排队列表
    public static void createLineTable(){
        for(int i = 0; i < 5; i++){
            Line line = new Line();
            ArrayList<String> ID = new ArrayList<>();
            HospitalBed hospitalBed = new HospitalBed();
            hospitalBed.setDepartment(departmentTable.get(i));
            HashMap<String, Integer> ICU10 = new HashMap<>();
            //ICU10.put("ICU", 0);
            ICU10.put("普通", 0);
            hospitalBed.setCategory(ICU10);
            line.setId(ID);
            line.setHospitalBed(hospitalBed);
            line.setRoom("普通");
            lineTable.add(line);
            Line line1 = new Line();
            ArrayList<String> ID1 = new ArrayList<>();
            hospitalBed.setDepartment(departmentTable.get(i));
            ICU10.put("ICU", 0);
            hospitalBed.setCategory(ICU10);
            line1.setId(ID1);
            line1.setHospitalBed(hospitalBed);
            line1.setRoom("ICU");
            lineTable.add(line1);
        }
    }
    //初始化病床数量
    public static void createHospitalBed(){
        for(int i = 0; i < 5; i++){
            HospitalBed hospitalBed = new HospitalBed();
            hospitalBed.setDepartment(departmentTable.get(i));
            hospitalBedTable.add(hospitalBed);
        }

        HashMap<String,Integer> ICU1 = new HashMap<>();
        ICU1.put("ICU",1);ICU1.put("普通",20);
        hospitalBedTable.get(0).setCategory(ICU1);


        HashMap<String,Integer> ICU2 = new HashMap<>();
        ICU2.put("ICU",2);ICU2.put("普通",25);
        hospitalBedTable.get(1).setCategory(ICU2);

        HashMap<String,Integer> ICU3 = new HashMap<>();
        ICU3.put("ICU",3);ICU3.put("普通",15);
        hospitalBedTable.get(2).setCategory(ICU3);


        HashMap<String,Integer> ICU4 = new HashMap<>();
        ICU4.put("ICU",3);ICU4.put("普通",13);
        hospitalBedTable.get(03).setCategory(ICU4);

        HashMap<String,Integer> ICU5 = new HashMap<>();
        ICU5.put("ICU",4);ICU5.put("普通",20);
        hospitalBedTable.get(4).setCategory(ICU5);

    }
    //初始化住院护士信息
    public static void createInPatientTable(){
        for (int i = 0; i < 5; i++) {
            InPatientNurse inPatientNurse = new InPatientNurse();
            inPatientNurse.setId("300"+i);
            inPatientNurse.setAccount("300"+i);
            inPatientNurse.setPassword("300"+i);
            inPatientNurseTable.add(inPatientNurse);
        }
        inPatientNurseTable.get(0).setName("刘");
        inPatientNurseTable.get(1).setName("毕");
        inPatientNurseTable.get(2).setName("张");
        inPatientNurseTable.get(3).setName("聂");
        inPatientNurseTable.get(4).setName("潘");
    }
    //创建门诊医生表，并初始化信息
    public static void creatDoctorTable(){
        for (int i=0;i<5;i++){
            Doctor doctor = new Doctor();
            doctor.setId("200"+i);
            doctor.setAccount("200"+i);
            doctor.setPassword("200"+i);

            doctorTable.add(doctor);
        }
        //获取第0个数据，赋值
        doctorTable.get(0).setName("扁鹊");
        //创建部门
        doctorTable.get(0).setDepartment(departmentTable.get(0));
        doctorTable.get(0).setGrade("初级医师");
        doctorTable.get(0).setCall("123456");
        HashMap<Integer,String> workplanToBianQue = new HashMap<>();
        workplanToBianQue.put(1,"坐诊");
        workplanToBianQue.put(2,"");
        workplanToBianQue.put(3,"坐诊");
        workplanToBianQue.put(4,"坐诊");
        workplanToBianQue.put(5,"");
        workplanToBianQue.put(6,"");
        workplanToBianQue.put(7,"坐诊");
        doctorTable.get(0).setWorkplan(workplanToBianQue);

        //获取第1个数据，赋值
        doctorTable.get(1).setName("孙思邈");
        //创建部门
        doctorTable.get(1).setDepartment(departmentTable.get(1));
        doctorTable.get(1).setGrade("主治医师");
        doctorTable.get(1).setCall("123457");
        HashMap<Integer,String> workplanToSunSimiao = new HashMap<>();
        workplanToSunSimiao.put(1,"");
        workplanToSunSimiao.put(2,"坐诊");
        workplanToSunSimiao.put(3,"坐诊");
        workplanToSunSimiao.put(4,"坐诊");
        workplanToSunSimiao.put(5,"");
        workplanToSunSimiao.put(6,"");
        workplanToSunSimiao.put(7,"");
        doctorTable.get(1).setWorkplan(workplanToSunSimiao);

        //获取第2个数据，赋值
        doctorTable.get(2).setName("李时珍");
        //创建部门
        doctorTable.get(2).setDepartment(departmentTable.get(2));
        doctorTable.get(2).setGrade("副主任医生");
        doctorTable.get(2).setCall("1234568");
        HashMap<Integer,String> workplanLiShizhen = new HashMap<>();
        workplanLiShizhen.put(1,"坐诊");
        workplanLiShizhen.put(2,"坐诊");
        workplanLiShizhen.put(3,"");
        workplanLiShizhen.put(4,"坐诊");
        workplanLiShizhen.put(5,"坐诊");
        workplanLiShizhen.put(6,"");
        workplanLiShizhen.put(7,"");
        doctorTable.get(2).setWorkplan(workplanLiShizhen);

        //获取第3个数据，赋值
        doctorTable.get(3).setName("华佗");
        //创建部门
        doctorTable.get(3).setDepartment(departmentTable.get(3));
        doctorTable.get(3).setGrade("专家");
        doctorTable.get(3).setCall("123459");
        HashMap<Integer,String> workplanToHuaTuo = new HashMap<>();
        workplanToHuaTuo.put(1,"");
        workplanToHuaTuo.put(2,"");
        workplanToHuaTuo.put(3,"坐诊");
        workplanToHuaTuo.put(4,"坐诊");
        workplanToHuaTuo.put(5,"坐诊");
        workplanToHuaTuo.put(6,"坐诊");
        workplanToHuaTuo.put(7,"坐诊");
        doctorTable.get(3).setWorkplan(workplanToHuaTuo);

        //获取第4个数据，赋值
        doctorTable.get(4).setName("张仲景");
        //创建部门
        doctorTable.get(4).setDepartment(departmentTable.get(4));
        doctorTable.get(4).setGrade("专家");
        doctorTable.get(4).setCall("123450");
        HashMap<Integer,String> workplanToZhangZhongjing = new HashMap<>();
        workplanToZhangZhongjing.put(1,"坐诊");
        workplanToZhangZhongjing.put(2,"");
        workplanToZhangZhongjing.put(3,"坐诊");
        workplanToZhangZhongjing.put(4,"坐诊");
        workplanToZhangZhongjing.put(5,"坐诊");
        workplanToZhangZhongjing.put(6,"");
        workplanToZhangZhongjing.put(7,"");
        doctorTable.get(4).setWorkplan(workplanToZhangZhongjing);
    }
    //创建科室信息表，并创建初始数据
    public static void createDepartmentTable(){
        //创建科室对象
        Department department01 = new Department();
        department01.setDid(1);
        department01.setName("呼吸内科");
        //将对象放入departmentTable对象中
        departmentTable.add(department01);

        //创建科室对象
        Department department02 = new Department();
        department02.setDid(2);
        department02.setName("儿科");
        //将对象放入departmentTable对象中
        departmentTable.add(department02);

        //创建科室对象
        Department department03 = new Department();
        department03.setDid(3);
        department03.setName("骨科");
        //将对象放入departmentTable对象中
        departmentTable.add(department03);

        //创建科室对象
        Department department04 = new Department();
        department04.setDid(4);
        department04.setName("神经内科");
        //将对象放入departmentTable对象中
        departmentTable.add(department04);

        //创建科室对象
        Department department05 = new Department();
        department05.setDid(5);
        department05.setName("耳鼻喉科");
        //将对象放入departmentTable对象中
        departmentTable.add(department05);
    }

    //创建挂号员信息表，并创建假数据
    public static void createRegistorTable() {
        for (int i = 0; i < 5; i++) {
            Register registor = new Register();
            registor.setId("100"+i);
            registor.setAccount("100"+i);
            registor.setPassword("100"+i);
            registor.setName("佩奇"+i);
            registerTable.add(registor);
        }
    }
}
