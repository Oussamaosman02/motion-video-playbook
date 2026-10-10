# Skills para hacer los vídeos

Una skill es una carpeta con un archivo `SKILL.md` que le enseña a Claude a hacer una tarea. Estas son las que uso con el playbook.

## Qué hay aquí

| Skill | Para qué sirve | Sesión |
|---|---|---|
| `hyperframes` | Punto de entrada: decide cómo se hace un vídeo con HyperFrames | 1 y 2 |
| `hyperframes-core` | Estructura del proyecto (`index.html`, tiempos, pistas) | 1 y 2 |
| `hyperframes-animation` | Animación: GSAP, transiciones, Three.js, Lottie | 1 y 2 |
| `hyperframes-creative` | Dirección creativa: paleta, tipografía, guion, ritmo | 1 |
| `hyperframes-audio` | Voz, música y efectos dentro del proyecto | 1 y 2 |
| `hyperframes-keyframes` | Fotogramas clave | 1 |
| `hyperframes-registry` | Bloques y componentes ya hechos | 1 |
| `hyperframes-cli` | Comandos: `check`, `snapshot`, `render`, `transcribe`, `tts` | 1 y 2 |
| `hyperframes-studio` | Vista previa en el navegador | 1 |
| `media-use` | Música, efectos, imágenes, iconos y logos | 1 y 2 |
| `general-video` | Vídeo genérico cuando no encaja otro formato | 1 |
| `product-launch-video` | Vídeo de lanzamiento de producto | 1 |
| `talking-head-recut` | Gráficos sobre un vídeo largo de alguien hablando | 2 |

La carpeta `opcional-elevenlabs` solo hace falta si pagas ElevenLabs: `text-to-speech`, `speech-to-text`, `music`, `sound-effects` y `setup-api-key`. Sin ElevenLabs, la voz y la transcripción salen gratis con `npx hyperframes tts` y `npx hyperframes transcribe`.

## Cómo instalarlas

**Claude Desktop o claude.ai:** en Configuración → Capacidades → Skills, sube uno a uno los archivos de la carpeta `zip` (y los de `opcional-elevenlabs/zip` si los quieres).

**Claude Code:** copia las carpetas de las skills (no los zip) dentro de `.claude/skills/` en tu carpeta de trabajo.

## De dónde vienen

Son skills públicas, copiadas tal cual:

- HyperFrames (todas menos las de ElevenLabs): https://github.com/heygen-com/hyperframes
- ElevenLabs: https://github.com/elevenlabs/skills

Para tener la última versión, con Node instalado: `npx skills add heygen-com/hyperframes` y `npx skills add elevenlabs/skills`.
