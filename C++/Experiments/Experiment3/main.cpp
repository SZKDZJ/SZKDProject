/*
���νṹͨ����ȡ�ļ�definition.txt�ļ�����
    ��ʽ�硰hospital 10 floor������ʾhospital��10��floor��
�����νṹ�����󣬿��Զ�ȡqueries.txt�еĲ�ѯ��ɶ�Ӧ�Ĳ�����
    ���������֣���what is connecting_corridor����˼�ǲ�ѯconnecting_corridor�м����Ӳ�����
    �����ڸ�ͼ�У�connecting_corridor����5�� supply room�����ӡ��:
        Part connecting_corridor subparts are:
             5 supply room
    ��how many floor hospital���ǲ�ѯhospital�м���floor����ô��ӡ:
        Hospital has 10 floor
*/

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// ����������ڵ�
class BiTNode {
private:
    string name;         // �ڵ�����
    int count;           // ����
    BiTNode* lchild;     // ����
    BiTNode* rchild;     // ���ֵ�

public:
    // ���캯��
    BiTNode(const string& name, int count)
        : name(name), count(count), lchild(nullptr), rchild(nullptr) {
    }
    // Getter �� Setter
    string getName() const { return name; }
    void setName(const string& newName) { name = newName; }

    int getCount() const { return count; }
    void setCount(int newCount) { count = newCount; }

    BiTNode* getLChild() const { return lchild; }
    void setLChild(BiTNode* child) { lchild = child; }

    BiTNode* getRChild() const { return rchild; }
    void setRChild(BiTNode* sibling) { rchild = sibling; }
};

class BinaryTree {
private:
    BiTNode* root;

     // �������ĵݹ麯��
    void destroyTree(BiTNode* node) {
        if (node == nullptr) {
            return;
        }
        destroyTree(node->getLChild());
        destroyTree(node->getRChild());
        delete node;
    }

public:
    BinaryTree() : root(nullptr) {}

    ~BinaryTree() {
        destroyTree(root);  // ������ʱ������
    }

    // �����½ڵ�
    BiTNode* createNode(const string& name, int count) {
        return new BiTNode(name, count);
    }

    // ���ҽڵ㣨���������
    BiTNode* findNode(BiTNode* node, const string& name) {
        if (!node) return nullptr;

        if (node->getName() == name) {
            cout << "? Found: " << name << " at " << node << endl;
            return node;
        }

        // �ݹ����������
        BiTNode* found = findNode(node->getLChild(), name);
        if (found) return found;

        // �ݹ�������������ֵܽڵ㣩
        return findNode(node->getRChild(), name);
    }

    // �����в���ڵ㣨LCRS ת����
    void insertNode(const string& parent, const string& child, int count) {
        if (!root) {
            root = createNode(parent, 1);
            cout << "? Created root: " << parent << " at " << root << endl;
        }

        BiTNode* parentNode = findNode(root, parent);
        if (!parentNode) {
            cout << "? Parent " << parent << " not found, skipping " << child << endl;
            return;
        }

        cout << "? Found parent: " << parent << " at " << parentNode << ", inserting child: " << child << endl;

        // ��� child �Ƿ��Ѿ�����
        BiTNode* existingChild = findNode(root, child);
        if (existingChild) {
            cout << "?? Child " << child << " already exists at " << existingChild << ", skipping creation." << endl;
            return;
        }

        // �����ӽڵ�
        BiTNode* childNode = createNode(child, count);
        cout << "? Created child: " << child << " at " << childNode << endl;

        // ���뵽���ڵ�
        if (!parentNode->getLChild()) {
            parentNode->setLChild(childNode);
            cout << "? " << child << " set as FIRST child of " << parent << endl;
        } else {
            BiTNode* sibling = parentNode->getLChild();
            while (sibling->getRChild()) {
                sibling = sibling->getRChild();
            }
            sibling->setRChild(childNode);
            cout << "?? " << child << " added as a SIBLING of " << sibling->getName() << endl;
        }
    }

    // ��ӡ���ṹ
    void printTree(BiTNode* root, int level = 0) {
        if (!root) return;

        for (int i = 0; i < level; i++) cout << "    ";
        cout << root->getName() << " (" << root->getCount() << ") at " << root << endl;

        printTree(root->getLChild(), level + 1);
        printTree(root->getRChild(), level);
    }

    // ��ȡ�ļ���������
    void readDefinitions(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "�޷����ļ�: " << filename << endl;
            return;
        }

        string line;
        while (getline(file, line)) {
            size_t firstSpace = line.find(' ');
            size_t secondSpace = line.find(' ', firstSpace + 1);

            if (firstSpace == string::npos || secondSpace == string::npos) {
                cout << "�ļ���ʽ����������" << line << endl;
                continue;
            }

            string parent = line.substr(0, firstSpace);
            int count = stoi(line.substr(firstSpace + 1, secondSpace - firstSpace - 1));
            string child = line.substr(secondSpace + 1);

            insertNode(parent, child, count);
        }

        file.close();
    }

    // ��ѯĳ�ڵ��ֱ���Ӳ���
    void queryWhatIs(const string& part) {
        BiTNode* node = findNode(root, part);

        if (!node) {
            cout << "Part " << part << " not found." << endl;
            return;
        }

        if (!node->getLChild()) {
            cout << "Part " << part << " has no subparts." << endl;
        }
        else {
            cout << "Part " << part << " subparts are:" << endl;
            BiTNode* child = node->getLChild();
            while (child) {
                cout << "    " << child->getCount() << " " << child->getName() << endl;
                child = child->getRChild();
            }
        }
    }

    // �ݹ�ͳ�Ʋ���������
    int countParts(BiTNode* node, const string& target, int currentCount) {
        if (!node) return 0;

        // �����ǰ�ڵ���Ŀ��ڵ㣬�ۻ�������
        int total = 0;
        if (node->getName() == target) {
            total += currentCount;
        }

        // �����ӽڵ㣬���Ե�ǰ�ڵ������
        BiTNode* child = node->getLChild();
        while (child) {
            total += countParts(child, target, currentCount * child->getCount());
            child = child->getRChild();
        }

        return total;
    }

    // ��ѯĳ����������
    void queryHowMany(const string& parent, const string& part) {
        BiTNode* node = findNode(root, parent);

        if (!node) {
            cout << parent << " not found." << endl;
            return;
        }

        // �Ӹ��ڵ㿪ʼ����Ŀ�겿��������
        int total = countParts(node, part,1);
        cout << parent << " has " << total << " " << part << endl;
    }

    // �����ѯ
    void processQueries(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "�޷��򿪲�ѯ�ļ�: " << filename << endl;
            return;
        }

        string line;
        while (getline(file, line)) {
            size_t firstSpace = line.find(' ');
            if (firstSpace == string::npos) continue;

            string command = line.substr(0, firstSpace);
            string rest = line.substr(firstSpace + 1);

            if (command == "whatis") {
                queryWhatIs(rest);
            }
            else if (command == "howmany") {
                size_t secondSpace = rest.find(' ');
                if (secondSpace == string::npos) continue;

                string part = rest.substr(0, secondSpace);
                string parent = rest.substr(secondSpace + 1);

                queryHowMany(parent, part);
            }
        }

        file.close();
    }

    // ��ӡ���ṹ
    void printTree() {
        printTree(root);
    }
};

int main() {
    BinaryTree tree;

    // ������
    tree.readDefinitions("/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment3/definitions.txt");

    // ��ӡ���ṹ
    cout << "���ɵ����ṹ��" << endl;
    tree.printTree();

    // �����ѯ
    tree.processQueries("/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment3/queries.txt");

    return 0;
}