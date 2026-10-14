package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestUIAndNav(t *testing.T) {
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	serveUI(w, req)
	if w.Code != 200 {
		t.Errorf("UI ผิดพลาด: %d", w.Code)
	}
	if w.Body.Len() < 1000 {
		t.Error("HTML สั้นเกินไป น่าจะมีตาราง+Navbar")
	}
}

func TestRedirect(t *testing.T) {
	req := httptest.NewRequest("GET", "/redirect?to=/logs", nil)
	w := httptest.NewRecorder()
	redirectHandler(w, req)
	if w.Code != 303 {
		t.Error("Redirect ไม่ทำงาน")
	}
	if w.Header().Get("Location") != "/logs" {
		t.Error("เป้าหมายผิด")
	}
}

func TestJobToggle(t *testing.T) {
	req := httptest.NewRequest("POST", "/api/toggle/zyntro-start", nil)
	w := httptest.NewRecorder()
	apiToggle(w, req)
	mu.Lock()
	defer mu.Unlock()
	if jobs[0].Enabled != false {
		t.Error("Checkbox เปิด/ปิด ไม่ทำงาน")
	}
}

func TestLogAppend(t *testing.T) {
	before := len(logs)
	addLog("test", "ทดสอบ", nil)
	if len(logs) != before+1 {
		t.Error("Log ไม่เพิ่ม")
	}
}
