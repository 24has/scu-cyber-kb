+++
id = "setup-totp"
title = "How to set up a TOTP app"
category = "multi-factor-authentication"
updated = "2026-08-22"
applies_to = "All staff and students"
time_required = "5 minutes"
+++

**Requirements:** any TOTP app (Google Authenticator or other).

<div class="steps">

1. Install your chosen TOTP app before you start.
2. On your computer, go to [mysignins.microsoft.com/security-info](https://mysignins.microsoft.com/security-info) and sign in.
3. Click **Add sign-in method**, select **Authenticator app**, then click **Add**.
4. Below the QR code, click **I want to use a different authenticator app**. A new QR code appears. This one works with any TOTP app.
5. Scan the QR code with your TOTP app. **Google Authenticator:** tap the plus icon, then Scan a QR code.
6. Your app now shows a six-digit code that refreshes every 30 seconds. On your computer, click **Next**, enter the code, then click **Done**.
7. Confirm **Authenticator app** appears under your sign-in methods.

</div>

## Signing in with a TOTP app

<div class="steps">

1. Sign in with your SCU email and password as usual.
2. When the MFA prompt appears, click **Use a verification code** (or **I can't use my Microsoft Authenticator app right now** on some screens).
3. Open your TOTP app, find the six-digit code for your SCU account, and type it in.
4. Click **Verify**.

</div>

## Common questions

<div class="faq-item">

**I do not have a smartphone. Can I still do MFA?**

Yes. You can use a passkey on your laptop (Windows Hello or Touch ID), a TOTP app on your desktop, or a hardware security key.

</div>

<div class="faq-item">

**What if my device does not have a fingerprint reader or face scan?**

You can use your device PIN instead. Every device that supports passkeys supports PIN-based passkeys. The PIN is tied to that specific device and is not sent online.

</div>

<div class="faq-item">

**What if I share a computer?**

Store your passkey on your phone. When you sign in on the shared computer, a prompt appears on your phone. Your passkey stays on your phone. If you do not have a phone that supports passkeys, contact the Technology Services Service Desk.

</div>

<div class="faq-item">

**What happens to my passkeys when I get a new phone?**

Passkeys stored in iCloud Keychain (iPhone) or Google Password Manager (Android) sync to your new device when you restore from backup. Register a second passkey on another device as a backup.

</div>

<div class="faq-item">

**What happens to my TOTP codes when I get a new phone?**

Google Authenticator can transfer codes between phones. If you lose access, go to [mysignins.microsoft.com/security-info](https://mysignins.microsoft.com/security-info) on a computer, delete the old entry, and set up again.

</div>

<div class="faq-item">

**What happens to Microsoft Authenticator when I get a new phone?**

On your old phone, open the app, go to Settings, and turn on cloud backup. On your new phone, install the app and restore from backup. If you no longer have your old phone, go to [mysignins.microsoft.com/security-info](https://mysignins.microsoft.com/security-info), delete the old Authenticator entry, and set up again.

</div>

<div class="faq-item">

**Can I register more than one method?**

Yes. Each method appears separately on your Security info page. Register at least two so you have a backup.

</div>

<div class="faq-item">

**Can I still use SMS codes?**

Only until 1 February 2027. After that, SMS MFA stops working.

</div>

<div class="faq-item">

**What if I do not want to use a passkey?**

Microsoft Authenticator and TOTP apps are both more secure than SMS. They are valid alternatives. The passkey is recommended because it is fastest and most secure, but it is not required.

</div>