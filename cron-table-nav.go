package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"sync"
	"time"
)

// 🧱 โครงสร้างข้อมูล
type CronJob struct {
	ID         string    `json:"id"`
	Name       string    `json:"name"`
	Schedule   string    `json:"schedule"`
	TargetTime string    `json:"target_time"`
	ScriptPath string    `json:"script_path"`
	LogPath    string    `json:"log_path"`
	LogFile    string    `json:"log_file"`
	Enabled    bool      `json:"enabled"`
	Status     string    `json:"status"`
	LastRun    time.Time `json:"last_run"`
}

type LogEntry struct {
	Time    time.Time `json:"time"`
	Message string    `json:"message"`
	Type    string    `json:"type"`
	Link    *Link     `json:"link,omitempty"`
}
type Link struct {
	Href string `json:"href"`
	Text string `json:"text"`
}

// 📦 สถานะทั่วโลก
var (
	jobs = []CronJob{
		{
			ID:         "zyntro-start",
			Name:       "🚀 Auto Start ZyntroAI",
			Schedule:   "0 8 * * *",
			TargetTime: "08:00 น.",
			ScriptPath: "~/start-service.sh",
			LogPath:    "~/zyntro-logs/cron.log",
			LogFile:    "/logs/cron.log",
			Enabled:    true,
			Status:     "idle",
			LastRun:    time.Now().Add(-24 * time.Hour),
		},
		{
			ID:         "gitlab-sync",
			Name:       "🔄 GitLab ↔ GitHub Sync",
			Schedule:   "*/15 * * * *",
			TargetTime: "ทุก 15 นาที",
			ScriptPath: "~/sync-repos.sh",
			LogPath:    "~/zyntro-logs/sync.log",
			LogFile:    "/logs/sync.log",
			Enabled:    true,
			Status:     "success",
			LastRun:    time.Now().Add(-15 * time.Minute),
		},
		{
			ID:         "security-scan",
			Name:       "🛡️ DevSecOps Scan",
			Schedule:   "0 22 * * *",
			TargetTime: "22:00 น.",
			ScriptPath: "~/scan-security.sh",
			LogPath:    "~/zyntro-logs/scan.log",
			LogFile:    "/logs/scan.log",
			Enabled:    false,
			Status:     "idle",
			LastRun:    time.Now().Add(-48 * time.Hour),
		},
	}
	logs    []LogEntry
	mu      sync.Mutex
	logFile = "dashboard-system.log"
)

// 📝 บันทึก Log + ไฟล์
func addLog(typ, msg string, link *Link) {
	mu.Lock()
	defer mu.Unlock()
	entry := LogEntry{Time: time.Now(), Message: msg, Type: typ, Link: link}
	logs = append([]LogEntry{entry}, logs...)
	if len(logs) > 100 {
		logs = logs[:100]
	}
	f, _ := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer f.Close()
	fmt.Fprintf(f, "[%s] %s | %s\n", entry.Time.Format("15:04:05"), typ, msg)
}

// 🚀 รันงาน
func runJob(id string) error {
	mu.Lock()
	idx := -1
	for i := range jobs {
		if jobs[i].ID == id {
			jobs[i].Status = "running"
			idx = i
			break
		}
	}
	mu.Unlock()
	if idx == -1 {
		return fmt.Errorf("ไม่พบงาน")
	}

	addLog("info", fmt.Sprintf("▶️ เริ่มรัน: %s", jobs[idx].Name), &Link{"/jobs/"+id, "ดูรายละเอียด"})
	cmd := exec.Command("bash", "-c", jobs[idx].ScriptPath)
	err := cmd.Start()
	if err != nil {
		mu.Lock()
		jobs[idx].Status = "error"
		mu.Unlock()
		addLog("error", fmt.Sprintf("❌ ล้มเหลว: %v", err), nil)
		return err
	}

	go func() {
		cmd.Wait()
		mu.Lock()
		jobs[idx].Status = "success"
		jobs[idx].LastRun = time.Now()
		mu.Unlock()
		addLog("success", fmt.Sprintf("✅ เสร็จ: %s", jobs[idx].Name), &Link{"/artifacts/report.html", "รายงาน"})
	}()
	return nil
}

// 🌐 UI: ตาราง + Navbar + ปุ่ม Redirect
const fullHTML = `
<!DOCTYPE html>
<html lang="th">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Cron Table + Nav | ZyntroAI</title>
	<style>
		*{box-sizing:border-box;margin:0;padding:0}
		body{font-family:system-ui,sans-serif;background:#0f172a;color:#f1f5f9;min-height:100vh}

		/* 🧭 Navbar */
		.navbar{background:#1e293b;padding:1rem;position:sticky;top:0;z-index:999;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;border-bottom:2px solid #334155}
		.nav-brand{font-size:1.3rem;font-weight:700}
		.nav-brand a{color:#38bdf8;text-decoration:none}
		.nav-links{display:flex;gap:1rem;flex-wrap:wrap}
		.nav-links a{color:#cbd5e1;padding:.5rem .75rem;border-radius:.375rem;text-decoration:none}
		.nav-links a:hover,.nav-links a.active{background:#334155;color:#fff}
		.clock{color:#38bdf8;font-weight:600}

		/* 📦 Container */
		.container{max-width:1200px;margin:0 auto;padding:1.5rem}
		h1,h2{margin:1.5rem 0;color:#f8fafc}

		/* 📊 ตารางหลัก */
		.table-wrap{overflow-x:auto;border-radius:.5rem;background:#1e293b;margin:1rem 0}
		table{width:100%;border-collapse:collapse;min-width:800px}
		th,td{padding:1rem;text-align:left;border-bottom:1px solid #334155}
		th{background:#0f172a;color:#94a3b8;font-weight:600;white-space:nowrap}
		tr:hover{background:#273449}
		.status{display:inline-block;padding:.25rem .6rem;border-radius:999;font-size:.85rem;font-weight:500}
		.status-idle{background:#334155;color:#cbd5e1}
		.status-running{background:#f59e0b22;color:#fbbf24;border:1px solid #f59e0b}
		.status-success{background:#22c55e22;color:#4ade80;border:1px solid #22c55e}
		.status-error{background:#ef444422;color:#f87171;border:1px solid #ef4444}
		.chk{width:1.3rem;height:1.3rem;accent-color:#22c55e}

		/* 🔗 ปุ่ม Nav/Redirect */
		.btn-group{display:flex;gap:.5rem;flex-wrap:wrap}
		.btn{padding:.5rem 1rem;border-radius:.375rem;font-size:.9rem;text-decoration:none;border:none;cursor:pointer}
		.btn-primary{background:#2563eb;color:white}
		.btn-primary:hover{background:#1d4ed8}
		.btn-success{background:#16a34a;color:white}
		.btn-warning{background:#d97706;color:white}
		.btn-danger{background:#dc2626;color:white}
		.btn-link{background:transparent;color:#38bdf8;border:1px solid #38bdf8}
		.btn-sm{padding:.35rem .75rem;font-size:.85rem}

		/* 📋 Log Panel */
		.log-section{background:#1e293b;border-radius:.5rem;padding:1.5rem;margin-top:2rem}
		.log-box{background:#020617;padding:1rem;border-radius:.375rem;max-height:350px;overflow-y:auto;font-family:monospace;font-size:.9rem;margin-top:1rem}
		.log-line{padding:.35rem 0;border-bottom:1px solid #1e293b}
		.log-time{color:#64748b;margin-right:.5rem}
		.log-info{color:#93c5fd}.log-success{color:#4ade80}.log-warn{color:#fcd34d}.log-error{color:#fca5a5}

		/* 📱 Responsive */
		@media(max-width:768px){
			th,td{padding:.75rem .5rem}
			.btn{padding:.4rem .7rem;font-size:.85rem}
			.navbar{padding:.75rem}
		}
	</style>
</head>
<body>
	<!-- 🧭 Navbar -->
	<nav class="navbar">
		<div class="nav-brand"><a href="/">⏰ ZyntroAI Cron</a></div>
		<div class="nav-links">
			<a href="/" class="active">🏠 หน้าแรก</a>
			<a href="/jobs" onclick="event.preventDefault()">📋 งานทั้งหมด</a>
			<a href="/logs" target="_blank">📂 Logs</a>
			<a href="/settings" onclick="event.preventDefault()">⚙️ ตั้งค่า</a>
			<a href="/docs" target="_blank">📖 คู่มือ</a>
		</div>
		<div class="clock" id="clock">🇹🇭 00:00:00</div>
	</nav>

	<main class="container">
		<h1>📅 ตารางจัดการ Cron Job</h1>

		<!-- 📊 ตารางหลัก -->
		<div class="table-wrap">
			<table>
				<thead>
					<tr>
						<th>#</th>
						<th>เปิด</th>
						<th>ชื่องาน</th>
						<th>Schedule</th>
						<th>เวลาเป้าหมาย</th>
						<th>สถานะ</th>
						<th>รันล่าสุด</th>
						<th>เส้นทางสคริปต์</th>
						<th>การกระทำ / นำทาง</th>
					</tr>
				</thead>
				<tbody>
					{{range $i, $job := .Jobs}}
					<tr>
						<td>{{inc $i}}</td>
						<td><input type="checkbox" class="chk" {{if .Enabled}}checked{{end}} onchange="toggleJob('{{.ID}}')"></td>
						<td><strong><a href="/jobs/{{.ID}}" class="btn btn-link btn-sm">{{.Name}}</a></strong></td>
						<td><code>{{.Schedule}}</code></td>
						<td>{{.TargetTime}}</td>
						<td><span class="status status-{{.Status}}">{{if eq .Status "running"}}⏳ ทำงาน{{else if eq .Status "success"}}✅ สำเร็จ{{else if eq .Status "error"}}❌ ผิดพลาด{{else}}⏸️ รอ{{end}}</span></td>
						<td>{{.LastRun.Format "02/01 15:04"}}</td>
						<td><a href="file://{{.ScriptPath}}" class="btn btn-link btn-sm" target="_blank">📁 เปิด</a></td>
						<td>
							<div class="btn-group">
								<a href="#run" class="btn btn-primary btn-sm" onclick="runJob('{{.ID}}');return false;">▶️ รัน</a>
								<a href="{{.LogFile}}" class="btn btn-success btn-sm" target="_blank">📄 Log</a>
								<a href="/jobs/{{.ID}}/edit" class="btn btn-warning btn-sm">✏️ แก้ไข</a>
								<a href="/redirect?to=/jobs/{{.ID}}" class="btn btn-link btn-sm">➡️ ไป</a>
							</div>
						</td>
					</tr>
					{{end}}
				</tbody>
			</table>
		</div>

		<!-- 📌 ปุ่มนำทางด่วน -->
		<div style="margin:1.5rem 0;display:flex;gap:1rem;flex-wrap:wrap">
			<a href="/new" class="btn btn-primary">➕ สร้างงานใหม่</a>
			<a href="/export/json" class="btn btn-link" target="_blank">📤 ส่งออก JSON</a>
			<a href="/import" class="btn btn-link">📥 นำเข้า</a>
			<a href="#top" class="btn btn-link">⬆️ ขึ้นบน</a>
		</div>

		<!-- 📝 Log เรียลไทม์ -->
		<section class="log-section">
			<h2>📚 บันทึกกิจกรรม — <a href="/logs" target="_blank" class="btn btn-link btn-sm">เปิดเต็มหน้าต่าง ↗</a></h2>
			<div class="log-box" id="logBox">
				{{range .Logs}}
				<div class="log-line log-{{.Type}}">
					<span class="log-time">[{{.Time.Format "15:04:05"}}]</span>
					{{.Message}}
					{{if .Link}} — <a href="{{.Link.Href}}" target="_blank" rel="noopener noreferrer" style="color:#38bdf8">{{.Link.Text}}</a>{{end}}
				</div>
				{{end}}
			</div>
		</section>
	</main>

	<script>
		// ⏰ นาฬิกาเรียลไทม์
		function updateClock(){
			const t=new Date().toLocaleTimeString("th-TH",{timeZone:"Asia/Bangkok",hour12:false});
			document.getElementById("clock").textContent="🇹🇭 "+t;
		}
		setInterval(updateClock,1000);updateClock();

		// 📡 API
		async function runJob(id){await fetch("/api/run/"+id,{method:"POST"});location.reload()}
		async function toggleJob(id){await fetch("/api/toggle/"+id,{method:"POST"});location.reload()}

		// 🔄 อัปเดต Log อัตโนมัติทุก 3 วินาที
		setInterval(async()=>{
			const res=await fetch("/api/logs");
			const data=await res.json();
			const box=document.getElementById("logBox");
			box.innerHTML=data.map(l=>`
				<div class="log-line log-${l.type}">
					<span class="log-time">[${new Date(l.time).toLocaleTimeString("th-TH")}]</span>
					${l.message}
					${l.link?` — <a href="${l.link.href}" target="_blank" style="color:#38bdf8">${l.link.text}</a>`:""}
				</div>
			`).join("");
		},3000);
	</script>
</body>
</html>
`

// 🧩 Template Helper
func inc(i int) int { return i + 1 }

// 🌐 Handlers
func serveUI(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	data := struct {
		Jobs []CronJob
		Logs []LogEntry
	}{jobs, logs}

	w.Header().Set("Content-Type", "text/html;charset=utf-8")

	// 🧱 แทนที่พื้นฐาน (สามารถใช้ html/template ได้เต็มที่)
	tpl := fullHTML
	// 🔁 แทนที่ตัวแปรแบบง่าย (สำหรับความกระชับ)
	// ใช้ fmt.Sprintf หรือ template engine จริงในงานจริง
	// --- สำหรับตัวอย่างนี้ render ตรงๆ ---
	// ✅ ในที่นี้จะใช้ html/template อย่างถูกต้อง
	import "html/template"
	t, err := template.New("cron").Funcs(template.FuncMap{"inc": inc}).Parse(fullHTML)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	t.Execute(w, data)
}

func serveLogsAPI(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(logs)
}

func redirectHandler(w http.ResponseWriter, r *http.Request) {
	to := r.URL.Query().Get("to")
	if to == "" {
		to = "/"
	}
	http.Redirect(w, r, to, http.StatusSeeOther)
}

func apiRun(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/api/run/"):]
	if err := runJob(id); err != nil {
		http.Error(w, err.Error(), 404)
		return
	}
	w.WriteHeader(200)
}

func apiToggle(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/api/toggle/"):]
	mu.Lock()
	defer mu.Unlock()
	for i := range jobs {
		if jobs[i].ID == id {
			jobs[i].Enabled = !jobs[i].Enabled
			addLog("info", fmt.Sprintf("🔄 เปิด/ปิด: %s = %v", id, jobs[i].Enabled), nil)
			w.WriteHeader(200)
			return
		}
	}
	http.NotFound(w, r)
}

func main() {
	// 🚀 เริ่มต้น
	addLog("info", "✅ ระบบ Cron Table + Nav พร้อมใช้งาน", &Link{"/docs/start.html", "เริ่มต้นใช้งาน"})
	addLog("success", "📊 โหลดรายการงานสำเร็จ", nil)

	// 📡 Routes
	http.HandleFunc("/", serveUI)
	http.HandleFunc("/api/logs", serveLogsAPI)
	http.HandleFunc("/api/run/", apiRun)
	http.HandleFunc("/api/toggle/", apiToggle)
	http.HandleFunc("/redirect", redirectHandler)

	// 🧭 Static Redirect Nav
	http.HandleFunc("/jobs", func(w http.ResponseWriter, r *http.Request) { http.Redirect(w, r, "/", 302) })
	http.HandleFunc("/logs", func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(logs)
	})

	// ⏰ Cron Scheduler ภายใน
	go func() {
		ticker := time.NewTicker(1 * time.Minute)
		defer ticker.Stop()
		for range ticker.C {
			now := time.Now().In(time.FixedZone("TH", 7*3600))
			if now.Hour() == 8 && now.Minute() == 0 {
				for _, j := range jobs {
					if j.Enabled {
						runJob(j.ID)
					}
				}
			}
		}
	}()

	fmt.Println("🚀 เปิดที่: http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
