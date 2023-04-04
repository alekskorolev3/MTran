int main()
{


   int a[] = {1,2,3,4};

   int i = 0;

   float x = 10 + 5;

   int b = i[0];

   int c = 2;

   for (i = 1; i <= c + 3; i++)
   {
      if (i == 1)
      {
         printf(c);
         continue;
      }
      if (i == 2)
      {
         printf(c);
         continue;
      }
      c = (i + c) * 2;
      c = i;
      i = c;
      printf(c);
   }
   return 0;
}