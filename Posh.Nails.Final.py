'''
Program:   Appointment Scheduling Application
Developers: Emilio Cortes, Anh Ho, Rachael Luong, Antonio Teran
Date:      4/24/2025
Purpose:   The application allows users to log in using their preferred email, selecting their desired services, nail technicians, date and time of appointment, paying with Apple Pay, or entering the credit card details manually, and finally receiving a booking confirmation. 
'''

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

        # Dictionary to hold all page frames
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
        target_width = 170
        original_width, original_height = original_image.size
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)
        resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
        self.google_logo = ImageTk.PhotoImage(resized_image)

        logo_label = tk.Label(self, image=self.google_logo)
        logo_label.pack(pady=5)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("SigninPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Google Sign In", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Select your Google Account:").pack(pady=5)
       
        self.selected_account = tk.StringVar(self)
        self.selected_account.set(GOOGLE_ACCOUNTS[0])
        option_menu = tk.OptionMenu(self, self.selected_account, *GOOGLE_ACCOUNTS)
        option_menu.pack(pady=5)
        tk.Button(self, text="Continue", command=self.choose_account).pack(pady=5)
   
    def choose_account(self):
        account = self.selected_account.get()
        if not account:
            messagebox.showerror("Error", "Please select a Google account.")
            return
        self.controller.data["email"] = account
        self.controller.show_frame("ServicesPage")

class AppleSigninPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
       
        original_image = Image.open("apple.jpg")
        target_width = 120
        original_width, original_height = original_image.size
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)
        resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
        self.apple_logo = ImageTk.PhotoImage(resized_image)

        logo_label = tk.Label(self, image=self.apple_logo)
        logo_label.pack(pady=5)
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("SigninPage"))\
            .pack(anchor="w", padx=10, pady=5)
        tk.Label(self, text="Apple Sign In", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Select your Apple Account:").pack(pady=5)
       
        self.selected_account = tk.StringVar(self)
        self.selected_account.set(APPLE_ACCOUNTS[0])
        option_menu = tk.OptionMenu(self, self.selected_account, *APPLE_ACCOUNTS)
        option_menu.pack(pady=5)
        tk.Button(self, text="Continue", command=self.choose_account).pack(pady=5)
   
    def choose_account(self):
        account = self.selected_account.get()
        if not account:
            messagebox.showerror("Error", "Please select an Apple account.")
            return
        self.controller.data["email"] = account
        self.controller.show_frame("ServicesPage")

class ServicesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
       
        tk.Label(self, text="Select Services", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self, text="Choose one or more services:").pack(pady=5)
       
        self.service_vars = {}
        for service, price in SERVICES.items():
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=f"{service} - ${price}", variable=var)
            chk.pack(anchor="w", padx=20)
            self.service_vars[service] = var
       
        tk.Button(self, text="Continue to Appointment", command=self.save_services).pack(pady=10)
   
    def save_services(self):
        selected_services = [s for s, v in self.service_vars.items() if v.get()]
        if not selected_services:
            messagebox.showerror("Error", "Please select at least one service.")
            return
        self.controller.data["services"] = selected_services
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
        available_dates = self.generate_dates()
        self.date_var.set(available_dates[0])
        self.date_option = tk.OptionMenu(self, self.date_var, *available_dates, command=self.date_changed)
        self.date_option.pack(pady=5)
        tk.Label(self, text="Select Time:").pack(pady=5)
        self.time_var = tk.StringVar(self)
        available_times = self.get_available_times(self.date_var.get())
        self.time_var.set(available_times[0])
        self.time_option = tk.OptionMenu(self, self.time_var, *available_times)
        self.time_option.pack(pady=5)
        tk.Label(self, text="Select Technician(s) (max 2):").pack(pady=5)
        self.tech_vars = {}
        for tech in TECHNICIANS:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=tech, variable=var)
            chk.pack(anchor="w", padx=20)
            self.tech_vars[tech] = var
        tk.Button(self, text="Continue to Checkout", command=self.save_appointment).pack(pady=10)
   
    def generate_dates(self):
        today = datetime.today()
        return [(today + timedelta(days=i)).strftime("%m/%d/%Y") for i in range(7)]
   
    def get_available_times(self, date_str):
        return ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
                "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"]
   
    def date_changed(self, new_date):
        times = self.get_available_times(new_date)
        self.time_var.set(times[0])
        menu = self.time_option["menu"]
        menu.delete(0, "end")
        for t in times:
            menu.add_command(label=t, command=lambda v=t: self.time_var.set(v))
   
    def save_appointment(self):
        date_text = self.date_var.get().strip()
        time_text = self.time_var.get().strip()
        if not date_text or not time_text:
            messagebox.showerror("Error", "Please select a date and time.")
            return
        try:
            datetime.strptime(date_text, "%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return
        selected_techs = [t for t, v in self.tech_vars.items() if v.get()]
        if not selected_techs:
            messagebox.showerror("Error", "Please select at least one technician.")
            return
        if len(selected_techs) > 2:
            messagebox.showerror("Error", "Please select at most 2 technicians.")
            return
        self.controller.data["appointment"] = {
            "date": date_text,
            "time": time_text,
            "technicians": selected_techs
        }
        self.controller.show_frame("CheckoutPage")

class CheckoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("AppointmentPage"))\
            .pack(anchor="w", padx=10, pady=5)
       
        self.summary_label = tk.Label(self, text="Checkout", font=("Helvetica", 16))
        self.summary_label.pack(pady=10)
       
        self.summary_text = tk.Text(self, height=15, width=50)
        self.summary_text.pack(pady=5)
        self.summary_text.config(state="disabled")
       
        tk.Label(self, text="Tip (optional):").pack(pady=5)
        self.tip_entry = tk.Entry(self, width=10)
        self.tip_entry.pack(pady=5)
       
        tk.Label(self, text="Promo Code (optional):").pack(pady=5)
        self.promo_entry = tk.Entry(self, width=20)
        self.promo_entry.pack(pady=5)
       
        self.payment_method = tk.StringVar(value="apple_pay")
        tk.Label(self, text="Select Payment Method:").pack(pady=5)
        tk.Radiobutton(self, text="Apple Pay", variable=self.payment_method,
                       value="apple_pay").pack()
        tk.Radiobutton(self, text="Credit/Debit Card", variable=self.payment_method,
                       value="credit_card").pack()
       
        tk.Button(self, text="Pay Now", command=self.process_checkout).pack(pady=8)
   
    def update_summary(self):
        services = self.controller.data.get("services", [])
        subtotal = sum(SERVICES[svc] for svc in services)
        tax = subtotal * 0.0825
        tip = 0.0
        try:
            tip = float(self.tip_entry.get().strip())
        except ValueError:
            tip = 0.0
        total = subtotal + tax + tip
       
        summary = "Services:\n"
        for svc in services:
            summary += f" - {svc}: ${SERVICES[svc]}\n"
        summary += "\n"
       
        appointment = self.controller.data.get("appointment", {})
        if appointment:
            summary += "Appointment Details:\n\n"
            summary += f"Date: {appointment.get('date', 'N/A')}\n\n"
            summary += f"Time: {appointment.get('time', 'N/A')}\n\n"
            techs = appointment.get("technicians", [])
            summary += f"Technician(s): {', '.join(techs) if techs else 'N/A'}\n\n"
       
        summary += f"Subtotal: ${subtotal:.2f}\n"
        summary += f"Tax (8.25%): ${tax:.2f}\n"
        summary += f"Total: ${total:.2f}"
       
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state="disabled")
       
        self.controller.data["checkout"] = {
            "tip": tip,
            "promo": self.promo_entry.get().strip(),
            "payment_method": self.payment_method.get()
        }
   
    def process_checkout(self):
        self.update_summary()
        if self.payment_method.get() == "credit_card":
            self.controller.show_frame("PaymentPage")
        else:
            self.controller.show_frame("ConfirmationPage")
   
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_summary()

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Button(self, text="Go Back", command=lambda: controller.show_frame("CheckoutPage"))\
            .pack(anchor="w", padx=10, pady=5)
       
        tk.Label(self, text="Enter Payment Details", font=("Helvetica", 16)).pack(pady=10)
       
        tk.Label(self, text="Cardholder First Name:").pack(pady=5)
        self.first_name = tk.Entry(self, width=30)
        self.first_name.pack(pady=5)
       
        tk.Label(self, text="Cardholder Last Name:").pack(pady=5)
        self.last_name = tk.Entry(self, width=30)
        self.last_name.pack(pady=5)
       
        tk.Label(self, text="Card Number:").pack(pady=5)
        self.card_number = tk.Entry(self, width=30)
        self.card_number.pack(pady=5)
       
        tk.Label(self, text="Expiry Date (MM/YYYY):").pack(pady=5)
        self.expiry = tk.Entry(self, width=15)
        self.expiry.pack(pady=5)
       
        tk.Label(self, text="CVV:").pack(pady=5)
        self.cvv = tk.Entry(self, width=10, show="*")
        self.cvv.pack(pady=5)
       
        tk.Button(self, text="Confirm Payment", command=self.confirm_payment).pack(pady=10)
   
    def confirm_payment(self):
        first = self.first_name.get().strip()
        last = self.last_name.get().strip()
        card = self.card_number.get().strip()
        expiry = self.expiry.get().strip()
        cvv = self.cvv.get().strip()
       
        if not all([first, last, card, expiry, cvv]):
            messagebox.showerror("Error", "All payment fields are required.")
            return
        if not card.isdigit():
            messagebox.showerror("Error", "Card number must be numeric.")
            return
        if len(card) not in (15, 16):
            messagebox.showerror("Error", "Card number must be 15 or 16 digits long.")
            return
        if len(card) == 15:
            if not (cvv.isdigit() and len(cvv) == 4):
                messagebox.showerror("Error", "For a 15-digit card number, the CVV must be 4 digits.")
                return
        else:
            if not (cvv.isdigit() and len(cvv) == 3):
                messagebox.showerror("Error", "For a 16-digit card number, the CVV must be 3 digits.")
                return
        try:
            exp_date = datetime.strptime(expiry, "%m/%Y")
            if exp_date < datetime.now():
                messagebox.showerror("Error", "Card is expired.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid expiry date format. Use MM/YYYY.")
            return
       
        self.controller.data["payment"] = {
            "first_name": first,
            "last_name": last,
            "card_number": card[-4:],
            "expiry": expiry
        }
        self.controller.show_frame("ConfirmationPage")

class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        original_image = Image.open("tick.jpg")
        target_width = 120
        original_width, original_height = original_image.size
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)
        resized_image = original_image.resize((target_width, target_height), Image.LANCZOS)
        self.tick_logo = ImageTk.PhotoImage(resized_image)

        logo_label = tk.Label(self, image=self.tick_logo)
        logo_label.pack(pady=5)

        self.label = tk.Label(self, text="Booking Confirmation", font=("Helvetica", 16))
        self.label.pack(pady=10)
        self.details = tk.Text(self, height=15, width=50)
        self.details.pack(pady=5)
        self.details.config(state="disabled")
        tk.Button(self, text="Exit", command=self.quit_app).pack(pady=10)

    def update_confirmation(self):
        email       = self.controller.data.get("email", "Unknown")
        services    = self.controller.data.get("services", [])
        appointment = self.controller.data.get("appointment", {})
        checkout    = self.controller.data.get("checkout", {})
        payment     = self.controller.data.get("payment", None)

        subtotal = sum(SERVICES[svc] for svc in services)
        tax      = subtotal * 0.0825
        tip      = checkout.get("tip", 0)

        # Handle promo code "5OFF"
        promo_code = checkout.get("promo", "").upper()
        discount   = 5 if promo_code == "5OFF" else 0

        total = subtotal + tax + tip - discount

        conf_str  = f"Thank you, {email}!\nYour appointment is confirmed.\n\n"
        conf_str += "Appointment Details:\n\n"
        conf_str += f"Date: {appointment.get('date', 'N/A')}\n\n"
        conf_str += f"Time: {appointment.get('time', 'N/A')}\n\n"
        techs = appointment.get("technicians", [])
        conf_str += f"Technician(s): {', '.join(techs) if techs else 'N/A'}\n\n"
        conf_str += "Services Booked:\n"
        for svc in services:
            conf_str += f"  {svc} - ${SERVICES[svc]}\n"
        conf_str += f"\nSubtotal: ${subtotal:.2f}\n"
        conf_str += f"Tax (8.25%): ${tax:.2f}\n"
        conf_str += f"Tip: ${tip:.2f}\n"
        if discount > 0:
            conf_str += f"Promo Discount: ${discount:.2f}\n"
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

