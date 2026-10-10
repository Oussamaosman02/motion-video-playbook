# Motion video playbook

Recetas y plantillas para hacer vídeos de motion graphics con Claude y [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP → MP4).

## Cómo usarlo

1. Abre este repositorio en Claude (claude.ai/code, Claude Desktop o Claude Code).
2. Pídele a Claude que lea `PLAYBOOK.md` y elija el formato que mejor encaje con tu vídeo.
3. Claude copia la carpeta `template/` de ese formato, cambia guion, marca y datos, revisa con `npx hyperframes check` y `snapshot`, y renderiza con `npx hyperframes render`.

Hace falta Node 22 o superior y ffmpeg.

## Qué hay

- `PLAYBOOK.md`: todos los formatos, con una tabla de cuándo usar cada uno. La Parte LF resume las técnicas de vídeo largo.
- Una carpeta por formato, con su `PLAYBOOK.md` y su `template/`.
- `tools/`: scripts compartidos (audio, imágenes, transcripción).
- `skills/`: las skills de Claude que se usan, con un zip por skill para subirlas a Claude Desktop o claude.ai (ver `skills/LEEME.md`). Las mismas están en `.claude/skills/` para que Claude Code las cargue solo.

## Lo que no está incluido

- El formato `kinetic-hud-film` (AK en `PLAYBOOK.md`): usaba material de un cliente.
- Las imágenes de personajes de `cartoon-duo`: pon las tuyas en `cartoon-duo/template/assets/` con los nombres que espera `index.html`.
- `tools/yt_download.sh` y las carpetas `../x-batch`, `../sfx-forensics` y `../long-video-refs` que mencionan los documentos: son privadas, así que esos enlaces y `tools/sfx_feel_check.sh` no funcionan aquí.

## Créditos

Las skills de `skills/` vienen de [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) y [elevenlabs/skills](https://github.com/elevenlabs/skills). Los fotogramas de referencia pertenecen a sus autores y están solo como referencia de estilo.
