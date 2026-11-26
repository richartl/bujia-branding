# Incorporación y aprobación

1. Inspecciona lo recibido en [inbox](../inbox/) o en la conversación. Identifica contenido, duplicados y recursos relacionados. Conserva el original y compara el contenido si sospechas que existe una copia idéntica.
2. Propón un identificador estable, un nombre descriptivo, una categoría y una versión conforme al [versionamiento](VERSIONING.md). Registra la [procedencia confirmada](../masters/README.md), los créditos y los derechos conocidos. Usa `unknown` o indica que el dato está pendiente cuando corresponda.
3. Guarda los originales aprobados expresamente como maestras en [masters](../masters/). Usa [drafts](../drafts/) para propuestas de identidad y [designs](../designs/) para proyectos por aplicación. Conserva el archivo original durante la clasificación. Si se renombra o mueve desde inbox, conserva sus bytes y registra el nombre recibido. Si hace falta convertirlo, genera un derivado independiente.
4. Crea la ficha Markdown junto al archivo a partir de la plantilla de [maestra](../templates/asset.md), [variante](../templates/variation.md) o [diseño](../templates/design.md). Vincula la versión exacta de origen y su maestra cuando apliquen.
5. Actualiza el [catálogo](../CATALOG.md) mediante enlaces relativos al archivo, su ficha (en la columna de nombre) y la maestra. Añade una vista previa solo si existe una imagen compatible. Usa la misma fila para actualizar el estado de una versión y una fila nueva para una versión nueva.

## Estados

| Estado | Significado |
| --- | --- |
| `draft` | Propuesta en preparación. |
| `review` | Candidata pendiente de decisión del propietario. |
| `approved` | Versión aprobada expresamente para el uso registrado. |
| `rejected` | Propuesta rechazada. Se conserva su historial y su fuente. |
| `archived` | Recurso retirado que se conserva para consulta. |

Antes de solicitar aprobación, completa el [checklist visual](APPROVAL_CHECKLIST.md) y muestra el resultado. Registra la decisión, el alcance y la fecha conocida en la ficha y el catálogo. Para diseños aprobados, agrega en [approved](../approved/) una entrada Markdown enlazada al archivo y su ficha. Mantén una sola copia de trabajo por versión. Si se archiva mediante traslado, actualiza los enlaces y preserva la trazabilidad de los derivados. Consulta la [protección de originales](../masters/README.md) para las maestras.
