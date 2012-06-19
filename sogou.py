#!/usr/bin/env python


def compute_sogou_tag(timestamp, hostname):
    s = timestamp + hostname + 'SogouExplorerProxy'

    total_len = len(s)
    numb_iter = total_len / 4
    numb_left = total_len % 4

    tag = total_len

    for i in range(numb_iter):
        low = (ord(s[4 * i + 1]) << 8) + ord(s[4 * i])
        high = (ord(s[4 * i + 3]) << 8) + ord(s[4 * i + 2])

        tag += low
        tag ^= tag << 16
        tag ^= high << 11
        tag &= 0xFFFFFFFF
        tag += tag >> 11

    tag &= 0xFFFFFFFF
    if numb_left == 3:
        tag += (ord(s[-2]) << 8) + ord(s[-3])
        tag ^= tag << 16
        tag ^= ord(s[-1]) << 18
        tag &= 0xFFFFFFFF
        tag += tag >> 11
    elif numb_left == 2:
        tag += (ord(s[-1]) << 8) + ord(s[-2])
        tag ^= tag << 11
        tag &= 0xFFFFFFFF
        tag += tag >> 17
    elif numb_left == 1:
        tag += ord(s[-1])
        tag ^= tag << 10
        tag &= 0xFFFFFFFF
        tag += tag >> 1

    tag ^= tag << 3
    tag &= 0xFFFFFFFF
    tag += tag >> 5

    tag ^= tag << 4
    tag &= 0xFFFFFFFF
    tag += tag >> 17

    tag ^= tag << 25
    tag &= 0xFFFFFFFF
    tag += tag >> 6

    tag &= 0xFFFFFFFF
    return ('00000000' + hex(tag)[2:].rstrip('L'))[-8:]

if __name__ == '__main__':
    t = '4fe01fa9'
    d = '123.youku.com'
    #t = '4fdfe48a'
    #d = 's.plcloud.music.qq.com'
    print compute_sogou_tag(t, d)
