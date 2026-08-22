+++
id = "mfa"
title = "Multi-factor authentication (MFA)"
category = "knowledge-base"
subcategory = "mfa"
updated = "2026-08-22"
applies_to = "All staff and students"
action_required = "1 February 2027"
+++

## What is changing

Microsoft is phasing out SMS-based multi-factor authentication. SMS codes are a security risk. They can be intercepted, stolen in SIM-swap attacks, or phished. They also fail when you have no phone signal.

All staff and students need to move to a better method by 1 February 2027. After that date, SMS codes stop working for MFA.

You still sign in with your SCU email and password. MFA is the second check. What changes is how you prove it is really you.

## Your options

<div class="table-wrap">

| Method | Speed | Offline? | Needs a phone? | Can it be phished? |
|---|---|---|---|---|
| Passkey (recommended) | ~1 second | Yes | No | No |
| Microsoft Authenticator | ~3 seconds | No | Yes | No |
| TOTP app | ~15 seconds | Yes | No | No |
| Security key | ~1 second | Yes | No | No |
| SMS code | 10-30 seconds | No | Yes | Yes |

</div>

The passkey is fastest and most secure. Microsoft Authenticator and TOTP apps are also solid choices if a passkey does not suit you.

## Option 1: a passkey

A passkey uses your fingerprint, face, or device PIN instead of a code. It takes about a second and cannot be phished.

A passkey is a digital key stored on your device. When you sign in, your device confirms it is you locally. Your fingerprint or face data never leaves your device.

You only need one passkey. Add at least two as a backup.

<div class="table-wrap">

| Where | How it works |
|---|---|
| Your laptop or desktop | The passkey sits in your device's secure chip. Use Windows Hello, Touch ID, or your PIN. |
| Your phone or tablet | The passkey lives on your phone. When you sign in on a computer, your phone confirms your identity over Bluetooth. |
| A security key | A small USB or NFC key. Plug it in or tap it. Good for shared computers or if you do not have a phone. |

</div>

### Register a passkey

Before you start, have your SCU username, password, and current MFA method (SMS or voice call) ready. If using a phone, turn Bluetooth on and keep the phone nearby.

<div class="steps">

1. On your computer, go to <a href="https://mysignins.microsoft.com/security-info">mysignins.microsoft.com/security-info</a>
2. Sign in. Complete MFA if asked.
3. Click **Add sign-in method** → **Passkey** → **Add**.
4. Pick where to store it:
   - **This device** — saves to your computer. Use Windows Hello, Touch ID, or your PIN.
   - **Phone or tablet** — scan the QR code with your phone camera. Authenticate with fingerprint, face, or PIN. Your phone will confirm future sign-ins from this computer.
   - **Security key** — insert or tap your key. Touch the button or sensor when prompted.
5. Check **Passkey** appears on your Security info page. Done.

</div>

<div class="callout callout--gold">

If you registered on your phone: when you sign in on a computer, your phone will ask you to verify. Keep Bluetooth on for both devices.

</div>

### Sign in with a passkey

<div class="steps">

1. Sign in with email and password as usual.
2. At the MFA prompt, click **Continue** or **Use passkey**.
3. Authenticate — fingerprint, face, PIN, or security key.
4. Done.

</div>

## Option 2: Microsoft Authenticator

Microsoft Authenticator is a free phone app. You tap **Approve** on a push notification instead of typing a code. You need a smartphone (iPhone or Android) with internet access.

### Set it up

<div class="steps">

1. Install Microsoft Authenticator on your phone. Do not open it yet.
2. On your computer, go to <a href="https://mysignins.microsoft.com/security-info">mysignins.microsoft.com/security-info</a> and sign in.
3. Click **Add sign-in method** → **Authenticator app** → **Add**.
4. A QR code appears on screen. Leave this page open.
5. Open Authenticator on your phone. Tap **+** or **Add account** → **Work or school account** → **Scan QR code**. Point your camera at the code.
6. A test notification lands on your phone. Open it, tap **Approve**, and type the two-digit number from your screen.
7. Click **Next** then **Done**.

</div>

### Sign in with Authenticator

<div class="steps">

1. Sign in with email and password.
2. A notification appears on your phone. Open it.
3. Type the two-digit number shown on your computer screen.
4. Tap **Yes** or **Approve**.

</div>

## Option 3: a TOTP app

TOTP stands for time-based one-time password. The app shows a six-digit code that changes every 30 seconds. You type this code at sign-in.

It works on phones and desktop computers. You do not need a Microsoft account. It works offline. Common apps: Google Authenticator (free), Authy (free, desktop and phone), Bitwarden (built into the password manager).

### Set it up

<div class="steps">

1. Install your TOTP app.
2. On your computer, go to <a href="https://mysignins.microsoft.com/security-info">mysignins.microsoft.com/security-info</a> and sign in.
3. Click **Add sign-in method** → **Authenticator app** → **Add**.
4. Below the QR code, click **I want to use a different authenticator app**. A new code appears. This one works with any TOTP app.
5. Scan the QR code with your app (Google Authenticator: tap + then Scan a QR code).
6. The app now shows a six-digit code. On your computer, click **Next**, type the code, click **Done**.

</div>

### Sign in with a TOTP app

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