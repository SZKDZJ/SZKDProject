#include<stdio.h>
#include <stdbool.h>
#include<stdlib.h>
#include <math.h>
#include <assert.h>

//�ṹ�嶨��
typedef struct {
	int* elem_zzq;
	int length_zzq;
	int listsize_zzq;
} Sqlist_zzq;

//����˳���
void InitList_zzq(Sqlist_zzq* L_zzq){
	//��ʼ�ռ�100
	L_zzq->elem_zzq = (int*)malloc(3 * sizeof(int));
	//�ڴ����ʧ�����˳�
	if (!L_zzq->elem_zzq) {
		printf("��ʼ��ʧ��\n");
		exit(OVERFLOW);
	}
	printf("��ʼ���ɹ�\n");
	L_zzq->length_zzq = 0;
	L_zzq->listsize_zzq = 3;
}

//����˳���
void DestroyList_zzq(Sqlist_zzq* L_zzq) {
	//��֤�����Ⱦ�����
	assert(L_zzq);

	free(L_zzq->elem_zzq);
	L_zzq->elem_zzq = NULL;
}

//����
bool compare_zzq(int a_zzq, int b_zzq) {
	return a_zzq == b_zzq;
}
int LocateElem_zzq(Sqlist_zzq* L_zzq, int e_zzq, bool(*compare_zzq)(int��int)) {
	//��ָ���һ��Ԫ��
	int i_zzq = 1;
	int* p_zzq = L_zzq->elem_zzq;
	
	while (i_zzq <= L_zzq->length_zzq && !compare_zzq(*p_zzq++, e_zzq)) {
		i_zzq++;
	}
	if (i_zzq <= L_zzq->length_zzq) {
		printf("��%dƥ��ĵ�һ��Ԫ��λ%d\n", e_zzq, i_zzq);
		return i_zzq;
	}
	else {
		printf("δƥ��\n");
		return 0;
	}
}

//β������Ԫ��
int ListAdd_zzq(Sqlist_zzq* L_zzq, int e_zzq) {
	//�жϴ洢�ռ�
	if (L_zzq->length_zzq >= L_zzq->listsize_zzq) {
		//����50��λ
		int* newBase_zzq;
		newBase_zzq = (int*)realloc(L_zzq->elem_zzq, (L_zzq->listsize_zzq + 50) * sizeof(int));
		if (!newBase_zzq) {
			printf("����ʧ��\n");
			exit(OVERFLOW);
		}
		L_zzq->elem_zzq = newBase_zzq; //�»�ַ
		L_zzq->listsize_zzq += 50;
		printf("���ݳɹ�\n");
	}

	L_zzq->elem_zzq[L_zzq->length_zzq] = e_zzq;
	L_zzq->length_zzq++;
	printf("%dβ����ӳɹ�\n", e_zzq);
}

//���� ���ڵ�i��λ�ò��뼴��ԭ��i��λ��ǰ���룩
int ListInsert_zzq(Sqlist_zzq* L_zzq, int i_zzq, int e_zzq) {
	//���жϲ���λ���Ƿ�Ϸ�
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq + 1) {
		printf("����λ�ò��Ϸ�\n");
		return 0;
	}

	//����洢�ռ䲻���������´洢�ռ�
	if (L_zzq->length_zzq >= L_zzq->listsize_zzq) {
		//����50��λ
		int* newBase_zzq;
		newBase_zzq = (int*)realloc(L_zzq->elem_zzq, (L_zzq->listsize_zzq + 50) * sizeof(int));
		if (!newBase_zzq) {
			printf("����ʧ��\n");
			exit(OVERFLOW);
		}
		L_zzq->elem_zzq = newBase_zzq; //�»�ַ
		L_zzq->listsize_zzq += 50;
		printf("���ݳɹ�\n");
	}

	int* q_zzq;
	q_zzq = &(L_zzq->elem_zzq[i_zzq - 1]); //qָʾ����λ�ã�����i��Ԫ�ص�ַ
	int* p_zzq;
	for (p_zzq = &(L_zzq->elem_zzq[L_zzq->length_zzq - 1]); p_zzq >= q_zzq; --p_zzq) {
		*(p_zzq + 1) = *p_zzq;
	}
	*q_zzq = e_zzq;
	L_zzq->length_zzq++;
	printf("%d����ɹ�\n",e_zzq);
	return 1;
}

//ɾ�� ��ɾ����i��λ��Ԫ�أ�
int ListDelete_zzq(Sqlist_zzq* L_zzq, int i_zzq) {
	//���ж�ɾ��λ���Ƿ�Ϸ�
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq) {
		printf("ɾ��λ�ò��Ϸ�\n");
		return 0;
	}

	int *p_zzq;
	p_zzq = &(L_zzq->elem_zzq[i_zzq - 1]); 
	int e_zzq;
	e_zzq = *p_zzq; //����ɾ��Ԫ�ظ�ֵ��e_zzq
	int* q_zzq;
	q_zzq = L_zzq->elem_zzq + L_zzq->length_zzq - 1; //��βԪ��λ��
	for (p_zzq++; p_zzq <= q_zzq; p_zzq++) {
		*(p_zzq - 1) = *p_zzq;
	}
	L_zzq->length_zzq--;
	printf("ɾ����%d��Ԫ��%d�ɹ�\n",i_zzq,e_zzq);
	return e_zzq;
}

//�޸�
int ListModify_zzq(Sqlist_zzq* L_zzq, int i_zzq, int e_zzq) {
	//��ȷ���޸�λ���Ƿ�Ϸ�
	if (i_zzq<1 || i_zzq>L_zzq->length_zzq) {
		printf("�޸�λ�ò��Ϸ�\n");
		return 0;
	}

	int* p_zzq;
	p_zzq = &(L_zzq->elem_zzq[i_zzq - 1]);
	*p_zzq = e_zzq;
	printf("�޸ĳɹ�\n");
	return 1;
}

//�ϲ�˳�����֪˳�����Ա�La��Lb���ǵݼ����򣬹鲢ΪLc���ǵݼ�����
void MergeList(Sqlist_zzq La_zzq, Sqlist_zzq Lb_zzq, Sqlist_zzq* Lc_zzq) {
	int* pa_zzq, * pb_zzq, * pc_zzq;
	pa_zzq = La_zzq.elem_zzq;
	pb_zzq = Lb_zzq.elem_zzq;
	Lc_zzq->listsize_zzq = Lc_zzq->length_zzq = La_zzq.length_zzq + Lb_zzq.length_zzq;
	pc_zzq = Lc_zzq->elem_zzq = (int*)malloc(Lc_zzq->listsize_zzq * sizeof(int));
	if (!Lc_zzq->elem_zzq) {
		printf("Lc_zzq��ʼ��ʧ��\n");
		exit(OVERFLOW);
	}
	int* pa_last_zzq, * pb_last_zzq;
	pa_last_zzq = La_zzq.elem_zzq + La_zzq.length_zzq - 1; //ָ��pΪ��ַ���� pa_last_zzq =&(La_zzq.elem_zzq[La_zzq.length_zzq - 1])
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

//��ӡ
void PrintList(Sqlist_zzq* L_zzq) {
	for (int i = 0; i < L_zzq->length_zzq; i++) {
		printf("%d\t", L_zzq->elem_zzq[i]);
	}
	printf("\n");
}

//����
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
