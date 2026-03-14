# routes/auth.py
"""
Rutas de Autenticación - Controlador para manejar login, registro y logout
Misma estructura que IAChatRoutes para mantener consistencia
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.utils.auth_engine import AuthEngine

class AuthRoutes:
    """
    Controlador de autenticación - Maneja todas las rutas /auth/*
    Sigue el mismo patrón que IAChatRoutes y DestinosRoutes
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el blueprint y el motor de autenticación
        
        Args:
            db_connection: Conexión a la base de datos (opcional)
        """
        # ===== CONFIGURACIÓN DEL BLUEPRINT =====
        # Todas las rutas empezarán con /auth
        self.blueprint = Blueprint(
            "auth",
            __name__,
            url_prefix="/auth"
        )
        
        # ===== INICIALIZAR MOTOR =====
        # El motor maneja toda la lógica de negocio
        self.engine = AuthEngine(db_connection)
        
        # ===== REGISTRAR RUTAS =====
        self.register_routes()
    
    def register_routes(self):
        """
        Registra todas las rutas del controlador
        """
        
        # Ruta de login: /auth/login
        # Muestra el formulario de login (GET) y procesa el login (POST)
        self.blueprint.add_url_rule(
            "/login",
            view_func=self.login,
            methods=["GET", "POST"]
        )
        
        # Ruta de registro: /auth/registro
        # Muestra el formulario de registro (GET) y procesa el registro (POST)
        self.blueprint.add_url_rule(
            "/registro",
            view_func=self.registro,
            methods=["GET", "POST"]
        )
        
        # Ruta de logout: /auth/logout
        # Cierra la sesión del usuario
        self.blueprint.add_url_rule(
            "/logout",
            view_func=self.logout
        )
        
        # API endpoint: /auth/api/verificar
        # Verifica si hay sesión activa (para AJAX)
        self.blueprint.add_url_rule(
            "/api/verificar",
            view_func=self.verificar_sesion
        )
    
    def login(self):
        """
        Ruta: /auth/login
        Métodos: GET (mostrar formulario), POST (procesar login)
        Templates: auth/login.html
        """
        if request.method == "GET":
            # Mostrar formulario de login
            # Si ya hay sesión, redirigir al inicio
            if 'usuario_id' in session:
                return redirect(url_for('main.index'))
            return render_template("auth/login.html")
        
        # ===== PROCESAR LOGIN (POST) =====
        # Obtener datos del formulario
        email = request.form.get('email', '')
        contra = request.form.get('contra', '')
        
        # Intentar login
        resultado = self.engine.login(email, contra)
        
        if resultado['exito']:
            # Guardar usuario en sesión
            session['usuario_id'] = resultado['usuario']['id']
            session['usuario_nombre'] = resultado['usuario']['nombre']
            session['usuario_email'] = resultado['usuario']['email']
            
            # Redirigir a la página anterior o al inicio
            next_page = request.args.get('next', url_for('main.index'))
            return redirect(next_page)
        else:
            # Mostrar error
            return render_template("auth/login.html", error=resultado['error'], email=email)
    
    def registro(self):
        """
        Ruta: /auth/registro
        Métodos: GET (mostrar formulario), POST (procesar registro)
        Templates: auth/register.html
        """
        if request.method == "GET":
            # Mostrar formulario de registro
            # Si ya hay sesión, redirigir al inicio
            if 'usuario_id' in session:
                return redirect(url_for('main.index'))
            return render_template("auth/register.html")
        
        # ===== PROCESAR REGISTRO (POST) =====
        # Obtener datos del formulario
        nombre = request.form.get('nombre', '')
        email = request.form.get('email', '')
        contra = request.form.get('contra', '')
        contra_confirm = request.form.get('contra_confirm', '')
        
        # Validar que las contraseñas coincidan
        if contra != contra_confirm:
            return render_template(
                "auth/register.html", 
                error="Las contraseñas no coinciden",
                nombre=nombre,
                email=email
            )
        
        # Intentar registro
        resultado = self.engine.registrar(nombre, email, contra)
        
        if resultado['exito']:
            # Registro exitoso, redirigir a login
            return redirect(url_for('auth.login', registro_exitoso=1))
        else:
            # Mostrar error
            return render_template(
                "auth/register.html",
                error=resultado['error'],
                nombre=nombre,
                email=email
            )
    
    def logout(self):
        """
        Ruta: /auth/logout
        Método: GET
        Cierra la sesión del usuario y redirige al inicio
        """
        # Limpiar sesión
        session.pop('usuario_id', None)
        session.pop('usuario_nombre', None)
        session.pop('usuario_email', None)
        
        # Redirigir al inicio
        return redirect(url_for('main.index'))
    
    def verificar_sesion(self):
        """
        Ruta: /auth/api/verificar
        Método: GET
        API endpoint para verificar si hay sesión activa
        """
        from flask import jsonify
        
        if 'usuario_id' in session:
            return jsonify({
                'logueado': True,
                'usuario': {
                    'id': session['usuario_id'],
                    'nombre': session.get('usuario_nombre', ''),
                    'email': session.get('usuario_email', '')
                }
            })
        else:
            return jsonify({'logueado': False})