/*
树形结构通过读取文件definition.txt文件创建
    格式如“hospital 10 floor”，表示hospital有10层floor。
将树形结构创建后，可以读取queries.txt中的查询完成对应的操作。
    操作有两种：“what is connecting_corridor”意思是查询connecting_corridor有几个子部件。
    比如在该图中，connecting_corridor含有5个 supply room，则打印出:
        Part connecting_corridor subparts are:
             5 supply room
    “how many floor hospital”是查询hospital有几个floor，那么打印:
        Hospital has 10 floor
*/

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// 定义二叉树节点
class BiTNode {
private:
    string name;         // 节点名称
    int count;           // 数量
    BiTNode* lchild;     // 左孩子
    BiTNode* rchild;     // 右兄弟

public:
    // 构造函数
    BiTNode(const string& name, int count)
        : name(name), count(count), lchild(nullptr), rchild(nullptr) {
    }
    // Getter 和 Setter
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

     // 销毁树的递归函数
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
        destroyTree(root);  // 在析构时销毁树
    }

    // 创建新节点
    BiTNode* createNode(const string& name, int count) {
        return new BiTNode(name, count);
    }

    // 查找节点（先序遍历）
    BiTNode* findNode(BiTNode* node, const string& name) {
        if (!node) return nullptr;

        if (node->getName() == name) {
            cout << "? Found: " << name << " at " << node << endl;
            return node;
        }

        // 递归查找左子树
        BiTNode* found = findNode(node->getLChild(), name);
        if (found) return found;

        // 递归查找右子树（兄弟节点）
        return findNode(node->getRChild(), name);
    }

    // 在树中插入节点（LCRS 转换）
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

        // 检查 child 是否已经存在
        BiTNode* existingChild = findNode(root, child);
        if (existingChild) {
            cout << "?? Child " << child << " already exists at " << existingChild << ", skipping creation." << endl;
            return;
        }

        // 创建子节点
        BiTNode* childNode = createNode(child, count);
        cout << "? Created child: " << child << " at " << childNode << endl;

        // 插入到父节点
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

    // 打印树结构
    void printTree(BiTNode* root, int level = 0) {
        if (!root) return;

        for (int i = 0; i < level; i++) cout << "    ";
        cout << root->getName() << " (" << root->getCount() << ") at " << root << endl;

        printTree(root->getLChild(), level + 1);
        printTree(root->getRChild(), level);
    }

    // 读取文件并构建树
    void readDefinitions(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "无法打开文件: " << filename << endl;
            return;
        }

        string line;
        while (getline(file, line)) {
            size_t firstSpace = line.find(' ');
            size_t secondSpace = line.find(' ', firstSpace + 1);

            if (firstSpace == string::npos || secondSpace == string::npos) {
                cout << "文件格式错误，跳过：" << line << endl;
                continue;
            }

            string parent = line.substr(0, firstSpace);
            int count = stoi(line.substr(firstSpace + 1, secondSpace - firstSpace - 1));
            string child = line.substr(secondSpace + 1);

            insertNode(parent, child, count);
        }

        file.close();
    }

    // 查询某节点的直接子部件
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

    // 递归统计部件的总数
    int countParts(BiTNode* node, const string& target, int currentCount) {
        if (!node) return 0;

        // 如果当前节点是目标节点，累积其数量
        int total = 0;
        if (node->getName() == target) {
            total += currentCount;
        }

        // 遍历子节点，乘以当前节点的数量
        BiTNode* child = node->getLChild();
        while (child) {
            total += countParts(child, target, currentCount * child->getCount());
            child = child->getRChild();
        }

        return total;
    }

    // 查询某部件的数量
    void queryHowMany(const string& parent, const string& part) {
        BiTNode* node = findNode(root, parent);

        if (!node) {
            cout << parent << " not found." << endl;
            return;
        }

        // 从父节点开始计算目标部件的数量
        int total = countParts(node, part,1);
        cout << parent << " has " << total << " " << part << endl;
    }

    // 处理查询
    void processQueries(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            cout << "无法打开查询文件: " << filename << endl;
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

    // 打印树结构
    void printTree() {
        printTree(root);
    }
};

int main() {
    BinaryTree tree;

    // 构建树
    tree.readDefinitions("/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment3/definitions.txt");

    // 打印树结构
    cout << "生成的树结构：" << endl;
    tree.printTree();

    // 处理查询
    tree.processQueries("/Users/zqz/Documents/Studying/Project/C++/Experiments/Experiment3/queries.txt");

    return 0;
}