#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#define ARRAY_LENGTH_zzq(array) (sizeof(array) / sizeof((array)[0]))

//??????
typedef struct MinHeap_zzq {
	int* heap_zzq;
	int maxSize_zzq;
	int size_zzq;
}MinHeap_zzq;

//?§Ø???????
int isEmpty_zzq(MinHeap_zzq* m_zzq) {
	return m_zzq->size_zzq == 0;
}

//?§Ø?????????
int isFull_zzq(MinHeap_zzq* m_zzq) {
	return m_zzq->size_zzq == m_zzq->maxSize_zzq;
}

//??????
void makeEmpty_zzq(MinHeap_zzq* m_zzq) {
	m_zzq->size_zzq = 0;
}

//????parent??child
void swap_zzq(int* arr_zzq, int child_zzq, int parent_zzq) {
	int tmp_zzq = arr_zzq[child_zzq];
	arr_zzq[child_zzq] = arr_zzq[parent_zzq];
	arr_zzq[parent_zzq] = tmp_zzq;
}

//???????????
void filterDown_zzq(int* arr_zzq, int start_zzq, int endOfHeap_zzq) {
	int parent_zzq = start_zzq;
	int child_zzq = 2 * parent_zzq + 1;
	while (child_zzq < endOfHeap_zzq) {
		int index_zzq = child_zzq;
		if ((child_zzq + 1) < endOfHeap_zzq && arr_zzq[child_zzq + 1] < arr_zzq[child_zzq]) {
			index_zzq = child_zzq + 1;
		}

		if (arr_zzq[parent_zzq] > arr_zzq[index_zzq]) {
			swap_zzq(arr_zzq, index_zzq, parent_zzq);
			parent_zzq = child_zzq;
			child_zzq = 2 * parent_zzq + 1;
		}
		else {
			break;
		}
	}
}

//????§Ó??????
void filterUp_zzq(int* arr_zzq, int start_zzq) {
	int child_zzq = start_zzq;
	int parent_zzq = (child_zzq - 1) / 2;
	while (parent_zzq >= 0) {
		if (arr_zzq[child_zzq] < arr_zzq[parent_zzq]) {
			swap_zzq(arr_zzq, child_zzq, parent_zzq);
			child_zzq = parent_zzq;
			parent_zzq = (child_zzq - 1) / 2;
		}
		else {
			break;
		}
	}

}
void Insert_zzq(MinHeap_zzq* m_zzq, int x_zzq) {
	if (isFull_zzq(m_zzq)) {
		printf("????????,%d ???????\n", x_zzq);
		return;
	}
	m_zzq->heap_zzq[m_zzq->size_zzq] = x_zzq;
	filterUp_zzq(m_zzq->heap_zzq, m_zzq->size_zzq);
	m_zzq->size_zzq++;
}

//?????????§³maxSize,?????????
void Init_zzq(MinHeap_zzq* m_zzq,  int maxSize_zzq) {
	m_zzq->maxSize_zzq = maxSize_zzq;
	m_zzq->heap_zzq = (int*)malloc(sizeof(int) * (maxSize_zzq));
	if (m_zzq->heap_zzq == NULL) {
		fprintf(stderr, "Memory allocation failed\n");
		exit(EXIT_FAILURE);
	}
	m_zzq->size_zzq = 0;
}

void copy_zzq(int* dest_zzq, int* src_zzq, int size_zzq) {
	for (int i = 0; i < size_zzq; i++) {
		dest_zzq[i] = src_zzq[i];
	}
}

//????????????????????????§³????
void CreateMinHeap_zzq(MinHeap_zzq* m_zzq, int arr_zzq[], int size_zzq) {
	m_zzq->size_zzq = size_zzq;
	copy_zzq(m_zzq->heap_zzq, arr_zzq, size_zzq);
	for (int i_zzq = (m_zzq->size_zzq - 1) / 2; i_zzq >= 0; i_zzq--) {
		filterDown_zzq(m_zzq->heap_zzq, i_zzq, m_zzq->size_zzq);
	}

}

//?????§³?????
int Remove_zzq(MinHeap_zzq* m_zzq) {
	if (isEmpty_zzq(m_zzq)) {
		printf("???????\n");
		return -1;
	}
	int x_zzq = m_zzq->heap_zzq[0];

	m_zzq->heap_zzq[0] = m_zzq->heap_zzq[m_zzq->size_zzq - 1];
	m_zzq->size_zzq--;
	filterDown_zzq(m_zzq->heap_zzq, 0, m_zzq->size_zzq);

	return x_zzq;
}

//?????
void Print_zzq(MinHeap_zzq* m_zzq) {
	for (int i_zzq = 0; i_zzq < m_zzq->size_zzq; i_zzq++) {
		printf("%d ", m_zzq->heap_zzq[i_zzq]);
	}
	printf("\n");
}

//??????
int* HeapSort_zzq(MinHeap_zzq* m_zzq) {
	int* arr_zzq = (int*)malloc(sizeof(int) * (m_zzq->size_zzq));
	copy_zzq(arr_zzq, m_zzq->heap_zzq, m_zzq->size_zzq);
	for (int i_zzq = m_zzq->size_zzq - 1; i_zzq > 0; i_zzq--) {
		swap_zzq(arr_zzq, 0, i_zzq);
		filterDown_zzq(arr_zzq, 0, i_zzq);
	}
	return arr_zzq;
}


int main() {
	int arr_zzq[] = { 2,4,10,5 };
	int n_zzq = ARRAY_LENGTH_zzq(arr_zzq);
	MinHeap_zzq m_zzq;

	//?????????????????10
	Init_zzq(&m_zzq, 8);

	//??????????(filterDown)
	CreateMinHeap_zzq(&m_zzq, arr_zzq, n_zzq);
	Print_zzq(&m_zzq);

	//??????(filterUp)
	Insert_zzq(&m_zzq, 4);
	Insert_zzq(&m_zzq, 80);
	Insert_zzq(&m_zzq, 3);
	Insert_zzq(&m_zzq, 77);
	Print_zzq(&m_zzq);

	//??????????§³???
	int min_zzq = Remove_zzq(&m_zzq);
	Print_zzq(&m_zzq);
	printf("??§³???%d\n", min_zzq);

	//????????
	int* desc_zzq = HeapSort_zzq(&m_zzq);
	for (int i = 0; i < m_zzq.size_zzq; i++) {
		printf("%d ", desc_zzq[i]);
	}
	printf("\n");

	free(desc_zzq);
	free(m_zzq.heap_zzq);

	return 0;
}