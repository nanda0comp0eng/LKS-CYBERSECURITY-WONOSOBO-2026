# NotesVault

## Challenge Description

**Difficulty:** Beginner-Intermediate  
**Category:** Web Security 
**Author:** pyrg  
**Flag:** `LKSWNSB{1d0r_l3ak5_uU1D5_3v3rywh3r3}`

NotesVault is a secure note-taking platform where users can create public or private notes. The admin user has left a secret flag in a private note. Can you find it?

**Objective:** Exploit an Insecure Direct Object Reference (IDOR) vulnerability to access the admin's private note and retrieve the flag.

---

## Setup Instructions

### Option 1: Docker (Recommended)

```bash
# Clone or extract the challenge files
cd ctf-notesvault

# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Open http://localhost:3000 in your browser
```

### Option 2: Manual Setup

```bash
# Install dependencies
npm install

# Initialize database
node init-db.js

# Start the application
node app.js

# Access at http://localhost:3000
```

---

## Test Credentials

- **Admin Account:**
  - Username: `admin`
  - Password: `admin123`
  
- **Test Accounts:**
  - Username: `alice` / Password: `alice123`
  - Username: `bob` / Password: `bob123`

> ⚠️ **Note:** You should NOT use the admin credentials to get the flag! The challenge is to exploit the vulnerability without knowing the admin password.

---

## Application Features

1. **User Registration & Authentication**
2. **Create Notes** (Public or Private)
3. **View Personal Dashboard**
4. **Browse Public Notes Feed**
5. **View User Profiles**

---

## Vulnerability Overview

This challenge contains **TWO vulnerabilities** that must be chained together:

### Vulnerability #1: Information Disclosure via API
**Endpoint:** `/api/profile/:username`

The API endpoint returns ALL of a user's notes (including private ones) with their UUIDs visible in the JSON response.

```javascript
// VULNERABLE CODE
app.get('/api/profile/:username', (req, res) => {
    db.all('SELECT uuid, title, is_public FROM notes WHERE user_id = ?', 
        [user.id], 
        (err, notes) => {
            res.json({
                username: user.username,
                bio: user.bio,
                notes: notes // ⚠️ Returns ALL notes including private!
            });
        }
    );
});
```

### Vulnerability #2: Missing Authorization Check
**Endpoint:** `/notes?uuid=<UUID>`

This endpoint displays any note by UUID without checking if:
- The note is public
- The current user owns the note

```javascript
// VULNERABLE CODE
app.get('/notes', (req, res) => {
    db.get('SELECT * FROM notes WHERE uuid = ?', [uuid], (err, note) => {
        // ⚠️ No privacy or ownership check!
        res.render('note', { note });
    });
});
```

---

## Solution Walkthrough

### Step 1: Create an Account
1. Navigate to http://localhost:3000
2. Click "Register" and create a new account
3. Explore the application to understand its functionality

### Step 2: Find the Admin User
1. Go to "Public Notes" page
2. You'll see public notes from various users including `admin`
3. Click on the `admin` username to view their profile

### Step 3: Intercept the API Call
1. Open **Browser DevTools** (F12) and go to the "Network" tab
   - OR use **Burp Suite** to intercept HTTP traffic

2. On the admin's profile page, you'll see an API call to:
   ```
   GET /api/profile/admin
   ```

3. Examine the API response:
   ```json
   {
     "username": "admin",
     "bio": "System Administrator",
     "notes": [
       {
         "uuid": "abc123-public-1",
         "title": "Welcome to NotesVault!",
         "is_public": 1
       },
       {
         "uuid": "xyz789-public-2",
         "title": "Check out our features",
         "is_public": 1
       },
       {
         "uuid": "def456-PRIVATE",
         "title": "Secret Admin Note",
         "is_public": 0  // ⚠️ PRIVATE NOTE WITH UUID LEAKED!
       }
     ]
   }
   ```

### Step 4: Extract Private Note UUID
1. Copy the UUID of the private note (where `is_public: 0`)
2. The title "Secret Admin Note" looks promising!

### Step 5: Access the Private Note
1. Manually navigate to:
   ```
   http://localhost:3000/notes?uuid=<PRIVATE_UUID>
   ```
   
2. Replace `<PRIVATE_UUID>` with the actual UUID you copied

3. The application will display the private note content without checking authorization!

### Step 6: Capture the Flag
The private note contains:
```
FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}
```

---

## Key Learning Points

1. **IDOR (Insecure Direct Object Reference):**
   - Never expose internal object identifiers without proper authorization
   - Always validate that the requesting user has permission to access the resource

2. **Information Disclosure:**
   - API endpoints should only return data the user is authorized to see
   - Filter sensitive information before sending responses

3. **Defense Strategies:**
   - Implement proper access control checks
   - Use indirect references (mapping IDs that are user-specific)
   - Apply the principle of least privilege

---

## How to Fix the Vulnerabilities

### Fix #1: Filter Private Notes in API Response
```javascript
app.get('/api/profile/:username', (req, res) => {
    db.all('SELECT uuid, title, is_public FROM notes WHERE user_id = ?', 
        [user.id], 
        (err, notes) => {
            // Only return public notes OR notes owned by requester
            const visibleNotes = notes.filter(note => 
                note.is_public || req.session.userId === user.id
            );
            
            res.json({
                username: user.username,
                bio: user.bio,
                notes: visibleNotes
            });
        }
    );
});
```

### Fix #2: Add Authorization Check
```javascript
app.get('/notes', (req, res) => {
    const { uuid } = req.query;
    
    db.get('SELECT * FROM notes WHERE uuid = ?', [uuid], (err, note) => {
        if (err || !note) return res.status(404).send('Note not found');
        
        // Check if note is public OR user owns it
        if (!note.is_public && note.user_id !== req.session.userId) {
            return res.status(403).send('Access denied');
        }
        
        res.render('note', { note });
    });
});
```

---

## Additional Challenges (Optional)

Try these advanced variations:

1. **Find all private notes** from all users in the database
2. **Automate the exploitation** using a Python script
3. **Write a Burp Suite extension** to detect this vulnerability
4. **Implement rate limiting** to prevent enumeration attacks

---

## Tools You Can Use

- **Browser DevTools** (Built into Chrome/Firefox - Press F12)
- **Burp Suite Community Edition** (HTTP proxy for security testing)
- **Postman** or **curl** (API testing)
- **Python + requests library** (Automation)

---

## References

- [OWASP Top 10 - Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [OWASP IDOR Guide](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
- [PortSwigger IDOR Labs](https://portswigger.net/web-security/access-control/idor)

---

## Challenge Author

Created for CTF practice - IDOR vulnerability exploitation

**Flag Format:** `LKSWNSB{...}`

FLAG: LKSWNSB{1d0r_l3ak5_uU1D5_3v3rywh3r3}

Good luck! 🚩
