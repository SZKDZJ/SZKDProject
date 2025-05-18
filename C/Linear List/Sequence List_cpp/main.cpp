#include<iostream>
using namespace std;

#define INITLIST_SIZE 100
#define LIST_INCREMENT 50

//˳�����
typedef struct {
	int* elem;
	int length;
	int listsize;
}SqList;

//˳���ṹ��ʼ��
void InitList_Sq(SqList& L) {
	L.elem = (int*)malloc(INITLIST_SIZE * sizeof(int));
	if (!L.elem)exit(OVERFLOW);
	L.length = 0;
	L.listsize = INITLIST_SIZE;
};

//˳���ṹ����
void DestroyList(SqList& L) {
	if (L.elem) {
		free(L.elem);
	}
};

//����˳���Ԫ��
//�ж�compare()��������
bool compare(int a, int b) {
	return a == b;
};
int LocateList_Sq(SqList& L, int e, bool(*compare)(int, int)) {
	int i = 1;  // i ��ʾ��1��Ԫ��λ��
	int* p = L.elem; //��ָ��p��ʾ˳�����Ԫ�ش洢λ�ã���ʱ��ʾ��һ��Ԫ��λ��
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