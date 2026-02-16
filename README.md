# Netherious Server Configuration (Repo Mode)

Este repositorio contiene la configuración, mods y resource packs del servidor **Netherious**, sincronizados mediante **AutoModpack**.

## Estructura del Modpack
- **mods/**: Todos los archivos `.jar` necesarios para el cliente y el servidor.
- **config/**: Archivos de configuración críticos (Default Options, Resource Pack Overrides).
- **resourcepacks/**: Packs de texturas obligatorios y recomendados.
- **manifest.json**: Metadatos del modpack.

## Cómo Actualizar
1. Realiza los cambios necesarios en las carpetas locales.
2. Sube los archivos al repositorio.
3. Crea un nuevo **Release** en GitHub con el nombre de la versión (ej. `v1.0`).
4. Sube el contenido de `Netherious-Modpack/` en un archivo `.zip` llamado `modpack.zip` al release.
5. El servidor detectará el último release y sincronizará con los clientes.

## Configuración del Servidor
Asegúrate de que el archivo `automodpack-server.json` en tu servidor apunte a este repositorio:
```json
{
  "modpackUrl": "https://github.com/Ian9Franco/netherious_svconfig/releases/latest/download/modpack.zip"
}
```

---
*Generado automáticamente para el servidor Netherious.*
