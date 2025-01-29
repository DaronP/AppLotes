import tkinter as tk
from tkinter import ttk
from db import execute_query, execute_non_query

def mostrar_pagina_reportes(parent, conn):
    page_bg = "#9A9898"

    frame = tk.Frame(parent, bg=page_bg)
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Reportes y Resúmenes", font=("Arial", 14, "bold"), bg="#9A9898").pack(pady=10)

    style = ttk.Style()
    style.theme_use("clam")

    btn_generar = tk.Button(
        frame, text="Generar Reportes",
        command=lambda: generar_reportes(conn, frame)
    )
    btn_generar.pack(pady=5)

    #generar_reportes(conn, frame)

    return frame


def generar_reportes(conn, contenedor):
    """
    Lógica para consultar la BD y mostrar los reportes solicitados:
      1) Suma de pagos por mes, por año, y total.
      2) Cálculo de comisiones (ej. IVA, ISR) para los comisionistas.
      3) Número de lotes vendidos, fecha de venta, cliente, saldo o pago total.
    Puedes mostrar los datos en Treeview u otros widgets.
    """

    # Limpiar cualquier widget previo
    for widget in contenedor.winfo_children():
        if isinstance(widget, ttk.Treeview) or isinstance(widget, tk.LabelFrame):
            widget.destroy()

    # (1) REPORTES DE PAGOS ACUMULADOS
    # -----------------------------------------------------------------
    lf_pagos = tk.LabelFrame(contenedor, text="Reporte de Pagos Acumulados", bg="#9A9898")
    lf_pagos.pack(fill="x", padx=10, pady=5)

    # a) Pagos por mes
    # Ejemplo de consulta (ajusta la lógica según tu esquema: SUM(monto_recibido) o lo que manejes en 'control_pagos')
    query_mes = """
        SELECT MONTH(fecha_compra) AS mes, YEAR(fecha_compra) AS anio, SUM(monto_recibido) AS total_mes
        FROM control_pagos
        GROUP BY YEAR(fecha_compra), MONTH(fecha_compra)
        ORDER BY YEAR(fecha_compra), MONTH(fecha_compra)
    """
    resultados_mes = execute_query(conn, query_mes)

    # b) Pagos por año
    query_anio = """
        SELECT YEAR(fecha_compra) AS anio, SUM(monto_recibido) AS total_anio
        FROM control_pagos
        GROUP BY YEAR(fecha_compra)
        ORDER BY YEAR(fecha_compra)
    """
    resultados_anio = execute_query(conn, query_anio)

    # c) Total de pagos en toda la historia
    query_total = "SELECT SUM(monto_recibido) AS total_global FROM control_pagos"
    resultado_total = execute_query(conn, query_total)

    # Mostrar en labels, por ejemplo:
    # Por mes:
    texto_mes = "Pagos por Mes/Año:\n"
    for fila in resultados_mes:
        mes = fila[0]
        anio = fila[1]
        total_mes = fila[2]
        texto_mes += f" - {anio}-{mes:02d}: {total_mes:,.2f}\n"

    tk.Label(lf_pagos, text=texto_mes, bg="#9A9898", justify="left").pack(anchor="w", padx=5, pady=5)

    # Por año:
    texto_anio = "Pagos por Año:\n"
    for fila in resultados_anio:
        anio = fila[0]
        total_a = fila[1]
        texto_anio += f" - {anio}: {total_a:,.2f}\n"

    tk.Label(lf_pagos, text=texto_anio, bg="#9A9898", justify="left").pack(anchor="w", padx=5, pady=5)

    # Total global
    total_global = resultado_total[0][0] if resultado_total and resultado_total[0][0] else 0
    tk.Label(lf_pagos, text=f"Total Histórico de Pagos: {total_global:,.2f}", bg="#9A9898").pack(anchor="w", padx=5, pady=5)

    # (2) CÁLCULO DE COMISIONES, IVA E ISR
    # -----------------------------------------------------------------
    lf_comisiones = tk.LabelFrame(contenedor, text="Cálculo de Comisiones e Impuestos", bg="#9A9898")
    lf_comisiones.pack(fill="x", padx=10, pady=5)

    # Ejemplo: Tomamos la primera venta (o las ventas) de 'control_pagos' y 
    # calculamos comisiones para cada comisionista.
    # Ajusta la lógica según tu esquema y fórmulas reales.

    query_comisiones = """
        SELECT c.dpi, c.nombre AS comisionista_nombre,
               SUM(cp.monto_recibido) AS total_ventas
        FROM control_pagos cp
        JOIN comisionistas c ON cp.com_id = c.com_id
        GROUP BY cp.com_id
    """
    resultados_comisiones = execute_query(conn, query_comisiones)

    # Ejemplo de cálculo de la comisión = 5% del total de ventas, IVA=12% e ISR=5% (solo como ejemplo).
    texto_comisiones = "Comisiones por Comisionista:\n"
    for fila in resultados_comisiones:
        id_comisionista = fila[0]
        nombre_comisionista = fila[1]
        total_ventas = float(fila[2]) if fila[2] else 0

        comision_base = total_ventas * 0.05  # 5% de comisión
        iva = comision_base * 0.12  # 12% de IVA sobre la comisión
        isr = comision_base * 0.05  # 5% de ISR sobre la comisión (ejemplo)

        # Monto neto de la comisión después de IVA e ISR (depende de la ley y tu lógica)
        comision_neta = comision_base - (iva + isr)

        texto_comisiones += (
            f" - {nombre_comisionista} (DPI: {id_comisionista}):\n"
            f"   Total Ventas: {total_ventas:,.2f}\n"
            f"   Comisión Base (5%): {comision_base:,.2f}\n"
            f"   IVA (12% de comisión): {iva:,.2f}\n"
            f"   ISR (5% de comisión): {isr:,.2f}\n"
            f"   Comisión Neta: {comision_neta:,.2f}\n"
        )

    tk.Label(lf_comisiones, text=texto_comisiones, bg="#9A9898", justify="left").pack(anchor="w", padx=5, pady=5)

    # (3) LOTES VENDIDOS, FECHA DE VENTA, CLIENTE, SALDO O PAGO TOTAL
    # -----------------------------------------------------------------
    lf_lotes = tk.LabelFrame(contenedor, text="Lotes Vendidos", bg="#9A9898")
    lf_lotes.pack(fill="both", expand=True, padx=10, pady=5)

    # Crear un Treeview para mostrar filas
    columnas = ("lote_id", "fecha_venta", "cliente", "saldo_o_pago_total")
    tree_lotes = ttk.Treeview(lf_lotes, columns=columnas, show="headings")
    tree_lotes.pack(fill="both", expand=True)

    tree_lotes.heading("lote_id", text="Lote")
    tree_lotes.heading("fecha_venta", text="Fecha Venta")
    tree_lotes.heading("cliente", text="Cliente")
    tree_lotes.heading("saldo_o_pago_total", text="Saldo / Pago Total")

    # Ajustar ancho y alineación
    for col in columnas:
        tree_lotes.column(col, anchor="center", width=120)

    # Consulta ejemplo:
    query_lotes_vendidos = """
        SELECT cp.lote_id,
               cp.fecha_compra AS fecha_venta,
               cl.nombre AS cliente_nombre,
               (cp.saldo_actual) AS saldo_o_pago
        FROM control_pagos cp
        JOIN clientes cl ON cp.cliente_id = cl.cliente_id
        -- Suponiendo 'lotes' se marca como disponible='N' cuando se vende, 
        -- o se podría filtrar con otra condición
        -- JOIN lotes l ON cp.lote_id = l.lote_id
        ORDER BY cp.fecha_compra
    """
    resultados_lotes = execute_query(conn, query_lotes_vendidos)

    for fila in resultados_lotes:
        lote_id = fila[0]
        fecha_venta = fila[1]
        cliente = fila[2]
        saldo_o_pago = fila[3]

        tree_lotes.insert("", tk.END, values=(lote_id, fecha_venta, cliente, f"{saldo_o_pago:,.2f}"))

    # Si quisieras mostrar el conteo total de lotes vendidos, etc.
    tk.Label(lf_lotes, text=f"Total Lotes: {len(resultados_lotes)}", bg="#9A9898").pack(anchor="w", padx=5, pady=5)
