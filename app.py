
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import locale
import os
from datetime import date

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)
import os

LOGO_PATH = os.path.join("static", "logo_sacrosanto.png")


def limpiar_numero(texto):
    return float(texto.replace('.', '').replace(',', ''))

def formatear_numero(valor):
    try:
        return locale.format_string("%d", int(round(float(valor))), grouping=True)
    except:
        return valor

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            vs = limpiar_numero(request.form['valor_servicio'])
            fc = limpiar_numero(request.form['faltante_carencia'])

            vpc = (vs * fc) / 30
            pc = (fc * 100) / 30
            vps = vs - vpc
            ps = 100 - pc

            datos = [
                f"Valor Servicio Sede: ${formatear_numero(vs)}",
                f"Días Restantes Para Cumplir Carencias: {formatear_numero(fc)} días",
                "",
                f"Valor a pagar Cliente: ${formatear_numero(vpc)}",
                f"Porcentaje que paga Cliente: {int(round(pc))}%",
                "",
                f"Valor a pagar Sacrosanto: ${formatear_numero(vps)}",
                f"Porcentaje que paga Sacrosanto: {int(round(ps))}%"
            ]

            pdf = FPDF()
            pdf.add_page()
            pdf.image(LOGO_PATH, x=60, y=20, w=90)
            pdf.set_font("Arial", size=12)
            pdf.ln(80)
            for linea in datos:
                pdf.cell(0, 10, txt=linea, ln=1, align='C')

            fecha_actual = date.today().strftime("%Y-%m-%d")
            pdf_path = f"valor_carencia_{fecha_actual}.pdf"
            pdf.output(pdf_path)
            return send_file(pdf_path, as_attachment=True)
        except Exception as e:
            return f"<h3>Error: {e}</h3>"
    return render_template('index.html')

if __name__ == '__main__':
   import os

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

