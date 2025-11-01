from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle
from functools import partial
import sqlite3
import os

# Ajustar tamaño de ventana solo si se ejecuta en PC
if platform in ('linux', 'win', 'macosx'):
    Window.size = (800, 600)

# -------------------------
# Código Kivy Language (KV) - Diseño Reestructurado
# -------------------------
KV_CODE = """
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

# --- Menú Principal ---
<MenuPrincipalScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(30)
        canvas.before:
            Color:
                rgba: 0.9, 0.95, 1, 1 # Fondo Azul Claro
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'ADMINISTRACIÓN DE GESTIÓN' # Título Mejorado
            font_size: '32sp'
            size_hint_y: None
            height: dp(80)
            bold: True
            color: 0.1, 0.5, 0.8, 1 # Color del título

        Widget:
            size_hint_y: None
            height: dp(20)

        Button:
            text: 'Gestión de Stock'
            font_size: '22sp'
            size_hint_y: None
            height: dp(70)
            background_color: 0.1, 0.5, 0.8, 1 # Botón Azul Principal
            on_press: app.root.current = 'stock'

        Button:
            text: 'Registro de Ventas'
            font_size: '22sp'
            size_hint_y: None
            height: dp(70)
            background_color: 0.1, 0.5, 0.8, 1 # Botón Azul Principal
            on_press: app.root.current = 'ventas'

        Widget:

# --- Gestión de Stock ---
<GestionStockScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(25)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0.9, 0.95, 1, 1 # Fondo Azul Claro
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'MOVIMIENTO DE STOCK'
            font_size: '28sp'
            size_hint_y: None
            height: dp(50)
            bold: True
            color: 0.1, 0.5, 0.8, 1

        BoxLayout: # Agrupador de Inputs (como una tarjeta)
            orientation: 'vertical'
            size_hint_y: None
            height: dp(200)
            padding: dp(15)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1 # Fondo Blanco para Inputs
                Rectangle:
                    pos: self.pos
                    size: self.size

            TextInput:
                id: nombre_input
                hint_text: 'Nombre del producto'
                multiline: False
                height: dp(40)
                font_size: '18sp'

            TextInput:
                id: cantidad_input
                hint_text: 'Cantidad'
                multiline: False
                input_filter: 'int'
                height: dp(40)
                font_size: '18sp'

            TextInput:
                id: precio_input
                hint_text: 'Precio unitario'
                multiline: False
                input_filter: 'float'
                height: dp(40)
                font_size: '18sp'

        BoxLayout:
            size_hint_y: None
            height: dp(65)
            spacing: dp(15)
            padding: [0, dp(5), 0, 0]

            Button:
                text: 'ENTRADA (+)'
                font_size: '18sp'
                background_color: 0.2, 0.7, 0.2, 1 # Verde para Entrada
                on_press: root.entrada_stock(self)

            Button:
                text: 'SALIDA (-)'
                font_size: '18sp'
                background_color: 0.9, 0.3, 0.2, 1 # Rojo para Salida
                on_press: root.salida_stock(self)

        Widget:

        Button:
            text: 'Volver al Menú Principal'
            font_size: '18sp'
            size_hint_y: None
            height: dp(60)
            background_color: 0.5, 0.5, 0.5, 1
            on_press: app.root.current = 'menu'

# --- Registro de Ventas ---
<RegistroVentasScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(25)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0.9, 0.95, 1, 1 # Fondo Azul Claro
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'STOCK ACTUAL Y VENTA RÁPIDA'
            font_size: '28sp'
            size_hint_y: None
            height: dp(50)
            bold: True
            color: 0.1, 0.5, 0.8, 1

        # --- Encabezado de la Tabla (Mejora Visual Clave) ---
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            padding: [dp(10), 0]
            canvas.before:
                Color:
                    rgba: 0.1, 0.5, 0.8, 0.9 # Azul para el encabezado
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: 'Producto'
                color: 1, 1, 1, 1
                size_hint_x: 0.35
            Label:
                text: 'Stock'
                color: 1, 1, 1, 1
                size_hint_x: 0.2
            Label:
                text: 'Precio'
                color: 1, 1, 1, 1
                size_hint_x: 0.2
            Label:
                text: 'Cant.'
                size_hint_x: 0.15
                color: 1, 1, 1, 1
            Label:
                text: 'Acción'
                size_hint_x: 0.1

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            GridLayout:
                id: grid
                cols: 1
                spacing: dp(1) # Espacio reducido entre filas
                size_hint_y: None
                height: self.minimum_height

        BoxLayout:
            size_hint_y: None
            height: dp(65)
            spacing: dp(15)
            padding: [0, dp(5), 0, 0]

            Button:
                text: 'ACTUALIZAR LISTA'
                font_size: '18sp'
                background_color: 0.6, 0.6, 0.6, 1
                on_press: root.cargar_datos_productos()

            Button:
                text: 'Volver al Menú Principal'
                font_size: '18sp'
                background_color: 0.5, 0.5, 0.5, 1
                on_press: app.root.current = 'menu'
"""


# -------------------------
# Pantalla de menú principal
# -------------------------
class MenuPrincipalScreen(Screen):
    pass


# -------------------------
# Pantalla de gestión de stock
# -------------------------
class GestionStockScreen(Screen):

    def entrada_stock(self, instance):
        nombre_input = self.ids.nombre_input
        cantidad_input = self.ids.cantidad_input
        precio_input = self.ids.precio_input
        self.movimiento_stock('ENTRADA', nombre_input, cantidad_input, precio_input)

    def salida_stock(self, instance):
        nombre_input = self.ids.nombre_input
        cantidad_input = self.ids.cantidad_input
        precio_input = self.ids.precio_input
        self.movimiento_stock('SALIDA', nombre_input, cantidad_input, precio_input)

    def movimiento_stock(self, tipo, nombre_input, cantidad_input, precio_input):
        nombre = nombre_input.text.strip()
        cantidad = cantidad_input.text.strip()
        precio = precio_input.text.strip()

        if not nombre or not cantidad or not precio:
            print("⚠️ Campos incompletos.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            print("⚠️ Cantidad o precio inválido.")
            return

        app = App.get_running_app()
        ok = app.procesar_movimiento_stock(nombre, cantidad, precio, tipo)
        if ok:
            print(f"✅ Movimiento de {tipo.lower()} registrado correctamente.")
        else:
            print("❌ Error: no se pudo procesar el movimiento (stock insuficiente o error de DB).")

        nombre_input.text = ''
        cantidad_input.text = ''
        precio_input.text = ''


# -------------------------
# Pantalla de registro de ventas
# -------------------------
class RegistroVentasScreen(Screen):

    def on_pre_enter(self, *args):
        self.cargar_datos_productos()

    def cargar_datos_productos(self):
        grid = self.ids.grid
        grid.clear_widgets()
        app = App.get_running_app()
        productos = app.obtener_productos()

        grid.bind(minimum_height=grid.setter('height'))

        for p in productos:
            id_prod, nombre, stock, precio = p
            self.agregar_fila_producto(nombre, stock, precio, id_prod)

    def agregar_fila_producto(self, nombre, stock, precio, id_producto):
        
        # Fila de producto (más estética)
        fila = BoxLayout(size_hint_y=None, height=dp(55), padding=[dp(10), dp(5)])

        # 1. Creamos el rectángulo de fondo usando Canvas
        with fila.canvas.before:
            Color(0.98, 0.98, 0.98, 1) 
            rect = Rectangle(pos=fila.pos, size=fila.size)
        
        # 2. Definimos una función de actualización local para el rectángulo (FIX del error anterior)
        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size

        # 3. Enlazamos la función al cambio de posición y tamaño (FIX del error anterior)
        fila.bind(pos=update_rect, size=update_rect)

        # Labels de datos (alineados con el encabezado)
        
        # 4. CORRECCIÓN: Nombre del producto (alineación y color)
        name_label = Label(text=nombre, 
                           size_hint_x=0.35, 
                           color=(0, 0, 0, 1), # Color negro explícito
                           halign='left', 
                           valign='middle')
        
        # Enlazamos el tamaño del texto al tamaño de la etiqueta para que la alineación funcione
        name_label.bind(size=lambda instance, value: instance.setter('text_size')(instance, value))
        
        fila.add_widget(name_label)

        # 5. CORRECCIÓN: Stock (alineación y color)
        fila.add_widget(Label(text=f"{stock}", size_hint_x=0.2, color=(0, 0, 0, 1), valign='middle'))
        
        # 6. CORRECCIÓN: Precio (alineación y color)
        fila.add_widget(Label(text=f"${precio:.2f}", size_hint_x=0.2, color=(0, 0, 0, 1), valign='middle'))

        # Input de Venta
        input_venta = TextInput(hint_text='Cant.', multiline=False, input_filter='int', size_hint_x=0.15, font_size='16sp')
        
        # Botón de Vender (color de venta)
        btn_vender = Button(text='Vender', size_hint_x=0.1, background_color=(0.9, 0.3, 0.2, 1), font_size='14sp')

        btn_vender.bind(on_press=partial(self.realizar_venta, id_producto, precio, input_venta))

        fila.add_widget(input_venta)
        fila.add_widget(btn_vender)

        grid = self.ids.grid
        grid.add_widget(fila)


    def realizar_venta(self, id_producto, precio, input_venta, *args):
        cantidad = input_venta.text.strip()
        if not cantidad:
            return
        try:
            cantidad = int(cantidad)
        except ValueError:
            print("⚠️ Cantidad inválida.")
            return
        app = App.get_running_app()
        ok = app.restar_stock(id_producto, cantidad)
        if ok:
            print(f"💰 Venta registrada ({cantidad} unidades, total ${precio * cantidad:.2f})")
            self.cargar_datos_productos()
        else:
            print("❌ No hay stock suficiente o error en la base de datos.")
        input_venta.text = ''


# -------------------------
# Clase principal de la App
# -------------------------
class GestionApp(App):

    def build(self):
        # 1. Cargar el código KV
        Builder.load_string(KV_CODE)

        # 2. Crear carpeta segura para la base de datos
        self.db_path = os.path.join(self.user_data_dir, 'inventario.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conectar_db()
        self.crear_tabla()

        # 3. Configurar el ScreenManager
        sm = ScreenManager()
        sm.add_widget(MenuPrincipalScreen(name='menu'))
        sm.add_widget(GestionStockScreen(name='stock'))
        sm.add_widget(RegistroVentasScreen(name='ventas'))
        return sm

    # --- Base de datos ---
    def conectar_db(self):
        self.conexion = sqlite3.connect(self.db_path)
        self.cursor = self.conexion.cursor()

    def crear_tabla(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            stock INTEGER,
            precio REAL
        )''')
        self.conexion.commit()

    def procesar_movimiento_stock(self, nombre, cantidad, precio, tipo_movimiento):
        """
        Inserta o actualiza producto según tipo_movimiento.
        """
        try:
            self.cursor.execute("SELECT stock FROM productos WHERE nombre = ?", (nombre,))
            row = self.cursor.fetchone()
            if row is None:
                if tipo_movimiento == 'SALIDA':
                    return False
                # Insertar nuevo producto
                self.cursor.execute("INSERT INTO productos (nombre, stock, precio) VALUES (?, ?, ?)",
                                    (nombre, cantidad, precio))
            else:
                stock_actual = row[0]
                nuevo_stock = stock_actual + (cantidad if tipo_movimiento == 'ENTRADA' else -abs(cantidad))
                if nuevo_stock < 0:
                    return False
                # Actualizar stock y precio
                self.cursor.execute("UPDATE productos SET stock = ?, precio = ? WHERE nombre = ?",
                                    (nuevo_stock, precio, nombre))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error SQL: {e}")
            self.conexion.rollback()
            return False

    def restar_stock(self, id_producto, cantidad):
        try:
            self.cursor.execute("SELECT stock FROM productos WHERE id = ?", (int(id_producto),))
            row = self.cursor.fetchone()
            if row is None:
                return False
            stock_actual = row[0]
            if stock_actual < cantidad:
                return False
            self.cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, int(id_producto)))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al restar stock: {e}")
            self.conexion.rollback()
            return False

    def obtener_productos(self):
        self.cursor.execute("SELECT id, nombre, stock, precio FROM productos ORDER BY nombre")
        return self.cursor.fetchall()

    def on_stop(self):
        try:
            self.conexion.close()
        except Exception:
            pass


# -------------------------
# Ejecutar la app
# -------------------------
if __name__ == '__main__':
    GestionApp().run()
