package home;

/**
 * 患者类：用于描述患者信息
 * 作者：张子琪
 * 时间：0721
 */

public class Patient {
    private String id;
    private String name;
    private String general;
    private int age;
    private String depart;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getGeneral() {
        return general;
    }

    public void setGeneral(String general) {
        this.general = general;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getDepart() {
        return depart;
    }

    public void setDepart(String depart) {
        this.depart = depart;
    }

    @Override
    public String toString() {
        return "Patient{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", general='" + general + '\'' +
                ", age='" + age + '\'' +
                ", depart='" + depart + '\'' +
                '}';
    }
}
