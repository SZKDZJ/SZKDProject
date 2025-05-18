/*
	停车场模拟：
	利用栈实现单道停车场，也就是该停车场先进来的车只能最后出，
	如果某辆车想出车道，必须先把其前面的车先退出栈，等该车开走，再将之前的车压入栈。
	输入文件如附件文件中data.txt所示，其中格式如：“COOLONE arrives”，表示COOLONE的车到达；
	输出如文件output.txt所示，其中格式为：“COOLONE was moved 0 times while it was here”，表示该车在离开之前没有移动过。
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#define MAXSIZE 5 // 停车场容量

using namespace std;

// 定义车辆类
class Car {
private:
    string car_name; 
    int times;        

public:
    // 构造函数
    Car(string name = "", int t = 0) : car_name(name), times(t) {}
    // 获取车名
    string getCarName() const {
        return car_name;
    }
    // 设置车名
    void setCarName(const string& name) {
        car_name = name;
    }
    // 获取被移动次数
    int getTimes() const {
        return times;
    }
    // 设置被移动次数
    void setTimes(int t) {
        times = t;
    }
    // 增加移动次数
    void incrementTimes() {
        times++;
    }
};

// 定义栈类
class CarStack {
private:
    Car* stackArray; // 栈数组
    int top;         // 栈顶指针
    int capacity;    // 栈的容量

public:
    // 构造函数，初始化栈
    CarStack(int size = MAXSIZE) : capacity(size), top(-1) {
        stackArray = new Car[capacity];
        if (!stackArray) {
            cout << "内存分配失败\n";
            exit(EXIT_FAILURE);
        }
    }

    // 析构函数，释放内存
    ~CarStack() {
        delete[] stackArray;
    }

    // 入栈操作
    bool push(const Car& car) {
        if (top == capacity - 1) {
            // 如果栈已满
            cout << "停车场已满，无法入栈 " << car.getCarName() << endl;
            return false;
        }
        else {
            stackArray[++top] = car;  // 将车辆压入栈中
            return true;
        }
    }

    // 出栈操作
    Car pop() {
        if (top == -1) {
            cout << "停车场空，无法出栈\n";
            exit(EXIT_FAILURE);  // 栈空时无法出栈，终止程序
        }
        else {
            return stackArray[top--];  // 返回栈顶元素并将栈顶指针向下移动
        }
    }

    // 查看栈顶元素
    Car peek() {
        if (top == -1) {
            cout << "停车场空\n";
            exit(EXIT_FAILURE);  // 栈空时无法查看栈顶元素，终止程序
        }
        else {
            return stackArray[top];
        }
    }

    // 判断栈是否为空
    bool isEmpty() {
        return top == -1;
    }

    // 判断栈是否已满
    bool isFull() {
        return top == capacity - 1;
    }

    // 获取栈大小
    int size() {
        return top + 1;
    }
};

// 停车场类（使用汽车栈实现）
class ParkingLot {
private:
    CarStack stack;        
    vector<string> output_log; // 输出日志

public:
    ParkingLot(int cap = MAXSIZE) : stack(cap) {}

    // 车辆到达
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

    // 车辆离开
    void carDeparts(const string& car_name) {
        CarStack temp_stack(MAXSIZE);  // 临时栈存放中间车辆
        bool found = false;

        // 出栈查找车辆
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
                top_car.incrementTimes(); // 更新移动车辆的移动次数
                temp_stack.push(top_car);
            }
        }

        if (!found) {
            string message = "Error: " + car_name + " was not found in the parking lot.";
            //output_log.push_back(message);
            cout << message << endl;
        }

        // 将临时栈中的车辆重新压回停车场
        while (!temp_stack.isEmpty()) {
            stack.push(temp_stack.pop());
        }
    }

    // 输出所有日志到文件
    void writeLog(const string& output_file) {
        ofstream file(output_file);
        if (file.is_open()) {
            for (const auto& log : output_log) {
                file << log << endl;
            }
            cout << "所有车辆信息已写入文件 " << output_file << endl;
        }
        else {
            cout << "无法打开输出文件 " << output_file << endl;
        }
        file.close();
    }

    // 统计所有未离开的车辆
    void summarizeRemainingCars() {
        while (!stack.isEmpty()) {
            Car remaining_car = stack.pop();
            string message = remaining_car.getCarName() + " was moved " + to_string(remaining_car.getTimes()) + " times while it was here.";
            output_log.push_back(message);
            cout << message << endl;
        }
    }
};

// 单道停车场模拟
void simulateParking(const string& input_file, const string& output_file) {
    ParkingLot parking_lot; // 创建停车场对象

    ifstream infile(input_file);
    if (!infile.is_open()) {
        cout << "无法打开输入文件 " << input_file << endl;
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

    // 统计未离开的车辆并写入文件
    parking_lot.summarizeRemainingCars();
    parking_lot.writeLog(output_file);
}

int main() {
    // 输入输出文件名
    string input_file = "/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment2/data.txt";
    string output_file = "output.txt";

    // 模拟停车场操作
    simulateParking(input_file, output_file);

    return 0;
}