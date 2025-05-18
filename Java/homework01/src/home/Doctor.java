package home;

/**
 * 医生类：用于描述医生信息
 * 作者：张子琪
 * 时间：0721
 */

public class Doctor {
    private String account;
    private String password;
    private String name;
    private String depart;
    private String grade;

    public String getAccount() {
        return account;
    }

    public String getPassword() {
        return password;
    }

    public String getName() {
        return name;
    }

    public String getDepart() {
        return depart;
    }

    public String getGrade() {
        return grade;
    }

    public void setAccount(String account) {
        this.account = account;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setDepart(String depart) {
        this.depart = depart;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    @Override
    public String toString() {
        return "Doctor{" +
                "account='" + account + '\'' +
                ", password='" + password + '\'' +
                ", name='" + name + '\'' +
                ", depart='" + depart + '\'' +
                ", grade='" + grade + '\'' +
                '}';
    }
}
