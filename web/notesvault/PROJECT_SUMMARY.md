# NotesVault CTF Challenge - Project Summary

## Overview

This is a complete, production-ready CTF (Capture The Flag) challenge focused on **IDOR (Insecure Direct Object Reference)** vulnerabilities. The challenge is designed for beginner to intermediate security learners.

## What's Included

### Application Files
- **app.js** - Main Express.js server with intentional IDOR vulnerabilities
- **init-db.js** - Database initialization script with seed data
- **package.json** - Node.js dependencies
- **views/** - EJS templates for all pages
  - index.ejs (home page)
  - register.ejs & login.ejs (authentication)
  - dashboard.ejs (user's notes)
  - public.ejs (public notes feed)
  - profile.ejs (user profiles)
  - note.ejs (individual note view)
- **public/** - Static assets (CSS)

### Docker Configuration
- **Dockerfile** - Container configuration
- **docker-compose.yml** - Easy deployment setup

### Documentation
- **README.md** - Complete setup and challenge guide
- **SOLUTION.md** - Detailed exploitation walkthrough
- **HINTS.md** - Progressive hints for participants
- **PROJECT_SUMMARY.md** - This file

### Tools & Scripts
- **exploit.py** - Python automation script for exploitation
- **start.sh** - Bash script for quick startup
- **test.sh** - Verification script to confirm vulnerability

## Quick Start

```bash
# Using Docker (Recommended)
cd ctf-notesvault
docker-compose up -d

# OR Manual Setup
cd ctf-notesvault
npm install
node init-db.js
node app.js

# Access at http://localhost:3000
```

## The Challenge

**Objective:** Find the admin's secret flag stored in a private note

**Flag:** `FLAG{1d0r_l3ak5_uU1D5_3v3rywh3r3}`

### Vulnerabilities Implemented

1. **Information Disclosure** - API endpoint leaks UUIDs of private notes
   - Endpoint: `/api/profile/:username`
   - Returns ALL notes (public and private) with UUIDs

2. **Missing Authorization** - Note viewing doesn't check ownership
   - Endpoint: `/notes?uuid=<UUID>`
   - Displays any note without verifying user permissions

### Solution Summary

1. Visit admin's profile page
2. Intercept API call using DevTools or Burp Suite
3. Extract UUID of private note from API response
4. Access private note directly using the UUID
5. Retrieve the flag

## Educational Value

This challenge teaches:
- **IDOR vulnerability identification**
- **API security analysis**
- **Browser DevTools usage**
- **Authorization bypass techniques**
- **Proper access control implementation**

## Security Features (Intentionally Absent)

To make this a valid learning exercise, the following security controls are intentionally missing:

- ✗ No authorization checks on note access
- ✗ No filtering of private data in API responses
- ✗ No rate limiting
- ✗ No logging of suspicious access patterns

## Test Accounts

```
Admin:
  Username: admin
  Password: admin123
  
Test Users:
  Username: alice / Password: alice123
  Username: bob / Password: bob123
```

## File Structure

```
ctf-notesvault/
├── app.js                 # Main application
├── init-db.js            # Database setup
├── package.json          # Dependencies
├── Dockerfile            # Container config
├── docker-compose.yml    # Docker deployment
├── start.sh             # Quick start script
├── test.sh              # Verification script
├── exploit.py           # Automated exploit
├── README.md            # Main documentation
├── SOLUTION.md          # Complete solution
├── HINTS.md             # Progressive hints
├── views/               # EJS templates
│   ├── index.ejs
│   ├── register.ejs
│   ├── login.ejs
│   ├── dashboard.ejs
│   ├── public.ejs
│   ├── profile.ejs
│   ├── note.ejs
│   └── partials/
│       └── header.ejs
├── public/              # Static files
│   └── style.css
└── database/            # SQLite database
    └── notes.db (created at runtime)
```

## Technology Stack

- **Backend:** Node.js + Express.js
- **Database:** SQLite3
- **Templating:** EJS
- **Authentication:** bcrypt + express-session
- **Containerization:** Docker

## Key Code Snippets

### Vulnerable Endpoint #1: Profile API
```javascript
app.get('/api/profile/:username', (req, res) => {
    // BUG: Returns ALL notes including private ones with UUIDs!
    db.all('SELECT uuid, title, is_public FROM notes WHERE user_id = ?', 
        [user.id], 
        (err, notes) => {
            res.json({
                username: user.username,
                bio: user.bio,
                notes: notes // Contains UUIDs of private notes!
            });
        }
    );
});
```

### Vulnerable Endpoint #2: Note Access
```javascript
app.get('/notes', (req, res) => {
    const { uuid } = req.query;
    
    db.get('SELECT * FROM notes WHERE uuid = ?', [uuid], (err, note) => {
        // BUG: Doesn't check if note is_public or if user owns it!
        res.render('note', { note });
    });
});
```

## Deployment Options

### Local Development
```bash
npm install
node init-db.js
node app.js
```

### Docker
```bash
docker-compose up -d
```

### Production Deployment
- Can be deployed to any Node.js hosting platform
- Requires minimal resources (SQLite database)
- Port 3000 must be accessible

## Testing the Vulnerability

### Manual Testing
1. Browse to `/public`
2. Click admin profile
3. Open DevTools → Network tab
4. Examine `/api/profile/admin` response
5. Find private note UUID
6. Access `/notes?uuid=<UUID>`

### Automated Testing
```bash
# Run the exploit script
python3 exploit.py

# Or verify with test script
./test.sh
```

## Learning Outcomes

After completing this challenge, participants will understand:

1. **What is IDOR?**
   - How to identify IDOR vulnerabilities
   - Common attack patterns
   - Real-world impact

2. **API Security**
   - Importance of filtering sensitive data
   - Proper response design
   - Information disclosure risks

3. **Access Control**
   - Authorization vs Authentication
   - Implementing proper checks
   - Defense in depth

4. **Security Tools**
   - Browser DevTools for security testing
   - Burp Suite basics
   - API testing techniques

## Remediation Guide

The SOLUTION.md file includes complete code fixes for both vulnerabilities:

1. **Filter API responses** - Only return data user is authorized to see
2. **Implement authorization checks** - Verify ownership before displaying notes
3. **Additional hardening** - Rate limiting, logging, indirect references

## CTF Integration

This challenge can be integrated into:
- **CTFd platforms** - Use as a web challenge
- **HackTheBox style boxes** - Deploy as a vulnerable service
- **Training environments** - Teach IDOR concepts
- **Bug bounty training** - Simulate real vulnerabilities

## Difficulty Rating

**Beginner-Intermediate** because:
- Requires basic understanding of web apps
- Needs ability to use DevTools or Burp Suite
- No complex exploitation required
- Teaches fundamental security concept

## Support & Issues

This is a standalone challenge with complete documentation:
- README.md - Setup and overview
- SOLUTION.md - Complete solution
- HINTS.md - Progressive hints

## License & Usage

This challenge is provided for educational purposes. Feel free to:
- Use in CTF competitions
- Modify for training purposes
- Share with attribution
- Use in educational settings

## Credits

Challenge designed to teach IDOR vulnerabilities through practical exploitation.

---

**Happy Hacking! 🚩**
