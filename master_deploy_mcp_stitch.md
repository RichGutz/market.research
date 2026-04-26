# Guía Maestra: Despliegue y Configuración de Stitch MCP

Esta guía documenta el proceso técnico realizado para habilitar el Model Context Protocol (MCP) de Google Stitch en el entorno de desarrollo, superando las limitaciones de detección automática de gcloud en Windows.

## Estado Actual
- **Proyecto Gcloud**: `mcp-stitch-491400`
- **Estado de Conexión**: ✓ Connected (Verificado 2026-03-26)
- **Solución Técnica Aplicada**: Corrección de Project ID en `.claude.json` + Patch x86 en `index.js`.

### Hallazgo Crítico (Bug Solucionado)
El servidor `stitch-mcp-auto` tenía un bug en Windows que omitía la carpeta `Program Files (x86)` al buscar el binario de `gcloud`. Esto se solucionó:
1. Creando un `fixed_stitch_launcher.js` para la sesión inicial.
2. Aplicando un parche permanente en `C:\Users\rguti\AppData\Local\npm-cache\_npx\06384f72c3f8ab7f\node_modules\stitch-mcp-auto\index.js`.

### Pasos Finales de Éxito
1. Habilitación de API **Cloud Resource Manager** (Crítico para validación).
2. Habilitación de API **Stitch** y **Service Usage**.
3. Uso del proyecto `mcp-stitch-491400`.
4. Finalización del Wizard en el puerto 8086.

## 1. Infraestructura: Google Cloud SDK (gcloud CLI)

Para que Stitch MCP funcione, es obligatorio tener el SDK de Google Cloud instalado.

### Pasos de Instalación:
1. **Descarga**: Se utilizó el instalador bootstrapping oficial de Google:
   `https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe`
2. **Instalación Silenciosa**: Se ejecutó mediante el flag `/S` para evitar interrupciones visuales:
   ```powershell
   .\GoogleCloudSDKInstaller.exe /S /allusers /noreporting
   ```
3. **Ubicación**: El binario quedó instalado en:
   `C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd`

## 2. Autenticación y Selección de Proyecto

El acceso a los recursos de diseño de Stitch requiere una identidad de Google Cloud activa.

1. **Login**: Ejecutar `gcloud init` interactivamente.
2. **Cuenta**: Se utilizó `rich@kaizencapital.pe`.
3. **Proyecto**: Se seleccionó el proyecto específicamente creado para Stitch:
   - **Project ID**: `mcp-stitch-491400`
   - **Nombre**: `MCP-STITCH`

## 3. El Bypass Manual (Solución al error de PATH)

El instalador automático `npx stitch-mcp-auto-setup` suele fallar en Windows al no detectar el comando `gcloud` globalmente (incluso si está instalado).

### La Solución: Inyección Directa en `.claude.json`
Se editó el archivo de configuración maestra de Claude CLI ubicado en `C:\Users\rguti\.claude.json`.

Se insertó el siguiente bloque dentro de la sección de `projects` correspondiente a `Tienda.APPLE.PS5`:

```json
"mcpServers": {
  "stitch": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "stitch-mcp-auto"
    ],
    "env": {
      "GOOGLE_CLOUD_PROJECT": "mcp-stitch-491400"
    }
  }
}
```

## 4. Verificación de Operatividad

Para confirmar que el "puente" (bridge) está vivo, se puede verificar en la terminal de Claude con:

```bash
# Debería listar los recursos de Stitch si el server está configurado
claude mcp list
```

---
## 5. MANTENIMIENTO TÉCNICO: Protocolo de Conexión "Cero Dudas" para Claude

> [!IMPORTANT]
> **SI LA CONEXIÓN FALLA O DICE 'PROJECT NOT FOUND', SIGUE ESTOS PASOS EXACTOS:**

### A. Archivo de Configuración de Claude
La configuración **NO** está en archivos del repositorio, sino en el perfil del usuario:
- **Ruta**: `C:\Users\rguti\.claude.json`
- **Sección Crítica**: `projects > C:/Users/rguti/Tienda.APPLE.PS5 > mcpServers > stitch`

### B. El Project ID Correcto
El único ID válido es **`mcp-stitch-491400`**. Cualquier referencia a `mcp-stitch-fresh` u otros nombres debe ser corregida inmediatamente en el `.claude.json`.

### C. Autenticación de Google Cloud (Gcloud Auth)
Claude debe verificar que el sistema esté logueado con la cuenta autorizada:
- **Cuenta**: `rich@kaizencapital.pe`
- **Comando de Verificación**: `gcloud auth list` (Asegurarse de que el asterisco `*` esté en la cuenta mencionada).
- **Comando de Proyecto Activo**: `gcloud config set project mcp-stitch-491400`

### D. Verificación del Servidor MCP
Desde el terminal de Claude Code, ejecuta:
```bash
claude mcp list
```
Deberías ver: `stitch: npx -y stitch-mcp-auto - ✓ Connected`. Si aparece un tache `✗`, verifica que el entorno tenga acceso a `npx` y que `GOOGLE_CLOUD_PROJECT` esté en el `env` del JSON.

---
## 6. Integración Programática (Bridge para Gemini)

Para que un agente de IA pueda realizar consultas directas a Stitch y obtener geometrías (shards), se ha implementado una arquitectura de "Puente" que supera la interactividad involuntaria del servidor.

### A. El Lanzador Fijo (`fixed_stitch_launcher.js`)
Ubicación: `C:\Users\rguti\Tienda.APPLE.PS5\fixed_stitch_launcher.js`
Este script es **vital** porque:
1. Inyecta el PATH de `gcloud` (x86) dinámicamente.
2. Carga Stitch directamente desde la caché de `npx` para evitar latencias de red.
3. Asegura que `GOOGLE_CLOUD_PROJECT` sea siempre `mcp-stitch-491400`.

### B. El Bridge Python (`stitch_bridge.py`)
Ubicación: `C:\Users\rguti\Tienda.APPLE.PS5\stitch_bridge.py`
Proporciona una interfaz limpia para llamar a herramientas de Stitch:
```bash
# Ejemplo para listar herramientas disponibles
python stitch_bridge.py listTools "{}"

# Ejemplo para generar shards (si la herramienta está activa)
python stitch_bridge.py stitch_iphone_16 "{ \"fidelity\": \"ultra\" }"
```

### C. Protocolo de "Mano a Mano" (Next Gemini)
1. **Verificar PATH**: gcloud DEBE estar en `C:\Program Files (x86)\Google\Cloud SDK\...`
2. **Setup Wizard**: Si el bridge devuelve "No response", ejecuta `node fixed_stitch_launcher.js` manualmente una vez para completar cualquier re-autenticación necesaria en la terminal.
3. **Proyecto**: NO usar `mcp-stitch-fresh`. Usar siempre **`mcp-stitch-491400`**.

---
**Actualización realizada por Antigravity (2026-03-26) para el próximo GEMINI.**
