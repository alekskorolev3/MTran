int main()
{

   int i = 0;

   int b = i * 3;

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
      c = i + c;
      c = i;
      i = c;
      printf(c);
   }
   return 0;
}

