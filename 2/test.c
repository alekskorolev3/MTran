int main() {
   int i, n, a = 0, b = 'a', c;

   for (i = 1; i <= 20; i++) {
      if (i == 1) {
         printf(a);
         continue;
      }
      if (i == 2) {
         printf(b);
         continue;
      }
      c = a + b;
      a = b;
      b = c;
      printf(c);
   }

   return 0;
}