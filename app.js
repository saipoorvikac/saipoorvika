const express = require("express");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const cors = require("cors");
const crypto = require("crypto");

const app = express();
app.use(express.json());
app.use(cors());

const PORT = 5000;
const SECRET = "super_secure_key";

// ===== In-memory DB =====
let users = [];
let patients = [];

// ===== Encryption (basic HIPAA-style simulation) =====
function encrypt(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

// ===== AUTH =====
app.post("/api/register", async (req, res) => {
  const hashed = await bcrypt.hash(req.body.password, 10);

  users.push({
    email: encrypt(req.body.email),
    password: hashed
  });

  res.json({ message: "User registered securely" });
});

app.post("/api/login", async (req, res) => {
  const emailHash = encrypt(req.body.email);

  const user = users.find(u => u.email === emailHash);
  if (!user) return res.status(400).send("User not found");

  const valid = await bcrypt.compare(req.body.password, user.password);
  if (!valid) return res.status(400).send("Invalid password");

  const token = jwt.sign({ email: emailHash }, SECRET);
  res.json({ token });
});

// ===== AUTH MIDDLEWARE =====
function auth(req, res, next) {
  const token = req.headers.authorization;
  if (!token) return res.status(401).send("No token");

  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    res.status(401).send("Invalid token");
  }
}

// ===== PATIENT =====
app.post("/api/patient", auth, (req, res) => {
  const encryptedName = encrypt(req.body.name);

  patients.push({
    name: encryptedName,
    createdAt: new Date()
  });

  res.json({ message: "Patient stored securely" });
});

app.get("/api/patient", auth, (req, res) => {
  res.json(patients);
});

// ===== ANALYTICS (Predictive) =====
app.get("/api/analytics", auth, (req, res) => {
  const heartRate = Math.floor(Math.random() * 50) + 60;
  const bp = Math.floor(Math.random() * 40) + 100;

  let risk = "Low";
  if (heartRate > 100 || bp > 140) risk = "High";

  res.json({
    heartRate,
    bloodPressure: bp,
    risk,
    prediction:
      risk === "High"
        ? "Potential cardiovascular issue"
        : "Stable condition"
  });
});

// ===== PERFORMANCE (Pagination example) =====
app.get("/api/patient-list", auth, (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = 5;

  const start = (page - 1) * limit;
  const end = start + limit;

  res.json({
    data: patients.slice(start, end),
    page
  });
});

// ===== NOTIFICATIONS =====
app.post("/api/notify", auth, (req, res) => {
  console.log("🔔 ALERT:", req.body.message);
  res.json({ message: "Notification triggered" });
});

// ===== FRONTEND UI =====
app.get("/", (req, res) => {
  res.send(`
  <html>
  <head>
    <title>Healthcare System</title>
  </head>
  <body style="font-family: Arial; padding:20px">

    <h1>Healthcare Monitoring System</h1>

    <h3>Register</h3>
    <input id="rEmail" placeholder="Email"/>
    <input id="rPass" type="password" placeholder="Password"/>
    <button onclick="register()">Register</button>

    <h3>Login</h3>
    <input id="lEmail" placeholder="Email"/>
    <input id="lPass" type="password" placeholder="Password"/>
    <button onclick="login()">Login</button>

    <h3>Add Patient</h3>
    <input id="pName" placeholder="Patient Name"/>
    <button onclick="addPatient()">Add</button>

    <h3>Analytics</h3>
    <button onclick="analytics()">Run Prediction</button>

    <h3>Notification</h3>
    <input id="msg" placeholder="Message"/>
    <button onclick="notify()">Send Alert</button>

    <pre id="output"></pre>

    <script>
      let token = "";

      async function register(){
        await fetch("/api/register",{
          method:"POST",
          headers:{"Content-Type":"application/json"},
          body:JSON.stringify({
            email:rEmail.value,
            password:rPass.value
          })
        });
        alert("Registered");
      }

      async function login(){
        const res = await fetch("/api/login",{
          method:"POST",
          headers:{"Content-Type":"application/json"},
          body:JSON.stringify({
            email:lEmail.value,
            password:lPass.value
          })
        });

        const data = await res.json();
        token = data.token;
        alert("Logged in");
      }

      async function addPatient(){
        await fetch("/api/patient",{
          method:"POST",
          headers:{
            "Content-Type":"application/json",
            "Authorization":token
          },
          body:JSON.stringify({name:pName.value})
        });
        alert("Patient added");
      }

      async function analytics(){
        const res = await fetch("/api/analytics",{
          headers:{ "Authorization":token }
        });
        const data = await res.json();
        output.innerText = JSON.stringify(data,null,2);
      }

      async function notify(){
        await fetch("/api/notify",{
          method:"POST",
          headers:{
            "Content-Type":"application/json",
            "Authorization":token
          },
          body:JSON.stringify({message:msg.value})
        });
        alert("Notification sent");
      }
    </script>

  </body>
  </html>
  `);
});

// ===== START SERVER =====
app.listen(PORT, () => {
  console.log("🚀 Server running at http://localhost:" + PORT);
});