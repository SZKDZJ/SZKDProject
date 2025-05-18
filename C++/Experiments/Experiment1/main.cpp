#include <iostream>
#include <string>
#include<algorithm>
#include<vector>
using namespace std;

// 定义学生节点
typedef struct student_Node {
    string name;
    string ID;
    float Math;
    float Chinese;
    float English;
    struct student_Node* next;
} student_Node;

// 定义学生链表
typedef struct studentList {
    student_Node* head_student;
    student_Node* tail_student;
    int student_length;
} *student_List;

// 初始化链表
student_List Init_StudentList() {
    student_List L = new studentList();
    if (!L) {
        cout << "初始化失败\n";
        exit(EXIT_FAILURE);
    }
    L->head_student = nullptr;
    L->tail_student = nullptr;
    L->student_length = 0;
    return L;
}

// 申请学生节点
student_Node* Apply_StudentNode() {
    student_Node* node = new student_Node();
    if (!node) {
        cout << "学生节点内存分配失败\n";
        exit(EXIT_FAILURE);
    }

    node->next = nullptr;
    cout << "请输入学生姓名：\n";
    cin >> node->name;
    cout << "请输入学生学号：\n";
    cin >> node->ID;
    cout << "请输入学生语文成绩：\n";
    cin >> node->Chinese;
    cout << "请输入学生数学成绩：\n";
    cin >> node->Math;
    cout << "请输入学生英语成绩：\n";
    cin >> node->English;

    return node;
}

// 尾插法添加学生
void Add_StudentList(student_List L) {
    student_Node* node = Apply_StudentNode();
    if (L->head_student != nullptr) {
        L->tail_student->next = node;
        L->tail_student = node;
    }
    else {
        L->head_student = node;
        L->tail_student = node;
    }
    L->student_length++;
    cout << "添加成功！\n";
}

//修改学生信息操作
student_Node* Modify_Student_opt(int choose, student_Node* node) {
    if (choose == 1) {
        cout << "学生姓名改为：\n";
        cin >> node->name;
    }
    else if (choose == 2) {
        cout << "学生ID改为：\n";
        cin >> node->ID;
    }
    else if (choose == 3) {
        cout << "学生语文成绩改为：\n";
        cin >> node->Chinese;
    }
    else if (choose == 4) {
        cout << "学生数学成绩改为：\n";
        cin >> node->Math;
    }
    else if (choose == 5) {
        cout << "学生英语成绩改为：\n";
        cin >> node->English;
    }
    
    return node;
}

//修改学生信息
void Modify_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息。\n";
        return;
    }

    string modifyID;
    cout << "请输入要修改的学生学号：\n";
    cin >> modifyID;

    student_Node* current = L->head_student;
    while (current) {
        if (current->ID == modifyID) {
            cout << "---------------------\n";
            cout << "学生姓名: " << current->name << "\n";
            cout << "学号: " << current->ID << "\n";
            cout << "语文成绩: " << current->Chinese << "\n";
            cout << "数学成绩: " << current->Math << "\n";
            cout << "英语成绩: " << current->English << "\n";
            cout << "---------------------\n";
            cout << "请输入要修改的信息：\n";
            cout << "1、学生姓名 \n";
            cout << "2、学号 \n";
            cout << "3、语文成绩 \n";
            cout << "4、数学成绩 \n";
            cout << "5、英语成绩 \n";
            //cout << "6、退出 \n";

            int choose;
            cin >> choose;
            current = Modify_Student_opt(choose,current);
            cout << "-----修改后的信息-----\n";
            cout << "学生姓名: " << current->name << "\n";
            cout << "学号: " << current->ID << "\n";
            cout << "语文成绩: " << current->Chinese << "\n";
            cout << "数学成绩: " << current->Math << "\n";
            cout << "英语成绩: " << current->English << "\n";
            cout << "------修改成功-------\n";
            return;
        }
        current = current->next;
    }

    cout << "未找到学号为 " << modifyID << " 的学生。\n";
}

// 查询学生信息
void Search_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息。\n";
        return;
    }

    string searchID;
    cout << "请输入要查询的学生学号：\n";
    cin >> searchID;

    student_Node* current = L->head_student;
    while (current) {
        if (current->ID == searchID) {
            cout << "---------------------\n";
            cout << "学生姓名: " << current->name << "\n";
            cout << "学号: " << current->ID << "\n";
            cout << "语文成绩: " << current->Chinese << "\n";
            cout << "数学成绩: " << current->Math << "\n";
            cout << "英语成绩: " << current->English << "\n";
            return;
        }
        current = current->next;
    }

    cout << "未找到学号为 " << searchID << " 的学生。\n";
}

// 打印所有学生信息
void Print_AllStudents(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息。\n";
        return;
    }

    student_Node* current = L->head_student;
    while (current) {
        cout << "学生姓名: " << current->name << "\n";
        cout << "学号: " << current->ID << "\n";
        cout << "语文成绩: " << current->Chinese << "\n";
        cout << "数学成绩: " << current->Math << "\n";
        cout << "英语成绩: " << current->English << "\n";
        cout << "---------------------\n";
        current = current->next;
    }
}

// 查询全科总分统计
void Query_TotalScores(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息，无法进行查询。\n";
        return;
    }

    float maxTotal = -1;
    float minTotal = 301;
    float totalAllScores = 0;
    int studentCount = 0;

    vector<pair<string, float>> totalScores; // 用于排名

    student_Node* current = L->head_student;
    student_Node* max = L->head_student;
    student_Node* min = L->head_student;

    while (current) {
        float totalScore = current->Chinese + current->Math + current->English;

        totalScores.push_back({ current->name, totalScore });

        if (totalScore > maxTotal) {
            maxTotal = totalScore;
            max = current;
        }
        if (totalScore < minTotal) {
            minTotal = totalScore;
            min = current;
        }
        totalAllScores += totalScore;
        studentCount++;
        current = current->next;
    }

    float averageTotal = totalAllScores / studentCount;

    cout << "全科总分统计结果：\n";
    cout << "最高总分: " << maxTotal << "      学生姓名:" << max->name << "      学生ID:" << max->ID << "\n";
    cout << "最低总分: " << minTotal << "      学生姓名:" << min->name << "      学生ID:" << min->ID << "\n";
    cout << "平均总分: " << averageTotal << "\n";

    // 排名
    sort(totalScores.begin(), totalScores.end(),
        [](const pair<string, float>& a, const pair<string, float>& b) {
            return a.second > b.second;
        });

    cout << "总分排名：\n";
    for (int i = 0; i < totalScores.size(); i++) {
        cout << i + 1 << ". " << totalScores[i].first << " - " << totalScores[i].second << "\n";
    }
}

//删除学生节点
void Delete_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息，无法删除。\n";
        return;
    }

    string deleteID;
    cout << "请输入要删除的学生学号：\n";
    cin >> deleteID;

    student_Node* current = L->head_student;
    student_Node* prev = nullptr;

    while (current) {
        if (current->ID == deleteID) {
            // 如果是头节点
            if (current == L->head_student) {
                L->head_student = current->next;
                if (current == L->tail_student) { // 如果链表只有一个节点
                    L->tail_student = nullptr;
                }
            }
            else { // 如果是中间或尾节点
                prev->next = current->next;
                if (current == L->tail_student) {
                    L->tail_student = prev; // 更新尾节点
                }
            }

            delete current; // 释放内存
            L->student_length--;
            cout << "学号为 " << deleteID << " 的学生信息已删除。\n";
            return;
        }
        prev = current;
        current = current->next;
    }

    cout << "未找到学号为 " << deleteID << " 的学生。\n";
}

// 释放链表内存
void Free_StudentList(student_List L) {
    student_Node* current = L->head_student;
    while (current) {
        student_Node* temp = current;
        current = current->next;
        delete temp;
    }
    delete L;
}

//统计某门课的最高分、最低分、平均分情况
// 查询单科成绩
void Query_SubjectScores(student_List L) {
    if (L->student_length == 0) {
        cout << "当前没有学生信息，无法进行查询。\n";
        return;
    }

    int subjectChoice;
    cout << "请选择查询科目：\n";
    cout << "1. 语文\n";
    cout << "2. 数学\n";
    cout << "3. 英语\n";
    cin >> subjectChoice;

    if (subjectChoice < 1 || subjectChoice > 3) {
        cout << "输入无效，请重新选择。\n";
        return;
    }

    float maxScore = -1;
    float minScore = 151;
    float totalScore = 0;
    int studentCount = 0;

    student_Node* current = L->head_student;
    student_Node* max = L->head_student;
    student_Node* min = L->head_student;
    vector<pair<string, float>> subjectScores; 

    while (current) {
        float score;
        if (subjectChoice == 1) {
            score = current->Chinese;
        }
        else if (subjectChoice == 2) {
            score = current->Math;
        }
        else if (subjectChoice == 3) {
            score = current->English;
        }

        subjectScores.push_back({ current->name, score });

        if (score > maxScore) {
            maxScore = score;
            max = current;
        }
        if (score < minScore) {
            minScore = score;
            min = current;
        }
        totalScore += score;
        studentCount++;
        current = current->next;
    }

    float averageScore = totalScore / studentCount;
    string subjectName = (subjectChoice == 1) ? "语文" : (subjectChoice == 2) ? "数学" : "英语";

    cout << subjectName << "科目统计结果：\n";
    cout << "最高分: " << maxScore << "      学生姓名:" << max->name << "      学生ID:" << max->ID << "\n";
    cout << "最低分: " << minScore << "      学生姓名:" << min->name << "      学生ID:" << min->ID << "\n";
    cout << "平均分: " << averageScore << "\n";

    // 排名
    sort(subjectScores.begin(), subjectScores.end(),
        [](const pair<string, float>& a, const pair<string, float>& b) {
            return a.second > b.second;
        });

    cout << subjectName << "成绩排名：\n";
    for (int i = 0; i < subjectScores.size(); i++) {
        cout << i + 1 << ". " << subjectScores[i].first << " - " << subjectScores[i].second << "\n";
    }
}

// 主菜单操作
void main_menu(int choose, student_List L) {
    if (choose == 1) {
        // 添加学生
        Add_StudentList(L);
    }
    else if (choose == 2) {
        // 修改学生信息
        Modify_Student(L);
    }
    else if (choose == 3) {
        // 查询学生信息
        Search_Student(L);
    }
    else if (choose == 4) {
        // 查询科目成绩
        Query_SubjectScores(L);
    }
    else if (choose == 5) {
        // 查询全科总分成绩
        Query_TotalScores(L);
    }
    else if (choose == 6) {
        // 打印所有学生信息
        Print_AllStudents(L);
    }
    else if (choose == 7) {
        // 删除学生
        Delete_Student(L);
    }
}

// 主函数
int main() {
    student_List L_student = Init_StudentList();
    int choose = 0;

    while (true) {
        cout << "----请选择操作：-----\n";
        cout << "    1、添加学生\n";
        cout << "    2、修改学生信息\n";
        cout << "    3、查询学生信息\n";
        cout << "    4、查询科目成绩\n";
        cout << "    5、查询全科总分成绩\n";
        cout << "    6、打印所有学生信息\n";
        cout << "    7、删除学生\n";
        cout << "    8、退出\n";

        cin >> choose;

        if (choose == 8) {
            cout << "----学生成绩统计系统已退出--------\n";
            break;
        }
        else {
            main_menu(choose, L_student);
        }
    }

    Free_StudentList(L_student);
    return 0;
}