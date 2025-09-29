# 🚀 CONFIGURACIÓN DE RENDER - JP_LegalBot

## ⚡ Variables de Entorno Requeridas

Configura estas variables de entorno en el panel de Render:

### 🔑 Azure OpenAI (OBLIGATORIAS)
```
AZURE_OPENAI_ENDPOINT=https://legalbotfoundry.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=lKAUXrhG1ttvP3Q9TnQJcO3GlgJhOs7sQakiTwLU6d51Nuh7ckMoJQQJ99BIACHYHv6XJ3w3AAAAACOGPaZO
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
```

### 🔐 Seguridad
```
SECRET_KEY=jp_legalbot_secret_key_2025_azure
FLASK_ENV=production
FLASK_DEBUG=false
```

### 🌐 Configuración del Servidor
```
PORT=10000
HOST=0.0.0.0
```

### 📊 Opcionales (Para funcionalidades avanzadas)
```
OPENAI_TIMEOUT=30
MAX_REQUESTS_PER_MINUTE=30
SESSION_TIMEOUT_HOURS=8
```

## 🔧 Pasos para Configurar en Render

1. **Ve a tu servicio en Render Dashboard**

2. **Navega a la pestaña "Environment"**

3. **Agrega cada variable de entorno:**
   - Clic en "Add Environment Variable"
   - Ingresa el nombre (ej: `AZURE_OPENAI_ENDPOINT`)
   - Ingresa el valor correspondiente
   - Clic en "Save Changes"

4. **Variables CRÍTICAS que DEBES configurar:**
   ```
   AZURE_OPENAI_ENDPOINT=https://legalbotfoundry.cognitiveservices.azure.com/
   AZURE_OPENAI_KEY=lKAUXrhG1ttvP3Q9TnQJcO3GlgJhOs7sQakiTwLU6d51Nuh7ckMoJQQJ99BIACHYHv6XJ3w3AAAAACOGPaZO
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
   SECRET_KEY=jp_legalbot_secret_key_2025_azure
   FLASK_ENV=production
   PORT=10000
   ```
   SECRET_KEY=[genera una clave aleatoria de 32+ caracteres]
   ```

5. **Después de agregar todas las variables:**
   - Clic en "Manual Deploy" para redesplegar
   - O hacer un nuevo commit al repositorio

## ⚠️ IMPORTANTE

- **NO subas las claves al código fuente**
- Usa solo variables de entorno en Render
- La clave `AZURE_OPENAI_KEY` debe ser válida y activa
- El endpoint debe ser exacto (con / al final)

## 🧪 Verificación

Una vez configurado, el sistema debería mostrar:
```
✅ Cliente Azure OpenAI configurado correctamente
   📡 Endpoint: https://legalbotfoundry.cognitiveservices.azure.com/
   🚀 Deployment: gpt-4.1
```

En lugar de:
```
❌ Configuración Azure OpenAI faltante o incompleta
```

## 🔄 Si hay problemas

1. Verifica que todas las variables estén configuradas
2. Revisa los logs de Render para errores específicos
3. Asegúrate de que la clave Azure OpenAI sea válida
4. Verifica que el deployment `gpt-4.1` esté activo en Azure