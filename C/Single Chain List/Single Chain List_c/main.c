#include<stdio.h>
#include<stdlib.h>

typedef struct LNode_zzq {
	int data_zzq;
	struct LNode_zzq* next_zzq;
}LNode_zzq, * LinkList_zzq;

//���Ĵ����븳ֵ
LNode_zzq* InitLNode_zzq(int e_zzq) {
	LNode_zzq* p_zzq = (LNode_zzq*)malloc(sizeof(LNode_zzq));
	if (p_zzq == NULL) return NULL;
	p_zzq->data_zzq = e_zzq;
	p_zzq->next_zzq = NULL;
	return p_zzq;
}

//�����ʼ��
LinkList_zzq InitList_zzq() {
	LinkList_zzq L_zzq = (LinkList_zzq)malloc(sizeof(LNode_zzq));
	if (L_zzq == NULL) {
		printf("�ڴ����ʧ��\n");
		exit(1);
	}
	L_zzq->data_zzq = 0;
	L_zzq->next_zzq = NULL;
	return L_zzq;
}

//ȡ��i��Ԫ��
int GetElem_zzq(LinkList_zzq L_zzq, int i_zzq,int* e_zzq) {
	LNode_zzq* p_zzq = L_zzq->next_zzq;
	int j_zzq = 1;
	while (p_zzq && j_zzq < i_zzq) {
		p_zzq = p_zzq->next_zzq;
		j_zzq++;
	}
	if (!p_zzq || i_zzq < j_zzq) {
		printf("λ��%d���Ϸ�\n", i_zzq);
		return 0;
	}
	*e_zzq = p_zzq->data_zzq;
	return 1;
}

//�ڵ�i��λ�ò�������Ԫ��
int ListInsert_zzq(LinkList_zzq L_zzq, int i_zzq, int e_zzq) {
	LNode_zzq* p_zzq = L_zzq;
	int j_zzq = 0;
	while (p_zzq && j_zzq < i_zzq - 1) {
		p_zzq = p_zzq->next_zzq;
		j_zzq++;
	}
	if (!p_zzq || j_zzq > i_zzq - 1) {
		printf("λ��%d���ڱ���С��1\n", i_zzq);
		return 0;
	}
	LNode_zzq* s_zzq = InitLNode_zzq(e_zzq);
	s_zzq->next_zzq = p_zzq->next_zzq;
	p_zzq->next_zzq = s_zzq;
	printf("�ɹ��ڵ�%dλ�ò���Ԫ��%d\n", i_zzq, e_zzq);
	return 1;
}

//β��
void ListPushBack_zzq(LinkList_zzq L_zzq, int e_zzq){
	LNode_zzq* p_zzq = InitLNode_zzq(e_zzq);
	//������Ϊ��
	if (L_zzq->next_zzq == NULL){
		L_zzq->next_zzq = p_zzq;
	}
	else{
		LNode_zzq* q_zzq = L_zzq->next_zzq;
		while (q_zzq->next_zzq != NULL){
			q_zzq = q_zzq->next_zzq;
		}
		q_zzq->next_zzq = p_zzq;
	}
	printf("�ɹ�����Ԫ��%d\n", e_zzq);
}

//ɾ����i�����
int ListDelete_zzq(LinkList_zzq L_zzq, int i_zzq, int* e_zzq) {
	LNode_zzq* p_zzq = L_zzq->next_zzq;
	int j_zzq = 0;
	while (p_zzq->next_zzq && j_zzq < i_zzq - 2) {
		p_zzq = p_zzq->next_zzq;
		++j_zzq;
	}
	if (!(p_zzq->next_zzq) || j_zzq > i_zzq - 2) {
		printf("ɾ��λ�ò��Ϸ�\n");
		return 0;
	}
	LNode_zzq* q_zzq;
	q_zzq = p_zzq->next_zzq;
	p_zzq->next_zzq = q_zzq->next_zzq;
	*e_zzq = q_zzq->data_zzq;
	free(q_zzq);
	printf("�ɹ�ɾ����%d��Ԫ��%d\n", i_zzq, *e_zzq);
	return 1;

}

//���ҵ�һ��ֵΪx�Ľ�㲢���ؽ���ָ��
LNode_zzq* ListFind_zzq(LinkList_zzq L_zzq, int e_zzq){
	LNode_zzq* p_zzq = L_zzq->next_zzq;
	int j_zzq = 0;
	while (p_zzq != NULL){
		j_zzq++;
		if (p_zzq->data_zzq == e_zzq){
			printf("������ֵΪ%d��Ԫ��λ�ڵ�%d��\n", e_zzq, j_zzq);
			return p_zzq;
		}
		p_zzq = p_zzq->next_zzq;
	}
	//�Ҳ�������NULLָ��
	printf("������û��ֵΪ%d��Ԫ��\n", e_zzq);
	return NULL;
}

//��ղ���
void ClearList_zzq(LinkList_zzq* L_zzq) {
	LNode_zzq* p_zzq = *L_zzq;
	LNode_zzq* q_zzq = NULL;
	while (p_zzq != NULL) {
		q_zzq = p_zzq;
		p_zzq = p_zzq->next_zzq;
		free(q_zzq);
		q_zzq = NULL;
	}
	free(q_zzq);
	q_zzq = NULL;
	printf("������\n");
}

// ��������n������Ԫ�أ�������ͷ���ĵ�����
void CreateList_zzq(LinkList_zzq L_zzq, int n_zzq) {
	LNode_zzq* p_zzq;
	printf("���뽵�����룬�Ա���к����ϲ����������\n");
	for (int i_zzq = n_zzq; i_zzq > 0; --i_zzq) {
		int e_zzq;
		printf("�����%d��Ԫ��:",i_zzq);
		scanf_s("%d",&e_zzq);
		p_zzq = InitLNode_zzq(e_zzq);
		p_zzq->next_zzq = L_zzq->next_zzq;
		L_zzq->next_zzq = p_zzq;
	}
}

//����ĸ���
LinkList_zzq CopyList_zzq(LinkList_zzq L_zzq) {
	LinkList_zzq LCopy_zzq = InitList_zzq();
	LNode_zzq* q_zzq = L_zzq;
	LNode_zzq* p_zzq = LCopy_zzq;

	while (q_zzq->next_zzq != NULL) {
		p_zzq->data_zzq = q_zzq->data_zzq;
		q_zzq = q_zzq->next_zzq;
		LNode_zzq* t_zzq = InitLNode_zzq(0);
		p_zzq->next_zzq = t_zzq;
		p_zzq = p_zzq->next_zzq;
	}
	p_zzq->data_zzq = q_zzq->data_zzq;
	p_zzq->next_zzq = NULL;
	return LCopy_zzq;
}

//�ϲ���La, LbΪͷ���������������� (�Ա���La��Lb)
LinkList_zzq Merge_LinkList_zzq(LinkList_zzq La_zzq, LinkList_zzq Lb_zzq) {
	LinkList_zzq La_copy_zzq = CopyList_zzq(La_zzq);
	LinkList_zzq Lb_copy_zzq = CopyList_zzq(Lb_zzq);
	LNode_zzq* pa_zzq = La_copy_zzq->next_zzq;
	LNode_zzq* pb_zzq = Lb_copy_zzq->next_zzq;
	LNode_zzq* pc_zzq = La_copy_zzq;
	LinkList_zzq Lc_zzq = La_copy_zzq;

	while (pa_zzq != NULL && pb_zzq != NULL) {
		if (pa_zzq->data_zzq > pb_zzq->data_zzq) {
			pc_zzq->next_zzq = pb_zzq;
			pc_zzq = pb_zzq;
			pb_zzq = pb_zzq->next_zzq;
		}
		else if (pa_zzq->data_zzq < pb_zzq->data_zzq) {
			pc_zzq->next_zzq = pa_zzq;
			pc_zzq = pa_zzq;
			pa_zzq = pa_zzq->next_zzq;
		}
		else {
			LNode_zzq* ptr_zzq;
			pc_zzq->next_zzq = pa_zzq;
			pa_zzq = pa_zzq->next_zzq;
			pc_zzq = pc_zzq->next_zzq;
			ptr_zzq = pb_zzq;
			pb_zzq = pb_zzq->next_zzq;
			free(ptr_zzq);
		}
	}
	if (pa_zzq == NULL) {
		pc_zzq->next_zzq = pb_zzq;
	}
	else {
		pc_zzq->next_zzq = pa_zzq;
	}
	free(Lb_copy_zzq);
	return Lc_zzq;
}

//��ӡ����
int PrintList_zzq(LinkList_zzq L_zzq)
{
	LNode_zzq* p_zzq = L_zzq->next_zzq;
	if (p_zzq == NULL) {
		printf("LΪ�գ��޷���ӡ����\n");
		return 0;
	}
	while (p_zzq != NULL){
		printf("%d\t", p_zzq->data_zzq);
		p_zzq = p_zzq->next_zzq;
	}
	printf("\n");
	return 1;
}

//����
int main() {
	LinkList_zzq L1_zzq, L2_zzq, L3_zzq;
	L1_zzq = InitList_zzq();
	ListPushBack_zzq(L1_zzq, 3);
	ListPushBack_zzq(L1_zzq, 8);
	ListPushBack_zzq(L1_zzq, 55);
	ListPushBack_zzq(L1_zzq, 77);
	ListPushBack_zzq(L1_zzq, 98);
	PrintList_zzq(L1_zzq);
	int e1_zzq = 0, e2_zzq = 0;
	GetElem_zzq(L1_zzq, 3, &e1_zzq);
	printf("�õ���Ԫ�ظ���e1:%d\n",e1_zzq);
	ListInsert_zzq(L1_zzq, 4, 25);
	PrintList_zzq(L1_zzq);
	ListDelete_zzq(L1_zzq, 4, &e2_zzq);
	printf("ɾ����Ԫ�ظ���e2:%d\n", e2_zzq);
	PrintList_zzq(L1_zzq);
	LNode_zzq* p_zzq;
	p_zzq = ListFind_zzq(L1_zzq, 55);
	printf("�ҵ��Ľ�㸳��p:%d\n", p_zzq->data_zzq);

	L2_zzq = InitList_zzq();
	CreateList_zzq(L2_zzq, 3);
	PrintList_zzq(L2_zzq);

	L3_zzq = Merge_LinkList_zzq(L1_zzq, L2_zzq);
	PrintList_zzq(L3_zzq);

	ClearList_zzq(&L1_zzq);
	ClearList_zzq(&L2_zzq);
	ClearList_zzq(&L3_zzq);

	return 0;
}