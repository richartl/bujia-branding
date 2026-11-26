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
