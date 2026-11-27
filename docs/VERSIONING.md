# Versionamiento de recursos

Usa `identificador-vMAJOR.MINOR.PATCH[-descriptor].ext` en minúsculas, con guiones y un descriptor opcional en inglés. Usa el mismo nombre base para la ficha Markdown. Comienza en `1.0.0`. Incrementa `PATCH` en correcciones pequeñas, `MINOR` en cambios localizados o variantes controladas y `MAJOR` en rediseños autorizados. Al subir un nivel, vuelve a cero en las posiciones inferiores. Asigna una versión libre dentro del identificador, aunque la fuente sea una versión anterior. Ejemplos hipotéticos: `giraffe-v1.0.0.png`, `giraffe-v1.1.0-yellow-mug.png`, `giraffe-v1.1.1-yellow-mug.png`.

Registra en la ficha la maestra y la ruta y versión exactas de origen. Si esa ruta puede cambiar, registra también el commit disponible que identifica la fuente. Evita nombres como `final2.png`. Guarda cada resultado en un archivo nuevo. Cuando se registren cambios en Git, agrupa recurso, ficha y catálogo para que el historial sea legible.

Para recuperar una versión, empieza en el [catálogo](../CATALOG.md) y abre su enlace. Si ya no está en la ruta actual, localiza el commit y la ruta histórica con `git log --all --follow -- ruta/al/archivo`. El agente puede copiar los bytes de esa versión mediante `git show COMMIT:ruta/histórica` a una ruta nueva previamente comprobada, conservando el original actual y comprobando que el comando terminó con éxito. Documenta el origen si se incorpora la copia recuperada.

## Versiones en el catálogo público

Usa el mismo identificador y categoría para variantes de una misma ilustración, por ejemplo al cambiar solo su color. Asigna un identificador propio a una composición independiente, aunque pertenezca a la misma serie. El sitio muestra una tarjeta por recurso y reúne en ella todas sus versiones aprobadas. Conserva la versión de origen en la ficha para identificar correctamente las variantes de las series antiguas.

Cada imagen aprobada tiene un código público con formato `<código-base>-vMAJOR.MINOR.PATCH`. Por ejemplo, `dtf-shirt-back-v1.2.0` identifica exactamente la espalda de playera con el rótulo crema. Usa **Copiar código** en su ficha para indicar qué archivo debe servir de base. Un código sin versión identifica la familia. Si el encargo requiere un original exacto, usa el código completo. Desde la raíz del repositorio, `python site/build.py --find dtf-shirt-back-v1.2.0` devuelve la ruta del archivo aprobado.
