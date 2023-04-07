int main()
{
    int n = 5;
    int res = 1;
    if (n == 0)
    {
        return 0;
    }
    do {
        res = res * n;
        n = n - 1;
    } while (n > 1);
    printf(res);
    return 0;
}
