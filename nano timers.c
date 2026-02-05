#include <stdio.h>
#include <sys/time.h>

static struct timeval currenttime;

void tl_update_time(void) {
    gettimeofday(&currenttime, NULL);
}

long tl_milliseconds(void) {
    return currenttime.tv_sec * 1000L + currenttime.tv_usec / 1000L;
}

int main() {
    tl_update_time();
    printf("Current time: %ld ms\n", tl_milliseconds());
    return 0;
}
