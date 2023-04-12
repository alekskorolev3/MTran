int main() {



  int s[] = {3,7,6,4, 10, 0, 12, 2};

  int n = 8;

  for (int i = 0; i < n; i++)
  {

       for(int j = 0; j < (n - i); j++)
       {
           if(s[j] > s[j+1])
           {
              int tmp = s[j];
              int tmp2 = s[j+1];
              s[j] = tmp2;
              s[j+1] = tmp;
           }
        }
    }

  printf(s);

  return 0;
}
