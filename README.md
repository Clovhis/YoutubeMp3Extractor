# YouTube MP3 Cutter

Aplicación de escritorio en Python para descargar un fragmento de un video de YouTube y guardarlo como archivo MP3.

## ¿Qué hace la aplicación?

1. Permite ingresar la URL de un video de YouTube.
2. Se elige un tiempo de inicio y de fin (en formato `mm:ss` o `hh:mm:ss`).
3. Al presionar el botón, descarga solo ese fragmento utilizando `yt-dlp`.
4. Convierte el audio a `mp3` mediante `ffmpeg`.
5. Guarda el resultado en `C:\YoutubeCuts` (se crea automáticamente si no existe).

El nombre del archivo incluye parte del título del video y la fecha/hora de descarga.

## Requisitos para ejecutarla

- **Sistema operativo:** Windows.
- **Python 3.8+** (si se ejecuta el código fuente).
- `yt-dlp` y `ffmpeg` disponibles en el `PATH` (al compilar con PyInstaller se pueden incluir).

## Cómo usarla

```bash
python app.py
```

1. Ingresa la URL de YouTube.
2. Especifica el tiempo de inicio y fin del fragmento.
3. Presiona **Download clip** y espera el mensaje de éxito.

El archivo MP3 se guardará dentro de `C:\YoutubeCuts`.

## Cómo compilarla a EXE

1. Instala las dependencias:
   ```bash
   pip install yt-dlp pyinstaller
   ```
2. Ejecuta PyInstaller:
   ```bash
   pyinstaller --onefile --noconsole app.py
   ```
3. El ejecutable aparecerá en la carpeta `dist/`. Se puede distribuir sin necesidad de instalación.

## GitHub Actions

El repositorio incluye un workflow que se ejecuta al hacer push a cualquier rama que comience con `feature/`.

El workflow realiza lo siguiente:

1. Descarga el código y configura Python en un runner de Windows.
2. Instala `yt-dlp` y `pyinstaller`.
3. Compila la aplicación a un único `exe` con PyInstaller.
4. Empaqueta el ejecutable en un archivo `zip`.
5. Crea un release automático en GitHub y adjunta el `zip` generado.
