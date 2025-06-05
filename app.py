import streamlit as st
import datetime
from significados import significados_caldeos
from compatibilidad import compatibilidad
from definiciones import definiciones_caldeas
from definiciones_otros import definiciones_otros
from collections import defaultdict
from numeros_ausentes import significados_ausentes
from collections import Counter
from diadelnacimiento import dias_nacimiento
from letraInicialDelNombre import letra_inicial_caldea
import pandas as pd



# Tabla de valores caldeos
caldeo_valores = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8,
}

def valor_caldeo_letra(letra):
    tabla_caldea = {
        1: "A I J Q Y", 
        2: "B K R", 
        3: "C G L S", 
        4: "D M T", 
        5: "E H N X", 
        6: "U V W", 
        7: "O Z", 
        8: "F P"
    }
    letra = letra.upper()
    for valor, letras in tabla_caldea.items():
        if letra in letras.split():
            return valor
    return None



def calcular_valor_caldeo(cadena):
    return sum(caldeo_valores.get(c, 0) for c in cadena.upper() if c in caldeo_valores)

def reducir(numero):
    while numero > 9 and numero not in [11, 22, 33, 44]:
        numero = sum(int(d) for d in str(numero))
    return numero

def calcular_numero_nombre(nombre):
    nombre = ''.join(filter(str.isalpha, nombre.upper()))
    total = sum(caldeo_valores.get(letra, 0) for letra in nombre)
    return total, reducir(total)

def calcular_numero_destino(fecha):
    numeros = [int(d) for d in fecha.strftime("%d%m%Y")]
    total = sum(numeros)
    return total, reducir(total)

def separar_vocales_consonantes(nombre):
    vocales = 'AEIOU'
    nombre = ''.join(filter(str.isalpha, nombre.upper()))
    solo_vocales = ''.join([c for c in nombre if c in vocales])
    solo_consonantes = ''.join([c for c in nombre if c not in vocales])
    return solo_vocales, solo_consonantes

def mostrar_significado(numero):
    with st.expander(f"🔍 Ver significado del número {numero}"):
        st.write(significados_caldeos.get(numero, "Significado aún no disponible."))

def mostrar_compatibilidad(nombre_num, destino_num):
    compatibles = compatibilidad.get(nombre_num, "")
    compatibles_lista = []

    for x in compatibles.split(","):
        x = x.strip()
        if x:
            partes = x.split("→")[0].strip().split()
            if partes and partes[0].isdigit():
                compatibles_lista.append(int(partes[0]))

    st.success("**❤️ Compatibilidad entre Nombre y Destino:")
    if destino_num in compatibles_lista:
        st.success(f"¡Compatibles! El número {nombre_num} es compatible con el {destino_num}.")
    else:
        st.error(f"No son altamente compatibles. El número {nombre_num} se lleva mejor con: {compatibles}.")

def analizar_numeros_en_nombre(nombre):
    nombre_limpio = ''.join(filter(str.isalpha, nombre.upper()))
    letras_por_numero = defaultdict(list)
    conteo_por_numero = defaultdict(int)

    for letra in nombre_limpio:
        numero = caldeo_valores.get(letra)
        if numero:
            letras_por_numero[numero].append(letra)
            conteo_por_numero[numero] += 1

    return letras_por_numero, conteo_por_numero



zoom = st.slider("Zoom (tamaño de fuente)", 12, 32, 16)

st.markdown(f"""
    <style>
    html, body, [class*="css"]  {{
        font-size: {zoom}px;
    }}
    </style>
    """, unsafe_allow_html=True)

st.write("Texto ajustado según el zoom elegido.")

# 🔢 Interfaz
st.title("🔮Kalking True")
tabs = st.tabs(["🔢 Cálculo de Números", "📖 Significados", "📘 Definiciones", "📘 Definiciones otras"])


with tabs[0]:
    st.write("Calcula los números principales a partir de tu nombre completo, apodo y fecha de nacimiento.")
    #apodo = st.text_input("Nombre de apodo o firma", value="Papi")
    #nombre = st.text_input("Nombre completo", value="Jhon Erickson Olivares Ramos")
    nombre = st.text_input("Nombre completo")
    apodo = st.text_input("Nombre de apodo o firma")
    fecha = st.date_input(
        "Fecha de nacimiento",
        value=datetime.date(1982, 3, 21),
        min_value=datetime.date(1930, 1, 1),
        max_value=datetime.date.today()
    )

    if st.button("Calcular"):
        if nombre and fecha:
            total_nombre, nombre_reducido = calcular_numero_nombre(nombre)
            total_destino, destino_reducido = calcular_numero_destino(fecha)

            solo_vocales, solo_consonantes = separar_vocales_consonantes(nombre)
            alma_valor = calcular_valor_caldeo(solo_vocales)
            personalidad_valor = calcular_valor_caldeo(solo_consonantes)
            alma_reducida = reducir(alma_valor)
            personalidad_reducida = reducir(personalidad_valor)

            primer_nombre = nombre.strip().split()[0]
            total_primer_nombre, primer_nombre_reducido = calcular_numero_nombre(primer_nombre)

            total_apodo, apodo_reducido = calcular_numero_nombre(apodo)

            st.subheader("🧾 Resultados:")
            st.markdown("---")
            
            

            st.success(f"**Número del Nombre:** {total_nombre} → **{nombre_reducido}**")
            mostrar_significado(total_nombre)
            mostrar_significado(nombre_reducido)
            st.markdown("---")
            
            
            

            st.success("**🔡 Análisis por partes del nombre:**")
            partes_nombre = nombre.strip().split()
            for parte in partes_nombre:
                parte_limpia = ''.join(filter(str.isalpha, parte))
                valor_parte = calcular_valor_caldeo(parte_limpia)
                with st.container():
                    
                    st.write(f"**{parte}** → **{valor_parte}**")
                    mostrar_significado(valor_parte)
            st.markdown("---")



            

            st.success(f"**Número del Destino:** {total_destino} → **{destino_reducido}**")
            mostrar_significado(total_destino)
            mostrar_significado(destino_reducido)
            st.markdown("---")
            
            
            

            mostrar_compatibilidad(nombre_reducido, destino_reducido)
            st.markdown("---")
            
            
            
            

            st.success(f"**Número del Alma (vocales):** {alma_valor} → **{alma_reducida}**")
            mostrar_significado(alma_valor)
            mostrar_significado(alma_reducida)
            st.markdown("---")
            
            
            

            st.success(f"**Número de la Personalidad (consonantes):** {personalidad_valor} → **{personalidad_reducida}**")
            mostrar_significado(personalidad_valor)
            mostrar_significado(personalidad_reducida)
            st.markdown("---")
            
            
            

            st.success(f"**Número del Primer Nombre:** {total_primer_nombre} → **{primer_nombre_reducido}**")
            mostrar_significado(total_primer_nombre)
            mostrar_significado(primer_nombre_reducido)
            st.markdown("---")
            
            

            st.success(f"**Número del Apodo o Firma:** {total_apodo} → **{apodo_reducido}**")
            mostrar_significado(total_apodo)
            mostrar_significado(apodo_reducido)
            st.markdown("---")
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # Análisis de Números Ausentes
            

            nombre_limpio = ''.join(filter(str.isalpha, nombre.upper()))
            conteo_letras = Counter(nombre_limpio)
            conteo_numeros = {i: 0 for i in range(1, 10)}

            for letra in nombre_limpio:
                valor = caldeo_valores.get(letra, 0)
                if valor in conteo_numeros:
                    conteo_numeros[valor] += 1

            st.success("**📉 Análisis de Números Ausentes en el Nombre**")

            tabla = []
            for numero in range(1, 10):
                letras_asociadas = [letra for letra, val in caldeo_valores.items() if val == numero]
                letras_presentes = [l for l in nombre_limpio if l in letras_asociadas]
                tabla.append((numero, ', '.join(letras_presentes) or '-', conteo_numeros[numero]))

            st.table(
                {
                    "Número": [x[0] for x in tabla],
                    "Letras encontradas": [x[1] for x in tabla],
                    "Cantidad": [x[2] for x in tabla],
                }
            )

            ausentes = [numero for numero, count in conteo_numeros.items() if count == 0 and numero != 9]

            if ausentes:
                with st.expander("🔎 Ver análisis de números ausentes"):
                    for numero in ausentes:
                        if numero == 9:
                            st.info("El número 9 **siempre está ausente** en nombres según la numerología caldea, ya que no se le asigna ninguna letra. No indica una carencia negativa.")
                        else:
                            st.markdown(significados_ausentes.get(numero, f"No hay información para el número {numero}."))
            else:
                st.success("✅ No hay números ausentes en el nombre.")
            st.markdown("---")


            
            
            
            # 🔍 Análisis del Día de Nacimiento
            st.success("**🗓️ Análisis del Día de Nacimiento**")

            dia_nacimiento = fecha.day
            info_dia = dias_nacimiento.get(dia_nacimiento)

            if info_dia:
                with st.expander(f"🌞 Día {dia_nacimiento}: {info_dia['tipo']}"):
                    st.markdown(f"**🧠 Explicación:** {info_dia['explicacion']}")
                    st.markdown(f"**🎁 Dones naturales:** {info_dia['dones_naturales']}")
                    st.markdown(f"**⚠️ Retos:** {info_dia['retos']}")
                    
                    reduccion = info_dia['reduccion']
                    st.markdown(f"**🔢 Reducción ({reduccion['valor']} - {reduccion['tipo']}):** {reduccion['significado']}")
            else:
                st.warning("No hay información disponible para este día.")
            st.markdown("---")


            


            
            
            
            # 🔠 Análisis de la letra inicial del nombre y apodo
            st.success("**🔠 Análisis de la letra inicial del nombre / apodo**")

            def mostrar_analisis_inicial(etiqueta, texto):
                if texto:
                    inicial = texto.strip()[0].upper()
                    valor = valor_caldeo_letra(inicial)
                    if valor and valor in letra_inicial_caldea:
                        info = letra_inicial_caldea[valor]

                        # Resumen visible
                        st.markdown(f"**📛 {etiqueta} → Letra inicial:** {inicial} = {valor}")

                        # Expander para ver el análisis completo
                        with st.expander(f"🔍 Ver análisis de la letra inicial del {etiqueta.lower()}"):
                          
                            st.markdown(f"**🔢 Interpretación de la letra inicial \"{inicial}\" = {valor}**")
                            st.markdown(f"Letra: {inicial} → Número {valor} ({info['planeta']})")
                            st.markdown(f"🧠 **Significado profundo:** {info['descripcion']}")
                            st.markdown("**✅ Fortalezas:**")
                            for f in info["fortalezas"]:
                                st.markdown(f"- {f}")
                            st.markdown("**⚠️ Sombra o desafíos:**")
                            for s in info["sombras"]:
                                st.markdown(f"- {s}")
                            st.markdown(f"🌌 **Vibración espiritual:** {info['vibracion_espiritual']}")
                    else:
                        st.warning(f"No se pudo calcular la letra inicial para: {texto}")

            # Mostrar análisis de nombre y apodo
            mostrar_analisis_inicial("Nombre", nombre)
            if apodo:
                mostrar_analisis_inicial("Apodo", apodo)
            st.markdown("---")


            
            
            
            
 




            # 🧾 Tabla de resumen final
            st.success("**📋 Resumen General de Resultados**")

            dia_nacimiento = fecha.day
            dia_info = dias_nacimiento.get(dia_nacimiento, {})
            tipo_dia = dia_info.get("tipo", "No disponible")
            reduccion_dia = dia_info.get("reduccion", {}).get("valor", "—")

            letra_nombre = nombre.strip()[0].upper()
            letra_apodo = apodo.strip()[0].upper() if apodo else "-"
            valor_letra_nombre = valor_caldeo_letra(letra_nombre)
            valor_letra_apodo = valor_caldeo_letra(letra_apodo) if apodo else "-"

            # Compatibilidad
            compatibles = compatibilidad.get(nombre_reducido, "")
            compatibles_lista = []
            for x in compatibles.split(","):
                x = x.strip()
                if x:
                    partes = x.split("→")[0].strip().split()
                    if partes and partes[0].isdigit():
                        compatibles_lista.append(int(partes[0]))
            es_compatible = "✅ Sí" if destino_reducido in compatibles_lista else "❌ No"

            # Números Ausentes
            nombre_limpio = ''.join(filter(str.isalpha, nombre.upper()))
            conteo_numeros = {i: 0 for i in range(1, 10)}
            for letra in nombre_limpio:
                valor = caldeo_valores.get(letra, 0)
                if valor in conteo_numeros:
                    conteo_numeros[valor] += 1
            ausentes = [str(num) for num, count in conteo_numeros.items() if count == 0 and num != 9]
            ausentes_str = ', '.join(ausentes) if ausentes else "Ninguno"

            # Armar tabla
            resumen_datos = {
                "Concepto": [
                    "Número del Nombre",
                    "Número del Destino",
                    "Número del Alma (vocales)",
                    "Número de la Personalidad (consonantes)",
                    "Número del Primer Nombre",
                    "Número del Apodo",
                    "Día de Nacimiento",
                    "Letra Inicial del Nombre",
                    "Letra Inicial del Apodo",
                    "Compatibilidad",
                    "Números Ausentes"
                ],
                "Valor": [
                    f"{total_nombre} / {nombre_reducido}",
                    f"{total_destino} / {destino_reducido}",
                    f"{alma_valor} / {alma_reducida}",
                    f"{personalidad_valor} / {personalidad_reducida}",
                    f"{total_primer_nombre} / {primer_nombre_reducido}",
                    f"{total_apodo} / {apodo_reducido}",
                    f"{dia_nacimiento} ({tipo_dia}) / {reduccion_dia}",
                    f"{letra_nombre} / {valor_letra_nombre}",
                    f"{letra_apodo} / {valor_letra_apodo}",
                    es_compatible,
                    ausentes_str
                ]
            }
            st.markdown(f"""
            <div style="text-align: center;">
            <strong>Nombre:</strong> {nombre} <br>
            <strong>Fecha de nacimiento:</strong> {fecha.strftime('%d/%m/%Y')} <br><br></div>""", unsafe_allow_html=True)
            
            df_resumen = pd.DataFrame(resumen_datos)
            st.table(df_resumen)
            st.markdown("---")
            
            
            






 
            
            
            
            
            
            
        else:
            st.warning("Por favor, completa ambos campos.")
            

with tabs[1]:
    st.header("**📖 Significados de los Números**")

    # Obtener todos los números ordenados
    numeros = sorted(significados_caldeos.keys())

    # Mostrar cada número con su expander
    for numero in numeros:
        with st.expander(f"**🔢 Número {numero}**"):
            st.write(significados_caldeos[numero])

with tabs[2]:
    st.header("**📘 Conceptos de Numerología Caldea**")
    st.write("Haz clic sobre cada concepto para ver su definición e interpretación.")

    for concepto, descripcion in definiciones_caldeas.items():
        with st.expander(f"**📎  {concepto}**"):
            st.write(descripcion)


with tabs[3]:
    st.title("**Otras Definiciones Numerológicas**")
    for titulo, descripcion in definiciones_otros.items():
        with st.expander(f"**📎  {titulo}**"):
            st.markdown(descripcion)
