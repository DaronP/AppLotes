import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import execute_query, execute_non_query
import datetime

def crear_ingreso_pago(parent, conn):
    """
    Página que combina:
    1. Selección o creación de Cliente.
    2. Selección o creación de Comisionista (opcional).
    3. Selección de Lote existente (desde la BD).
    4. Datos de plan de pago (plan anual, enganche, etc.), con cálculos automáticos.
    5. Inserción de todo en la tabla control_pagos.
    """
    frame = tk.Frame(parent, bg='#9A9898')
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Ingreso de pagos", font=('Arial', 18), bg='#9A9898').grid(row=0, column=0, padx=5, pady=5, sticky="e")

    style = ttk.Style()
    style.theme_use("clam")

    # --- 1) CLIENTE (nuevo o existente) ---

    tk.Label(frame, text="Cliente:", bg='#9A9898').grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_clientes = ttk.Combobox(frame, state='readonly')
    combo_clientes.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Cargar clientes
    clientes = obtener_clientes(conn)  # [(id_cliente, nombre), ...]
    lista_clientes = [f"{c[0]} - {c[1]}" for c in clientes]
    combo_clientes['values'] = lista_clientes

    btn_nuevo_cliente = tk.Button(
        frame, text="Registrar Nuevo Cliente",
        command=lambda: ventana_nuevo_cliente(parent, conn, combo_clientes)
    )
    btn_nuevo_cliente.grid(row=1, column=2, padx=5, pady=5)

    # --- 2) COMISIONISTA (nuevo o existente) ---
    tk.Label(frame, text="Comisionista:", bg='#9A9898').grid(row=2, column=0, padx=5, pady=5, sticky="e")
    combo_comisionistas = ttk.Combobox(frame, state='readonly')
    combo_comisionistas.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    comisionistas = obtener_comisionistas(conn)  # [(id_comisionista, nombre), ...]
    lista_comisionistas = [f"{c[0]}" for c in comisionistas]
    combo_comisionistas['values'] = lista_comisionistas

    # --- 3) LOTE (solo existente en este ejemplo) ---
    tk.Label(frame, text="Lote:", bg='#9A9898').grid(row=3, column=0, padx=5, pady=5, sticky="e")
    combo_lotes = ttk.Combobox(frame, state='readonly')
    combo_lotes.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    lotes = obtener_lotes(conn)  # [(lote_id, valor, sector, ...), ...]
    lista_lotes = [f"{l[0]}" for l in lotes]  # supondremos que l[0] es lote_id
    combo_lotes['values'] = lista_lotes

    # --- 4) Datos del plan de pagos (enganche, plan anual, etc.) y Cálculos automáticos ---
    tk.Label(frame, text="Enganche Pagado (Si/No):", bg='#9A9898').grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_enganche_pagado = ttk.Combobox(frame, state='readonly')
    entry_enganche_pagado.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    entry_enganche_pagado['values'] = ['No', 'Si']
    entry_enganche_pagado.current(0)

    tk.Label(frame, text="Tipo de pago:", bg='#9A9898').grid(row=5, column=0, padx=5, pady=5, sticky="e")
    entry_tipo_pago = ttk.Combobox(frame, state='readonly')
    entry_tipo_pago.grid(row=5, column=1, padx=5, pady=5, sticky="w")
    entry_tipo_pago['values'] = ['Efectivo', 'Cheque', 'Transferencia/Deposito']

    tk.Label(frame, text="Plan Anual (años):", bg='#9A9898').grid(row=6, column=0, padx=5, pady=5, sticky="e")
    entry_plan_anual = tk.Entry(frame)
    entry_plan_anual.grid(row=6, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="No. Recibo:", bg='#9A9898').grid(row=7, column=0, padx=5, pady=5, sticky="e")
    entry_recibo = tk.Entry(frame)
    entry_recibo.grid(row=7, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Monto Recibido:", bg='#9A9898').grid(row=8, column=0, padx=5, pady=5, sticky="e")
    entry_monto_recibido = tk.Entry(frame)
    entry_monto_recibido.grid(row=8, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Fecha Compra:", bg='#9A9898').grid(row=9, column=0, padx=5, pady=5, sticky="e")
    entry_fecha_compra = DateEntry(frame, date_pattern='yyyy-mm-dd')
    entry_fecha_compra.grid(row=9, column=1, padx=5, pady=5, sticky="w")

    # Labels para mostrar info derivada
    tk.Label(frame, text="Valor Base Lote:", bg='#9A9898').grid(row=10, column=0, padx=5, pady=5, sticky="e")
    lbl_valor_lote = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_valor_lote.grid(row=10, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Valor Total con Intereses (sin enganche):", bg='#9A9898').grid(row=11, column=0, padx=5, pady=5, sticky="e")
    lbl_valor_total = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_valor_total.grid(row=11, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Saldo actual:", bg='#9A9898').grid(row=12, column=0, padx=5, pady=5, sticky="e")
    lbl_saldo_actual = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_saldo_actual.grid(row=12, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="No. mensualidades pagadas", bg='#9A9898').grid(row=13, column=0, padx=5, pady=5, sticky="e")
    lbl_mensualidad_no = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_mensualidad_no.grid(row=13, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Mensualidades:", bg='#9A9898').grid(row=14, column=0, padx=5, pady=5, sticky="e")
    lbl_mensualidades = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_mensualidades.grid(row=14, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Pago Mensual:", bg='#9A9898').grid(row=15, column=0, padx=5, pady=5, sticky="e")
    lbl_pago_mensual = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_pago_mensual.grid(row=15, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Fecha ultimo pago:", bg='#9A9898').grid(row=16, column=0, padx=5, pady=5, sticky="e")
    lbl_ultima_fecha = tk.Label(frame, text="N/A", bg='#9A9898')
    lbl_ultima_fecha.grid(row=16, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Notas:", bg='#9A9898').grid(row=17, column=0, padx=5, pady=5, sticky="e")
    entry_notas = tk.Text(frame, width=50, height=3)
    entry_notas.grid(row=17, column=1, padx=5, pady=5, sticky="w")

    # Botón para Calcular
    btn_calcular = tk.Button(
        frame,
        text="Calcular",
        command=lambda: calcular_campos(conn, combo_clientes.get(), combo_lotes.get(), entry_plan_anual, 
                                        lbl_valor_lote, lbl_valor_total,
                                        lbl_pago_mensual, lbl_mensualidades, lbl_saldo_actual, lbl_mensualidad_no, lbl_ultima_fecha)
    )
    btn_calcular.grid(row=18, column=0, columnspan=2, pady=10)

    # Botón final para Guardar en control_pagos
    btn_guardar = tk.Button(
        frame,
        text="Guardar datos",
        command=lambda: guardar_control_pagos(parent,
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
            lbl_pago_mensual['text'],      # calculado
            entry_recibo.get(),
            lbl_saldo_actual['text'],
            lbl_mensualidad_no['text'],
            entry_tipo_pago.get(),
            entry_notas.get("1.0", "end-1c")
        )
    )
    btn_guardar.grid(row=19, column=0, columnspan=2, pady=10)

    btn_eliminar_registro = tk.Button(
        frame, text="Eliminar registro de cliente",
        command=lambda: ventana_eliminar_registro(parent, conn)
    )
    btn_eliminar_registro.grid(row=19, column=1, columnspan=2, pady=10)

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

def ventana_eliminar_registro(parent, conn):

    top = tk.Toplevel(parent)
    top.title("Eliminar registro")

    tk.Label(top, text="Ingrese DPI del cliente y numero de lote para eliminar el registro.").grid(row=0, column=0, padx=5, pady=5, sticky="e")

    tk.Label(top, text="DPI:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_dpi = tk.Entry(top)
    entry_dpi.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(top, text="Numero de lote:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_lote = tk.Entry(top)
    entry_lote.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    btn_guardar = tk.Button(
        top, text="Eliminar Registro",
        command=lambda: eliminar_registro(parent, conn, entry_dpi.get(), entry_lote.get(), top)
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

    # Refrescar el combo_clientes:
    clientes = obtener_clientes(conn)
    lista = [f"{c[0]} - {c[1]}" for c in clientes]
    combo_clientes['values'] = lista
    combo_clientes.current(len(lista)-1)  # Seleccionar al final (opcional)

def eliminar_registro(parent, conn, dpi, lote, top):
    if not lote or not dpi:
        messagebox.showwarning("Campos Vacíos", "El nombre y DPI son obligatorios.")
        return
    
    query = 'DELETE cp FROM control_pagos cp JOIN clientes c ON cp.cliente_id = c.cliente_id WHERE c.dpi = %s AND lote_id = %s;'

    execute_non_query(conn, query, (dpi, lote))
    execute_non_query(conn, 'UPDATE lotes SET disponible = %s WHERE lote_id = %s', (True, lote))
    messagebox.showinfo("Éxito", "eliminacion de registro con éxito.")

    top.destroy()
    crear_ingreso_pago(parent, conn)

# -------------------------------------------------------------------
# OBTENER DATOS DE BD
# -------------------------------------------------------------------
def obtener_clientes(conn):
    query = "SELECT dpi, nombre FROM clientes"
    return execute_query(conn, query)

def obtener_comisionistas(conn):
    query = "SELECT nombre FROM comisionistas"
    return execute_query(conn, query)

def obtener_lotes(conn):
    query = "SELECT lote_id, valor, sector FROM lotes"
    return execute_query(conn, query)

# -------------------------------------------------------------------
# CALCULOS AUTOMÁTICOS
# -------------------------------------------------------------------
def calcular_campos(conn, cliente_id_str, lote_id_str, plan_anual_str, lbl_valor_lote, lbl_valor_total, lbl_pago_mensual, lbl_mensualidades, lbl_saldo_actual, lbl_mensualidad_no, lbl_ultima_fecha):
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
    
    try:
        cliente_dpi = cliente_id_str.split(' - ')[0]
        cliente_dpi = int(cliente_dpi)
        id_cliente_res = execute_query(conn, 'SELECT cliente_id FROM clientes WHERE dpi = %s', (cliente_dpi))
        cliente_id = int(id_cliente_res[0]['valor'] if isinstance(id_cliente_res[0], dict) else id_cliente_res[0][0])
    except:
        messagebox.showerror("Error", "No se pudo interpretar el DPI del cliente.")
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
        plan_anual_res = execute_query(conn, 'SELECT plan_anual FROM control_pagos WHERE cliente_id = %s AND lote_id = %s ORDER BY saldo_actual DESC LIMIT 1', (cliente_id, lote_id))
        
        if plan_anual_res:
            plan_anual_res = plan_anual_res[0]['valor'] if isinstance(plan_anual_res[0], dict) else plan_anual_res[0][0]
            plan_anual = plan_anual_res
            plan_anual_str.delete(0, 'end')
            plan_anual_str.insert(0, plan_anual)
        else:
            plan_anual = float(plan_anual_str.get())
    except:
        messagebox.showerror("Error", "Plan Anual debe ser numérico.")
        return
    

    lote_disponible = execute_query(conn, 'SELECT disponible FROM lotes WHERE lote_id = %s', lote_id)
    lote_disponible = lote_disponible[0]['valor'] if isinstance(lote_disponible[0], dict) else lote_disponible[0][0]
    propietario_lote = execute_query(conn, 'SELECT propietario FROM lotes WHERE lote_id = %s', (lote_id))
    propietario_lote = propietario_lote[0]['valor'] if isinstance(propietario_lote[0], dict) else propietario_lote[0][0]

    if not lote_disponible and (propietario_lote != cliente_id):
        messagebox.showerror("Error", "Lote no disponible para su venta.")
        return

    '''
    --------------------------------------------------
    Correccion aca
    --------------------------------------------------
    '''

    # EJEMPLO de factor de interés
    # Factor simple: 10% por cada 5 años
    factor = 1 + 0.10*(plan_anual/5.0)
    valor_total = float(valor_base) * factor

    # Calcular un pago mensual aproximado
    # Mensualidades = plan_anual * 12
    mensualidades = plan_anual * 12
    pago_mensual = 0
    if mensualidades > 0:
        pago_mensual = valor_total / mensualidades

    '''
    --------------------------------------------------
    --------------------------------------------------
    '''
    
    saldo_actual_res = execute_query(conn, 'SELECT saldo_actual FROM control_pagos WHERE cliente_id = %s AND lote_id = %s ORDER BY saldo_actual DESC LIMIT 1', (cliente_id, lote_id))
    try:
        saldo_actual = saldo_actual_res[0]['valor'] if isinstance(saldo_actual_res[0], dict) else saldo_actual_res[0][0]
    except:
        saldo_actual = 0

    '''mensualidad_res = execute_query(conn, 'SELECT mensualidad FROM control_pagos WHERE cliente_id = %s AND lote_id = %s ORDER BY mensualidad DESC LIMIT 1', (cliente_id, lote_id))
    
    if not mensualidad_res or mensualidad_res == ():
        mensualidad = 0
    else:
        mensualidad = mensualidad_res[0]['valor'] if isinstance(mensualidad_res[0], dict) else mensualidad_res[0][0]
        mensualidad = int(mensualidad)'''
    
    mensualidad = int(round(float(saldo_actual)/float(pago_mensual)))
    if not mensualidad:
        mensualidad = 0

    
    fecha_ultimo_pago_res = execute_query(conn, 'SELECT fecha_compra FROM control_pagos WHERE cliente_id = %s AND lote_id = %s ORDER BY fecha_compra DESC LIMIT 1', (cliente_id, lote_id))
    if not fecha_ultimo_pago_res or fecha_ultimo_pago_res == ():
        fecha_ultimo_pago = None
    else:
        fecha_ultimo_pago = fecha_ultimo_pago_res[0]['valor'] if isinstance(fecha_ultimo_pago_res[0], dict) else fecha_ultimo_pago_res[0][0]
        fecha_ultimo_pago = fecha_ultimo_pago.strftime("%d/%m/%Y")

    # Actualizar los labels
    lbl_valor_lote.config(text=f"Q{valor_base:,.2f}")
    lbl_valor_total.config(text=f"Q{valor_total:,.2f}")
    lbl_pago_mensual.config(text=f"Q{pago_mensual:,.2f}")
    lbl_mensualidades.config(text=f"{int(mensualidades)} meses")
    lbl_mensualidad_no.config(text=f"{int(mensualidad)}")
    lbl_saldo_actual.config(text=f"Q{saldo_actual:,.2f}")
    lbl_ultima_fecha.config(text=f"{fecha_ultimo_pago}")

# -------------------------------------------------------------------
# GUARDAR EN control_pagos
# -------------------------------------------------------------------
def guardar_control_pagos(parent,
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
    pago_mensual_str,
    recibo,
    saldo_actual,
    mensualidad,
    tipo_pago,
    notas
):
    """
    Inserta en la tabla control_pagos usando los datos elegidos y calculados.
    """
    # 1. Determinar id_cliente
    if cliente_str == "<Nuevo Cliente>":
        messagebox.showerror("Error", "Primero registre o seleccione un cliente.")
        return
    try:
        dpi_cliente = int(cliente_str.split("-")[0].strip())
        id_cliente_res = execute_query(conn, 'SELECT cliente_id FROM clientes WHERE dpi = %s', (dpi_cliente))
        id_cliente = int(id_cliente_res[0]['valor'] if isinstance(id_cliente_res[0], dict) else id_cliente_res[0][0])
    except:
        messagebox.showerror("Error", "No se pudo obtener id_cliente.")
        return

    # 2. Determinar id_comisionista
    try:        
        id_comisionista_res = execute_query(conn, 'SELECT com_id FROM comisionistas WHERE nombre = %s', (comisionista_str))
        id_comisionista = int(id_comisionista_res[0]['valor'] if isinstance(id_comisionista_res[0], dict) else id_comisionista_res[0][0])
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
        recibo = int(recibo)
    except:
        messagebox.showerror("Error", "No se pudo obtener recibo.")
        return
    
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

    if enganche_pagado == 'Si':
        enganche_pagado = 1
    else: 
        enganche_pagado = 0

    fecha_ultimo_pago = list(execute_query(conn, 'SELECT fecha_compra FROM control_pagos WHERE cliente_id = %s AND lote_id = %s ORDER BY fecha_compra DESC LIMIT 1', (id_cliente, id_lote)))
    if not fecha_ultimo_pago:
        fecha_ultimo_pago = None


    saldo_actual = float(saldo_actual.replace('Q', '').replace(',', '')) + monto_recibido

    mensualidad = int(mensualidad) + 1

    lote_disponible = execute_query(conn, 'SELECT disponible FROM lotes WHERE lote_id = %s', id_lote)
    lote_disponible = lote_disponible[0]['valor'] if isinstance(lote_disponible[0], dict) else lote_disponible[0][0]
    propietario_lote = execute_query(conn, 'SELECT propietario FROM lotes WHERE lote_id = %s', (id_lote))
    propietario_lote = propietario_lote[0]['valor'] if isinstance(propietario_lote[0], dict) else propietario_lote[0][0]

    if not lote_disponible and (propietario_lote != id_cliente):
        messagebox.showerror("Error", "Lote no disponible para su venta.")
        return

    query = """
    INSERT INTO control_pagos (
        cliente_id,
        com_id,
        lote_id,
        saldo_inicial,
        monto_recibido,
        fecha_compra,
        plan_anual,
        enganche_pagado,
        pago_mensual,
        saldo_actual,
        mensualidad,
        fecha_ultimo_pago,
        valor_total,
        num_recibo_fisico,
        tipo_pago,
        notas
    ) VALUES (
        %s, 
        %s, 
        %s,
        %s, 
        %s, 
        %s,
        %s, 
        %s, 
        %s,
        %s, 
        %s, 
        %s,
        %s, 
        %s,
        %s,
        %s
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
        saldo_actual,
        mensualidad,
        fecha_ultimo_pago,
        valor_total,
        recibo,
        tipo_pago,
        notas
    )

    execute_non_query(conn, query, params)
    execute_non_query(conn, 'UPDATE lotes SET disponible = %s, propietario = %s WHERE lote_id = %s', (False, id_cliente, id_lote))
    messagebox.showinfo("Guardado", "Datos guardados satisfactoriamente.")
    # Volver a crear la página 1
    crear_ingreso_pago(parent, conn)


"""
def crear_ingreso_pago(parent, conn):
    # Crear el frame donde estarán los elementos de la página 1
    frame = tk.Frame(parent, bg='#9A9898')
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Ingreso de pagos", font=('Arial', 18), bg='#9A9898').place(relx=0.4, rely=0.03)

    style = ttk.Style()
    style.theme_use("clam")

    # Labels actualizables
    label0 = tk.Label(frame, text="Nombre: ", bg='#9A9898')
    label1 = tk.Label(frame, text="Saldo Inicial: ", bg='#9A9898')
    label2 = tk.Label(frame, text="Fecha de Compra: ", bg='#9A9898')
    label3 = tk.Label(frame, text="Mensualidad: ", bg='#9A9898')
    label4 = tk.Label(frame, text="Valor Total: ", bg='#9A9898')
    label5 = tk.Label(frame, text="Saldo Actual: ", bg='#9A9898')
    label6 = tk.Label(frame, text="Comisionista: ", bg='#9A9898')

    # Crear elementos de entrada (Drop-downs y selector de fecha)
    tk.Label(frame, text="DPI cliente", bg='#9A9898').place(relx=0.005, rely=0.15)
    option1 = ttk.Combobox(frame)
    option1.place(relx=0.095, rely=0.15, relwidth=0.2)

    tk.Label(frame, text="Lote", bg='#9A9898').place(relx=0.005, rely=0.2)
    option2 = ttk.Combobox(frame, state='readonly')
    option2.place(relx=0.095, rely=0.2, relwidth=0.2)

    

    cargar_datos_combobox(conn, option1, option2) 


    #Resto de ingresos

    tk.Label(frame, text="Monto", bg='#9A9898').place(relx=0.005, rely=0.55)
    text1 = ttk.Entry(frame)
    text1.place(relx=0.095, rely=0.55, relwidth=0.2)

    tk.Label(frame, text="Mensualidad", bg='#9A9898').place(relx=0.005, rely=0.6)
    text2 = ttk.Entry(frame)
    text2.place(relx=0.095, rely=0.6, relwidth=0.2)

    tk.Label(frame, text="No. Recibo", bg='#9A9898').place(relx=0.005, rely=0.65)
    text3 = ttk.Entry(frame)
    text3.place(relx=0.095, rely=0.65, relwidth=0.2)

    tk.Label(frame, text="Fecha", bg='#9A9898').place(relx=0.005, rely=0.7)
    date_selector = DateEntry(frame)
    date_selector.place(relx=0.095, rely=0.7, relwidth=0.2)

    #Verify button
    submit_button = tk.Button(frame, text="Verificar Información", 
                              command=lambda: verify(conn, parent, option1, option2, label0, label1, label2, label3, label4, label5, label6, frame))
    submit_button.place(relx=0.005, rely=0.3)

    # Botón para ingresar datos
    label7 = tk.Label(frame, text="", bg='#9A9898')
    submit_button = tk.Button(frame, text="Ingresar Datos", 
                              command=lambda: ingresar_datos(option1, option2, date_selector, label0, label1, label2, label3, label4, label5, label6, label7))
    submit_button.place(relx=0.005, rely=0.85)


    # Colocar los labels actualizables con posiciones relativas
    label0.place(relx=0.5, rely=0.1)
    label1.place(relx=0.5, rely=0.15)
    label2.place(relx=0.5, rely=0.2)
    label3.place(relx=0.5, rely=0.25)
    label4.place(relx=0.5, rely=0.3)
    label5.place(relx=0.5, rely=0.35)
    label6.place(relx=0.5, rely=0.4)
    label7.place(relx=0.1, rely=0.85)

    return frame

def cargar_datos_combobox(conn, option1, option2):
    # Consulta para obtener la información (ajusta según tu tabla y columna)
    resultados_cli = execute_query(conn, "SELECT dpi FROM clientes")
    resultados_lote = execute_query(conn, "SELECT lote_id FROM lotes")

    # Convertir los resultados en una lista de valores
    lista_clientes = []
    for fila in resultados_cli:
        if isinstance(fila, dict):
            lista_clientes.append(fila['nombre'])
        else:
            lista_clientes.append(fila[0])
    
    lista_lotes = []
    for fila in resultados_lote:
        if isinstance(fila, dict):
            lista_lotes.append(fila['lote'])
        else:
            lista_lotes.append(fila[0])

    # Asignar la lista resultante al Combobox
    option1['values'] = lista_clientes
    option2['values'] = lista_lotes


def verify(conn, parent, option1, option2, label0, label1, label2, label3, label4, label5, label6, frame):
    resultados_cli = execute_query(conn, "SELECT * FROM clientes WHERE dpi = %s", (option1.get()))
    if not resultados_cli:
        respuesta = messagebox.askyesno("Cliente no encontrado", "Datos del cliente ingresado no fueron encontrados. ¿Desea ingresar los nuevos datos?")
        if respuesta:
            ventana_datos = tk.Toplevel(parent)
            ventana_datos.title("Ingresar Datos Personales")

            tk.Label(ventana_datos, text="Nombre:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
            entry_nombre = tk.Entry(ventana_datos)
            entry_nombre.grid(row=0, column=1, sticky="w", padx=10, pady=5)

            tk.Label(ventana_datos, text="DPI:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            entry_dpi = tk.Entry(ventana_datos)
            entry_dpi.grid(row=1, column=1, sticky="w", padx=10, pady=5)

            tk.Label(ventana_datos, text="Dirección:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
            entry_direccion = tk.Entry(ventana_datos)
            entry_direccion.grid(row=2, column=1, sticky="w", padx=10, pady=5)

            # Botón para guardar o procesar los datos
            btn_guardar = tk.Button(
                ventana_datos, 
                text="Guardar",
                command=lambda: guardar_datos(conn, parent, frame, entry_dpi.get(), entry_nombre.get(), entry_direccion.get(), ventana_datos)
            )
            btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)
    else:
        if option2.get():
            cargar_lotes = execute_query(conn, "SELECT c.lote_id FROM control_pagos c JOIN clientes cli ON c.cliente_id = cli.cliente_id WHERE cli.dpi = %s ORDER BY c.lote_id ASC;", (option1.get()))
            lista_lotes = []
            for fila in cargar_lotes:
                if isinstance(fila, dict):
                    lista_lotes.append(fila['lote'])
                else:
                    lista_lotes.append(fila[0])

            # Asignar la lista resultante al Combobox
            option2['values'] = lista_lotes

        else:
            resultados_lote = execute_query(conn, "SELECT *, cli.nombre as 'nombre_cliente' FROM control_pagos c JOIN clientes cli ON c.cliente_id = cli.cliente_id JOIN lotes l ON c.lote_id = l.lote_id WHERE cli.dpi = %s AND l.lote_id = %s;", (option1.get(), option2.get()))
            if not resultados_lote:
                messagebox.showinfo('Nuevo cliente', 'Datos de factura no encontrados, cliente nuevo.')
                option2['values'] = []


    label0.config(text=f"Nombre: ")
    label1.config(text=f"Saldo Inicial: ")
    label2.config(text=f"Fecha de Compra: ")
    label3.config(text=f"Mensualidad: ")
    label4.config(text=f"Valor Total: ")
    label5.config(text=f"Saldo Actual: ")
    label6.config(text=f"Comisionista: ")

def ingresar_datos(option1, option2, date_selector, label0,  label1, label2, label3, label4, label5, label6, label7):
    # Actualizar los labels con los valores seleccionados
    label0.config(text=f"Nombre: ")
    label1.config(text=f"Saldo Inicial: ")
    label2.config(text=f"Fecha de Compra: ")
    label3.config(text=f"Mensualidad: ")
    label4.config(text=f"Valor Total: ")
    label5.config(text=f"Saldo Actual: ")
    label6.config(text=f"Comisionista: ")
    label7.config(text="Datos ingresados correctamente")

def guardar_datos(conn, parent, page1_frame, dpi, nombre, direccion, ventana):
    execute_non_query(conn, "INSERT INTO clientes(dpi, nombre, direccion) VALUES(%s, %s, %s)", (dpi, nombre, direccion))

    # Destruir el frame actual de la página 1
    page1_frame.destroy()
    # Volver a crear la página 1
    crear_ingreso_pago(parent, conn)

    ventana.destroy()


"""

