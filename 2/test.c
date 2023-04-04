int main()
{

   int i[] = {1,2,3,4};

   int b = i[0];

   float c = 2.75;

   for (i = 1; i <= 20 + 3; i++)
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

