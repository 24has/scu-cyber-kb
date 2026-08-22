+++
id = "setup-totp"
title = "Set up a TOTP app"
category = "knowledge-base"
updated = "2026-08-22"
applies_to = "All staff and students"
time_required = "About 5 minutes"
+++

## What is a TOTP app?

TOTP stands for time-based one-time password. The app shows a six-digit code that changes every 30 seconds. You type this code at sign-in.

It works on phones and desktop computers. You do not need a Microsoft account. It works offline.

Common apps: Google Authenticator (free, iPhone and Android), Authy (free, desktop and phone), Bitwarden (built into the password manager).

## Set it up

<div class="steps">

1. Install your TOTP app.
2. On your computer, go to <a href="https://mysignins.microsoft.com/security-info">mysignins.microsoft.com/security-info</a> and sign in.
3. Click **Add sign-in method** → **Authenticator app** → **Add**.
4. Below the QR code, click **I want to use a different authenticator app**. A new code appears. This one works with any TOTP app.
5. Scan the QR code with your app (Google Authenticator: tap + then Scan a QR code).
6. The app now shows a six-digit code. On your computer, click **Next**, type the code, click **Done**.

</div>

## Sign in with a TOTP app

<div class="steps">

1. Sign in with email and password.
2. Click **Use a verification code**.
3. Open your app. Find the six-digit code for SCU. Type it in.
4. Click **Verify**.

</div>

## Common questions

<div class="faq">

**I do not have a smartphone.**

You can use a TOTP app on your desktop (Authy Desktop, Bitwarden), a passkey on your laptop, or a security key.

**No fingerprint reader on my device.**

Use your device PIN. Every device that supports passkeys lets you use a PIN instead.

**I share a computer.**

Store your passkey on your phone. When you sign in, your phone asks you to verify. The passkey never touches the shared computer.

**New phone — what happens to my passkeys?**

iCloud Keychain or Google Password Manager sync them when you restore from backup. Register a second passkey as backup.

**New phone — what happens to my TOTP codes?**

Most apps can transfer. Google Authenticator has a transfer feature. If you lose access, delete the old entry at <a href="https://mysignins.microsoft.com/security-info">mysignins.microsoft.com/security-info</a> and set up again.

**New phone — what happens to Microsoft Authenticator?**

Restore from cloud backup if you had it turned on. If not, delete the old entry and start fresh.

**Can I use more than one method?**

Yes. Each method appears on your Security info page. Register at least two so you are never locked out.

**Can I keep using SMS?**

Only until 1 February 2027. After that, SMS stops.

**What if I do not want a passkey?**

Microsoft Authenticator and TOTP apps work fine. Passkey is recommended because it is fastest, but it is not the only choice.

</div>