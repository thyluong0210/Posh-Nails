import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# Sample data
SERVICES = {
    'Manicure': 20,
    'Pedicure': 25,
    'Gel Manicure': 30,
    'Matte Color': 15,
    'Gel Color': 18
}
TECHNICIANS = ['Elyn', 'Maria', 'Sam']
GOOGLE_ACCOUNTS = ['user1@gmail.com', 'user2@gmail.com', 'user3@gmail.com']
APPLE_ACCOUNTS = ['user1@icloud.com', 'user2@icloud.com', 'user3@icloud.com']

class PoshNailsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posh Nails Appointment Booking")
        self.geometry("700x700")
       
        # Dictionary to store session data
        self.data = {}
       
        # Create a top frame for the logo/image
        image_frame = tk.Frame(self)
        image_frame.pack(side="top", fill="x")

        self.image = ImageTk.PhotoImage(Image.open("poshnails.jpg"))
        image_label = tk.Label(image_frame, image=self.image)
        image_label.pack(pady=2)

        # Centered second container
        container = tk.Frame(self, width=400, height=700)
        container.place(relx=0.5, rely=0.55, anchor="center")

        self.frames = {}
        for F in (SigninPage, GoogleSigninPage, AppleSigninPage, ServicesPage,
                  AppointmentPage, CheckoutPage, PaymentPage, ConfirmationPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
       
        self.show_frame("SigninPage")
   
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class SigninPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
       
        tk.Label(self, text="Sign In", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack(pady=5)
        tk.Button(self, text="Continue", command=self.sign_in).pack(pady=5)
        tk.Button(self, text="Continue with Google",
                  command=lambda: controller.show_frame("GoogleSigninPage")).pack(pady=5)
        tk.Button(self, text="Continue with Apple",
                  command=lambda: controller.show_frame("AppleSigninPage")).pack(pady=5)
   
    def sign_in(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Email address is required.")
            return
        if "@" not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        self.controller.data["email"] = email
        self.controller.show_frame("ServicesPage")

class GoogleSigninPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        original_image = Image.open("google.jpg")
        tw=170; w,h=original_image.size
        resized = original_image.resize((tw, int(tw*h/w)), Image.LANCZOS)
        self.google_logo = ImageTk.PhotoImage(resized)
        tk.Label(self, image=self.google_logo).pack(pady=5)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("SigninPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Google Sign In", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Select your Google Account:").pack(pady=5)
        self.selected_account = tk.StringVar(self)
        self.selected_account.set(GOOGLE_ACCOUNTS[0])
        tk.OptionMenu(self, self.selected_account, *GOOGLE_ACCOUNTS).pack(pady=5)
        tk.Button(self, text="Continue", command=self.choose_account).pack(pady=5)
   
    def choose_account(self):
        acct = self.selected_account.get()
        if not acct:
            messagebox.showerror("Error", "Please select a Google account.")
            return
        self.controller.data["email"] = acct
        self.controller.show_frame("ServicesPage")

class AppleSigninPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        orig = Image.open("apple.jpg")
        tw=120; w,h=orig.size
        resized = orig.resize((tw, int(tw*h/w)), Image.LANCZOS)
        self.apple_logo = ImageTk.PhotoImage(resized)
        tk.Label(self, image=self.apple_logo).pack(pady=5)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("SigninPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Apple Sign In", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Select your Apple Account:").pack(pady=5)
        self.selected_account = tk.StringVar(self)
        self.selected_account.set(APPLE_ACCOUNTS[0])
        tk.OptionMenu(self, self.selected_account, *APPLE_ACCOUNTS).pack(pady=5)
        tk.Button(self, text="Continue", command=self.choose_account).pack(pady=5)
   
    def choose_account(self):
        acct = self.selected_account.get()
        if not acct:
            messagebox.showerror("Error", "Please select an Apple account.")
            return
        self.controller.data["email"] = acct
        self.controller.show_frame("ServicesPage")

class ServicesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.logo_img = ImageTk.PhotoImage(Image.open("PNLogo.png"))
        self.logo_label = tk.Label(self, image=self.logo_img)
        self.logo_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        tk.Label(self, text="Select Services", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Choose one or more services:").pack(pady=5)
        self.service_vars = {}
        for s,p in SERVICES.items():
            var = tk.IntVar()
            tk.Checkbutton(self, text=f"{s} - ${p}", variable=var).pack(anchor="w", padx=20)
            self.service_vars[s] = var
        tk.Button(self, text="Continue to Appointment", command=self.save_services).pack(pady=10)
   
    def save_services(self):
        chosen = [s for s,var in self.service_vars.items() if var.get()==1]
        if not chosen:
            messagebox.showerror("Error", "Please select at least one service.")
            return
        self.controller.data["services"] = chosen
        self.controller.show_frame("AppointmentPage")

class AppointmentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("ServicesPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Appointment Booking", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Select Date:").pack(pady=5)
        self.date_var = tk.StringVar(self)
        dates = [(datetime.today()+timedelta(days=i)).strftime("%m/%d/%Y") for i in range(7)]
        self.date_var.set(dates[0])
        tk.OptionMenu(self, self.date_var, *dates, command=lambda d: None).pack(pady=5)
        tk.Label(self, text="Select Time:").pack(pady=5)
        self.time_var = tk.StringVar(self)
        times = ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM"]
        self.time_var.set(times[0])
        self.time_option = tk.OptionMenu(self, self.time_var, *times)
        self.time_option.pack(pady=5)
        tk.Label(self, text="Select Technician(s) (max 2):").pack(pady=5)
        self.tech_vars = {}
        for t in TECHNICIANS:
            var = tk.IntVar()
            tk.Checkbutton(self, text=t, variable=var).pack(anchor="w", padx=20)
            self.tech_vars[t] = var
        tk.Button(self, text="Continue to Checkout", command=self.save_appointment).pack(pady=10)
   
    def save_appointment(self):
        d = self.date_var.get().strip(); tm = self.time_var.get().strip()
        if not d or not tm:
            messagebox.showerror("Error","Please select a date and time."); return
        try: datetime.strptime(d,"%m/%d/%Y")
        except: messagebox.showerror("Error","Invalid date format. Please use MM/DD/YYYY."); return
        techs = [t for t,var in self.tech_vars.items() if var.get()==1]
        if not techs:
            messagebox.showerror("Error","Please select at least one technician."); return
        if len(techs)>2:
            messagebox.showerror("Error","Please select at most 2 technicians."); return
        self.controller.data["appointment"] = {"date":d,"time":tm,"technicians":techs}
        self.controller.show_frame("CheckoutPage")

class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("AppointmentPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Checkout", font=("Helvetica", 16)).pack(pady=10)
        self.summary_text = tk.Text(self, height=15, width=50)
        self.summary_text.pack(pady=5); self.summary_text.config(state="disabled")
        tk.Label(self, text="Tip (optional):").pack(pady=5)
        self.tip_entry = tk.Entry(self, width=10); self.tip_entry.pack(pady=5)
        tk.Label(self, text="Promo Code (optional):").pack(pady=5)
        self.promo_entry = tk.Entry(self, width=20); self.promo_entry.pack(pady=5)
        self.payment_method = tk.StringVar(value="apple_pay")
        tk.Label(self, text="Select Payment Method:").pack(pady=5)
        tk.Radiobutton(self, text="Apple Pay", variable=self.payment_method, value="apple_pay").pack()
        tk.Radiobutton(self, text="Credit/Debit Card", variable=self.payment_method, value="credit_card").pack()
        tk.Button(self, text="Pay Now", command=self.process_checkout).pack(pady=8)
   
    def update_summary(self):
        services = self.controller.data.get("services", [])
        subtotal = sum(SERVICES[s] for s in services)
        tax = subtotal * 0.06
        tip = 0.0
        try: tip = float(self.tip_entry.get().strip())
        except: tip = 0.0
        total = subtotal + tax + tip
        summary = "Services:\n"
        for s in services:
            summary += f" - {s}: ${SERVICES[s]}\n"
        summary += "\n"
        appt = self.controller.data.get("appointment", {})
        summary += "Appointment Details:\n\n"
        summary += f"Date: {appt.get('date','N/A')}\n\n"
        summary += f"Time: {appt.get('time','N/A')}\n\n"
        summary += f"Technician(s): {', '.join(appt.get('technicians',[]))}\n\n"
        summary += f"Subtotal: ${subtotal:.2f}\n"
        summary += f"Tax (6%): ${tax:.2f}\n"
        summary += f"Total: ${total:.2f}"
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0",tk.END)
        self.summary_text.insert(tk.END,summary)
        self.summary_text.config(state="disabled")
        self.controller.data["checkout"] = {
            "tip": tip,
            "promo": self.promo_entry.get().strip(),
            "payment_method": self.payment_method.get()
        }
   
    def process_checkout(self):
        self.update_summary()
        if self.payment_method.get()=="credit_card":
            self.controller.show_frame("PaymentPage")
        else:
            self.controller.show_frame("ConfirmationPage")
    def tkraise(self,*a,**k):
        super().tkraise(*a,**k)
        self.update_summary()

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("CheckoutPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Enter Payment Details", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Cardholder First Name:").pack(pady=5)
        self.first_name = tk.Entry(self, width=30); self.first_name.pack(pady=5)
        tk.Label(self, text="Cardholder Last Name:").pack(pady=5)
        self.last_name = tk.Entry(self, width=30); self.last_name.pack(pady=5)
        tk.Label(self, text="Card Number:").pack(pady=5)
        self.card_number = tk.Entry(self, width=30); self.card_number.pack(pady=5)
        tk.Label(self, text="Expiry Date (MM/YYYY):").pack(pady=5)
        self.expiry = tk.Entry(self, width=15); self.expiry.pack(pady=5)
        tk.Label(self, text="CVV:").pack(pady=5)
        self.cvv = tk.Entry(self, width=10, show="*"); self.cvv.pack(pady=5)
        tk.Button(self, text="Confirm Payment", command=self.confirm_payment).pack(pady=10)
   
    def confirm_payment(self):
        f = self.first_name.get().strip()
        l = self.last_name.get().strip()
        c = self.card_number.get().strip()
        e = self.expiry.get().strip()
        v = self.cvv.get().strip()
        if not all([f,l,c,e,v]):
            messagebox.showerror("Error","All payment fields are required."); return
        if not c.isdigit() or len(c) not in (15,16):
            messagebox.showerror("Error","Card must be 15 or 16 digits."); return
        if len(c)==15 and (not v.isdigit() or len(v)!=4):
            messagebox.showerror("Error","15‑digit card needs 4‑digit CVV."); return
        if len(c)==16 and (not v.isdigit() or len(v)!=3):
            messagebox.showerror("Error","16‑digit card needs 3‑digit CVV."); return
        try:
            exp_date = datetime.strptime(e,"%m/%Y")
            if exp_date<datetime.now():
                messagebox.showerror("Error","Card is expired."); return
        except:
            messagebox.showerror("Error","Invalid expiry format."); return
        self.controller.data["payment"] = {
            "first_name": f, "last_name": l,
            "card_number": c[-4:], "expiry": e
        }
        self.controller.show_frame("ConfirmationPage")

class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load and show tick image
        orig = Image.open("tick.jpg")
        tw=120; w,h=orig.size
        resized=orig.resize((tw,int(tw*h/w)),Image.LANCZOS)
        self.tick_logo=ImageTk.PhotoImage(resized)
        tk.Label(self, image=self.tick_logo).pack(pady=5)

        self.label = tk.Label(self, text="Booking Confirmation", font=("Helvetica", 16))
        self.label.pack(pady=10)
        self.details = tk.Text(self, height=15, width=50)
        self.details.pack(pady=5)
        self.details.config(state="disabled")
        tk.Button(self, text="Exit", command=self.quit_app).pack(pady=10)
   
    def update_confirmation(self):
        email = self.controller.data.get("email", "Unknown")
        services = self.controller.data.get("services", [])
        appointment = self.controller.data.get("appointment", {})
        checkout = self.controller.data.get("checkout", {})
        payment = self.controller.data.get("payment", None)
       
        subtotal = sum(SERVICES[s] for s in services)
        tax = subtotal * 0.06
        tip = checkout.get("tip", 0)
        total = subtotal + tax + tip

        # Apply promo code
        promo = checkout.get("promo", "").upper()
        discount = 0
        if promo == "5OFF":
            discount = 5
            total -= discount
       
        conf_str = f"Thank you, {email}!\nYour appointment is confirmed.\n\n"
        conf_str += "Appointment Details:\n\n"
        conf_str += f"Date: {appointment.get('date', 'N/A')}\n\n"
        conf_str += f"Time: {appointment.get('time', 'N/A')}\n\n"
        techs = appointment.get("technicians", [])
        conf_str += f"Technician(s): {', '.join(techs) if techs else 'N/A'}\n\n"
        conf_str += "Services Booked:\n"
        for svc in services:
            conf_str += f"  {svc} - ${SERVICES[svc]}\n"
        conf_str += f"\nSubtotal: ${subtotal:.2f}\n"
        conf_str += f"Tax (6%): ${tax:.2f}\n"
        conf_str += f"Tip: ${tip:.2f}\n"
        if discount > 0:
            conf_str += f"Promo Discount: -${discount:.2f}\n"
        conf_str += f"Total: ${total:.2f}\n\n"
        if payment:
            conf_str += f"Payment: Credit/Debit Card ending in {payment['card_number']}\n"
        else:
            conf_str += "Payment: Apple Pay\n"
        conf_str += "\n✓ Payment Successful\nYou may now exit this window."
       
        self.details.config(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, conf_str)
        self.details.config(state="disabled")
   
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_confirmation()
   
    def quit_app(self):
        self.controller.destroy()

if __name__ == "__main__":
    app = PoshNailsApp()
    app.mainloop()

# Posh-Nails
