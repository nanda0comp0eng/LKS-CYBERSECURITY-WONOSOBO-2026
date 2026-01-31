import express from "express";
import http from "http";
import path from "path";
import { fileURLToPath } from "url";
import { WebSocketServer } from "ws";
import mysql from "mysql2/promise";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = parseInt(process.env.PORT || "8080", 10);

const DB_HOST = process.env.DB_HOST || "127.0.0.1";
const DB_USER = process.env.DB_USER || "ctfuser";
const DB_PASS = process.env.DB_PASS || "ctfpass";
const DB_NAME = process.env.DB_NAME || "ctf";

async function makeDb() {
  return mysql.createPool({
    host: DB_HOST,
    user: DB_USER,
    password: DB_PASS,
    database: DB_NAME,
    connectionLimit: 5
  });
}

const app = express();
app.use(express.static(path.join(__dirname, "public")));

const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: "/ws" });

const db = await makeDb();

function safeJsonParse(s) {
  try { return JSON.parse(s); } catch { return null; }
}

wss.on("connection", (ws) => {
  ws.send(JSON.stringify({ type: "hello", msg: "connected" }));

  ws.on("message", async (buf) => {
    const data = safeJsonParse(buf.toString("utf8"));
    if (!data || data.type !== "verify") {
      ws.send(JSON.stringify({ type: "error", msg: "bad request" }));
      return;
    }

    const orderId = String(data.orderId ?? "");
    const email = String(data.email ?? "");

    try {
      const q =
        "SELECT 1 FROM orders " +
        "WHERE order_id = '" + orderId + "' " +
        "AND email = '" + email + "' " +
        "LIMIT 1";

      const [rows] = await db.query(q);

      const ok = Array.isArray(rows) && rows.length > 0;
      ws.send(JSON.stringify({ type: "result", ok }));
    } catch (e) {
      ws.send(JSON.stringify({ type: "result", ok: false }));
    }
  });
});

server.listen(PORT, () => {
  console.log(`CTF app listening on http://0.0.0.0:${PORT}`);
});
