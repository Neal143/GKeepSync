/**
 * GKeepSync Login Helper - Background Service Worker
 * Monitors EmbeddedSetup login, extracts oauth_token cookie,
 * sends it to GKeepSync app via localhost.
 */

const GKEEPSYNC_PORT = 28371;
const EMBEDDED_SETUP_URL = "https://accounts.google.com/EmbeddedSetup";

// Listen for tab updates - detect when user completes login
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status !== "complete") return;
    if (!tab.url || !tab.url.startsWith("https://accounts.google.com")) return;

    // Check for oauth_token cookie
    try {
        const cookie = await chrome.cookies.get({
            url: "https://accounts.google.com",
            name: "oauth_token",
        });

        if (cookie && cookie.value) {
            console.log("[GKeepSync] Found oauth_token cookie!");
            await sendTokenToApp(cookie.value);
        }
    } catch (err) {
        console.error("[GKeepSync] Error reading cookie:", err);
    }
});

/**
 * Send the oauth_token to GKeepSync desktop app via localhost
 */
async function sendTokenToApp(oauthToken) {
    const url = `http://127.0.0.1:${GKEEPSYNC_PORT}/token`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ oauth_token: oauthToken }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("[GKeepSync] Token sent successfully:", data);

            // Notify user via badge
            chrome.action.setBadgeText({ text: "✓" });
            chrome.action.setBadgeBackgroundColor({ color: "#2ecc71" });

            // Store status for popup
            chrome.storage.local.set({
                lastStatus: "success",
                lastTime: new Date().toLocaleString(),
            });
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (err) {
        console.error("[GKeepSync] Failed to send token:", err.message);

        chrome.action.setBadgeText({ text: "!" });
        chrome.action.setBadgeBackgroundColor({ color: "#e74c3c" });

        chrome.storage.local.set({
            lastStatus: "error",
            lastError: err.message,
            lastTime: new Date().toLocaleString(),
        });
    }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "openLogin") {
        chrome.tabs.create({ url: EMBEDDED_SETUP_URL });
        sendResponse({ ok: true });
    }
    return true;
});
