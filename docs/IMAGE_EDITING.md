# Protocolo de edición de imágenes

Antes de editar, identifica la maestra, el archivo y versión exactos de origen, el cambio autorizado, las zonas protegidas, los colores permitidos, la modalidad, el método y el nombre del resultado. Aplica la [jerarquía de referencias y las reglas visuales](../BRAND_GUIDELINES.md). El agente completa internamente la [plantilla de prompt](../prompts/) correspondiente.

## STRICT_EDIT

Modalidad predeterminada al pedir cambios en un archivo existente. Limita la operación al área autorizada y conserva dimensiones, composición, proporciones, personajes, expresiones, trazos, textura, fondo, objetos y colores fuera de ese alcance. Prioriza edición vectorial de la capa original, máscaras, manipulación de píxeles, sustitución localizada de color, composición, superposición o recorte según el pedido. Evita regenerar toda la imagen si existe una opción localizada. Cuando sea viable, compara los píxeles fuera de la máscara y comprueba que las dimensiones coinciden. Si solo hay edición generativa, verifica visualmente las zonas protegidas y comunica el alcance de esa comprobación.

## CONTROLLED_VARIATION

Usa la versión solicitada, la maestra y las referencias humanas pertinentes cuando estén disponibles. Cambia únicamente los aspectos autorizados, como pose, accesorio o entorno. Conserva la expresión y los rasgos esenciales salvo cambio autorizado. Compara la variante con las referencias para comprobar el lenguaje gráfico.

## CREATIVE_GENERATION

Crea una obra nueva dentro del lenguaje de Bujía aplicando la jerarquía de la guía visual. Guarda el resultado inicial como `draft`. Su incorporación como maestra sigue el [flujo de aprobación](ASSET_WORKFLOW.md).

En toda modalidad crea un archivo independiente, completa la [ficha de variante](../templates/variation.md) o de [diseño](../templates/design.md) y realiza la [revisión visual](APPROVAL_CHECKLIST.md). Si falta acceso a la imagen o capacidad de edición, sigue la [guía de inicio](GETTING_STARTED.md).

## Entrega de propuestas

Entrega una propuesta por imagen. Si el propietario pide varias propuestas, crea un archivo independiente para cada una. Usa una lámina con varias opciones únicamente cuando el propietario la solicite expresamente. Una propuesta individual puede incluir varios elementos que forman parte de la misma composición.

Muestra cada imagen directamente en la respuesta para revisión y enlaza su archivo cuando esté disponible. Si la sesión no puede mostrarla, indica esa limitación y facilita el acceso al archivo.

## Logo, Instagram y silueta de stickers

En cada sticker, usa el [logo ovalado maestro](../masters/logo/bujia-oval-logo-v1.0.0-red-cream.md) en un lugar discreto que pertenezca a la escena, como un letrero, una etiqueta sobre un objeto o un parche. Si se coloca cerca del borde, únelo visual y físicamente al cuerpo de la ilustración. Incluye siempre `@bujiaprojectgarage`, escrito exactamente así, legible al tamaño previsto y dentro de la misma silueta.

### Formato de corte

Si el propietario pide formato cuadrado o de silueta, usa ese formato. Si puedes identificar el formato por la composición, aplica la opción correspondiente. Cuando haya duda, entrega dos versiones independientes, una cuadrada y otra de silueta, y muestra ambas.

- **Silueta.** Sigue el contorno exterior de la ilustración y entrega un PNG con transparencia real fuera de ese contorno. Comprueba que el logo y el usuario de Instagram quedan dentro de una sola pieza, sin islas que exijan cortes separados. Respeta las aperturas interiores que deban llevar el material del sticker.
- **Cuadrado.** Conserva el fondo como parte de la pieza y usa el perímetro exterior para el corte. Si el propietario pide un cuadrado explícitamente, entrega un lienzo 1:1 y ajusta el encuadre sin deformar la ilustración.

Si falta el tamaño final o un troquel confirmado, presenta el resultado como propuesta pendiente de validación para impresión.
