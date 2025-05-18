#include <iostream>
#include <string>
#include<algorithm>
#include<vector>
using namespace std;

// ����ѧ���ڵ�
typedef struct student_Node {
    string name;
    string ID;
    float Math;
    float Chinese;
    float English;
    struct student_Node* next;
} student_Node;

// ����ѧ������
typedef struct studentList {
    student_Node* head_student;
    student_Node* tail_student;
    int student_length;
} *student_List;

// ��ʼ������
student_List Init_StudentList() {
    student_List L = new studentList();
    if (!L) {
        cout << "��ʼ��ʧ��\n";
        exit(EXIT_FAILURE);
    }
    L->head_student = nullptr;
    L->tail_student = nullptr;
    L->student_length = 0;
    return L;
}

// ����ѧ���ڵ�
student_Node* Apply_StudentNode() {
    student_Node* node = new student_Node();
    if (!node) {
        cout << "ѧ���ڵ��ڴ����ʧ��\n";
        exit(EXIT_FAILURE);
    }

    node->next = nullptr;
    cout << "������ѧ��������\n";
    cin >> node->name;
    cout << "������ѧ��ѧ�ţ�\n";
    cin >> node->ID;
    cout << "������ѧ�����ĳɼ���\n";
    cin >> node->Chinese;
    cout << "������ѧ����ѧ�ɼ���\n";
    cin >> node->Math;
    cout << "������ѧ��Ӣ��ɼ���\n";
    cin >> node->English;

    return node;
}

// β�巨���ѧ��
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
    cout << "��ӳɹ���\n";
}

//�޸�ѧ����Ϣ����
student_Node* Modify_Student_opt(int choose, student_Node* node) {
    if (choose == 1) {
        cout << "ѧ��������Ϊ��\n";
        cin >> node->name;
    }
    else if (choose == 2) {
        cout << "ѧ��ID��Ϊ��\n";
        cin >> node->ID;
    }
    else if (choose == 3) {
        cout << "ѧ�����ĳɼ���Ϊ��\n";
        cin >> node->Chinese;
    }
    else if (choose == 4) {
        cout << "ѧ����ѧ�ɼ���Ϊ��\n";
        cin >> node->Math;
    }
    else if (choose == 5) {
        cout << "ѧ��Ӣ��ɼ���Ϊ��\n";
        cin >> node->English;
    }
    
    return node;
}

//�޸�ѧ����Ϣ
void Modify_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ��\n";
        return;
    }

    string modifyID;
    cout << "������Ҫ�޸ĵ�ѧ��ѧ�ţ�\n";
    cin >> modifyID;

    student_Node* current = L->head_student;
    while (current) {
        if (current->ID == modifyID) {
            cout << "---------------------\n";
            cout << "ѧ������: " << current->name << "\n";
            cout << "ѧ��: " << current->ID << "\n";
            cout << "���ĳɼ�: " << current->Chinese << "\n";
            cout << "��ѧ�ɼ�: " << current->Math << "\n";
            cout << "Ӣ��ɼ�: " << current->English << "\n";
            cout << "---------------------\n";
            cout << "������Ҫ�޸ĵ���Ϣ��\n";
            cout << "1��ѧ������ \n";
            cout << "2��ѧ�� \n";
            cout << "3�����ĳɼ� \n";
            cout << "4����ѧ�ɼ� \n";
            cout << "5��Ӣ��ɼ� \n";
            //cout << "6���˳� \n";

            int choose;
            cin >> choose;
            current = Modify_Student_opt(choose,current);
            cout << "-----�޸ĺ����Ϣ-----\n";
            cout << "ѧ������: " << current->name << "\n";
            cout << "ѧ��: " << current->ID << "\n";
            cout << "���ĳɼ�: " << current->Chinese << "\n";
            cout << "��ѧ�ɼ�: " << current->Math << "\n";
            cout << "Ӣ��ɼ�: " << current->English << "\n";
            cout << "------�޸ĳɹ�-------\n";
            return;
        }
        current = current->next;
    }

    cout << "δ�ҵ�ѧ��Ϊ " << modifyID << " ��ѧ����\n";
}

// ��ѯѧ����Ϣ
void Search_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ��\n";
        return;
    }

    string searchID;
    cout << "������Ҫ��ѯ��ѧ��ѧ�ţ�\n";
    cin >> searchID;

    student_Node* current = L->head_student;
    while (current) {
        if (current->ID == searchID) {
            cout << "---------------------\n";
            cout << "ѧ������: " << current->name << "\n";
            cout << "ѧ��: " << current->ID << "\n";
            cout << "���ĳɼ�: " << current->Chinese << "\n";
            cout << "��ѧ�ɼ�: " << current->Math << "\n";
            cout << "Ӣ��ɼ�: " << current->English << "\n";
            return;
        }
        current = current->next;
    }

    cout << "δ�ҵ�ѧ��Ϊ " << searchID << " ��ѧ����\n";
}

// ��ӡ����ѧ����Ϣ
void Print_AllStudents(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ��\n";
        return;
    }

    student_Node* current = L->head_student;
    while (current) {
        cout << "ѧ������: " << current->name << "\n";
        cout << "ѧ��: " << current->ID << "\n";
        cout << "���ĳɼ�: " << current->Chinese << "\n";
        cout << "��ѧ�ɼ�: " << current->Math << "\n";
        cout << "Ӣ��ɼ�: " << current->English << "\n";
        cout << "---------------------\n";
        current = current->next;
    }
}

// ��ѯȫ���ܷ�ͳ��
void Query_TotalScores(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ���޷����в�ѯ��\n";
        return;
    }

    float maxTotal = -1;
    float minTotal = 301;
    float totalAllScores = 0;
    int studentCount = 0;

    vector<pair<string, float>> totalScores; // ��������

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

    cout << "ȫ���ܷ�ͳ�ƽ����\n";
    cout << "����ܷ�: " << maxTotal << "      ѧ������:" << max->name << "      ѧ��ID:" << max->ID << "\n";
    cout << "����ܷ�: " << minTotal << "      ѧ������:" << min->name << "      ѧ��ID:" << min->ID << "\n";
    cout << "ƽ���ܷ�: " << averageTotal << "\n";

    // ����
    sort(totalScores.begin(), totalScores.end(),
        [](const pair<string, float>& a, const pair<string, float>& b) {
            return a.second > b.second;
        });

    cout << "�ܷ�������\n";
    for (int i = 0; i < totalScores.size(); i++) {
        cout << i + 1 << ". " << totalScores[i].first << " - " << totalScores[i].second << "\n";
    }
}

//ɾ��ѧ���ڵ�
void Delete_Student(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ���޷�ɾ����\n";
        return;
    }

    string deleteID;
    cout << "������Ҫɾ����ѧ��ѧ�ţ�\n";
    cin >> deleteID;

    student_Node* current = L->head_student;
    student_Node* prev = nullptr;

    while (current) {
        if (current->ID == deleteID) {
            // �����ͷ�ڵ�
            if (current == L->head_student) {
                L->head_student = current->next;
                if (current == L->tail_student) { // �������ֻ��һ���ڵ�
                    L->tail_student = nullptr;
                }
            }
            else { // ������м��β�ڵ�
                prev->next = current->next;
                if (current == L->tail_student) {
                    L->tail_student = prev; // ����β�ڵ�
                }
            }

            delete current; // �ͷ��ڴ�
            L->student_length--;
            cout << "ѧ��Ϊ " << deleteID << " ��ѧ����Ϣ��ɾ����\n";
            return;
        }
        prev = current;
        current = current->next;
    }

    cout << "δ�ҵ�ѧ��Ϊ " << deleteID << " ��ѧ����\n";
}

// �ͷ������ڴ�
void Free_StudentList(student_List L) {
    student_Node* current = L->head_student;
    while (current) {
        student_Node* temp = current;
        current = current->next;
        delete temp;
    }
    delete L;
}

//ͳ��ĳ�ſε���߷֡���ͷ֡�ƽ�������
// ��ѯ���Ƴɼ�
void Query_SubjectScores(student_List L) {
    if (L->student_length == 0) {
        cout << "��ǰû��ѧ����Ϣ���޷����в�ѯ��\n";
        return;
    }

    int subjectChoice;
    cout << "��ѡ���ѯ��Ŀ��\n";
    cout << "1. ����\n";
    cout << "2. ��ѧ\n";
    cout << "3. Ӣ��\n";
    cin >> subjectChoice;

    if (subjectChoice < 1 || subjectChoice > 3) {
        cout << "������Ч��������ѡ��\n";
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
    string subjectName = (subjectChoice == 1) ? "����" : (subjectChoice == 2) ? "��ѧ" : "Ӣ��";

    cout << subjectName << "��Ŀͳ�ƽ����\n";
    cout << "��߷�: " << maxScore << "      ѧ������:" << max->name << "      ѧ��ID:" << max->ID << "\n";
    cout << "��ͷ�: " << minScore << "      ѧ������:" << min->name << "      ѧ��ID:" << min->ID << "\n";
    cout << "ƽ����: " << averageScore << "\n";

    // ����
    sort(subjectScores.begin(), subjectScores.end(),
        [](const pair<string, float>& a, const pair<string, float>& b) {
            return a.second > b.second;
        });

    cout << subjectName << "�ɼ�������\n";
    for (int i = 0; i < subjectScores.size(); i++) {
        cout << i + 1 << ". " << subjectScores[i].first << " - " << subjectScores[i].second << "\n";
    }
}

// ���˵�����
void main_menu(int choose, student_List L) {
    if (choose == 1) {
        // ���ѧ��
        Add_StudentList(L);
    }
    else if (choose == 2) {
        // �޸�ѧ����Ϣ
        Modify_Student(L);
    }
    else if (choose == 3) {
        // ��ѯѧ����Ϣ
        Search_Student(L);
    }
    else if (choose == 4) {
        // ��ѯ��Ŀ�ɼ�
        Query_SubjectScores(L);
    }
    else if (choose == 5) {
        // ��ѯȫ���ֳܷɼ�
        Query_TotalScores(L);
    }
    else if (choose == 6) {
        // ��ӡ����ѧ����Ϣ
        Print_AllStudents(L);
    }
    else if (choose == 7) {
        // ɾ��ѧ��
        Delete_Student(L);
    }
}

// ������
int main() {
    student_List L_student = Init_StudentList();
    int choose = 0;

    while (true) {
        cout << "----��ѡ�������-----\n";
        cout << "    1�����ѧ��\n";
        cout << "    2���޸�ѧ����Ϣ\n";
        cout << "    3����ѯѧ����Ϣ\n";
        cout << "    4����ѯ��Ŀ�ɼ�\n";
        cout << "    5����ѯȫ���ֳܷɼ�\n";
        cout << "    6����ӡ����ѧ����Ϣ\n";
        cout << "    7��ɾ��ѧ��\n";
        cout << "    8���˳�\n";

        cin >> choose;

        if (choose == 8) {
            cout << "----ѧ���ɼ�ͳ��ϵͳ���˳�--------\n";
            break;
        }
        else {
            main_menu(choose, L_student);
        }
    }

    Free_StudentList(L_student);
    return 0;
}