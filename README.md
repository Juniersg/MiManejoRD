
# MiManejoRD

**Mi Manejo** es una aplicación web para el control de finanzas personales. Permite a usuarios individuales gestionar sus cuentas, transacciones, deudas y pagos de forma organizada y segura.

## 🚀 Características principales

- Gestión de cuentas (efectivo, bancarias, tarjetas).
- Registro de ingresos y gastos con categorías.
- Control de deudas y pagos.
- Dashboard con saldos, gastos del mes y deudas activas.
- Reportes básicos (distribución de gastos, evolución mensual).
- Interfaz responsiva y mobile-first con Bootstrap.

## 🔐 Seguridad

- Autenticación básica con contraseñas cifradas usando **bcrypt**.
- Separación de datos por usuario mediante `id_usuario` en todas las tablas.
- Preparación para CSRF y manejo seguro de sesiones.

## 🧱 Modelo de Datos

El sistema utiliza una base de datos relacional en MySQL con las siguientes entidades:

- `Usuario`: registro de usuarios con roles.
- `Cuenta`: asociada a cada usuario.
- `Transaccion`: ingresos/gastos con categoría.
- `Deuda`: control de acreedores y vencimientos.
- `PagoDeuda`: pagos realizados sobre deudas.
- `Categoria`: normalización de categorías de gasto.

## 🧩 Arquitectura

- Backend: **Python + Flask**.
- Base de datos: **MySQL**.
- Patrón MVC simplificado.
- Diseño modular por funcionalidades (`cuentas`, `transacciones`, etc.).
- Uso de SQLAlchemy y migraciones con Alembic (planificado).

## 🎨 Interfaz

- HTML5 + Bootstrap 5.
- Estilo limpio y moderno.
- Pensado para dispositivos móviles (iPhone).
- Preparado para integración con gráficos (Chart.js).

## 📦 Despliegue

- Hosting en **Railway**.
- Preparación para CI/CD con GitHub Actions.
- Separación de ambientes: desarrollo, pruebas y producción.
- Uso de variables de entorno para credenciales.

## 📘 Buenas prácticas

- Control de versiones con Git.
- Código documentado y estructurado.
- Estándares PEP8 en Python.
- Manejo de errores y logs.
- Pruebas unitarias planificadas.

## 📈 Roadmap

- [x] Gestión de cuentas y transacciones.
- [x] Control de deudas y pagos.
- [ ] Reportes gráficos avanzados.
- [ ] Exportación de datos.
- [ ] Notificaciones y alertas.
- [ ] Autenticación avanzada (JWT/OAuth).
- [ ] Dockerización para portabilidad.

## 📄 Licencia

Este proyecto es personal y no está disponible para uso externo. Todos los derechos reservados.

---

Desarrollado por **Junier Soto Guerra**.
