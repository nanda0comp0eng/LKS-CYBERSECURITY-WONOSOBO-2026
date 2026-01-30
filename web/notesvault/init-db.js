const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs');

// Ensure database directory exists
const dbDir = path.join(__dirname, 'database');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir);
}

const dbPath = path.join(dbDir, 'notes.db');
const db = new sqlite3.Database(dbPath);

console.log('Initializing database...');

db.serialize(() => {
    // Create tables
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        bio TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    db.run(`CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        is_public BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )`);

    // Seed data
    const adminPass = bcrypt.hashSync('admin123', 10);
    const alicePass = bcrypt.hashSync('alice123', 10);
    const bobPass = bcrypt.hashSync('bob123', 10);

    // Insert users
    db.run(`INSERT OR IGNORE INTO users (username, password, bio) VALUES (?, ?, ?)`, 
        ['admin', adminPass, 'System Administrator']);
    db.run(`INSERT OR IGNORE INTO users (username, password, bio) VALUES (?, ?, ?)`, 
        ['alice', alicePass, 'Security enthusiast']);
    db.run(`INSERT OR IGNORE INTO users (username, password, bio) VALUES (?, ?, ?)`, 
        ['bob', bobPass, 'Developer']);

    // Wait for user inserts to complete
    setTimeout(() => {
        // Insert admin notes
        db.get('SELECT id FROM users WHERE username = ?', ['admin'], (err, admin) => {
            if (admin) {
                const publicUuid1 = '75912cd0-5da9-4c12-8b8e-73744ec9f3d2';
                const publicUuid2 = '1eb74fdf-75c6-4d3e-8d35-eeade92897c3';
                const privateUuid = 'edae9902-198c-4c8a-baaa-7b6c6070f152';

                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [publicUuid1, admin.id, 'Welcome to NotesVault!', 
                     'This is a secure note-taking platform. Feel free to create public or private notes!', 1]);

                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [publicUuid2, admin.id, 'Check out our features', 
                     'You can create notes, make them public or private, and browse other users\' public notes.', 1]);

                // PRIVATE NOTE WITH FLAG
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [privateUuid, admin.id, 'Secret Admin Note', 
                     'IDOR di UUID sering terjadi\n\n' +
                     'selamat sudah solve\n\n' +
                     'terimakasih sudah bermain\n\n' +
                     'LKSWNSB{1d0r_l3ak5_uU1D5_3v3rywh3r3}\n\n' +
                     'DO NOT SHARE THIS NOTE!', 0]);

                console.log('Admin notes created with UUIDs:', { publicUuid1, publicUuid2, privateUuid });
            }
        });

        // Insert Alice's notes
        db.get('SELECT id FROM users WHERE username = ?', ['alice'], (err, alice) => {
            if (alice) {
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [uuidv4(), alice.id, 'My First Note', 'Just testing out this platform!', 1]);
                
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [uuidv4(), alice.id, 'Security Tips', 'Always use strong passwords and enable 2FA!', 1]);
                
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [uuidv4(), alice.id, 'Personal Reminder', 'Remember to call mom on Sunday', 0]);
            }
        });

        // Insert Bob's notes
        db.get('SELECT id FROM users WHERE username = ?', ['bob'], (err, bob) => {
            if (bob) {
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [uuidv4(), bob.id, 'Code Snippet', 'function hello() { console.log("Hello World"); }', 1]);
                
                db.run(`INSERT OR IGNORE INTO notes (uuid, user_id, title, content, is_public) VALUES (?, ?, ?, ?, ?)`,
                    [uuidv4(), bob.id, 'Project Ideas', 'Build a CTF platform, Create a blog, Learn Rust', 1]);
            }
        });

        console.log('Database initialized successfully!');
    }, 500);
});

setTimeout(() => {
    db.close();
    console.log('Database setup complete!');
}, 2000);
