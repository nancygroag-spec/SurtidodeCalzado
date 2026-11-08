from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta_calzado_surtido"

ADMIN_VALIDO = "janeth120"
ADMIN_PASS = "123456"

# Diccionario dinámico: aquí arrancamos con uno de prueba, y los que se registren se sumarán solos
MAYORISTAS_VALIDOS = {
    "8991234567": "123" # Ejemplo: Teléfono como usuario y sus 3 números como contraseña
}

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        
        if usuario == ADMIN_VALIDO and password == ADMIN_PASS:
            session["usuario"] = usuario
            session["tipo"] = "admin"
            return redirect(url_for("catalogo"))
        
        elif usuario in MAYORISTAS_VALIDOS and MAYORISTAS_VALIDOS[usuario] == password:
            session["usuario"] = usuario
            session["tipo"] = "mayorista"
            return redirect(url_for("catalogo"))
        else:
            error = "Usuario o contraseña incorrectos."
            
    return render_template("login.html", error=error)

# --- NUEVA RUTA PARA QUE SE REGISTREN SOLOS ---
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre_usuario = request.form.get("nombre").strip().lower() # Guardamos su nombre como usuario
        telefono_password = request.form.get("telefono").strip()     # Su teléfono será su contraseña
        
        if nombre_usuario and telefono_password:
            # Guardamos al nuevo mayorista en tu diccionario
            MAYORISTAS_VALIDOS[nombre_usuario] = telefono_password
            return redirect(url_for("login"))
            
    return render_template("registro.html")
    

@app.route("/catalogo")
def catalogo():
    busqueda = request.args.get("q", "").lower()
    return render_template("index.html", busqueda=busqueda)

@app.route("/productos/<marca>")
def productos(marca):
    es_mayorista = "usuario" in session
    carpeta_marca = marca.upper()
    
    lista_productos = [
        {"img": f"{marca} ID001.PNG", "id": "05001", "precio": "$1,200 MXN"},
        {"img": f"{marca} ID002.PNG", "id": "05002", "precio": "$1,350 MXN"},
        {"img": f"{marca} ID003.PNG", "id": "05003", "precio": "$1,100 MXN"},
    ]
    
    return render_template("productos.html", marca=carpeta_marca, productos=lista_productos, es_mayorista=es_mayorista)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("catalogo"))

@app.route("/politica-devoluciones")
def politica_devoluciones():
    return render_template("devoluciones.html")

@app.route("/terminos-condiciones")
def terminos_condiciones():
    return render_template("terminos.html")

if __name__ == "__main__":
    app.run(debug=True)
    