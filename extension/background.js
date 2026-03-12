/**
 * GKeepSync Login Helper - Background Service Worker
 * Monitors EmbeddedSetup login, extracts oauth_token cookie,
 * auto-sends it (with email) to GKeepSync desktop app,
 * and saves the returned master_token for permanent use.
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
            console.log("[GKeepSync] Found oauth_token cookie! Auto-sending to app...");

            // Get user email from Chrome profile
            let email = "";
            try {
                const userInfo = await chrome.identity.getProfileUserInfo({ accountStatus: "ANY" });
                if (userInfo && userInfo.email) {
                    email = userInfo.email;
                }
            } catch (e) {
                console.warn("[GKeepSync] Could not fetch identity email", e);
            }

            // Fallback: check saved email
            if (!email) {
                const stored = await chrome.storage.local.get(["lastEmail"]);
                email = stored.lastEmail || "";
            }

            if (!email) {
                // No email available from profile - we will still send it. 
                // The desktop app might have the email entered in its UI.
                console.log("[GKeepSync] No email found from Chrome Identity, sending anyway...");
                chrome.storage.local.set({ oauth_token: cookie.value });
                chrome.action.setBadgeText({ text: "1" });
                chrome.action.setBadgeBackgroundColor({ color: "#e67e22" });
            }

            // Auto-send email + oauth_token to the desktop app
            try {
                const url = `http://127.0.0.1:${GKEEPSYNC_PORT}/token`;
                const response = await fetch(url, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email: email, oauth_token: cookie.value }),
                });

                if (response.ok) {
                    const data = await response.json();
                    const masterToken = data.master_token;
                    const resolvedEmail = data.email || email;

                    if (masterToken) {
                        // Save the permanent master_token (replaces temp oauth_token)
                        chrome.storage.local.set({
                            oauth_token: masterToken,
                            lastEmail: resolvedEmail,
                            lastStatus: "success",
                            lastTime: new Date().toLocaleString(),
                        });
                        console.log("[GKeepSync] Auto-login success! Master token saved.");
                    } else {
                        // App accepted but didn't return master_token
                        chrome.storage.local.set({
                            oauth_token: cookie.value,
                            lastEmail: resolvedEmail,
                            lastStatus: "success",
                            lastTime: new Date().toLocaleString(),
                        });
                        console.log("[GKeepSync] Auto-login success (no master_token returned).");
                    }

                    chrome.action.setBadgeText({ text: "✓" });
                    chrome.action.setBadgeBackgroundColor({ color: "#2ecc71" });
                } else {
                    console.error("[GKeepSync] App rejected token:", response.status);
                    // Save token for manual retry via popup
                    chrome.storage.local.set({
                        oauth_token: cookie.value,
                        lastStatus: "error",
                        lastError: `App từ chối (HTTP ${response.status})`,
                        lastTime: new Date().toLocaleString(),
                    });
                    chrome.action.setBadgeText({ text: "!" });
                    chrome.action.setBadgeBackgroundColor({ color: "#e74c3c" });
                }
            } catch (fetchErr) {
                console.error("[GKeepSync] Cannot reach app:", fetchErr.message);
                // App not running - save token for manual send via popup later
                chrome.storage.local.set({
                    oauth_token: cookie.value,
                    lastStatus: "error",
                    lastError: "App chưa bật",
                    lastTime: new Date().toLocaleString(),
                });
                chrome.action.setBadgeText({ text: "!" });
                chrome.action.setBadgeBackgroundColor({ color: "#e74c3c" });
            }
        }
    } catch (err) {
        console.error("[GKeepSync] Error reading cookie:", err);
    }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "openLogin") {
        chrome.tabs.create({ url: EMBEDDED_SETUP_URL });
        sendResponse({ ok: true });
    }
    return true;
});
