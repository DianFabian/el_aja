import flet as ft
from firebase_init import db

def RegisterPage(page: ft.Page):
    page.title = "Registro de usuario - EL AJA"

    nombre = ft.TextField(label="Nombre completo", width=300)
    correo = ft.TextField(label="Correo institucional", width=300)
    contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("", color=ft.colors.RED_600)
    boton_registro = ft.ElevatedButton("Registrarme", disabled=True)

    # 🔹 Habilitar botón si todos los campos tienen texto
    def validar_campos(e):
        boton_registro.disabled = not (
            nombre.value and correo.value and contraseña.value and confirmar.value
        )
        page.update()

    for campo in [nombre, correo, contraseña, confirmar]:
        campo.on_change = validar_campos

    # 🔹 Función para registrar usuario
    def registrar(e):
        mensaje.color = ft.colors.RED_600

        # Validaciones
        if not correo.value.endswith("@utsjr.edu.mx"):
            mensaje.value = "❌ Solo se permiten correos institucionales (@utsjr.edu.mx)."
        elif contraseña.value != confirmar.value:
            mensaje.value = "❌ Las contraseñas no coinciden."
        else:
            # Verificar si el correo ya está en uso
            usuarios = db.collection("usuarios").where("correo", "==", correo.value).stream()
            if any(u for u in usuarios):
                mensaje.value = "⚠️ Este correo ya está registrado."
            else:
                nuevo_usuario = {
                    "nombre": nombre.value,
                    "correo": correo.value,
                    "contraseña": contraseña.value,  # Se recomienda encriptar luego
                }
                db.collection("usuarios").add(nuevo_usuario)
                mensaje.value = "✅ Registro exitoso. Ya puedes iniciar sesión."
                mensaje.color = ft.colors.GREEN_600

                # Limpiar campos
                nombre.value = ""
                correo.value = ""
                contraseña.value = ""
                confirmar.value = ""
                boton_registro.disabled = True

        page.update()

    boton_registro.on_click = registrar

    return ft.View(
        "/register",
        [
            ft.AppBar(title=ft.Text("Registro de usuario"), bgcolor=ft.colors.BLUE_300),
            ft.Column(
                [
                    ft.Text("Crear cuenta EL AJA", size=24, weight="bold"),
                    nombre,
                    correo,
                    contraseña,
                    confirmar,
                    boton_registro,
                    ft.TextButton("Volver al login", on_click=lambda e: page.go("/")),
                    mensaje,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
