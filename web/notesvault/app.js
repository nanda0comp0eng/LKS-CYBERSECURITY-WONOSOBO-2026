const express = require('express');
const session = require('express-session');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');
const path = require('path');

const app = express();
const PORT = 3000;

// Database connection
const db = new sqlite3.Database(path.join(__dirname, 'database', 'notes.db'));

// Middleware
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'ctf-secret-key-2024',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 3600000 }
}));

// Auth middleware
const requireAuth = (req, res, next) => {
    if (!req.session.userId) {
        // If it's an API request, return 401 JSON instead of redirecting
        if (req.path.startsWith('/api/')) {
            return res.status(401).json({ error: 'Unauthorized' });
        }
        return res.redirect('/login');
    }
    next();
};

// ===== PAGE ROUTES =====

// Home page
app.get('/', (req, res) => {
    res.render('index', { user: req.session.username });
});

// Register page
app.get('/register', (req, res) => {
    if (req.session.userId) return res.redirect('/dashboard');
    res.render('register', { error: null, user: null });
});

// Handle Register Form Submission
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.render('register', { error: 'Username and password required', user: null });
    }
    
    const hashedPassword = await bcrypt.hash(password, 10);
    
    db.run('INSERT INTO users (username, password) VALUES (?, ?)', 
        [username, hashedPassword], 
        function(err) {
            if (err) {
                console.error('Registration error:', err);
                if (err.message && err.message.includes('UNIQUE constraint failed')) {
                    return res.render('register', { error: 'Username already exists', user: null });
                }
                return res.render('register', { error: 'Registration failed: ' + err.message, user: null });
            }
            
            req.session.userId = this.lastID;
            req.session.username = username;
            res.redirect('/dashboard');
        }
    );
});

// Login page
app.get('/login', (req, res) => {
    if (req.session.userId) return res.redirect('/dashboard');
    res.render('login', { error: null, user: null });
});

// Handle Login Form Submission
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    db.get('SELECT * FROM users WHERE username = ?', [username], async (err, user) => {
        if (err || !user) {
            return res.render('login', { error: 'Invalid credentials', user: null });
        }
        
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.render('login', { error: 'Invalid credentials', user: null });
        }
        
        req.session.userId = user.id;
        req.session.username = user.username;
        res.redirect('/dashboard');
    });
});

// Dashboard - user's own notes
app.get('/dashboard', requireAuth, (req, res) => {
    db.all('SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC', 
        [req.session.userId], 
        (err, notes) => {
            res.render('dashboard', { 
                user: req.session.username,
                notes: notes || []
            });
        }
    );
});

// Public notes feed
app.get('/public', requireAuth, (req, res) => {
    db.all(`SELECT notes.*, users.username 
            FROM notes 
            JOIN users ON notes.user_id = users.id 
            WHERE is_public = 1 
            ORDER BY notes.created_at DESC`, 
        (err, notes) => {
            res.render('public', { 
                user: req.session.username,
                notes: notes || []
            });
        }
    );
});

// User profile page
app.get('/profile/:username', (req, res) => {
    const { username } = req.params;
    
    db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
        if (err || !user) return res.status(404).send('User not found');
        
        res.render('profile', { 
            user: req.session.username,
            profileUser: user
        });
    });
});

// VULNERABLE ENDPOINT #2: View specific note - NO PRIVACY CHECK!
app.get('/notes', (req, res) => {
    const { uuid } = req.query;
    
    if (!uuid) {
        return res.status(400).send('UUID required');
    }
    
    db.get('SELECT notes.*, users.username FROM notes JOIN users ON notes.user_id = users.id WHERE uuid = ?', 
        [uuid], 
        (err, note) => {
            if (err || !note) return res.status(404).send('Note not found');
            
            // BUG: Doesn't check if note is_public or if user owns it!
            // This is the second vulnerability that allows viewing private notes
            res.render('note', { 
                user: req.session.username,
                note: note
            });
        }
    );
});

// ===== API ROUTES =====

// Register
app.post('/api/register', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
    }
    
    const hashedPassword = await bcrypt.hash(password, 10);
    
    db.run('INSERT INTO users (username, password) VALUES (?, ?)', 
        [username, hashedPassword], 
        function(err) {
            if (err) {
                console.error('API Registration error:', err);
                if (err.message && err.message.includes('UNIQUE constraint failed')) {
                    return res.status(400).json({ error: 'Username already exists' });
                }
                return res.status(500).json({ error: 'Registration failed: ' + err.message });
            }
            
            req.session.userId = this.lastID;
            req.session.username = username;
            res.json({ success: true });
        }
    );
});

// Login
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    db.get('SELECT * FROM users WHERE username = ?', [username], async (err, user) => {
        if (err || !user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        req.session.userId = user.id;
        req.session.username = user.username;
        res.json({ success: true });
    });
});

// Logout
app.post('/api/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true });
});

// Create note
app.post('/api/notes', requireAuth, (req, res) => {
    const { title, content, isPublic } = req.body;
    const uuid = uuidv4();
    
    db.run('INSERT INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)',
        [uuid, req.session.userId, title, content, isPublic ? 1 : 0],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Failed to create note' });
            }
            res.json({ success: true, uuid: uuid });
        }
    );
});

// Get public notes
app.get('/api/notes/public', (req, res) => {
    db.all(`SELECT notes.*, users.username 
            FROM notes 
            JOIN users ON notes.user_id = users.id 
            WHERE is_public = 1 
            ORDER BY notes.created_at DESC`, 
        (err, notes) => {
            if (err) return res.status(500).json({ error: 'Database error' });
            res.json(notes);
        }
    );
});

// Get current user's notes
app.get('/api/notes/my', requireAuth, (req, res) => {
    db.all('SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC',
        [req.session.userId],
        (err, notes) => {
            if (err) return res.status(500).json({ error: 'Database error' });
            res.json(notes);
        }
    );
});

// VULNERABLE ENDPOINT #1: Get user profile - LEAKS ALL NOTE UUIDs!
app.get('/api/profile/:username', (req, res) => {
    const { username } = req.params;
    
    db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
        if (err || !user) return res.status(404).json({ error: 'User not found' });
        
        // BUG: Returns ALL notes including private ones with UUIDs!
        // This is the first vulnerability - information disclosure
        db.all('SELECT uuid, title, is_public, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC', 
            [user.id], 
            (err, notes) => {
                res.json({
                    username: user.username,
                    bio: user.bio,
                    created_at: user.created_at,
                    notes: notes // Contains UUIDs of private notes!
                });
            }
        );
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`NotesVault CTF running on http://localhost:${PORT}`);
    console.log('Challenge: Find the admin\'s secret flag!');
});
