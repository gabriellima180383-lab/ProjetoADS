"""
GL Secure Manager
Sistema de Gestão de Segurança Patrimonial

Autor: GL Infinity Tech
"""

from src.views.login.login_view import LoginView


def main():
    app = LoginView()
    app.run()


if __name__ == "__main__":
    main()
