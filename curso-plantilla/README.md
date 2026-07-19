# Plantilla de curso en HTML

Una página lista para usar en **cualquier curso**. Solo cambias el título.

## Cómo usarla (explicación para peques… y adultos)

Imagina que esta plantilla es un **cuaderno con portada bonita**.  
Tú solo escribes el **nombre del curso** en la portada. El resto ya está dibujado.

### Paso 1 — Abre el archivo

Abre `curso-plantilla/index.html` con un editor de texto.

### Paso 2 — Cambia el título (un solo sitio)

Busca esta línea cerca del principio del `<body>`:

```html
data-course-title="Curso de HTML para Principiantes"
```

Cámbiala, por ejemplo:

```html
data-course-title="Curso de Matemáticas Divertidas"
```

Opcional: cambia también la frase corta:

```html
data-course-tagline="Sumar y restar sin aburrirte ni un minuto."
```

### Paso 3 — Guarda y mira

Abre `index.html` en el navegador. El título nuevo aparece en:

- la pestaña del navegador  
- la cabecera  
- el título grande del inicio  
- el pie de página  

## Carpetas

| Carpeta / archivo | Para qué sirve |
| --- | --- |
| `index.html` | La página del curso |
| `css/estilo.css` | Colores, tipografía y diseño |
| `js/curso.js` | Copia el título a toda la página y anima un poco |

## Personalizar un poco más

- **Módulos:** edita la lista dentro de `#modulos`.
- **Qué aprenderás:** edita la lista dentro de `#aprender`.
- **Colores:** están al inicio de `css/estilo.css` en `:root`.

## Ver en el navegador

Haz doble clic en `curso-plantilla/index.html`, o desde la terminal:

```bash
# Si tienes Python:
python3 -m http.server 8080 --directory curso-plantilla
```

Luego visita `http://localhost:8080`.
