# Matias Gajardo — portfolio completo

Sitio estático independiente de Wix, listo para servir con Docker y Nginx en el **puerto 89**.

## Subir al servidor

Copia esta carpeta completa al servidor (incluida `assets/`). Dentro de ella ejecuta:

```sh
docker compose up -d --build
```

Abre **http://IP-DE-TU-SERVIDOR:89**. El servidor debe tener Docker con Compose y permitir conexiones entrantes TCP al puerto 89. No requiere Node, Python, base de datos ni credenciales para funcionar. Docker descarga la imagen de Nginx durante la primera construcción.

También se incluye `matias-web.tar.gz` para subir el proyecto como un solo archivo:

```sh
mkdir -p matias-web
tar -xzf matias-web.tar.gz -C matias-web
cd matias-web
docker compose up -d --build
```

## Qué incluye

- 41 páginas HTML: portada, cinco disciplinas, 34 series/proyectos y biografía/contacto.
- 470 imágenes únicas recuperadas de las galerías públicas, incluidas las que Wix carga de forma diferida. Los archivos se sirven localmente, a una resolución máxima de 1800 px.
- Pintura, ilustración, fotografía, eróticos y arquitectura, con textos y títulos disponibles en el original.
- Visor de imágenes con títulos, descripciones disponibles, flechas, teclado, Escape y gestos táctiles.
- Enlaces a imágenes concretas, por ejemplo `pintura-conversaciones-con-mi-papadre.html#obra-5`, descarga y copia del enlace. La copia automática requiere HTTPS o localhost; en HTTP se indica cómo copiar la URL manualmente.
- Navegación entre series, menú móvil y páginas que pueden abrirse directamente.
- Contacto por teléfono y correo. El formulario prepara un mensaje en la aplicación de correo del visitante; el visitante lo envía desde allí.
- Reinicio automático, comprobación de salud y rotación de logs de Docker.

La composición es una reinterpretación del portfolio original, no una réplica visual exacta. El sitio de Wix permanece intacto. Las obras y textos pertenecen a sus respectivos autores.

## Operación

```sh
# Estado y salud
docker compose ps

# Logs
docker compose logs --tail=100 web

# Aplicar cambios en HTML/CSS/JS o imágenes
docker compose up -d --build

# Detener
docker compose down
```

El puerto del servidor se define en `compose.yaml` como `89:80`: puerto público 89, puerto interno de Nginx 80. El servicio de salud está en `/healthz`.

## Editar el contenido

Los archivos HTML ya están generados y se pueden editar directamente. Para mantener el catálogo centralizado, edita `content.json` y regenera (requiere Python 3 únicamente en el equipo donde editas):

```sh
python3 scripts/build_site.py
python3 tests/check_site.py
node --check app.js
```

`content.json` conserva las referencias originales como procedencia; el navegador carga las imágenes desde `assets/`. Los HTML y las imágenes permiten navegar sin conexión abriendo `index.html`, y las galerías siguen funcionando sin JavaScript como enlaces directos a las imágenes.

Se verifican los enlaces internos, las anclas, todas las imágenes locales y la sintaxis JavaScript. La revisión visual automatizada no estuvo disponible en este entorno.
