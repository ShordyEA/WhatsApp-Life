
# **📱 WhatsApp Life**

### ***Creamos soluciones personalizadas***

**WhatsApp Life** (by LyCodeLife) es una solución de escritorio avanzada para la automatización de envíos masivos por WhatsApp. Diseñada con una interfaz premium e intuitiva, permite gestionar campañas de mensajería en cadena, adjuntar múltiples archivos y administrar bases de datos de contactos sin depender de la API oficial, operando directamente sobre WhatsApp Web.

## **🚀 ¡Pruébalo ahora mismo\! (Versión Preconfigurada)**

¿No quieres lidiar con instalaciones de Python o dependencias? Hemos preparado un paquete completo para que no pierdas tiempo. Solo descarga, descomprime y empieza a testear inmediatamente:

🔥 [**👉 DESCARGAR VERSIÓN LISTA PARA USAR (MediaFire) 👈**](#bookmark=id.aa87nwfxkzbq) 🔥

*(El paquete incluye el ejecutable, entorno preconfigurado y Chromium portable para garantizar máxima compatibilidad).*

## **✨ Características Principales**

* **Secuencias de Mensajes (Campañas):** Configura múltiples pasos para cada contacto (ej. Mensaje 1 \+ Imágenes ➡️ Pausa ➡️ Mensaje 2).  
* **Soporte Multimedia Avanzado:** Envía texto, imágenes (.jpg, .png), videos (.mp4) y documentos (.pdf, .xlsx) en un solo flujo.  
* **Gestor de Contactos Integrado:** Importa listas desde Excel, crea plantillas de envío, y edita o elimina contactos directamente desde la interfaz.  
* **Dashboard en Tiempo Real:** Monitorea el estado de la campaña con tarjetas estadísticas (Enviados, Pendientes, Fallidos) y un registro de sistema (log) detallado.  
* **Persistencia Inteligente:** Guarda automáticamente tus listas personalizadas, el historial de envíos y la sesión de WhatsApp para no tener que escanear el código QR en cada uso.

## **🛡️ ¿Cómo reduce el riesgo de Ban?**

WhatsApp Life incorpora un "Motor de Comportamiento Humano" diseñado específicamente para mitigar los bloqueos algorítmicos de WhatsApp. Esto se logra mediante simulaciones orgánicas:

1. **Tiempos de Tipeo Dinámicos:** Los mensajes no se envían de golpe. El software simula la velocidad de escritura humana, insertando pausas aleatorias (0.5s \- 1.5s) entre líneas y mensajes.  
2. **Pausas Inter-Mensajes Naturales:** El tiempo de espera entre el envío a un contacto y al siguiente varía de forma aleatoria (entre 3 y 6 segundos), evitando el patrón robótico de envíos con tiempos exactos.  
3. **Descansos Humanos (Break Limits):** Después de procesar un lote de contactos (aleatoriamente entre 10 y 15), el bot toma un "descanso" prolongado (20 a 40 segundos) simulando que el usuario se ha levantado por un café o está leyendo otras conversaciones.  
4. **Uso de Perfiles de Chrome Locales:** Al aislar la sesión en un directorio de usuario (chrome\_session), WhatsApp detecta un navegador persistente y confiable, en lugar de un inicio de sesión anónimo y nuevo en cada ejecución.

**⚠️ Nota de Responsabilidad:** Ningún software de automatización web es 100% inmune a baneos si se utiliza para hacer SPAM agresivo. Se recomienda enviar mensajes a bases de datos *opt-in* (clientes que esperan recibir información) y calentar los números nuevos antes de lanzar campañas masivas.

## **⚙️ Instalación y Uso (PC)**

### **1\. Requisitos Previos**

* Tener instalado [Python 3.8 o superior](https://www.python.org/downloads/). (Asegúrate de marcar la casilla *"Add Python to PATH"* durante la instalación).  
* **Versión específica de Chrome:** Es indispensable contar con una versión de Google Chrome específica y compatible con el entorno, o en su defecto, utilizar un ejecutable portable de Chromium para evitar fallos por actualizaciones automáticas del navegador.

### **2\. Preparar el Entorno**

Clona o descarga este repositorio en tu computadora. Abre una terminal (Símbolo del sistema o PowerShell) en la carpeta del proyecto y ejecuta el siguiente comando para instalar las dependencias:

pip install selenium webdriver-manager openpyxl PyQt6

### **3\. Ejecutar el Software**

Una vez instaladas las dependencias, inicia el programa ejecutando el siguiente comando:

python whats.py

### **4\. Flujo de Trabajo (Quick Start)**

1. **Configura el Navegador:** La primera vez que presiones "Iniciar Campaña", el sistema te pedirá localizar tu navegador (Chrome o Chromium compatible).  
2. **Carga tus Contactos:** Ve a la pestaña **Gestor Contactos**, haz clic en *Importar Excel* o añade contactos manualmente. Guarda tu selección como una plantilla.  
3. **Diseña la Campaña:** Vuelve al **Panel Principal**. Selecciona tu plantilla de destinatarios. Escribe tu mensaje y añade los adjuntos. Utiliza el botón \+ para añadir más mensajes a la cadena si lo necesitas.  
4. **Escanea el QR (Solo la primera vez):** Al iniciar el bot, se abrirá una ventana de Chrome con WhatsApp Web. Escanea el código QR con tu teléfono. Las futuras sesiones recordarán tu inicio de sesión.  
5. **Deja que la magia ocurra:** Observa la consola en vivo y las estadísticas mientras WhatsApp Life hace el trabajo por ti.
