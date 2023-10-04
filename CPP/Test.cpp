#include <iostream>
#include <stdlib.h>   

int main(int argc, char const *argv[])
{
  int iSecret;

  iSecret = rand() % 10 + 1;

  for (int i = 0; i<10; i++){
  iSecret = rand() % 10 + 1;
  std::cout << iSecret << std::endl;
  }


  return 0;
}