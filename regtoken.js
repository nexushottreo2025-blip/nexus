// ==UserScript==
// @name         Discord Auto Register + Auto Verify + Token Capture
// @namespace    http://tampermonkey.net/
// @version      4.0
// @description  Auto register Discord with temp email, auto verify, and capture token
// @match        https://discord.com/register*
// @match        https://discord.com/channels/*
// @match        https://discord.com/app*
// @match        https://discord.com/verify*
// @match        https://click.discord.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_deleteValue
// @connect      localhost
// @connect      127.0.0.1
// @connect      email.devtai.net
// @connect      click.discord.com
// ==/UserScript==

(async () => {
  'use strict';

  const SERVER_URL = "http://localhost:5000/save-token";
  const EMAIL_API = "https://email.devtai.net/api";
  const DOMAINS = ["antdev.org", "epmtyfl.me", "sptech.io.vn"];

  let currentEmail = GM_getValue('discord_current_email', '');
  let currentUsername = GM_getValue('discord_current_username', '');
  let tokenSent = GM_getValue('discord_token_sent', false);
  let isVerifying = GM_getValue('discord_is_verifying', false);
  let verifyStep = GM_getValue('discord_verify_step', 0);

  const notify = (msg, type = 'success') => {
    const n = document.createElement('div');
    n.textContent = msg;
    const colors = {
      success: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      info: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      error: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    };
    n.style.cssText = `position:fixed;top:20px;right:20px;padding:15px 20px;background:${colors[type]};color:white;border-radius:12px;z-index:999999;font-size:14px;box-shadow:0 8px 16px rgba(0,0,0,0.3);animation:slideIn 0.3s ease-out;font-weight:500`;
    if (!document.querySelector('#notif-style')) {
      const s = document.createElement('style');
      s.id = 'notif-style';
      s.textContent = '@keyframes slideIn{from{transform:translateX(400px);opacity:0}to{transform:translateX(0);opacity:1}}@keyframes slideOut{from{transform:translateX(0);opacity:1}to{transform:translateX(400px);opacity:0}}';
      document.head.appendChild(s);
    }
    document.body.appendChild(n);
    setTimeout(() => {
      n.style.animation = 'slideOut 0.3s ease-out';
      setTimeout(() => n.remove(), 300);
    }, 3000);
  };
  
  const showInfo = () => {
    let box = document.querySelector('#discord-info-box');
    if (!box) {
      box = document.createElement('div');
      box.id = 'discord-info-box';
      box.style.cssText = 'position:fixed;top:20px;left:20px;padding:20px;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;border-radius:16px;z-index:999999;font-size:13px;box-shadow:0 10px 25px rgba(0,0,0,0.4);min-width:280px;max-width:380px;backdrop-filter:blur(10px);transition:all 0.3s ease';
      document.body.appendChild(box);
    }
    
    box.innerHTML = `<div style="font-weight:bold;margin-bottom:12px;font-size:15px;text-align:center;letter-spacing:0.5px">@NGUYEN GIA PHUC</div><div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:10px;margin-bottom:10px"><div style="margin-bottom:8px"><span style="opacity:0.8;font-size:11px">EMAIL:</span><br><span style="font-size:12px;word-break:break-all;font-weight:500">${currentEmail || 'Chưa có'}</span></div><div style="margin-bottom:8px"><span style="opacity:0.8;font-size:11px">USERNAME:</span><br><span style="font-size:12px;font-weight:500">${currentUsername || 'Chưa có'}</span></div><div><span style="opacity:0.8;font-size:11px">TRẠNG THÁI:</span><br><span id="status-text" style="font-size:12px;font-weight:500">${isVerifying ? `Đang verify (Step ${verifyStep})...` : tokenSent ? 'Đã lưu token' : 'Đang xử lý...'}</span></div></div><button id="reset-all-btn" style="width:100%;padding:12px;background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%);color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;font-size:13px;transition:all 0.3s ease;box-shadow:0 4px 12px rgba(240,147,251,0.4);margin-bottom:10px">Reset & Tạo Acc Mới</button><button id="reverify-btn" style="width:100%;padding:12px;background:linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;font-size:13px;transition:all 0.3s ease;box-shadow:0 4px 12px rgba(132,250,176,0.4)">Verify Lại</button>`;
    
    const resetBtn = box.querySelector('#reset-all-btn');
    resetBtn.addEventListener('mouseenter', () => {
      resetBtn.style.transform = 'translateY(-2px)';
      resetBtn.style.boxShadow = '0 6px 16px rgba(240,147,251,0.6)';
    });
    resetBtn.addEventListener('mouseleave', () => {
      resetBtn.style.transform = 'translateY(0)';
      resetBtn.style.boxShadow = '0 4px 12px rgba(240,147,251,0.4)';
    });
    resetBtn.addEventListener('click', resetAll);

    const reverifyBtn = box.querySelector('#reverify-btn');
    reverifyBtn.addEventListener('mouseenter', () => {
      reverifyBtn.style.transform = 'translateY(-2px)';
      reverifyBtn.style.boxShadow = '0 6px 16px rgba(132,250,176,0.6)';
    });
    reverifyBtn.addEventListener('mouseleave', () => {
      reverifyBtn.style.transform = 'translateY(0)';
      reverifyBtn.style.boxShadow = '0 4px 12px rgba(132,250,176,0.4)';
    });
    reverifyBtn.addEventListener('click', () => {
      if (!currentEmail) {
        notify("Không có thông tin email để verify!", 'error');
        return;
      }
      
      isVerifying = false;
      tokenSent = false;
      verifyStep = 0;
      GM_setValue('discord_is_verifying', false);
      GM_setValue('discord_token_sent', false);
      GM_setValue('discord_verify_step', 0);
      
      notify("Đang bắt đầu verify lại...", 'info');
      setTimeout(autoVerify, 1000);
    });
  };

  const updateStatus = (text) => {
    const st = document.querySelector('#status-text');
    if (st) st.textContent = text;
  };

  const resetAll = async () => {
    notify("Đang xóa toàn bộ dữ liệu...", 'info');
    localStorage.clear();
    sessionStorage.clear();
    document.cookie.split(";").forEach(c => document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"));
    if (window.indexedDB) {
      const dbs = await window.indexedDB.databases();
      dbs.forEach(db => db.name && window.indexedDB.deleteDatabase(db.name));
    }
    if ('caches' in window) {
      const names = await caches.keys();
      await Promise.all(names.map(n => caches.delete(n)));
    }
    if ('serviceWorker' in navigator) {
      const regs = await navigator.serviceWorker.getRegistrations();
      for (let r of regs) await r.unregister();
    }
    GM_deleteValue('discord_current_email');
    GM_deleteValue('discord_current_username');
    GM_deleteValue('discord_token_sent');
    GM_deleteValue('discord_is_verifying');
    GM_deleteValue('discord_verify_step');
    notify("Đã xóa toàn bộ dữ liệu!", 'success');
    document.querySelector('#discord-info-box')?.remove();
    setTimeout(() => window.location.replace('https://discord.com/register'), 2000);
  };

  const setVal = (el, val) => {
    const setter = Object.getOwnPropertyDescriptor(el.__proto__, 'value').set;
    const proto = Object.getPrototypeOf(el);
    const protoSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
    (setter && setter !== protoSetter ? protoSetter : setter).call(el, val);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  };

  const generateEmail = () => {
    const randomDomain = DOMAINS[Math.floor(Math.random() * DOMAINS.length)];
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let randomStr = '';
    for (let i = 0; i < 8; i++) {
      randomStr += chars[Math.floor(Math.random() * chars.length)];
    }
    const insertPos = Math.floor(Math.random() * (randomStr.length + 1));
    randomStr = randomStr.slice(0, insertPos) + 'giaphuc' + randomStr.slice(insertPos);
    return `${randomStr}@${randomDomain}`;
  };

  const getEmailMessages = (email) => new Promise((resolve, reject) => {
    GM_xmlhttpRequest({
      method: "GET",
      url: `${EMAIL_API}/email/${email}`,
      headers: { "Accept": "application/json" },
      timeout: 10000,
      onload: res => {
        try {
          if (res.status === 200) {
            const json = JSON.parse(res.responseText);
            resolve(json);
          } else reject(`API error: ${res.status}`);
        } catch (e) { reject("Parse error: " + e.message); }
      },
      onerror: () => reject("Connection failed"),
      ontimeout: () => reject("Timeout")
    });
  });

  const getMessageBody = (msgId) => new Promise((resolve, reject) => {
    GM_xmlhttpRequest({
      method: "GET",
      url: `${EMAIL_API}/inbox/${msgId}`,
      headers: { "Accept": "application/json" },
      timeout: 10000,
      onload: res => {
        try {
          if (res.status === 200) {
            const json = JSON.parse(res.responseText);
            resolve(json);
          } else reject(`API error: ${res.status}`);
        } catch (e) { reject("Parse error: " + e.message); }
      },
      onerror: () => reject("Connection failed"),
      ontimeout: () => reject("Timeout")
    });
  });

  const extractVerifyLink = (text) => {
    const regex = /https:\/\/click\.discord\.com\/ls\/click\?upn=[^\s]+/g;
    const matches = text.match(regex);
    if (!matches || matches.length === 0) return null;
    
    return matches[0];
  };

  const waitForVerifyEmail = async (email, maxAttempts = 30) => {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const messages = await getEmailMessages(email);
        
        if (Array.isArray(messages) && messages.length > 0) {
          const verifyMsg = messages.find(m => 
            m.fromAddress === "noreply@discord.com" && 
            m.subject?.includes("Xác Nhận")
          );
          
          if (verifyMsg && verifyMsg.id) {
            const body = await getMessageBody(verifyMsg.id);
            const fullText = body.textContent || body.htmlContent || '';
            const link = extractVerifyLink(fullText);
            if (link) return link;
          }
        }
      } catch (e) {
        console.error("Check email error:", e);
      }
      await new Promise(r => setTimeout(r, 2000));
    }
    throw new Error("Verify email not found");
  };

  const sendToken = (token, email, username) => {
    if (tokenSent) return Promise.resolve();
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method: "POST",
        url: SERVER_URL,
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify({ token, email, username }),
        onload: res => {
          if (res.status === 200) {
            tokenSent = true;
            GM_setValue('discord_token_sent', true);
            notify("Đã lưu token thành công!", 'success');
            updateStatus("Hoàn tất!");
            resolve();
          } else reject("Server error: " + res.status);
        },
        onerror: () => reject("Connection failed")
      });
    });
  };

  const captureToken = () => {
    const token = localStorage.getItem('token');
    if (token) return token.replace(/"/g, '');

    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(method, url) {
      this._url = url;
      return origOpen.apply(this, arguments);
    };

    XMLHttpRequest.prototype.send = function() {
      this.addEventListener('load', function() {
        if (this._url?.includes('discord.com/api')) {
          try {
            const auth = this.getResponseHeader('authorization');
            if (auth && !tokenSent) sendToken(auth, currentEmail, currentUsername);
          } catch (e) {}
        }
      });
      return origSend.apply(this, arguments);
    };

    return null;
  };

  const clickDropdown = async (sel, text) => {
    const dd = document.querySelector(sel);
    if (!dd) return false;
    dd.click();
    await new Promise(r => setTimeout(r, 500));
    const opts = Array.from(document.querySelectorAll('div[role="option"]'));
    const opt = opts.find(o => o.textContent.trim().toLowerCase() === text.toLowerCase());
    if (opt) {
      opt.click();
      return true;
    }
    return false;
  };

  const randomDOB = () => {
    const year = Math.floor(Math.random() * 18) + 1989;
    const month = Math.floor(Math.random() * 12) + 1;
    const day = Math.floor(Math.random() * 28) + 1;
    return { year, month, day };
  };

  const fillDOB = async () => {
    const dob = randomDOB();
    await clickDropdown('div[aria-label="Ngày"]', dob.day.toString());
    await clickDropdown('div[aria-label="Tháng"]', "tháng " + dob.month);
    await clickDropdown('div[aria-label="Năm"]', dob.year.toString());
  };

  const fillForm = async () => {
    const email = generateEmail();
    currentEmail = email;
    GM_setValue('discord_current_email', currentEmail);
    notify("Email: " + currentEmail, 'success');

    const username = "regaccbynggiaphuc" + Math.random().toString(36).slice(2, 7);
    currentUsername = username;
    GM_setValue('discord_current_username', username);

    const password = "kjtdzqa123@";
    const displayName = "fixenti";

    const emailInput = document.querySelector('input[type="email"][aria-label="Email"],input[name="email"]');
    if (!emailInput) {
      notify("Không tìm thấy input email", 'error');
      return;
    }
    setVal(emailInput, currentEmail);

    const displayNameInput = document.querySelector('input[aria-label="Tên hiển thị"]');
    const usernameInput = document.querySelector('input[aria-label="Tên đăng nhập"]');
    const passwordInput = document.querySelector('input[aria-label="Mật khẩu"]');
    const passwordConfirmInput = document.querySelector('input[aria-label="Xác nhận mật khẩu"]');

    if (displayNameInput) setVal(displayNameInput, displayName);
    if (usernameInput) setVal(usernameInput, username);
    if (passwordInput) setVal(passwordInput, password);
    if (passwordConfirmInput) setVal(passwordConfirmInput, password);

    await fillDOB();

    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      if (!cb.checked && cb.labels?.[0] && /email/i.test(cb.labels[0].textContent)) cb.click();
    });

    let resetBtn = document.querySelector("#resetEmailBtn");
    const submitBtn = document.querySelector('button[type="submit"].button__921c5');
    if (!resetBtn) {
      resetBtn = document.createElement("button");
      resetBtn.id = "resetEmailBtn";
      resetBtn.textContent = "Reset Mail";
      resetBtn.style.cssText = "margin-top:10px;padding:12px;cursor:pointer;background:linear-gradient(135deg, #fa709a 0%, #fee140 100%);color:white;border:none;border-radius:10px;font-weight:bold;transition:all 0.3s ease;box-shadow:0 4px 12px rgba(250,112,154,0.4)";
      resetBtn.type = "button";
      if (submitBtn) submitBtn.parentNode.insertBefore(resetBtn, submitBtn.nextSibling);
      
      resetBtn.addEventListener('mouseenter', () => {
        resetBtn.style.transform = 'translateY(-2px)';
        resetBtn.style.boxShadow = '0 6px 16px rgba(250,112,154,0.6)';
      });
      resetBtn.addEventListener('mouseleave', () => {
        resetBtn.style.transform = 'translateY(0)';
        resetBtn.style.boxShadow = '0 4px 12px rgba(250,112,154,0.4)';
      });
    }

    resetBtn.onclick = async () => {
      const newEmail = generateEmail();
      currentEmail = newEmail;
      GM_setValue('discord_current_email', currentEmail);
      notify("Email mới: " + currentEmail, 'success');
      if (emailInput) setVal(emailInput, currentEmail);
    };
  };

  const autoVerify = async () => {
    if (isVerifying || tokenSent) return;
    
    isVerifying = true;
    verifyStep = 1;
    GM_setValue('discord_is_verifying', true);
    GM_setValue('discord_verify_step', 1);
    
    showInfo();
    updateStatus("Đang đợi email verify...");
    notify("Đang đợi email verify...", 'info');

    try {
      const verifyLink = await waitForVerifyEmail(currentEmail);
      console.log("Found verify link:", verifyLink);
      notify("Đã tìm thấy link verify!", 'success');
      
      verifyStep = 2;
      GM_setValue('discord_verify_step', 2);
      updateStatus("Đang chuyển đến link verify...");
      
      setTimeout(() => {
        window.location.href = verifyLink;
      }, 1000);
      
    } catch (e) {
      notify(e.message, 'error');
      updateStatus("Lỗi verify");
      isVerifying = false;
      GM_setValue('discord_is_verifying', false);
      GM_setValue('discord_verify_step', 0);
    }
  };

  const handleVerifyLink = () => {
    const url = window.location.href;
    if (url.includes('click.discord.com')) {
      verifyStep = 3;
      GM_setValue('discord_verify_step', 3);
      
      notify("Đang xác thực...", 'info');
      showInfo();
      updateStatus("Đang xác thực, chờ 5s...");
      
      setTimeout(() => {
        verifyStep = 4;
        GM_setValue('discord_verify_step', 4);
        notify("Đã verify, đang chuyển đến channels...", 'success');
        window.location.href = "https://discord.com/channels/@me";
      }, 5000);
    }
  };

  const checkLogin = () => {
    if (tokenSent) return;

    const url = window.location.href;
    if (url.includes('/channels/') || url.includes('/app')) {
      
      if (isVerifying && verifyStep === 4) {
        verifyStep = 5;
        GM_setValue('discord_verify_step', 5);
        
        showInfo();
        updateStatus("Đang lấy token...");
        notify("Đang lấy token cho " + currentUsername, 'info');
      }

      const token = captureToken();
      if (token) {
        sendToken(token, currentEmail, currentUsername).then(() => {
          isVerifying = false;
          verifyStep = 0;
          GM_setValue('discord_is_verifying', false);
          GM_setValue('discord_verify_step', 0);
        });
      } else if (!tokenSent) {
        setTimeout(checkLogin, 2000);
      }
    }
  };

  const ensureInfoBox = () => {
    if (!document.querySelector('#discord-info-box')) {
      showInfo();
    }
  };

  const url = window.location.href;

  if (url.includes('/register')) {
    const interval = setInterval(() => {
      const emailInput = document.querySelector('input[type="email"][aria-label="Email"],input[name="email"]');
      if (emailInput) {
        clearInterval(interval);
        fillForm();
      }
    }, 500);
  } 
  else if (url.includes('click.discord.com')) {
    currentEmail = GM_getValue('discord_current_email', '');
    currentUsername = GM_getValue('discord_current_username', '');
    tokenSent = GM_getValue('discord_token_sent', false);
    isVerifying = GM_getValue('discord_is_verifying', false);
    verifyStep = GM_getValue('discord_verify_step', 0);
    
    handleVerifyLink();
  }
  else if (url.includes('/channels/') || url.includes('/app')) {
    currentEmail = GM_getValue('discord_current_email', '');
    currentUsername = GM_getValue('discord_current_username', '');
    tokenSent = GM_getValue('discord_token_sent', false);
    isVerifying = GM_getValue('discord_is_verifying', false);
    verifyStep = GM_getValue('discord_verify_step', 0);

    showInfo();
    setInterval(ensureInfoBox, 2000);

    if (currentEmail && currentUsername) {
      if (!tokenSent && !isVerifying) {
        setTimeout(autoVerify, 3000);
      } else if (isVerifying) {
        if (verifyStep === 4 || verifyStep === 5) {
          setTimeout(checkLogin, 2000);
        }
      }
    }

    setTimeout(checkLogin, 3000);
  }

})();