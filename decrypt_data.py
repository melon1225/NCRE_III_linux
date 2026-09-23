#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data.dat 解密脚本
=================
原理：该文件是「测未来」考试平台（JFT 系列）的 SQLite 题库数据库，
整体按 1024 字节一页做了 XOR 流加密（每页使用同一段 1024 字节密钥流）。

密钥流来源：文件中存在多页明文全零/空叶节点页（SQLite 空页，内容为
0x0d 00 00 00 00 04 00 ...），其密文即密钥流本身；其中偏移 0 和 5
需按 SQLite 空叶页头部修正（0x0d=页类型、0x0400=内容区起始）。

用法：python3 decrypt_data.py <输入.dat> <输出.db>
"""
import sys


def decrypt(src_path: str, dst_path: str) -> None:
    with open(src_path, 'rb') as f:
        data = f.read()

    # 取第 3 页（文件偏移 3072 起）作为空叶页密文（密钥流基础）
    empty_page = data[3 * 1024: 4 * 1024]
    key = bytearray(empty_page)
    key[0] ^= 0x0d          # SQLite 空叶表页类型 0x0d
    key[5] ^= 0x04          # 内容区起始 0x0400

    plain = bytes(b ^ key[i % 1024] for i, b in enumerate(data))
    with open(dst_path, 'wb') as f:
        f.write(plain)
    print(f'解密完成：{src_path} -> {dst_path}（{len(plain)} 字节）')
    assert plain[:16] == b'SQLite format 3\x00', '解密校验失败，文件头不是 SQLite 格式'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    decrypt(sys.argv[1], sys.argv[2])
#（注：内容由AI生成）
