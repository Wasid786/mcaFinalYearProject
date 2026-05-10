import smtplib
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURE YOUR SENDER ACCOUNT HERE
#  Use a Gmail account with an App Password:
#  Google Account → Security → 2-Step Verification → App Passwords
# ─────────────────────────────────────────────────────────────────────────────
SMTP_HOST         = "smtp.gmail.com"
SMTP_PORT         = 587
SENDER_EMAIL      = "madara21cabsa342@gmail.com"   # ← replace
SENDER_PASSWORD   = "azzohvlimozbxsyv"             # ← replace (App Password)
OTP_EXPIRY_SECONDS = 180                            # 3 minutes


def _generate_otp() -> str:
    return str(random.randint(100_000, 999_999))


def _send_email(recipient: str, otp: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Verification Code"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = recipient

    plain = (
        f"Your verification code is: {otp}\n"
        f"It expires in {OTP_EXPIRY_SECONDS // 60} minutes."
    )
    html = f"""
    <html><body>
      <div style="font-family:Arial,sans-serif;max-width:400px;margin:auto;
                  border:1px solid #ddd;border-radius:8px;padding:30px;">
        <h2 style="color:#2e7d32;">Email Verification</h2>
        <p>Use the code below to verify your email address.</p>
        <div style="font-size:36px;font-weight:bold;letter-spacing:8px;
                    color:#1b5e20;text-align:center;padding:20px 0;">{otp}</div>
        <p style="color:#888;font-size:12px;">
          This code expires in {OTP_EXPIRY_SECONDS // 60} minutes.<br>
          If you did not request this, please ignore this email.
        </p>
      </div>
    </body></html>
    """

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html,  "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())


class EmailOTPWindow:
    """
    Modal OTP verification window.

    - Sizes itself as a percentage of the screen so it looks good on any
      resolution (min 380 × 300, default ~28 % wide × 38 % tall).
    - Fonts scale with window width.

    Usage:
        EmailOTPWindow(parent, email="user@example.com", on_success=callback)
    """

    def __init__(
        self,
        parent: tk.Tk | tk.Toplevel,
        email: str,
        on_success=None,
    ):
        self.parent     = parent
        self.email      = email
        self.on_success = on_success
        self._otp       = ""
        self._sent_at   = 0.0

        # ── Window geometry: % of screen, centred ────────────────────────────
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()

        win_w = max(380, int(sw * 0.28))
        win_h = max(300, int(sh * 0.38))
        x_pos = (sw - win_w) // 2
        y_pos = (sh - win_h) // 2

        self.win = tk.Toplevel(parent)
        self.win.title("Email Verification")
        self.win.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.win.resizable(True, True)
        self.win.grab_set()                          # modal
        self.win.protocol("WM_DELETE_WINDOW", self._cancel)

        # Store for font scaling
        self._sw = sw

        self._build_ui()
        self._send_otp()

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        bg = "#f5f5f5"
        self.win.configure(bg=bg)

        sw = self._sw

        # ── Title ────────────────────────────────────────────────────────────
        title_font = ("Arial", max(16, int(sw * 0.014)), "bold")
        tk.Label(
            self.win, text="Verify Your Email",
            font=title_font, bg=bg, fg="#2e7d32",
        ).pack(pady=(int(self.win.winfo_reqheight() * 0.07) or 20, 6))

        # ── Info label ───────────────────────────────────────────────────────
        info_font = ("Arial", max(10, int(sw * 0.008)))
        self.info_lbl = tk.Label(
            self.win,
            text=f"A 6-digit code has been sent to:\n{self.email}",
            font=info_font, bg=bg, fg="#555", justify="center",
        )
        self.info_lbl.pack(pady=(0, 14))

        # ── OTP entry ────────────────────────────────────────────────────────
        entry_font = ("Arial", max(20, int(sw * 0.018)), "bold")
        entry_frame = tk.Frame(self.win, bg=bg)
        entry_frame.pack()

        self.var_otp  = tk.StringVar()
        self.otp_entry = ttk.Entry(
            entry_frame, textvariable=self.var_otp,
            font=entry_font, width=10, justify="center",
        )
        self.otp_entry.pack()
        self.otp_entry.focus()

        # ── Timer ────────────────────────────────────────────────────────────
        timer_font = ("Arial", max(9, int(sw * 0.007)))
        self.timer_lbl = tk.Label(
            self.win, text="", font=timer_font, bg=bg, fg="#e53935",
        )
        self.timer_lbl.pack(pady=6)

        # ── Buttons ──────────────────────────────────────────────────────────
        btn_font = ("Arial", max(11, int(sw * 0.009)), "bold")
        btn_frame = tk.Frame(self.win, bg=bg)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Verify", command=self._verify,
            bg="#2e7d32", fg="white", font=btn_font, width=9, cursor="hand2",
        ).grid(row=0, column=0, padx=6)

        self.resend_btn = tk.Button(
            btn_frame, text="Resend", command=self._send_otp,
            bg="#1565c0", fg="white", font=btn_font, width=9, cursor="hand2",
        )
        self.resend_btn.grid(row=0, column=1, padx=6)

        tk.Button(
            btn_frame, text="Cancel", command=self._cancel,
            bg="#b71c1c", fg="white", font=btn_font, width=9, cursor="hand2",
        ).grid(row=0, column=2, padx=6)

        self._tick()

    # ── OTP logic ────────────────────────────────────────────────────────────
    def _send_otp(self):
        self._otp     = _generate_otp()
        self._sent_at = time.time()
        self.resend_btn.config(state="disabled")
        self.info_lbl.config(text=f"Sending code to:\n{self.email} …")

        try:
            _send_email(self.email, self._otp)
            self.info_lbl.config(
                text=f"A 6-digit code has been sent to:\n{self.email}"
            )
        except Exception as e:
            messagebox.showerror(
                "Email Error", f"Could not send OTP:\n{e}", parent=self.win
            )
            self.info_lbl.config(text="Failed to send code. Check SMTP settings.")

        self.var_otp.set("")
        self.otp_entry.focus()

    def _verify(self):
        entered = self.var_otp.get().strip()

        if not entered:
            messagebox.showerror("Error", "Please enter the OTP.", parent=self.win)
            return

        if time.time() - self._sent_at > OTP_EXPIRY_SECONDS:
            messagebox.showerror(
                "Expired", "The OTP has expired. Please request a new one.",
                parent=self.win,
            )
            self.resend_btn.config(state="normal")
            return

        if entered == self._otp:
            messagebox.showinfo("Success", "Email verified successfully!", parent=self.win)
            self.win.destroy()
            if self.on_success:
                self.on_success()
        else:
            messagebox.showerror(
                "Error", "Incorrect OTP. Please try again.", parent=self.win
            )
            self.var_otp.set("")

    def _cancel(self):
        self.win.destroy()

    # ── Countdown timer ──────────────────────────────────────────────────────
    def _tick(self):
        if not self.win.winfo_exists():
            return
        remaining = int(OTP_EXPIRY_SECONDS - (time.time() - self._sent_at))
        if remaining > 0:
            self.timer_lbl.config(text=f"Code expires in {remaining}s")
            if remaining <= 30:
                self.resend_btn.config(state="normal")
            self.win.after(1000, self._tick)
        else:
            self.timer_lbl.config(text="Code expired — please resend.")
            self.resend_btn.config(state="normal")