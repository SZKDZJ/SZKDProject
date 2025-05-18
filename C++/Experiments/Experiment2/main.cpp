/*
	ͣ����ģ�⣺
	����ջʵ�ֵ���ͣ������Ҳ���Ǹ�ͣ�����Ƚ����ĳ�ֻ��������
	���ĳ������������������Ȱ���ǰ��ĳ����˳�ջ���ȸó����ߣ��ٽ�֮ǰ�ĳ�ѹ��ջ��
	�����ļ��總���ļ���data.txt��ʾ�����и�ʽ�磺��COOLONE arrives������ʾCOOLONE�ĳ����
	������ļ�output.txt��ʾ�����и�ʽΪ����COOLONE was moved 0 times while it was here������ʾ�ó����뿪֮ǰû���ƶ�����
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#define MAXSIZE 5 // ͣ��������

using namespace std;

// ���峵����
class Car {
private:
    string car_name; 
    int times;        

public:
    // ���캯��
    Car(string name = "", int t = 0) : car_name(name), times(t) {}
    // ��ȡ����
    string getCarName() const {
        return car_name;
    }
    // ���ó���
    void setCarName(const string& name) {
        car_name = name;
    }
    // ��ȡ���ƶ�����
    int getTimes() const {
        return times;
    }
    // ���ñ��ƶ�����
    void setTimes(int t) {
        times = t;
    }
    // �����ƶ�����
    void incrementTimes() {
        times++;
    }
};

// ����ջ��
class CarStack {
private:
    Car* stackArray; // ջ����
    int top;         // ջ��ָ��
    int capacity;    // ջ������

public:
    // ���캯������ʼ��ջ
    CarStack(int size = MAXSIZE) : capacity(size), top(-1) {
        stackArray = new Car[capacity];
        if (!stackArray) {
            cout << "�ڴ����ʧ��\n";
            exit(EXIT_FAILURE);
        }
    }

    // �����������ͷ��ڴ�
    ~CarStack() {
        delete[] stackArray;
    }

    // ��ջ����
    bool push(const Car& car) {
        if (top == capacity - 1) {
            // ���ջ����
            cout << "ͣ�����������޷���ջ " << car.getCarName() << endl;
            return false;
        }
        else {
            stackArray[++top] = car;  // ������ѹ��ջ��
            return true;
        }
    }

    // ��ջ����
    Car pop() {
        if (top == -1) {
            cout << "ͣ�����գ��޷���ջ\n";
            exit(EXIT_FAILURE);  // ջ��ʱ�޷���ջ����ֹ����
        }
        else {
            return stackArray[top--];  // ����ջ��Ԫ�ز���ջ��ָ�������ƶ�
        }
    }

    // �鿴ջ��Ԫ��
    Car peek() {
        if (top == -1) {
            cout << "ͣ������\n";
            exit(EXIT_FAILURE);  // ջ��ʱ�޷��鿴ջ��Ԫ�أ���ֹ����
        }
        else {
            return stackArray[top];
        }
    }

    // �ж�ջ�Ƿ�Ϊ��
    bool isEmpty() {
        return top == -1;
    }

    // �ж�ջ�Ƿ�����
    bool isFull() {
        return top == capacity - 1;
    }

    // ��ȡջ��С
    int size() {
        return top + 1;
    }
};

// ͣ�����ࣨʹ������ջʵ�֣�
class ParkingLot {
private:
    CarStack stack;        
    vector<string> output_log; // �����־

public:
    ParkingLot(int cap = MAXSIZE) : stack(cap) {}

    // ��������
    void carArrives(const string& car_name) {
        if (stack.isFull()) {
            string message = "Sorry " + car_name + ", the lot is full";
            output_log.push_back(message);
            cout << message << endl;
        }
        else {
            stack.push(Car(car_name));
            string message = car_name + " entered the parking lot.";
            //output_log.push_back(message);
            cout << message << endl;
        }
    }

    // �����뿪
    void carDeparts(const string& car_name) {
        CarStack temp_stack(MAXSIZE);  // ��ʱջ����м䳵��
        bool found = false;

        // ��ջ���ҳ���
        while (!stack.isEmpty()) {
            Car top_car = stack.pop();

            if (top_car.getCarName() == car_name) {
                found = true;
                string message = car_name + " was moved " + to_string(top_car.getTimes()) + " times while it was here.";
                output_log.push_back(message);
                cout << message << endl;
                break;
            }
            else {
                top_car.incrementTimes(); // �����ƶ��������ƶ�����
                temp_stack.push(top_car);
            }
        }

        if (!found) {
            string message = "Error: " + car_name + " was not found in the parking lot.";
            //output_log.push_back(message);
            cout << message << endl;
        }

        // ����ʱջ�еĳ�������ѹ��ͣ����
        while (!temp_stack.isEmpty()) {
            stack.push(temp_stack.pop());
        }
    }

    // ���������־���ļ�
    void writeLog(const string& output_file) {
        ofstream file(output_file);
        if (file.is_open()) {
            for (const auto& log : output_log) {
                file << log << endl;
            }
            cout << "���г�����Ϣ��д���ļ� " << output_file << endl;
        }
        else {
            cout << "�޷�������ļ� " << output_file << endl;
        }
        file.close();
    }

    // ͳ������δ�뿪�ĳ���
    void summarizeRemainingCars() {
        while (!stack.isEmpty()) {
            Car remaining_car = stack.pop();
            string message = remaining_car.getCarName() + " was moved " + to_string(remaining_car.getTimes()) + " times while it was here.";
            output_log.push_back(message);
            cout << message << endl;
        }
    }
};

// ����ͣ����ģ��
void simulateParking(const string& input_file, const string& output_file) {
    ParkingLot parking_lot; // ����ͣ��������

    ifstream infile(input_file);
    if (!infile.is_open()) {
        cout << "�޷��������ļ� " << input_file << endl;
        return;
    }

    string line;
    while (getline(infile, line)) {
        if (line.find("arrives") != string::npos) {
            string car_name = line.substr(0, line.find(" "));
            parking_lot.carArrives(car_name);
        }
        else if (line.find("departs") != string::npos) {
            string car_name = line.substr(0, line.find(" "));
            parking_lot.carDeparts(car_name);
        }
    }
    infile.close();

    // ͳ��δ�뿪�ĳ�����д���ļ�
    parking_lot.summarizeRemainingCars();
    parking_lot.writeLog(output_file);
}

int main() {
    // ��������ļ���
    string input_file = "/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment2/data.txt";
    string output_file = "output.txt";

    // ģ��ͣ��������
    simulateParking(input_file, output_file);

    return 0;
}