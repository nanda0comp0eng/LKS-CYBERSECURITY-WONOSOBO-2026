# WM-Header

**Category:** Web
**Author:** pyrg

ya header, header ya header



## ✅ Solution 

### Method 1 — Browser DevTools
1. Open the site in Chrome/Firefox.
2. Press **F12** → go to the **Network** tab.
3. Reload the page.
4. Click on the main document request.
5. Under **Response Headers**, find `X-Flag`.

### Method 2 — curl

```bash
curl -v http://localhost:5000/
# Look for: < X-Flag: LKSWNSB{...}
```

### Method 3 — Python

```python
import requests
r = requests.get("http://localhost:5000/")
print(r.headers.get("X-Flag"))
```

---

## 🏁 Flag

```
LKSWNSB{h3ad3r_jug4_p3nt1ng}
```

---

## ⚙️ Customization

| What | Where | How |
|------|-------|-----|
| Change the flag | `app.py` → `FLAG` variable | Edit the string |
| Change the port | `docker-compose.yml` → `ports` | e.g., `"8080:5000"` |
| Add new routes | `app.py` + `templates/` | Add a new route + template |
| Add more hints | `templates/hint.html` | Add another hint block |

---

> **Tip for CTF organizers:** To make it harder, remove the `/hint` page and the instructional text from `index.html`. Let players figure out the attack surface on their own.
