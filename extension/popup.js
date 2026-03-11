/**
 * GKeepSync Login Helper - Popup Script
 */

const statusEl = document.getElementById("status");
const loginBtn = document.getElementById("loginBtn");
const sendBtn = document.getElementById("sendBtn");
const emailInput = document.getElementById("emailInput");
const tokenInput = document.getElementById("tokenInput");
const toggleTokenBtn = document.getElementById("toggleTokenBtn");
const copyTokenBtn = document.getElementById("copyTokenBtn");

// 1. Initialize data when popup opens
async function initForm() {
    // Attempt to get email from Chrome Profile
    try {
        const userInfo = await chrome.identity.getProfileUserInfo();
        if (userInfo && userInfo.email) {
            emailInput.value = userInfo.email;
        }
    } catch (e) {
        console.warn("Could not fetch identity email", e);
    }

    // Load saved info from local storage
    chrome.storage.local.get(["oauth_token", "lastEmail", "lastStatus", "lastTime", "lastError"], (data) => {
        // Pre-fill email if we didn't get from identity and have a saved one
        if (!emailInput.value && data.lastEmail) {
            emailInput.value = data.lastEmail;
        }

        // Fill token if captured
        if (data.oauth_token) {
            tokenInput.value = data.oauth_token;
            sendBtn.disabled = false;
        } else {
            sendBtn.disabled = true;
        }

        // Show status
        if (data.lastStatus === "success") {
            statusEl.className = "status success";
            statusEl.textContent = `✅ Token đã gửi thành công! (${data.lastTime})`;
        } else if (data.lastStatus === "error") {
            statusEl.className = "status error";
            statusEl.textContent = `❌ Lỗi: ${data.lastError}. Hãy mở app GKeepSync trước!`;
        }
    });
}

// 2. Event Listeners
loginBtn.addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "openLogin" }, () => {
        statusEl.className = "status waiting";
        statusEl.textContent = "🌐 Đang mở trang đăng nhập...";
        window.close();
    });
});

toggleTokenBtn.addEventListener("click", () => {
    if (tokenInput.type === "password") {
        tokenInput.type = "text";
        toggleTokenBtn.textContent = "🙈";
    } else {
        tokenInput.type = "password";
        toggleTokenBtn.textContent = "👁️";
    }
});

copyTokenBtn.addEventListener("click", async () => {
    if (!tokenInput.value) return;
    try {
        await navigator.clipboard.writeText(tokenInput.value);
        const originalContent = copyTokenBtn.textContent;
        copyTokenBtn.textContent = "✅";
        setTimeout(() => {
            copyTokenBtn.textContent = originalContent;
        }, 2000);
    } catch (err) {
        console.error("Failed to copy", err);
    }
});

sendBtn.addEventListener("click", async () => {
    const email = emailInput.value.trim();
    const oathToken = tokenInput.value.trim();

    if (!email) {
        alert("Vui lòng nhập Email!");
        return;
    }
    if (!oathToken) {
        alert("Không tìm thấy Token. Vui lòng đăng nhập Google trước.");
        return;
    }

    // Save the manually edited email
    chrome.storage.local.set({ lastEmail: email });

    statusEl.className = "status waiting";
    statusEl.textContent = "🚀 Đang gửi đến app...";
    sendBtn.disabled = true;

    try {
        const url = `http://127.0.0.1:28371/token`;
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, oauth_token: oathToken }),
        });

        if (response.ok) {
            const data = await response.json();
            const masterToken = data.master_token;
            statusEl.className = "status success";
            statusEl.textContent = `✅ Đã kết nối! Master Token đã được lưu trữ vĩnh viễn. (Check App)`;

            // Replace oauth_token with the definitive master_token
            if (masterToken) {
                tokenInput.value = masterToken;
                chrome.storage.local.set({ oauth_token: masterToken });
            }

            chrome.storage.local.set({
                lastStatus: "success",
                lastTime: new Date().toLocaleString()
            });
            // Update badge
            chrome.action.setBadgeText({ text: "✓" });
            chrome.action.setBadgeBackgroundColor({ color: "#2ecc71" });
        } else {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP ${response.status}`);
        }
    } catch (err) {
        statusEl.className = "status error";
        statusEl.textContent = `❌ Lỗi: ${err.message}. GKeepSync App đã bật chưa?`;

        chrome.storage.local.set({
            lastStatus: "error",
            lastError: err.message,
            lastTime: new Date().toLocaleString()
        });

        chrome.action.setBadgeText({ text: "!" });
        chrome.action.setBadgeBackgroundColor({ color: "#e74c3c" });
    } finally {
        sendBtn.disabled = false;
    }
});

// Run init
initForm();
