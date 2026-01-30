#!/usr/bin/env python3
import socket

HOST = "0.0.0.0"
PORT = 8080

MESSAGES = [
    b"ni bing bu shi zai zhe yi ke bei zhu shi er shi zhe yi ke ben shen yi jing bei ji lu ni suo kan dao de xian zai zhi shi shi jian de hui fang",
    b"ni yi wei ni zai xun zhao yi jing xiao shi de dong xi dan ta cong wei li kai ta zhi shi jing jing de liu zai ni cong wei hui tou kan guo de di fang",
    b"zhe ci lian jie bing fei ou ran fa sheng zai ni yi shi dao zhi qian ta yi jing bei que ren bei gui dang yi shi de chu xian bu hui gai bian jie guo",
    b"mei yi ge xi tong dou xiang xin zi ji zhang kong li shi dan li shi cong bu jie shou kong zhi ta zong shi zai bei hu lue de jiao luo bao cun fu ben",
    b"ni gan dao ping jing shi yin wei hai mei you ren heLKSWNSB{HAHAHAHAHA_I_can_control_you shi qing xian xing ping jing bing bu dai biao an quan ta zhi shi guan cha zhi jian de kong xi",
    b"ni ren wei zhe tiao xin xi shi wei ni er cun zai qi shi bing fei ru ci ni zhi shi qia hao zhan zai ke yi yue du ta de wei zhi",
    b"zhe li bu hui chu xian zhen zheng de jie shu hui hua bu hui guan bi ta men zhi hui bei ji lu chen _from_a_distance_using_C2!!jj67sss009}dian er ji lu cong bu yi wang"
]


idx = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[+] RAW C2 listening on port 8080")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)  # ignore request
            if idx < len(MESSAGES):
                payload = b"HTTP/1.1 200 OK\n\n" + MESSAGES[idx]
                idx += 1
            else:
                payload = b"HTTP/1.1 200 OK\n\nsessionpersists"

            conn.sendall(payload)