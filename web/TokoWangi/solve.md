**Solution Walkthrough**

Vulnerability : Parameter Tampering

**Step 1:  Login**
1. Akses url di port 8001
2. Register dan login ke web

**Step 2: Get The Flag**
1. Untuk mendapatkan flag kita harus membeli produk bernama FLAG seharga "7777777", sedangkan user hanya memiliki uang dengan jumlah "100"
2. User dapat melakukan intercept pada request buy dan memodifikasi nilai dari parameter price dengan nilai yang kurang dari jumlah uang user.

**Flag : LKSWNSB{pr!ce_tampering_1s_b4d_ev3n_my_Gr4ndma_kn0ws_it}**