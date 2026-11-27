# Bujía Project Music

Repositorio privado de identidad gráfica del taller de construcción, mantenimiento y personalización de guitarras y bajos en Texcoco, México. GitHub es la fuente de verdad para los originales, sus fichas, el catálogo y el historial.

Para empezar, coloca tus imágenes en [inbox](inbox/) o adjúntalas al agente y pídele que las incorpore. Si una imagen ya es una maestra, indica expresamente que la apruebas como tal y comunica su procedencia si la conoces. Consulta la [guía de inicio](docs/GETTING_STARTED.md) para usar Codex, ChatGPT, Claude u otro agente.

| Ruta | Uso |
| --- | --- |
| [masters](masters/) | Originales de identidad reutilizables con aprobación explícita. |
| [identity](identity/) | Registros de paleta, tipografía, estilo y personajes. |
| [references](references/) | Referencias complementarias organizadas por tema, con fuente y derechos cuando se conozcan. |
| [inbox](inbox/) | Archivos nuevos pendientes de clasificación. |
| [drafts](drafts/) | Propuestas de identidad y modificaciones aún pendientes. |
| [designs](designs/) | Proyectos organizados por aplicación. |
| [approved](approved/) | Índice mediante enlaces a versiones de diseño aprobadas. |
| [exports](exports/) | Derivados preparados para un medio específico. |
| [archive](archive/) | Recursos retirados que se conservan por su valor histórico. |
| [docs](docs/) | Procedimientos de incorporación, edición, revisión, recuperación e impresión. |
| [prompts](prompts/) | Plantillas de trabajo para agentes. |
| [templates](templates/) | Fichas de maestras, variantes y diseños. |
| [.agents/skills](.agents/skills/) | Protocolo especializado portable. |

Consulta el [catálogo](CATALOG.md), la [guía visual](BRAND_GUIDELINES.md) y el [historial documental](CHANGELOG.md). Los agentes comienzan por [AGENTS.md](AGENTS.md).

Las referencias se agrupan por cultura punk, ilustración, serigrafía, fanzines, fotografía y tableros visuales. Los proyectos de diseño se agrupan por stickers, playeras, totebags, gorras, flyers, posters, señalética, empaque y redes sociales. La carpeta `references` dentro de la skill queda disponible para material complementario específico del protocolo. Las reglas vigentes se consultan en los documentos enlazados por la skill.

## Catálogo visual

El [catálogo de recursos](CATALOG.md) alimenta un sitio de GitHub Pages con miniaturas, búsqueda y filtros por uso y estado. Los enlaces a las fichas y archivos originales respetan el acceso al repositorio.

Para probarlo localmente, instala Pillow 12.2.0 y ejecuta `python site/build.py /tmp/bujia-catalog` desde la raíz. Abre el `index.html` generado. Los cambios en el catálogo y sus recursos regeneran el sitio mediante GitHub Actions.

En **Settings → Pages**, selecciona **GitHub Actions** como origen. El flujo **Catálogo en GitHub Pages** despliega desde `main` con la visibilidad configurada en Pages. En el sitio se publican miniaturas y datos de los recursos del catálogo. Los archivos originales y sus fichas siguen enlazados al repositorio.
