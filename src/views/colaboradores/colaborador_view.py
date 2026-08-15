import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk

import customtkinter as ctk
import cv2
from PIL import Image

from src.services.colaborador_service import ColaboradorService


class ColaboradorView:
    def __init__(self, master, usuario):

        self.master = master
        self.usuario = usuario

        self.service = ColaboradorService()

        self.colaborador_selecionado = None

        # ==================================================
        # CÂMERA
        # ==================================================

        self.camera = None
        self.janela_camera = None
        self.preview_camera = None

        # ==================================================
        # FOTOS
        # ==================================================

        self.foto_nova = None
        self.foto_edicao = None

        # ==================================================
        # JANELA PRINCIPAL
        # ==================================================

        self.window = ctk.CTkToplevel(master)

        self.window.title("GL Secure Manager - Colaboradores")

        self.window.geometry("1200x750")

        self.window.minsize(
            1000,
            650,
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.fechar,
        )

        self.criar_interface()

        self.carregar_colaboradores()

    # ==================================================
    # INTERFACE PRINCIPAL
    # ==================================================

    def criar_interface(self):

        self.titulo = ctk.CTkLabel(
            self.window,
            text="Gestão de Colaboradores",
            font=("Arial", 28, "bold"),
        )

        self.titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 10),
        )

        self.usuario_logado = ctk.CTkLabel(
            self.window,
            text=(
                f"Usuário logado: "
                f"{self.usuario['nome']} | "
                f"Perfil: "
                f"{self.usuario['perfil']}"
            ),
            font=("Arial", 14),
        )

        self.usuario_logado.pack(
            anchor="w",
            padx=30,
            pady=(0, 20),
        )

        # ==================================================
        # BOTÕES
        # ==================================================

        self.frame_acoes = ctk.CTkFrame(
            self.window,
            fg_color="transparent",
        )

        self.frame_acoes.pack(
            fill="x",
            padx=30,
            pady=(0, 10),
        )

        self.botao_novo = ctk.CTkButton(
            self.frame_acoes,
            text="Novo Colaborador",
            width=170,
            command=self.novo_colaborador,
        )

        self.botao_novo.pack(
            side="left",
        )

        self.botao_editar = ctk.CTkButton(
            self.frame_acoes,
            text="Editar Colaborador",
            width=170,
            command=self.editar_colaborador,
        )

        self.botao_editar.pack(
            side="left",
            padx=10,
        )

        self.botao_excluir = ctk.CTkButton(
            self.frame_acoes,
            text="Excluir Colaborador",
            width=170,
            command=self.excluir_colaborador,
        )

        self.botao_excluir.pack(
            side="left",
        )

        # ==================================================
        # TABELA
        # ==================================================

        self.tabela = ttk.Treeview(
            self.window,
            columns=(
                "id",
                "nome",
                "matricula",
                "cargo",
                "setor",
                "status",
            ),
            show="headings",
        )

        colunas = {
            "id": ("ID", 60),
            "nome": ("Nome", 280),
            "matricula": ("Matrícula", 130),
            "cargo": ("Cargo", 180),
            "setor": ("Setor", 180),
            "status": ("Status", 100),
        }

        for coluna, (titulo, largura) in colunas.items():
            self.tabela.heading(
                coluna,
                text=titulo,
            )

            self.tabela.column(
                coluna,
                width=largura,
            )

        self.tabela.column(
            "id",
            anchor="center",
        )

        self.tabela.column(
            "status",
            anchor="center",
        )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10,
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_colaborador,
        )

    # ==================================================
    # CARREGAR COLABORADORES
    # ==================================================

    def carregar_colaboradores(self):

        colaboradores = self.service.listar()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for colaborador in colaboradores:
            self.tabela.insert(
                "",
                "end",
                values=(
                    colaborador["id"],
                    colaborador["nome"],
                    colaborador["matricula"],
                    colaborador["cargo"],
                    colaborador["setor"] or "",
                    colaborador["status"],
                ),
            )

    # ==================================================
    # SELECIONAR COLABORADOR
    # ==================================================

    def selecionar_colaborador(self, event=None):

        selecao = self.tabela.selection()

        if not selecao:
            self.colaborador_selecionado = None

            return

        item = selecao[0]

        valores = self.tabela.item(
            item,
            "values",
        )

        if valores:
            self.colaborador_selecionado = int(valores[0])

            print(f"Colaborador selecionado: ID {self.colaborador_selecionado}")

    # ==================================================
    # NOVO COLABORADOR
    # ==================================================

    def novo_colaborador(self):

        self.foto_nova = None

        self.janela_novo = ctk.CTkToplevel(self.window)

        self.janela_novo.title("Novo Colaborador")

        self.janela_novo.geometry("850x650")

        self.janela_novo.resizable(
            False,
            False,
        )

        self.janela_novo.transient(self.window)

        self.janela_novo.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_novo,
            text="Novo Colaborador",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(
            pady=(25, 20),
        )

        frame_conteudo = ctk.CTkFrame(
            self.janela_novo,
            fg_color="transparent",
        )

        frame_conteudo.pack(
            fill="both",
            expand=True,
            padx=30,
        )

        frame_formulario = ctk.CTkFrame(
            frame_conteudo,
            fg_color="transparent",
        )

        frame_formulario.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 20),
        )

        self.nome_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
            placeholder_text="Nome completo",
        )

        self.nome_entry.pack(pady=10)

        self.matricula_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
            placeholder_text="Matrícula",
        )

        self.matricula_entry.pack(pady=10)

        self.cargo_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
            placeholder_text="Cargo",
        )

        self.cargo_entry.pack(pady=10)

        self.setor_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
            placeholder_text="Setor",
        )

        self.setor_entry.pack(pady=10)

        self.status_combo = ctk.CTkComboBox(
            frame_formulario,
            width=350,
            height=40,
            values=[
                "Ativo",
                "Inativo",
            ],
        )

        self.status_combo.pack(pady=10)

        self.status_combo.set("Ativo")

        # FOTO

        self.criar_area_foto(
            frame_conteudo,
            "novo",
        )

        self.mensagem_novo = ctk.CTkLabel(
            self.janela_novo,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_novo.pack(pady=5)

        self.botao_salvar_novo = ctk.CTkButton(
            self.janela_novo,
            width=350,
            height=40,
            text="SALVAR COLABORADOR",
            command=self.salvar_novo_colaborador,
        )

        self.botao_salvar_novo.pack(pady=(5, 20))

        self.nome_entry.focus()

    # ==================================================
    # ÁREA DE FOTO
    # ==================================================

    def criar_area_foto(
        self,
        parent,
        modo,
    ):

        frame_foto = ctk.CTkFrame(
            parent,
            width=280,
        )

        frame_foto.pack(
            side="right",
            fill="y",
            padx=10,
        )

        titulo = ctk.CTkLabel(
            frame_foto,
            text="Foto do Colaborador",
            font=("Arial", 18, "bold"),
        )

        titulo.pack(pady=(20, 15))

        preview = ctk.CTkLabel(
            frame_foto,
            text="Sem foto",
            width=220,
            height=260,
            corner_radius=8,
        )

        preview.pack(pady=10)

        if modo == "novo":
            self.preview_nova = preview

        else:
            self.preview_edicao = preview

        # ==================================================
        # TIRAR FOTO
        # ==================================================

        botao_camera = ctk.CTkButton(
            frame_foto,
            width=220,
            text="Tirar Foto",
            command=lambda: self.abrir_camera(modo),
        )

        botao_camera.pack(pady=5)

        # ==================================================
        # UPLOAD
        # ==================================================

        botao_upload = ctk.CTkButton(
            frame_foto,
            width=220,
            text="Selecionar Foto",
            command=lambda: self.selecionar_foto(modo),
        )

        botao_upload.pack(pady=5)

        # ==================================================
        # DOWNLOAD
        # ==================================================

        botao_download = ctk.CTkButton(
            frame_foto,
            width=220,
            text="Baixar Foto",
            command=lambda: self.baixar_foto(modo),
        )

        botao_download.pack(pady=5)

    # ==================================================
    # UPLOAD DA FOTO
    # ==================================================

    def selecionar_foto(self, modo):

        caminho = filedialog.askopenfilename(
            title="Selecionar Foto",
            filetypes=[
                (
                    "Imagens",
                    "*.jpg *.jpeg *.png *.bmp",
                ),
                (
                    "Todos os arquivos",
                    "*.*",
                ),
            ],
        )

        if not caminho:
            return

        try:
            if modo == "novo":
                self.foto_nova = caminho

                widget = self.preview_nova

            else:
                self.foto_edicao = caminho

                widget = self.preview_edicao

            self.carregar_preview(
                widget,
                caminho,
            )

        except Exception as erro:
            print(f"Erro ao selecionar foto: {erro}")

    # ==================================================
    # PREVIEW DA FOTO
    # ==================================================

    def carregar_preview(
        self,
        widget,
        caminho,
    ):

        if not caminho or not os.path.exists(caminho):
            widget.configure(
                image=None,
                text="Sem foto",
            )

            widget.image = None

            return

        try:
            imagem = Image.open(caminho)

            imagem.thumbnail((220, 260))

            foto = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size,
            )

            widget.configure(
                image=foto,
                text="",
            )

            widget.image = foto

        except Exception as erro:
            print(f"Erro ao carregar foto: {erro}")

            widget.configure(
                image=None,
                text="Erro ao carregar foto",
            )

    # ==================================================
    # CÂMERA
    # ==================================================

    def abrir_camera(self, modo):

        if self.janela_camera is not None:
            try:
                if self.janela_camera.winfo_exists():
                    self.janela_camera.lift()

                    self.janela_camera.focus_force()

                    return

            except tk.TclError:
                pass

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.camera.release()

            self.camera = None

            mensagem = "Não foi possível acessar a câmera."

            if modo == "novo":
                self.mensagem_novo.configure(text=mensagem)

            else:
                self.mensagem_editar.configure(text=mensagem)

            return

        self.janela_camera = ctk.CTkToplevel(self.window)

        self.janela_camera.title("Capturar Foto")

        self.janela_camera.geometry("700x600")

        self.janela_camera.resizable(
            False,
            False,
        )

        self.janela_camera.transient(self.window)

        self.janela_camera.grab_set()

        self.preview_camera = ctk.CTkLabel(
            self.janela_camera,
            text="Inicializando câmera...",
            width=620,
            height=450,
        )

        self.preview_camera.pack(pady=(20, 10))

        frame_botoes = ctk.CTkFrame(
            self.janela_camera,
            fg_color="transparent",
        )

        frame_botoes.pack(pady=10)

        botao_tirar = ctk.CTkButton(
            frame_botoes,
            text="Tirar Foto",
            width=180,
            command=lambda: self.tirar_foto(modo),
        )

        botao_tirar.pack(
            side="left",
            padx=5,
        )

        botao_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            width=180,
            command=self.fechar_camera,
        )

        botao_cancelar.pack(
            side="left",
            padx=5,
        )

        self.janela_camera.protocol(
            "WM_DELETE_WINDOW",
            self.fechar_camera,
        )

        self.atualizar_camera()

    # ==================================================
    # ATUALIZAR CÂMERA
    # ==================================================

    def atualizar_camera(self):

        if self.janela_camera is None or not self.janela_camera.winfo_exists():
            self.fechar_camera()

            return

        if self.camera is None:
            return

        sucesso, frame = self.camera.read()

        if sucesso:
            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB,
            )

            imagem = Image.fromarray(frame)

            imagem.thumbnail((620, 450))

            foto = ctk.CTkImage(
                light_image=imagem,
                dark_image=imagem,
                size=imagem.size,
            )

            self.preview_camera.configure(
                image=foto,
                text="",
            )

            self.preview_camera.image = foto

        self.janela_camera.after(
            30,
            self.atualizar_camera,
        )

    # ==================================================
    # TIRAR FOTO
    # ==================================================

    def tirar_foto(self, modo):

        if self.camera is None:
            return

        sucesso, frame = self.camera.read()

        if not sucesso:
            print("Não foi possível capturar a foto.")

            return

        pasta_fotos = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fotos",
        )

        os.makedirs(
            pasta_fotos,
            exist_ok=True,
        )

        if modo == "novo":
            nome_arquivo = f"foto_nova_{id(self)}.jpg"

        else:
            nome_arquivo = f"foto_edicao_{id(self)}.jpg"

        caminho = os.path.join(
            pasta_fotos,
            nome_arquivo,
        )

        sucesso = cv2.imwrite(
            caminho,
            frame,
        )

        if not sucesso:
            print("Erro ao salvar a foto capturada.")

            return

        if modo == "novo":
            self.foto_nova = caminho

            self.carregar_preview(
                self.preview_nova,
                caminho,
            )

        else:
            self.foto_edicao = caminho

            self.carregar_preview(
                self.preview_edicao,
                caminho,
            )

        self.fechar_camera()

    # ==================================================
    # FECHAR CÂMERA
    # ==================================================

    def fechar_camera(self):

        if self.camera is not None:
            try:
                self.camera.release()

            except Exception:
                pass

            self.camera = None

        if self.janela_camera is not None:
            try:
                if self.janela_camera.winfo_exists():
                    self.janela_camera.grab_release()

                    self.janela_camera.destroy()

            except tk.TclError:
                pass

        self.janela_camera = None

        self.preview_camera = None

    # ==================================================
    # SALVAR NOVO
    # ==================================================

    def salvar_novo_colaborador(self):

        nome = self.nome_entry.get()

        matricula = self.matricula_entry.get()

        cargo = self.cargo_entry.get()

        setor = self.setor_entry.get()

        status = self.status_combo.get()

        try:
            colaborador_id = self.service.criar(
                nome=nome,
                matricula=matricula,
                cargo=cargo,
                setor=setor,
                status=status,
                foto=self.foto_nova,
            )

            print(f"Colaborador criado com sucesso. ID: {colaborador_id}")

            self.janela_novo.destroy()

            self.foto_nova = None

            self.carregar_colaboradores()

        except ValueError as erro:
            self.mensagem_novo.configure(text=str(erro))

    # ==================================================
    # EDITAR COLABORADOR
    # ==================================================

    def editar_colaborador(self):

        if not self.colaborador_selecionado:
            print("Nenhum colaborador selecionado.")

            return

        colaborador = self.service.buscar_por_id(self.colaborador_selecionado)

        if not colaborador:
            print("Colaborador não encontrado.")

            return

        self.foto_edicao = None

        self.janela_editar = ctk.CTkToplevel(self.window)

        self.janela_editar.title("Editar Colaborador")

        self.janela_editar.geometry("850x650")

        self.janela_editar.resizable(
            False,
            False,
        )

        self.janela_editar.transient(self.window)

        self.janela_editar.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_editar,
            text="Editar Colaborador",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(pady=(25, 20))

        frame_conteudo = ctk.CTkFrame(
            self.janela_editar,
            fg_color="transparent",
        )

        frame_conteudo.pack(
            fill="both",
            expand=True,
            padx=30,
        )

        frame_formulario = ctk.CTkFrame(
            frame_conteudo,
            fg_color="transparent",
        )

        frame_formulario.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 20),
        )

        self.nome_editar_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
        )

        self.nome_editar_entry.pack(pady=10)

        self.nome_editar_entry.insert(
            0,
            colaborador["nome"],
        )

        self.matricula_editar_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
        )

        self.matricula_editar_entry.pack(pady=10)

        self.matricula_editar_entry.insert(
            0,
            colaborador["matricula"],
        )

        self.cargo_editar_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
        )

        self.cargo_editar_entry.pack(pady=10)

        self.cargo_editar_entry.insert(
            0,
            colaborador["cargo"],
        )

        self.setor_editar_entry = ctk.CTkEntry(
            frame_formulario,
            width=350,
            height=40,
        )

        self.setor_editar_entry.pack(pady=10)

        self.setor_editar_entry.insert(
            0,
            colaborador["setor"] or "",
        )

        self.status_editar_combo = ctk.CTkComboBox(
            frame_formulario,
            width=350,
            height=40,
            values=[
                "Ativo",
                "Inativo",
            ],
        )

        self.status_editar_combo.pack(pady=10)

        self.status_editar_combo.set(colaborador["status"])

        self.criar_area_foto(
            frame_conteudo,
            "edicao",
        )

        if colaborador["foto"]:
            self.carregar_preview(
                self.preview_edicao,
                colaborador["foto"],
            )

        self.mensagem_editar = ctk.CTkLabel(
            self.janela_editar,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_editar.pack(pady=5)

        self.botao_salvar_edicao = ctk.CTkButton(
            self.janela_editar,
            width=350,
            height=40,
            text="SALVAR ALTERAÇÕES",
            command=self.salvar_edicao_colaborador,
        )

        self.botao_salvar_edicao.pack(pady=(5, 20))

        self.nome_editar_entry.focus()

    # ==================================================
    # SALVAR EDIÇÃO
    # ==================================================

    def salvar_edicao_colaborador(self):

        nome = self.nome_editar_entry.get()

        matricula = self.matricula_editar_entry.get()

        cargo = self.cargo_editar_entry.get()

        setor = self.setor_editar_entry.get()

        status = self.status_editar_combo.get()

        try:
            self.service.atualizar(
                colaborador_id=self.colaborador_selecionado,
                nome=nome,
                matricula=matricula,
                cargo=cargo,
                setor=setor,
                status=status,
                foto=self.foto_edicao,
            )

            print(
                f"Colaborador ID {self.colaborador_selecionado} atualizado com sucesso."
            )

            self.janela_editar.destroy()

            self.foto_edicao = None

            self.carregar_colaboradores()

        except ValueError as erro:
            self.mensagem_editar.configure(text=str(erro))

    # ==================================================
    # EXCLUIR
    # ==================================================

    def excluir_colaborador(self):

        if not self.colaborador_selecionado:
            print("Nenhum colaborador selecionado.")

            return

        colaborador = self.service.buscar_por_id(self.colaborador_selecionado)

        if not colaborador:
            print("Colaborador não encontrado.")

            return

        self.janela_autorizacao = ctk.CTkToplevel(self.window)

        self.janela_autorizacao.title("Autorizar exclusão")

        self.janela_autorizacao.geometry("500x350")

        self.janela_autorizacao.resizable(
            False,
            False,
        )

        self.janela_autorizacao.transient(self.window)

        self.janela_autorizacao.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_autorizacao,
            text="Autorizar Exclusão",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(pady=(30, 20))

        informacao = ctk.CTkLabel(
            self.janela_autorizacao,
            text=(
                "Colaborador selecionado:\n"
                f"{colaborador['nome']}\n\n"
                "Esta operação não poderá "
                "ser desfeita."
            ),
            font=("Arial", 14),
            justify="center",
        )

        informacao.pack(pady=(0, 20))

        self.senha_autorizacao_entry = ctk.CTkEntry(
            self.janela_autorizacao,
            width=350,
            height=40,
            placeholder_text=("Digite sua senha para autorizar"),
            show="*",
        )

        self.senha_autorizacao_entry.pack(pady=10)

        self.mensagem_autorizacao = ctk.CTkLabel(
            self.janela_autorizacao,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_autorizacao.pack(pady=5)

        frame_botoes = ctk.CTkFrame(
            self.janela_autorizacao,
            fg_color="transparent",
        )

        frame_botoes.pack(pady=15)

        botao_cancelar = ctk.CTkButton(
            frame_botoes,
            text="CANCELAR",
            width=150,
            command=self.fechar_autorizacao,
        )

        botao_cancelar.pack(
            side="left",
            padx=5,
        )

        botao_confirmar = ctk.CTkButton(
            frame_botoes,
            text="CONFIRMAR",
            width=150,
            command=self.confirmar_exclusao,
        )

        botao_confirmar.pack(
            side="left",
            padx=5,
        )

        self.senha_autorizacao_entry.focus()

    # ==================================================
    # FECHAR AUTORIZAÇÃO
    # ==================================================

    def fechar_autorizacao(self):

        try:
            if self.janela_autorizacao.winfo_exists():
                self.janela_autorizacao.grab_release()

                self.janela_autorizacao.destroy()

        except tk.TclError:
            pass

    # ==================================================
    # CONFIRMAR EXCLUSÃO
    # ==================================================

    def confirmar_exclusao(self):

        senha = self.senha_autorizacao_entry.get()

        if not senha:
            self.mensagem_autorizacao.configure(text="Digite sua senha.")

            return

        try:
            self.service.excluir(
                colaborador_id=self.colaborador_selecionado,
                login_autorizador=self.usuario["login"],
                senha_autorizacao=senha,
            )

            print(
                f"Colaborador ID {self.colaborador_selecionado} excluído com sucesso."
            )

            self.colaborador_selecionado = None

            self.fechar_autorizacao()

            self.carregar_colaboradores()

        except ValueError as erro:
            self.mensagem_autorizacao.configure(text=str(erro))

    # ==================================================
    # BAIXAR FOTO
    # ==================================================

    def baixar_foto(self, modo):

        if modo == "novo":
            caminho = self.foto_nova

        else:
            if not self.colaborador_selecionado:
                return

            if self.foto_edicao:
                caminho = self.foto_edicao

            else:
                colaborador = self.service.buscar_por_id(self.colaborador_selecionado)

                if not colaborador:
                    return

                caminho = colaborador["foto"]

        if not caminho or not os.path.exists(caminho):
            mensagem = "Nenhuma foto disponível."

            if modo == "novo":
                self.mensagem_novo.configure(text=mensagem)

            else:
                self.mensagem_editar.configure(text=mensagem)

            return

        destino = filedialog.asksaveasfilename(
            title="Salvar Foto",
            defaultextension=".jpg",
            filetypes=[
                (
                    "Imagem JPEG",
                    "*.jpg",
                ),
                (
                    "Imagem PNG",
                    "*.png",
                ),
                (
                    "Todos os arquivos",
                    "*.*",
                ),
            ],
        )

        if not destino:
            return

        try:
            shutil.copy2(
                caminho,
                destino,
            )

            mensagem = "Foto salva com sucesso."

            if modo == "novo":
                self.mensagem_novo.configure(text=mensagem)

            else:
                self.mensagem_editar.configure(text=mensagem)

        except Exception as erro:
            mensagem = f"Erro ao salvar foto: {erro}"

            if modo == "novo":
                self.mensagem_novo.configure(text=mensagem)

            else:
                self.mensagem_editar.configure(text=mensagem)

    # ==================================================
    # FECHAR
    # ==================================================

    def fechar(self):

        self.fechar_camera()

        try:
            if self.window.winfo_exists():
                self.window.grab_release()

                self.window.destroy()

        except tk.TclError:
            pass

        try:
            if self.master.winfo_exists():
                self.master.deiconify()

        except tk.TclError:
            pass

    # ==================================================
    # EXECUÇÃO
    # ==================================================

    def run(self):

        self.window.deiconify()


if __name__ == "__main__":
    usuario_teste = {
        "id": 1,
        "nome": "Administrador do Sistema",
        "login": "admin",
        "perfil": "Administrador",
        "status": "Ativo",
    }

    root = ctk.CTk()

    root.withdraw()

    app = ColaboradorView(
        master=root,
        usuario=usuario_teste,
    )

    app.run()

    root.mainloop()
