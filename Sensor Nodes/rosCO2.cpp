#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

using namespace std;

int main(int argc, char const *argv[]) {
  int fd = open("/dev/ttyACM0", O_RDONLY);
  char co2_reading[15];

  //while(1) {
    read(fd, co2_reading, 15);

    printf("%s\n", co2_reading);
  //}

  return 0;
}
