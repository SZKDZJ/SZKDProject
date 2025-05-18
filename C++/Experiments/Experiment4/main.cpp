/*
（1）完成图基本操作；
	并将下图中图数据存储，其中边的数据在文件services.txt。
	格式如：“Lisbon Madrid 75 450”，表示Lisbon到Madrid距离为450，乘车费用为75。
（2）题目如下：
	输入起始城市和终点城市，可以给出两个城市的最小费用路线，并将路线给出
*/

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#define MAX_CITIES 100  // 假设最多100个城市
#define INF 1000000000 

// 节点类，表示图中的每个城市
class Node {
private:
    string name;  // 城市名称
    int cost;     // 费用
    int distance; // 距离
    Node* next;   // 指向下一个相邻城市的指针

public:
    Node(const string& city, int c, int d) : name(city), cost(c), distance(d), next(nullptr) {}

    // Getter 和 Setter 方法
    string getName() const { return name; }
    void setName(const string& cityName) { name = cityName; }

    int getCost() const { return cost; }
    void setCost(int c) { cost = c; }

    int getDistance() const { return distance; }
    void setDistance(int d) { distance = d; }

    Node* getNext() const { return next; }
    void setNext(Node* n) { next = n; }
};

// 图类，包含邻接表、Dijkstra算法
class Graph {
private:
    struct CityNode {
        string name;
        Node* neighbors;  // 相邻城市的链表
    } cities[MAX_CITIES];

    int cityCount;

public:
    Graph() {
        cityCount = 0;
        for (int i = 0; i < MAX_CITIES; ++i) {
            cities[i].name = "";
            cities[i].neighbors = nullptr;
        }
    }

    // 析构函数，释放动态分配的内存
    ~Graph() {
        for (int i = 0; i < cityCount; ++i) {
            Node* current = cities[i].neighbors;
            while (current != nullptr) {
                Node* temp = current;
                current = current->getNext();
                delete temp;  // 释放内存
            }
        }
    }

    // 查找城市索引
    int findCityIndex(const string& cityName) {
        for (int i = 0; i < cityCount; ++i) {
            if (cities[i].name == cityName) {
                return i;
            }
        }
        return -1;
    }

    // 添加城市
    void addCity(const string& cityName) {
        if (findCityIndex(cityName) == -1) {
            cities[cityCount++].name = cityName;
        }
    }

    // 添加边
    void addEdge(const string& city1, const string& city2, int cost, int distance) {
        int index1 = findCityIndex(city1);
        int index2 = findCityIndex(city2);

        if (index1 == -1) {
            addCity(city1);
            index1 = cityCount - 1;
        }
        if (index2 == -1) {
            addCity(city2);
            index2 = cityCount - 1;
        }

        Node* newNode = new Node(city2, cost, distance);
        newNode->setNext(cities[index1].neighbors);
        cities[index1].neighbors = newNode;
    }

    // Dijkstra算法计算最小费用路径
    pair<int, pair<int, string>> findMinCostPath(const string& start, const string& end) {
        bool visited[MAX_CITIES] = { false };
        int minCost[MAX_CITIES];
        int minDistance[MAX_CITIES];
        string path[MAX_CITIES];

        // 初始化
        int startIndex = findCityIndex(start);
        int endIndex = findCityIndex(end);

        if (startIndex == -1 || endIndex == -1) {
            return { -1, {-1, ""} }; // 如果起点或终点不存在，返回错误
        }

        for (int i = 0; i < cityCount; ++i) {
            minCost[i] = INF;
            minDistance[i] = INF;
            path[i] = "";
        }
        minCost[startIndex] = 0;
        minDistance[startIndex] = 0;
        path[startIndex] = start;

        while (true) {
            int minCostCity = -1;
            int currentCost = INF;

            // 找到当前未访问的最小费用的城市
            for (int i = 0; i < cityCount; ++i) {
                if (!visited[i] && minCost[i] < currentCost) {
                    currentCost = minCost[i];
                    minCostCity = i;
                }
            }

            if (minCostCity == -1) break; // 没有未访问的城市，结束

            visited[minCostCity] = true;

            // 如果找到了终点，返回结果
            if (minCostCity == endIndex) {
                return { minCost[minCostCity], {minDistance[minCostCity], path[minCostCity]} };
            }

            // 遍历当前城市的邻接城市
            Node* neighbor = cities[minCostCity].neighbors;
            while (neighbor != nullptr) {
                int neighborIndex = findCityIndex(neighbor->getName());
                int newCost = minCost[minCostCity] + neighbor->getCost();
                int newDistance = minDistance[minCostCity] + neighbor->getDistance();

                if (!visited[neighborIndex] && newCost < minCost[neighborIndex]) {
                    minCost[neighborIndex] = newCost;
                    minDistance[neighborIndex] = newDistance;
                    path[neighborIndex] = path[minCostCity] + " -> " + neighbor->getName();
                }
                neighbor = neighbor->getNext();
            }
        }

        return { -1, {-1, ""} }; // 未找到路径
    }
};

// 主程序
int main() {
    Graph graph;
    string filename = "/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment4/services.txt";

    // 从文件加载数据
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "无法打开文件: " << filename << endl;
        return 1;
    }

    string city1, city2;
    int cost, distance;
    while (file >> city1 >> city2 >> cost >> distance) {
        graph.addEdge(city1, city2, cost, distance);
    }
    file.close();

    // 获取起始城市和终点城市
    string startCity, endCity;
    cout << "请输入起始城市: ";
    cin >> startCity;
    cout << "请输入终点城市: ";
    cin >> endCity;

    // 计算最小费用路径
    auto result = graph.findMinCostPath(startCity, endCity);

    if (result.first != -1) {
        cout << "最小费用: " << result.first << endl;
        cout << "最短距离: " << result.second.first << endl;
        cout << "路线: " << result.second.second << endl;
    }
    else {
        cout << "无法找到从 " << startCity << " 到 " << endCity << " 的路径。" << endl;
    }

    return 0;
}