#include<stdio.h>
#include <stdbool.h>
#include<stdlib.h>
#include <math.h>
#include <assert.h>

//结构体定义
typedef struct {
	int* elem_zzq;
	int length_zzq;
	int listsize_zzq;
} Sqlist_zzq;

//创建顺序表
void InitList_zzq(Sqlist_zzq* L_zzq){
	//初始空间100
	L_zzq->elem_zzq = (int*)malloc(3 * sizeof(int));
	//内存分配失败则退出
	if (!L_zzq->elem_zzq) {
		printf("初始化失败\n");
		exit(OVERFLOW);
	}
	printf("初始化成功\n");
	L_zzq->length_zzq = 0;
	L_zzq->listsize_zzq = 3;
}

//销毁顺序表
void DestroyList_zzq(Sqlist_zzq* L_zzq) {
	//验证函数先决条件
	assert(L_zzq);

	free(L_zzq->elem_zzq);
	L_zzq->elem_zzq = NULL;
}

//查找
bool compare_zzq(int a_zzq, int b_zzq) {
	return a_zzq == b_zzq;
}
int LocateElem_zzq(Sqlist_zzq* L_zzq, int e_zzq, bool(*compare_zzq)(int，int)) {
	//先指向第一个元素
	int i_zzq = 1;
	int* p_zzq = L_zzq->elem_zzq;
	
	while (i_zzq <= L_zzq->length_zzq && !compare_zzq(*p_zzq++, e_zzq)) {
		i_zzq++;
	}
	if (i_zzq <= L_zzq->length_zzq) {
		printf("与%d匹配的第一个元素位%d\n", e_zzq, i_zzq);
		return i_zzq;
	}
	else {
		printf("未匹配\n");
		return 0;
	}
}

//尾部增加元素
int ListAdd_zzq(Sqlist_zzq* L_zzq, int e_zzq) {
	//判断存储空间
	if (L_zzq->length_zzq >= L_zzq->listsize_zzq) {
		//增加50单位
		int* newBase_zzq;
		newBase_zzq = (int*)realloc(L_zzq->elem_zzq, (L_zzq->listsize_zzq + 50) * sizeof(int));
		if (!newBase_zzq) {
			printf("扩容失败\n");
			exit(OVERFLOW);
		}
		L_zzq->elem_zzq = newBase_zzq; //新基址
		L_zzq->listsize_zzq += 50;
		printf("扩容成功\n");
	}

	L_zzq->elem_zzq[L_zzq->length_zzq] = e_zzq;
	L_zzq->length_zzq++;
	printf("%d尾部添加成功\n", e_zzq);
}

//插入 （在第i个位置插入即在原第i个位置前插入）
int ListInsert_zzq(Sqlist_zzq* L_zzq, int i_zzq, int e_zzq) {
	//先判断插入位置是否合法
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq + 1) {
		printf("插入位置不合法\n");
		return 0;
	}

	//如果存储空间不够，分配新存储空间
	if (L_zzq->length_zzq >= L_zzq->listsize_zzq) {
		//增加50单位
		int* newBase_zzq;
		newBase_zzq = (int*)realloc(L_zzq->elem_zzq, (L_zzq->listsize_zzq + 50) * sizeof(int));
		if (!newBase_zzq) {
			printf("扩容失败\n");
			exit(OVERFLOW);
		}
		L_zzq->elem_zzq = newBase_zzq; //新基址
		L_zzq->listsize_zzq += 50;
		printf("扩容成功\n");
	}

	int* q_zzq;
	q_zzq = &(L_zzq->elem_zzq[i_zzq - 1]); //q指示插入位置，即第i个元素地址
	int* p_zzq;
	for (p_zzq = &(L_zzq->elem_zzq[L_zzq->length_zzq - 1]); p_zzq >= q_zzq; --p_zzq) {
		*(p_zzq + 1) = *p_zzq;
	}
	*q_zzq = e_zzq;
	L_zzq->length_zzq++;
	printf("%d插入成功\n",e_zzq);
	return 1;
}

//删除 （删除第i个位置元素）
int ListDelete_zzq(Sqlist_zzq* L_zzq, int i_zzq) {
	//先判断删除位置是否合法
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq) {
		printf("删除位置不合法\n");
		return 0;
	}

	int *p_zzq;
	p_zzq = &(L_zzq->elem_zzq[i_zzq - 1]); 
	int e_zzq;
	e_zzq = *p_zzq; //将被删除元素赋值给e_zzq
	int* q_zzq;
	q_zzq = L_zzq->elem_zzq + L_zzq->length_zzq - 1; //表尾元素位置
	for (p_zzq++; p_zzq <= q_zzq; p_zzq++) {
		*(p_zzq - 1) = *p_zzq;
	}
	L_zzq->length_zzq--;
	printf("删除第%d个元素%d成功\n",i_zzq,e_zzq);
	return e_zzq;
}

//修改
int ListModify_zzq(Sqlist_zzq* L_zzq, int i_zzq, int e_zzq) {
	//先确定修改位置是否合法
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq) {
		printf("修改位置不合法\n");
		return 0;
	}

	int* p_zzq;
	p_zzq = &(L_zzq->elem_zzq[i_zzq - 1]);
	*p_zzq = e_zzq;
	printf("修改成功\n");
	return 1;
}

//合并顺序表（已知顺序线性表La和Lb按非递减排序，归并为Lc按非递减排序）
void MergeList(Sqlist_zzq La_zzq, Sqlist_zzq Lb_zzq, Sqlist_zzq* Lc_zzq) {
	int* pa_zzq, * pb_zzq, * pc_zzq;
	pa_zzq = La_zzq.elem_zzq;
	pb_zzq = Lb_zzq.elem_zzq;
	Lc_zzq->listsize_zzq = Lc_zzq->length_zzq = La_zzq.length_zzq + Lb_zzq.length_zzq;
	pc_zzq = Lc_zzq->elem_zzq = (int*)malloc(Lc_zzq->listsize_zzq * sizeof(int));
	if (!Lc_zzq->elem_zzq) {
		printf("Lc_zzq初始化失败\n");
		exit(OVERFLOW);
	}
	int* pa_last_zzq, * pb_last_zzq;
	pa_last_zzq = La_zzq.elem_zzq + La_zzq.length_zzq - 1; //指针p为地址，与 pa_last_zzq =&(La_zzq.elem_zzq[La_zzq.length_zzq - 1])
	pb_last_zzq = Lb_zzq.elem_zzq + Lb_zzq.length_zzq - 1;
	while (pa_zzq <= pa_last_zzq && pb_zzq <= pb_last_zzq)
	{
		if (*pa_zzq <= *pb_zzq) {
			*pc_zzq = *pa_zzq;
			pc_zzq++;
			pa_zzq++;
		}
		else {
			*pc_zzq = *pb_zzq;
			pc_zzq++;
			pb_zzq++;
		}
	}
	while (pa_zzq <= pa_last_zzq)
	{
		*pc_zzq = *pa_zzq;
		pc_zzq++;
		pa_zzq++;
	}
	while (pb_zzq <= pb_last_zzq)
	{
		*pc_zzq = *pb_zzq;
		pc_zzq++;
		pb_zzq++;
	}
}

//打印
void PrintList(Sqlist_zzq* L_zzq) {
	for (int i = 0; i < L_zzq->length_zzq; i++) {
		printf("%d\t", L_zzq->elem_zzq[i]);
	}
	printf("\n");
}

//测试
int main() {
	Sqlist_zzq L_zzq;
	InitList_zzq(&L_zzq);
	ListAdd_zzq(&L_zzq, 3);
	ListAdd_zzq(&L_zzq, 7);
	ListAdd_zzq(&L_zzq, 2);
	ListAdd_zzq(&L_zzq, 8);
	ListAdd_zzq(&L_zzq, 2);
	PrintList(&L_zzq);
	ListInsert_zzq(&L_zzq, 2, 100);
	PrintList(&L_zzq);
	ListDelete_zzq(&L_zzq, 4);
	PrintList(&L_zzq);
	ListModify_zzq(&L_zzq, 5, 2);
	PrintList(&L_zzq);
	LocateElem_zzq(&L_zzq, 3, compare_zzq);
	DestroyList_zzq(&L_zzq);

	Sqlist_zzq L1_zzq, L2_zzq,L3_zzq;
	InitList_zzq(&L1_zzq);
	ListAdd_zzq(&L1_zzq, 3);
	ListAdd_zzq(&L1_zzq, 7);
	ListAdd_zzq(&L1_zzq, 9);
	ListAdd_zzq(&L1_zzq, 9);
	ListAdd_zzq(&L1_zzq, 14);
	InitList_zzq(&L2_zzq);
	ListAdd_zzq(&L2_zzq, 2);
	ListAdd_zzq(&L2_zzq, 6);
	ListAdd_zzq(&L2_zzq, 7);
	ListAdd_zzq(&L2_zzq, 10);
	ListAdd_zzq(&L2_zzq, 11);
	MergeList(L1_zzq, L2_zzq, &L3_zzq);
	PrintList(&L1_zzq);
	PrintList(&L2_zzq);
	PrintList(&L3_zzq);
	DestroyList_zzq(&L1_zzq);
	DestroyList_zzq(&L2_zzq);
	DestroyList_zzq(&L3_zzq);
	return 0;
}
