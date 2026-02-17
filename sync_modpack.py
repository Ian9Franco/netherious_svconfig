import os
import shutil
import zipfile

# CONFIGURACIÓN DE RUTAS
SOURCE_DIR = r"D:\.mine\mo\.Netherious.core\1.20.1"
TARGET_MODS_DIR = r"c:\Code Projects\netherious_svconfig\Netherious-Modpack\mods"
PROJECT_ROOT = r"c:\Code Projects\netherious_svconfig"
MODPACK_FOLDER = os.path.join(PROJECT_ROOT, "Netherious-Modpack")
OUTPUT_ZIP = os.path.join(PROJECT_ROOT, "modpack.zip")

# CONFIGURACIÓN DE EXCLUSIONES PARA BUSQUEDA DE MODS
ROOT_EXCLUSIONS = [
    "DEL", "updates", ".Netherious", ".server", "datapacks", "inbox", "zip",
    "resourcepacks", "shaderpacks", "kube", "config" # Ignoramos estas en el origen ya que se gestionan manual en el repo
]

# Carpetas a ignorar dentro de SOURCE_DIR/.local
LOCAL_EXCLUSIONS = ["matic", "fab"]

def clean_folder(folder_path):
    """Limpia una carpeta manteniendo el .gitkeep."""
    print(f"Limpiando carpeta de mods: {folder_path}")
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if item != ".gitkeep":
                if os.path.isfile(item_path): os.remove(item_path)
                elif os.path.isdir(item_path): shutil.rmtree(item_path)

def collect_mods():
    """Busca y copia los .jar aplicando las reglas de exclusión."""
    mods_copied = 0
    clean_folder(TARGET_MODS_DIR)
    
    for item in os.listdir(SOURCE_DIR):
        item_path = os.path.join(SOURCE_DIR, item)
        
        # Solo procesamos carpetas
        if not os.path.isdir(item_path):
            continue
            
        # Saltamos carpetas excluidas
        if item in ROOT_EXCLUSIONS:
            continue

        if item == ".local":
            print(f"-> Procesando .local...")
            for sub in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub)
                
                # Ignoramos carpetas específicas de .local
                if os.path.isdir(sub_path) and sub in LOCAL_EXCLUSIONS:
                    continue
                
                # Jars directos en .local
                if os.path.isfile(sub_path) and sub.endswith(".jar"):
                    shutil.copy2(sub_path, TARGET_MODS_DIR)
                    mods_copied += 1
                
                # Jars en subcarpetas de .local
                elif os.path.isdir(sub_path):
                    for file in os.listdir(sub_path):
                        if file.endswith(".jar"):
                            shutil.copy2(os.path.join(sub_path, file), TARGET_MODS_DIR)
                            mods_copied += 1
        else:
            # Procesamos las categorías (Criaturas, Enemigos, etc.)
            print(f"-> Procesando categoría de mods: {item}")
            for root, dirs, files in os.walk(item_path):
                for file in files:
                    if file.endswith(".jar"):
                        shutil.copy2(os.path.join(root, file), TARGET_MODS_DIR)
                        mods_copied += 1
                        
    print(f"\n¡Éxito! Se recolectaron {mods_copied} mods.")

def create_zip():
    """Comprime TODO el contenido de Netherious-Modpack en modpack.zip"""
    print(f"\nGenerando/Actualizando {OUTPUT_ZIP}...")
    # 'w' sobreescribe el archivo si existe
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(MODPACK_FOLDER):
            for file in files:
                # No incluimos los .gitkeep en el zip final del usuario
                if file == ".gitkeep": continue
                
                file_path = os.path.join(root, file)
                # Ruta relativa para que dentro del zip sea mods/..., config/..., etc.
                arcname = os.path.relpath(file_path, MODPACK_FOLDER)
                zipf.write(file_path, arcname)
    print(f"¡Zip generado correctamente con todo el contenido del repo!")

if __name__ == "__main__":
    collect_mods()
    
    choice = input("\n¿Deseas generar el archivo modpack.zip ahora? (s/n): ").lower()
    if choice == 's':
        create_zip()
    else:
        print("\nProceso terminado.")
