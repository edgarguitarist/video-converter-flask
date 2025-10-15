# 📝 CHANGELOG - Cambio de Rutas de Salida CLI

## 🗓️ Fecha: 14 de Octubre, 2025

### 🎯 **Cambio Implementado**

**Comportamiento de rutas de salida por defecto en CLI**

- **❌ Anterior:** Archivos CLI se guardaban en `./converted/`
- **✅ Nuevo:** Archivos CLI se guardan en la misma carpeta del archivo de entrada

### 🔧 **Archivos Modificados**

1. **`app.py`**

   - Función `main()`: Lógica de ruta de salida CLI
   - Texto de ayuda: Actualizado para reflejar nuevo comportamiento
   - Sin cambios en interfaz web

2. **`README.md`**

   - Ejemplos CLI actualizados
   - Nueva sección "Comportamiento de Rutas de Salida"
   - Estructura del proyecto actualizada

3. **`USAGE.md`**

   - Ejemplos de conversión básica actualizados
   - Sección de gestión de archivos actualizada

4. **`DOCUMENTATION-STATUS.md`**
   - Referencias actualizadas al nuevo comportamiento

### 💡 **Justificación del Cambio**

#### **Problemas del comportamiento anterior:**

- Los usuarios esperaban que los archivos aparecieran junto al original
- Necesidad de buscar en carpeta `./converted/`
- Menos intuitivo para uso CLI

#### **Ventajas del nuevo comportamiento:**

- ✅ **Intuitivo**: Archivo convertido aparece donde el usuario lo espera
- ✅ **Organizado**: Mantiene archivos relacionados juntos
- ✅ **Consistente**: Comportamiento típico de herramientas CLI
- ✅ **Flexible**: Web mantiene su organización propia

### 📊 **Comparación de Comportamientos**

| Modo           | Entrada              | Salida (Anterior)                | Salida (Nueva)                                   |
| -------------- | -------------------- | -------------------------------- | ------------------------------------------------ |
| **CLI**        | `C:\Videos\clip.mov` | `./converted/clip.mp4`           | `C:\Videos\clip.mp4`                             |
| **PowerShell** | `D:\Movies\film.avi` | `./converted/film.mp4`           | `D:\Movies\film.mp4`                             |
| **Web**        | Upload via browser   | `./converted/film-timestamp.mp4` | `./converted/film-timestamp.mp4` _(sin cambios)_ |

### 🧪 **Ejemplos de Uso Actualizado**

#### **CLI Python:**

```powershell
# Nuevo comportamiento
python app.py --mp4 "C:\Videos\vacation.mov"
# Resultado: C:\Videos\vacation.mp4

# Con ruta específica (sin cambios)
python app.py --mp4 "video.mov" "C:\Output\converted.mp4"
# Resultado: C:\Output\converted.mp4
```

#### **PowerShell Functions:**

```powershell
# Nuevo comportamiento
cvt-mp4 "D:\MyVideos\clip.webm"
# Resultado: D:\MyVideos\clip.mp4

# Con ruta específica (sin cambios)
cvt-mkv "input.avi" "C:\Exports\output.mkv"
# Resultado: C:\Exports\output.mkv
```

#### **Interfaz Web (sin cambios):**

```
Archivo subido → ./converted/archivo-timestamp.formato
```

### ⚠️ **Consideraciones de Migración**

#### **Para usuarios existentes:**

- **Scripts automatizados**: Verificar que no dependan de `./converted/`
- **Workflows**: Actualizar referencias a ubicaciones de salida
- **Documentación**: Actualizar referencias internas

#### **Compatibilidad:**

- ✅ **Rutas específicas**: Sin cambios (segundo parámetro)
- ✅ **Interfaz web**: Sin cambios
- ✅ **Funciones PowerShell**: Comportamiento mejorado
- ⚠️ **Scripts CLI**: Pueden requerir ajustes menores

### 🔄 **Implementación Técnica**

#### **Código anterior:**

```python
# Usar directorio converted por defecto
input_path_obj = Path(input_file)
converted_dir = os.path.join(os.getcwd(), 'converted')
output_filename = f"{input_path_obj.stem}.{target_format}"
output_path = os.path.join(converted_dir, output_filename)
```

#### **Código nuevo:**

```python
# Usar la misma carpeta del archivo de entrada
input_path_obj = Path(input_file)
output_filename = f"{input_path_obj.stem}.{target_format}"
output_path = input_path_obj.parent / output_filename
output_path = str(output_path)  # Convertir a string
```

### ✅ **Estado de Implementación**

- [x] Código actualizado en `app.py`
- [x] Documentación actualizada (`README.md`, `USAGE.md`)
- [x] Ejemplos actualizados
- [x] Ayuda CLI actualizada
- [x] Scripts de prueba creados

### 🚀 **Próximos Pasos**

1. **Probar** el nuevo comportamiento con archivos reales
2. **Validar** que la interfaz web sigue funcionando correctamente
3. **Actualizar** cualquier script de automatización personal
4. **Comunicar** el cambio a usuarios del proyecto

---

**💡 Este cambio mejora significativamente la experiencia de usuario CLI manteniendo la organización de la interfaz web.**
