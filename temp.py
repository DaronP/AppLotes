import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_pagina_facturacion(parent, conn):
    """
    Página que combina:
    1. Selección o creación de Cliente.
    2. Selección o creación de Comisionista (opcional).
    3. Selección de Lote existente (desde la BD).
    4. Datos de plan de pago (plan anual, enganche, etc.), con cálculos automáticos.
    5. Inserción de todo en la tabla control_pagos.
    """
    frame = tk.Frame(parent)
    frame.place(relwidth=1, relheight=1)

    # --- 1) CLIENTE (nuevo o existente) ---

    tk.Label(frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_clientes = ttk.Combobox(frame, state='readonly')
    combo_clientes.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Cargar clientes
    clientes = obtener_clientes(conn)  # [(id_cliente, nombre), ...]
    lista_clientes = [f"{c[0]} - {c[1]}" for c in clientes]
    lista_clientes.append("<Nuevo Cliente>")
    combo_clientes['values'] = lista_clientes
    if lista_clientes:
        combo_clientes.current(0)

    btn_nuevo_cliente = tk.Button(
        frame, text="Registrar Nuevo Cliente",
        command=lambda: ventana_nuevo_cliente(parent, conn, combo_clientes)
    )
    btn_nuevo_cliente.grid(row=0, column=2, padx=5, pady=5)

    # --- 2) COMISIONISTA (nuevo o existente) ---
    tk.Label(frame, text="Comisionista:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_comisionistas = ttk.Combobox(frame, state='readonly')
    combo_comisionistas.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    comisionistas = obtener_comisionistas(conn)  # [(id_comisionista, nombre), ...]
    lista_comisionistas = [f"{c[0]} - {c[1]}" for c in comisionistas]
    lista_comisionistas.append("<Nuevo Comisionista>")
    combo_comisionistas['values'] = lista_comisionistas
    if lista_comisionistas:
        combo_comisionistas.current(0)

    btn_nuevo_comisionista = tk.Button(
        frame, text="Registrar Nuevo Comisionista",
        command=lambda: ventana_nuevo_comisionista(parent, conn, combo_comisionistas)
    )
    btn_nuevo_comisionista.grid(row=1, column=2, padx=5, pady=5)

    # --- 3) LOTE (solo existente en este ejemplo) ---
    tk.Label(frame, text="Lote:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    combo_lotes = ttk.Combobox(frame, state='readonly')
    combo_lotes.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    lotes = obtener_lotes(conn)  # [(lote_id, valor, sector, ...), ...]
    lista_lotes = [f"{l[0]}" for l in lotes]  # supondremos que l[0] es lote_id
    combo_lotes['values'] = lista_lotes
    if lista_lotes:
        combo_lotes.current(0)

    # --- 4) Datos del plan de pagos (enganche, plan anual, etc.) y Cálculos automáticos ---
    tk.Label(frame, text="Enganche Pagado (S/N):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_enganche_pagado = tk.Entry(frame)
    entry_enganche_pagado.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Plan Anual (años):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_plan_anual = tk.Entry(frame)
    entry_plan_anual.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Monto Recibido (Primer Pago):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    entry_monto_recibido = tk.Entry(frame)
    entry_monto_recibido.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Fecha Compra (YYYY-MM-DD):").grid(row=6, column=0, padx=5, pady=5, sticky="e")
    entry_fecha_compra = tk.Entry(frame)
    entry_fecha_compra.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    # Labels para mostrar info derivada
    tk.Label(frame, text="Valor Base Lote:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
    lbl_valor_lote = tk.Label(frame, text="N/A")
    lbl_valor_lote.grid(row=7, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Valor Total con Intereses:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
    lbl_valor_total = tk.Label(frame, text="N/A")
    lbl_valor_total.grid(row=8, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Pago Mensual:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
    lbl_pago_mensual = tk.Label(frame, text="N/A")
    lbl_pago_mensual.grid(row=9, column=1, padx=5, pady=5, sticky="w")

    # Botón para Calcular
    btn_calcular = tk.Button(
        frame,
        text="Calcular",
        command=lambda: calcular_campos(conn, combo_lotes.get(), entry_enganche_pagado.get(), 
                                        entry_plan_anual.get(), lbl_valor_lote, lbl_valor_total,
                                        lbl_pago_mensual)
    )
    btn_calcular.grid(row=10, column=0, columnspan=2, pady=10)

    # Botón final para Guardar en control_pagos
    btn_guardar = tk.Button(
        frame,
        text="Guardar en control_pagos",
        command=lambda: guardar_control_pagos(
            conn,
            combo_clientes.get(),
            combo_comisionistas.get(),
            combo_lotes.get(),
            lbl_valor_lote['text'],       # valor base (como string)
            lbl_valor_total['text'],      # valor total con intereses
            entry_enganche_pagado.get(),  # S/N
            entry_monto_recibido.get(),   # primer pago
            entry_fecha_compra.get(),     # fecha
            entry_plan_anual.get(),       # plan en años
            lbl_pago_mensual['text']      # calculado
        )
    )
    btn_guardar.grid(row=11, column=0, columnspan=2, pady=10)

    return frame

# -------------------------------------------------------------------
# LÓGICA DE "NUEVO CLIENTE"
# -------------------------------------------------------------------
def ventana_nuevo_cliente(parent, conn, combo_clientes):
    """
    Ventana Toplevel para registrar un nuevo cliente.
    Al guardar, se actualiza el Combobox principal si deseas.
    """
    top = tk.Toplevel(parent)
    top.title("Registrar Cliente")

    tk.Label(top, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = tk.Entry(top)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="DPI:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_dpi = tk.Entry(top)
    entry_dpi.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_direccion = tk.Entry(top)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    btn_guardar = tk.Button(
        top, text="Guardar",
        command=lambda: guardar_cliente_nuevo(conn, entry_nombre.get(), entry_dpi.get(), entry_direccion.get(), top, combo_clientes)
    )
    btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

def guardar_cliente_nuevo(conn, nombre, dpi, direccion, top, combo_clientes):
    if not nombre or not dpi:
        messagebox.showwarning("Campos Vacíos", "El nombre y DPI son obligatorios.")
        return

    query = "INSERT INTO clientes (nombre, dpi, direccion) VALUES (%s, %s, %s)"
    execute_non_query(conn, query, (nombre, dpi, direccion))
    messagebox.showinfo("Éxito", "Cliente registrado con éxito.")

    top.destroy()
    # Refrescar el combo_clientes si lo deseas:
    clientes = obtener_clientes(conn)
    lista = [f"{c[0]} - {c[1]}" for c in clientes]
    lista.append("<Nuevo Cliente>")
    combo_clientes['values'] = lista
    combo_clientes.current(len(lista)-1)  # Seleccionar al final (opcional)

# -------------------------------------------------------------------
# LÓGICA DE "NUEVO COMISIONISTA" (similares al de cliente)
# -------------------------------------------------------------------
def ventana_nuevo_comisionista(parent, conn, combo_comisionistas):
    top = tk.Toplevel(parent)
    top.title("Registrar Comisionista")

    tk.Label(top, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nombre = tk.Entry(top)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="DPI:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_dpi = tk.Entry(top)
    entry_dpi.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_direccion = tk.Entry(top)
    entry_direccion.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="Fecha Ingreso (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_fecha_ingreso = tk.Entry(top)
    entry_fecha_ingreso.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    btn_guardar = tk.Button(
        top, text="Guardar",
        command=lambda: guardar_comisionista_nuevo(conn, entry_nombre.get(), entry_dpi.get(), entry_direccion.get(), entry_fecha_ingreso.get(), top, combo_comisionistas)
    )
    btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

def guardar_comisionista_nuevo(conn, nombre, dpi, direccion, fecha_ingreso, top, combo_comisionistas):
    if not nombre or not dpi:
        messagebox.showwarning("Campos Vacíos", "El nombre y DPI son obligatorios.")
        return
    query = "INSERT INTO comisionistas (nombre, dpi, direccion, fecha_ingreso) VALUES (%s, %s, %s, %s)"
    execute_non_query(conn, query, (nombre, dpi, direccion, fecha_ingreso))
    messagebox.showinfo("Éxito", "Comisionista registrado con éxito.")
    top.destroy()

    # Refrescar combobox
    comisionistas = obtener_comisionistas(conn)
    lista = [f"{c[0]} - {c[1]}" for c in comisionistas]
    lista.append("<Nuevo Comisionista>")
    combo_comisionistas['values'] = lista
    combo_comisionistas.current(len(lista)-1)

# -------------------------------------------------------------------
# OBTENER DATOS DE BD
# -------------------------------------------------------------------
def obtener_clientes(conn):
    query = "SELECT id_cliente, nombre FROM clientes"
    return execute_query(conn, query)

def obtener_comisionistas(conn):
    query = "SELECT id_comisionista, nombre FROM comisionistas"
    return execute_query(conn, query)

def obtener_lotes(conn):
    query = "SELECT lote_id, valor, sector FROM lotes WHERE disponible = 'S'"
    return execute_query(conn, query)

# -------------------------------------------------------------------
# CALCULOS AUTOMÁTICOS
# -------------------------------------------------------------------
def calcular_campos(conn, lote_id_str, enganche_pagado, plan_anual_str, lbl_valor_lote, lbl_valor_total, lbl_pago_mensual):
    """
    1. Obtener el valor base del lote_id_str
    2. Calcular un factor de intereses
    3. Mostrar valor total y pago mensual, etc.
    """
    if not lote_id_str:
        messagebox.showwarning("Advertencia", "Seleccione un lote.")
        return

    # Convertir el lote a int si es necesario
    try:
        lote_id = int(lote_id_str)
    except:
        messagebox.showerror("Error", "No se pudo interpretar el Lote.")
        return

    # Obtener valor base del lote
    query = "SELECT valor FROM lotes WHERE lote_id = %s"
    res = execute_query(conn, query, (lote_id,))
    if not res:
        messagebox.showerror("Error", f"No se encontró Lote {lote_id}.")
        return
    valor_base = res[0]['valor'] if isinstance(res[0], dict) else res[0][0]

    # Convertir plan_anual a float o int
    try:
        plan_anual = float(plan_anual_str)
    except:
        messagebox.showerror("Error", "Plan Anual debe ser numérico.")
        return

    # EJEMPLO de factor de interés
    # Factor simple: 10% por cada 5 años
    factor = 1 + 0.10*(plan_anual/5.0)
    valor_total = valor_base * factor

    # Calcular un pago mensual aproximado
    # Mensualidades = plan_anual * 12
    mensualidades = plan_anual * 12
    pago_mensual = 0
    if mensualidades > 0:
        pago_mensual = valor_total / mensualidades

    # Actualizar los labels
    lbl_valor_lote.config(text=f"{valor_base:,.2f}")
    lbl_valor_total.config(text=f"{valor_total:,.2f}")
    lbl_pago_mensual.config(text=f"{pago_mensual:,.2f}")

    messagebox.showinfo("Cálculo Realizado", "Los valores se han actualizado en pantalla.")

# -------------------------------------------------------------------
# GUARDAR EN control_pagos
# -------------------------------------------------------------------
def guardar_control_pagos(
    conn,
    cliente_str,
    comisionista_str,
    lote_str,
    valor_lote_str,
    valor_total_str,
    enganche_pagado,
    monto_recibido_str,
    fecha_compra,
    plan_anual_str,
    pago_mensual_str
):
    """
    Inserta en la tabla control_pagos usando los datos elegidos y calculados.
    """
    # 1. Determinar id_cliente
    if cliente_str == "<Nuevo Cliente>":
        messagebox.showerror("Error", "Primero registre o seleccione un cliente.")
        return
    try:
        id_cliente = int(cliente_str.split("-")[0].strip())
    except:
        messagebox.showerror("Error", "No se pudo obtener id_cliente.")
        return

    # 2. Determinar id_comisionista
    if comisionista_str == "<Nuevo Comisionista>":
        messagebox.showerror("Error", "Primero registre o seleccione un comisionista.")
        return
    try:
        id_comisionista = int(comisionista_str.split("-")[0].strip())
    except:
        messagebox.showerror("Error", "No se pudo obtener id_comisionista.")
        return

    # 3. Determinar id_lote
    try:
        id_lote = int(lote_str)
    except:
        messagebox.showerror("Error", "No se pudo obtener id_lote.")
        return

    # Convertir numéricos
    try:
        monto_recibido = float(monto_recibido_str)
    except:
        monto_recibido = 0.0

    try:
        plan_anual = float(plan_anual_str)
    except:
        plan_anual = 0.0

    try:
        valor_lote = float(valor_lote_str.replace(",", ""))  # Por si tiene comas
    except:
        valor_lote = 0.0

    try:
        valor_total = float(valor_total_str.replace(",", ""))
    except:
        valor_total = valor_lote

    try:
        pago_mensual = float(pago_mensual_str.replace(",", ""))
    except:
        pago_mensual = 0.0

    # Como ejemplo, asumimos un saldo_inicial = valor_total - (un enganche real, si existiese).
    # Aquí lo simplificamos si no lo manejas por separado
    saldo_inicial = valor_total  

    query = """
    INSERT INTO control_pagos (
        id_cliente,
        id_comisionista,
        id_lote,
        saldo_inicial,
        monto_recibido,
        fecha_compra,
        plan_anual,
        enganche_pagado,
        pago_mensual,
        saldo_actual,
        mensualidad_lleva,
        fecha_ultimo_pago,
        valor_total,
        num_recibo_fisico
    ) VALUES (
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, 0, NULL,
        %s, NULL
    )
    """
    params = (
        id_cliente,
        id_comisionista,
        id_lote,
        saldo_inicial,
        monto_recibido,
        fecha_compra,
        plan_anual,
        enganche_pagado,
        pago_mensual,
        saldo_inicial,  # saldo_actual lo inicializamos igual a saldo_inicial
        valor_total
    )

    execute_non_query(conn, query, params)
    messagebox.showinfo("Guardado", "Datos guardados en control_pagos satisfactoriamente.")

# -------------------------------------------------------------------
# FUNCIONES GENERALES DE CONSULTA
# -------------------------------------------------------------------
def execute_query(conn, query, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()

def execute_non_query(conn, query, params=None):
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
    conn.commit()
