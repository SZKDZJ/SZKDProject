#include<iostream>
using namespace std;

#define INITLIST_SIZE 100
#define LIST_INCREMENT 50

//顺序表定义
typedef struct {
	int* elem;
	int length;
	int listsize;
}SqList;

//顺序表结构初始化
void InitList_Sq(SqList& L) {
	L.elem = (int*)malloc(INITLIST_SIZE * sizeof(int));
	if (!L.elem)exit(OVERFLOW);
	L.length = 0;
	L.listsize = INITLIST_SIZE;
};

//顺序表结构销毁
void DestroyList(SqList& L) {
	if (L.elem) {
		free(L.elem);
	}
};

//查找顺序表元素
//判断compare()函数声明
bool compare(int a, int b) {
	return a == b;
};
int LocateList_Sq(SqList& L, int e, bool(*compare)(int, int)) {
	int i = 1;  // i 表示第1个元素位置
	int* p = L.elem; //用指针p表示顺序表中元素存储位置，此时表示第一个元素位置
	while (!(*compare)(e,*p) && i <= L.length) {
		i++;
		*p++;
	}
	if (i <= L.length) {
		return i;
	}
	else {
		return 0;
	}
};


int main() {

}