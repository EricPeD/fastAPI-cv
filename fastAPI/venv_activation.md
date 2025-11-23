# Activación del Entorno Virtual (venv)

Para asegurar un desarrollo consistente y aislado de las dependencias del sistema, es fundamental trabajar dentro de un entorno virtual de Python.

## 1. Crear el Entorno Virtual (si aún no lo has hecho)

Si todavía no has creado un entorno virtual para este proyecto, puedes hacerlo con el siguiente comando en la raíz del proyecto (donde se encuentra `requirements.txt`):

```bash
python3 -m venv venv
```
Esto creará una carpeta llamada `venv` que contendrá tu entorno virtual aislado.

## 2. Activar el Entorno Virtual

Para activar el entorno virtual, usa el comando apropiado para tu sistema operativo y shell:

*   **En Linux o macOS (Bash/Zsh):**
    ```bash
    source venv/bin/activate
    ```

*   **En Windows (Command Prompt):**
    ```cmd
    venv\Scripts\activate.bat
    ```

*   **En Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

Una vez activado, verás `(venv)` al principio de tu prompt de terminal, indicando que estás operando dentro del entorno virtual.

## 3. Desactivar el Entorno Virtual

Cuando hayas terminado de trabajar en el proyecto y quieras salir del entorno virtual, simplemente ejecuta:

```bash
deactivate
```
Tu prompt volverá a su estado normal.

## 4. Instalación de Dependencias

Con el entorno virtual activado, puedes instalar todas las dependencias del proyecto listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

Esto instalará las librerías necesarias dentro de tu entorno virtual, sin afectar las librerías globales de tu sistema.

---
