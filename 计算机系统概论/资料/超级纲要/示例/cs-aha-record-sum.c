#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* 1: four bytes; 0: EOF before any byte; -2: partial field; -1: error. */
static int read4(int fd, unsigned char bytes[4]) {
    size_t done = 0;
    while (done < 4) {
        ssize_t r = read(fd, bytes + done, 4 - done);
        if (r < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        if (r == 0) return done == 0 ? 0 : -2;
        done += (size_t)r;
    }
    return 1;
}
static uint32_t be32(const unsigned char b[4]) {
    return ((uint32_t)b[0] << 24) | ((uint32_t)b[1] << 16)
         | ((uint32_t)b[2] << 8) | (uint32_t)b[3];
}
static int reject(int fd, const char *message) {
    fputs(message, stderr);
    if (close(fd) == -1) perror("close");
    return EXIT_FAILURE;
}
int main(int argc, char **argv) {
    if (argc != 2) {
        fputs("usage: record-sum file\n", stderr);
        return EXIT_FAILURE;
    }
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) { perror("open"); return EXIT_FAILURE; }
    unsigned char b[4];
    if (read4(fd, b) != 1)
        return reject(fd, "missing or incomplete header\n");
    uint32_t n = be32(b);
    if (n > 1000000u)
        return reject(fd, "too many elements\n");
    uint64_t total = 0;
    for (uint32_t i = 0; i < n; ++i) {
        if (read4(fd, b) != 1)
            return reject(fd, "missing or incomplete element\n");
        total += be32(b);
    }
    unsigned char extra;
    ssize_t r;
    do { r = read(fd, &extra, 1); } while (r < 0 && errno == EINTR);
    if (r < 0) return reject(fd, "cannot check file end\n");
    if (r > 0) return reject(fd, "unexpected trailing data\n");
    int ok = printf("%" PRIu64 "\n", total) >= 0;
    if (close(fd) == -1) { perror("close"); ok = 0; }
    if (fflush(stdout) == EOF) ok = 0;
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
