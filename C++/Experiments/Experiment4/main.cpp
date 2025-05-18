/*
��1�����ͼ����������
	������ͼ��ͼ���ݴ洢�����бߵ��������ļ�services.txt��
	��ʽ�磺��Lisbon Madrid 75 450������ʾLisbon��Madrid����Ϊ450���˳�����Ϊ75��
��2����Ŀ���£�
	������ʼ���к��յ���У����Ը����������е���С����·�ߣ�����·�߸���
*/

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#define MAX_CITIES 100  // �������100������
#define INF 1000000000 

// �ڵ��࣬��ʾͼ�е�ÿ������
class Node {
private:
    string name;  // ��������
    int cost;     // ����
    int distance; // ����
    Node* next;   // ָ����һ�����ڳ��е�ָ��

public:
    Node(const string& city, int c, int d) : name(city), cost(c), distance(d), next(nullptr) {}

    // Getter �� Setter ����
    string getName() const { return name; }
    void setName(const string& cityName) { name = cityName; }

    int getCost() const { return cost; }
    void setCost(int c) { cost = c; }

    int getDistance() const { return distance; }
    void setDistance(int d) { distance = d; }

    Node* getNext() const { return next; }
    void setNext(Node* n) { next = n; }
};

// ͼ�࣬�����ڽӱ�Dijkstra�㷨
class Graph {
private:
    struct CityNode {
        string name;
        Node* neighbors;  // ���ڳ��е�����
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

    // �����������ͷŶ�̬������ڴ�
    ~Graph() {
        for (int i = 0; i < cityCount; ++i) {
            Node* current = cities[i].neighbors;
            while (current != nullptr) {
                Node* temp = current;
                current = current->getNext();
                delete temp;  // �ͷ��ڴ�
            }
        }
    }

    // ���ҳ�������
    int findCityIndex(const string& cityName) {
        for (int i = 0; i < cityCount; ++i) {
            if (cities[i].name == cityName) {
                return i;
            }
        }
        return -1;
    }

    // ��ӳ���
    void addCity(const string& cityName) {
        if (findCityIndex(cityName) == -1) {
            cities[cityCount++].name = cityName;
        }
    }

    // ��ӱ�
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

    // Dijkstra�㷨������С����·��
    pair<int, pair<int, string>> findMinCostPath(const string& start, const string& end) {
        bool visited[MAX_CITIES] = { false };
        int minCost[MAX_CITIES];
        int minDistance[MAX_CITIES];
        string path[MAX_CITIES];

        // ��ʼ��
        int startIndex = findCityIndex(start);
        int endIndex = findCityIndex(end);

        if (startIndex == -1 || endIndex == -1) {
            return { -1, {-1, ""} }; // ��������յ㲻���ڣ����ش���
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

            // �ҵ���ǰδ���ʵ���С���õĳ���
            for (int i = 0; i < cityCount; ++i) {
                if (!visited[i] && minCost[i] < currentCost) {
                    currentCost = minCost[i];
                    minCostCity = i;
                }
            }

            if (minCostCity == -1) break; // û��δ���ʵĳ��У�����

            visited[minCostCity] = true;

            // ����ҵ����յ㣬���ؽ��
            if (minCostCity == endIndex) {
                return { minCost[minCostCity], {minDistance[minCostCity], path[minCostCity]} };
            }

            // ������ǰ���е��ڽӳ���
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

        return { -1, {-1, ""} }; // δ�ҵ�·��
    }
};

// ������
int main() {
    Graph graph;
    string filename = "/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment4/services.txt";

    // ���ļ���������
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "�޷����ļ�: " << filename << endl;
        return 1;
    }

    string city1, city2;
    int cost, distance;
    while (file >> city1 >> city2 >> cost >> distance) {
        graph.addEdge(city1, city2, cost, distance);
    }
    file.close();

    // ��ȡ��ʼ���к��յ����
    string startCity, endCity;
    cout << "��������ʼ����: ";
    cin >> startCity;
    cout << "�������յ����: ";
    cin >> endCity;

    // ������С����·��
    auto result = graph.findMinCostPath(startCity, endCity);

    if (result.first != -1) {
        cout << "��С����: " << result.first << endl;
        cout << "��̾���: " << result.second.first << endl;
        cout << "·��: " << result.second.second << endl;
    }
    else {
        cout << "�޷��ҵ��� " << startCity << " �� " << endCity << " ��·����" << endl;
    }

    return 0;
}