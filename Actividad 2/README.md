# SeguritoApp — Actividad 2

**Estudiante:** Otto Hernandez  
**Carné:** 08001620  
**Curso:** Aplicaciones Móviles  
**Cliente:** Agencia de seguros El Gran Árbol

## Entregables

| Entregable | Ubicación |
|---|---|
| Prototipo interactivo (HTML) | `prototipo/index.html` |
| Pantallas para Figma (PNG 390×844) | `assets/screens/` |
| Guía de usabilidad (PDF con carátula) | `docs/Guia_Usabilidad_SeguritoApp_OttoHernandez_08001620.pdf` |

## Cómo abrir el prototipo

1. Abre `prototipo/index.html` en el navegador.
2. Inicia sesión con cualquier correo y contraseña (campos vacíos a propósito).
3. Explora afiliados, solicitudes y notificaciones.

## Funciones cubiertas

- Consulta de **médicos**, **hospitales** y **laboratorios** afiliados (búsqueda y detalle).
- Solicitud de autorización de **medicamentos**.
- Solicitud de autorización de **hospitalización**.
- **Registro** de solicitudes con filtros por estado.
- **Notificaciones** de envío, aprobación y rechazo (simulación automática ~3.5 s).

## Prototipo en Figma

**Archivo:** [SeguritoApp - El Gran Arbol](https://www.figma.com/design/KUNHbRr9EhWoAgyBN8Fz6e/SeguritoApp---El-Gran-Arbol)

Pantallas (390 × 844) con Prototype conectado:
1. Iniciar sesión
2. Inicio
3. Red de afiliados
4. Detalle del afiliado
5. Autorización de medicamentos
6. Autorización de hospitalización
7. Mis solicitudes
8. Detalle de solicitud
9. Notificaciones

Para presentar: botón **Present** en Figma.

## Regenerar assets

```bash
python3 scripts/generate_screens.py
python3 scripts/generate_guia_pdf.py
```
