import customtkinter as crk


class LoginView:
    def _init_(self):

        self.window = ctk.CTk()

        self.window.title("GL Secure Manager")

        self.window.geometry("500x350")

        self.label = crk.CTkLabel(
            self.window,
            text="GL Secure Manager",
            font=("Arial", 24),
        )

        self.label.pack(pady=50)

    def run(self):

        self.window.mainloop()
