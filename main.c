#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>
#include<string.h>


#define STD_NUM 15

struct Student
{
	int STID;//�й�
	char name[20];//�̸�
	int attend;//�⼮
	double mid;//�߰�����
	double final;//�⸻����
	double sum;//����
	char grade;//����
	int rank;//���

};

void RANK(struct Student std_list[STD_NUM], int Fattend) //15�� 30%�� 4.5,A=4��
{
	

	struct Student temp;
	int i, j;
	int k=0;
	for (i = 0; i < STD_NUM; i++) {
		if (std_list[i].grade == 'F' && k < Fattend)
		{
			while(std_list[STD_NUM-k-1].grade == 'F' && k<Fattend) k++;
			temp = std_list[i];
			std_list[i] = std_list[STD_NUM - k - 1];
			std_list[STD_NUM - k - 1] = temp;
			k++;
		}
	}


      for(i=0; i<STD_NUM-Fattend; i++)
		for (j = 0; j < STD_NUM=Fattend-1; j++)
		{
			
			if (std_list[i].sum < std_list[i + 1].sum)
			{
				temp = std_list[i];
				std_list[i] = std_list[i + 1];
				std_list[i+1] = temp;

			}

		}
	  if(i < 4)//0~3����A
	  {
		  std_list[i].grade = 'A';
      }
	  else if (i < 10)//4~10 B
	  {
		  std_list[i].grade = 'B';
	  }
	  else if (i < STD_NUM && std_list[i].grade != 'F')//F �ƴ� 10~ = C 
	  {
		  std_list[i].grade = 'C';
	  }
	  if (std_list[i].grade != 'F' && i < 4)
		  for (i = 0; i < 4; i++)
		  {
			  std_list[i].rank = k + 1;
			  k++;
		  }
	  else if (std_list[i].grade != 'F' && i < 10)
		  for (i = 0; i < 10; i++)
		  {

			  std_list[i].rank = k + 4;
		  }
	  else if (std_list[i].grade = 'F')
		  std_list[i].rank = -1;
}

int main()
{
	int i;
	int ID;
	int count=0;//�⼮ ī��Ʈ
	int Fattend = 0;//F���� ī��Ʈ

	struct Student std_list[STD_NUM];

	FILE *fp = NULL; //���� ����
	fp = fopen("std_info.txt", "r"); 
	if (fp == NULL)
		printf("���� ���� ����\n");

	for (i = 0; i < STD_NUM; i++) {
		fscanf(fp, "%d %s", &std_list[i].STID, std_list[i].name); //�й��� �̸� �Է¹���
		for (i = 0; i < 15; i++)//�⼮ 15�� ���� ���� �ջ�
		{
			fscanf(fp, "%d", &std_list[i].attend);
			if (std_list[i].attend == 1) {//0 or 1�ε� 1�� ������ count++
				count++;
			}
		}
		fscanf(fp, "%lf %lf", &std_list[i].mid, &std_list[i].final);//�߰� �⸻ ���� �Է¹���
		std_list[i].sum = (
			(100 - count * 5) * 20 / 100
			+ (std_list[i].mid * 40 / 100)
			+ (std_list[i].final * 40 / 100));
		if (count >3||std_list[i].sum < 60)//count�� 3�̻��̰ų� ������ 60 �̸��ϰ�� F
		{
			std_list[i].grade = 'F';
			Fattend++;//F��������
		}

	}

	fclose(fp); //���ϴ���


	printf("==============[���� ��� ���α׷�]==============\n\n");
	printf("    1.��ü �л� ���� ����\n");
	printf("    2.�й� �˻�\n");
	printf("    3.����\n\n");
	printf(">");
	scanf_s("%d", &i);

	printf("�й�      �̸�  ����    ����  ���");
	if (i == 1)
	{
		for (i = 0; i < STD_NUM; i++)//
		{
			printf("%d %s %.2lf %c %d\n", std_list[i].STID, std_list[i].name, std_list[i].sum, std_list[i].grade, std_list[i].rank);
		}

	}
	if (i == 2);
	{   printf("�˻��� �й�");
		scanf("%d",&ID);
		for (i = 0;i < 15; i++)
		{
			if (ID == std_list[i].STID)
				printf("%d %s %.2lf %c %d", std_list[i].STID, std_list[i].name, std_list[i].sum, std_list[i].grade, std_list[i].rank);
		
		}

		
		
	}
	if (i == 3);
	{
		return 0;
	}



	
	return 0;

}