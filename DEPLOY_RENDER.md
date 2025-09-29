# 🚀 Deployment en Render - JP_IA

## Instrucciones para Deploy en Render.com

### 1. Preparación del Repositorio
✅ **Ya completado**: Todos los archivos necesarios están incluidos

### 2. Crear Servicio en Render

1. **Conectar GitHub**:
   - Ve a [render.com](https://render.com)
   - Connect Repository: `mmelendezJPPR/JP-LegalBot_V4`

2. **Configurar el Servicio**:
   - **Type**: Web Service
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile` (automático)
   - **Region**: Oregon (US West)

### 3. Variables de Entorno REQUERIDAS

Configura estas variables en Render Dashboard > Environment:

```bash
# AZURE OPENAI (OBLIGATORIO)
AZURE_OPENAI_ENDPOINT=https://legalbotfoundry.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=[tu_clave_azure_openai_aqui]
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1

# CONFIGURACIÓN DE PRODUCCIÓN
FLASK_ENV=production
FLASK_DEBUG=false
PORT=10000

# SEGURIDAD
SECRET_KEY=[genera_una_clave_secreta_larga_y_aleatoria]

# CONFIGURACIÓN OPCIONAL
OPENAI_TIMEOUT=30
MAX_REQUESTS_PER_MINUTE=30
SESSION_TIMEOUT_HOURS=8
```

### 4. Configuración del Build

Render detectará automáticamente el `Dockerfile` y:
- ✅ Instalará Python 3.11
- ✅ Instalará dependencias desde requirements.txt
- ✅ Configurará SQLite automáticamente
- ✅ Creará las bases de datos necesarias

### 5. Health Check

Render verificará automáticamente la salud de tu aplicación usando:
- **Endpoint**: `GET /health`
- **Respuesta esperada**: Status 200 con `{"status": "healthy"}`

### 6. Acceso al Sistema

Una vez desplegado:
- **URL**: `https://tu-app.onrender.com`
- **Usuario**: `admin@juntaplanificacion.pr.gov`
- **Contraseña**: `admin123`

### 7. Características del Deploy

✅ **Base de Datos**: SQLite (sin configuración adicional)
✅ **Autenticación**: SQLite-based con usuarios locales
✅ **Sistema Híbrido**: Motor de IA con búsqueda híbrida
✅ **Base de Conocimiento**: 1,416 documentos legales indexados
✅ **HTTPS**: Automático en Render
✅ **Escalado**: Automático
✅ **Health Checks**: Automáticos cada 30 segundos

### 8. Verificación del Deploy

Después del deployment, verifica:

1. **Health Check**: `https://tu-app.onrender.com/health`
2. **Login**: `https://tu-app.onrender.com/login`
3. **Test Endpoint**: `https://tu-app.onrender.com/test-endpoint`

### 9. Solución de Problemas

#### Error: "Application failed to start"
- Verificar que todas las variables de entorno estén configuradas
- Revisar logs en Render Dashboard

#### Error: "Database not found"
- ✅ **Solucionado**: Dockerfile inicializa bases de datos automáticamente

#### Error: "Azure OpenAI connection failed"
- Verificar que `AZURE_OPENAI_KEY` sea correcta
- Confirmar que el endpoint `https://legalbotfoundry.cognitiveservices.azure.com/` esté accesible

#### Timeout en primera carga
- Normal: La aplicación inicializa bases de datos en el primer inicio
- Esperar 2-3 minutos para la primera carga

### 10. Optimizaciones para Render

- **Memory**: ~200MB RAM
- **CPU**: Bajo uso
- **Storage**: ~50MB para bases de datos
- **Cold starts**: ~30 segundos (normal para apps con SQLite)

---

## 🎯 Checklist Final

- [ ] Repositorio conectado: `mmelendezJPPR/JP-LegalBot_V4`
- [ ] Runtime: Docker
- [ ] Region: Oregon (US West)
- [ ] Variables de entorno configuradas
- [ ] Health check funcionando: `/health`
- [ ] Login funcionando con credenciales de prueba

**¡Tu JP-LegalBot estará listo en Render! 🚀**

### 8. Logs Esperados

```
✅ Cliente OpenAI configurado correctamente
🔄 SQL Server no disponible, usando autenticación local
✅ Sistema Híbrido JP_IA v3.0 importado correctamente
✅ Cargados 12 tomos para análisis experto
🌐 Puerto: 10000
```

### 9. Tiempo de Deploy

- **Primera vez**: ~5-8 minutos (install drivers)
- **Updates**: ~2-3 minutos
- **Cold starts**: ~30 segundos

¡El sistema estará listo para usar! 🎉