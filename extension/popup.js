/**
 * GKeepSync Login Helper - Popup Script
 */

const statusEl = document.getElementById("status");
const loginBtn = document.getElementById("loginBtn");

// Load last status
chrome.storage.local.get(["lastStatus", "lastTime", "lastError"], (data) => {
    if (data.lastStatus === "success") {
        statusEl.className = "status success";
        statusEl.textContent = `✅ Token đã gửi thành công! (${data.lastTime})`;
    } else if (data.lastStatus === "error") {
        statusEl.className = "status error";
        statusEl.textContent = `❌ Lỗi: ${data.lastError}. Hãy mở app GKeepSync trước!`;
    }
});

// Open Google login
loginBtn.addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "openLogin" }, () => {
        statusEl.className = "status waiting";
        statusEl.textContent = "🌐 Đang mở trang đăng nhập...";
        window.close();
    });
});
