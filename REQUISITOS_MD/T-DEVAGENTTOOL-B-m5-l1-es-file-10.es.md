# **La solución: Diseño de instrucciones estratégicas** 

## **Instrucciones que guían el uso de una herramienta** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo hacer referencia a una herramienta en las instrucciones del agente</u>_ 

### **De la documentación del ADK:** 

“En las instrucciones de un agente, puedes hacer referencia directa a una herramienta utilizando el nombre de la función... Es fundamental instruir claramente al agente sobre cómo manejar los diferentes valores de devolución que una herramienta podría producir”. 

### **Qué proporcionan las instrucciones estratégicas:** 

- ✅ **Guía de selección de herramientas** : cuándo usar cada herramienta 

   - ✅ **Manejo de errores** : cómo responder a los diferentes tipos de errores 

- 

   - ✅ **Lógica secuencial** : en qué orden llamar a las herramientas 

- 

   - ✅ **Integración de resultados** : cómo usar los resultados de las herramientas 

- 

   - ✅ **Rutas de derivación** : qué hacer cuando las herramientas no pueden resolver el problema 

- 

**Principio clave:** Las instrucciones deben centrarse en **cuándo** y **cómo** usar las herramientas, no solo en **qué** hacen (las cadenas de documentación se encargan de eso). 

# **Conceptos básicos** 

## **1. Patrones de instrucciones para el uso de herramientas** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo hacer referencia a una</u>_ 

_<u>herramienta en las instrucciones del agente</u>_ 

### **Patrón 1: Guía de selección de herramientas** 

Indica al agente cuándo utilizar cada herramienta: 

instruction=""" 

Eres un agente de asistencia al cliente. 

Guía de selección de herramientas: 

- Utiliza check_order_status cuando el cliente pregunte sobre su pedido. 

- Utiliza process_refund cuando el cliente solicite un reembolso. 

- Utiliza lookup_customer cuando necesites información de la cuenta del cliente. 

Verifica siempre la información antes de tomar medidas. """ 

### **Patrón 2: Manejo de resultados** 

Dile al agente cómo manejar los diferentes resultados: 

instruction=""" 

Cuando utilices check_order_status, sigue estos pasos: 

1. Llama a la herramienta con el ID de pedido. 

2. Si el estado es “success”: 

- Informa al cliente el estado del pedido actual. 

- Proporciona información de seguimiento si está disponible. 

3. Si el estado es “error” con error_type “not_found”: 

- Pídele al cliente que verifique el ID de pedido. 

- Ofrece realizar la búsqueda por correo electrónico en su lugar 

4. Si el estado es 'error' con error_type 'invalid_format': 

- Explica que los IDs de pedido deben comenzar con “ORD”. 

- Solicita el formato correcto. """ 

### **Patrón 3: Uso secuencial de herramientas** 

Guía al agente a través de flujos de trabajo de varios pasos: 

instruction=""" Para las solicitudes de reembolso, sigue estos pasos: 1. Primero, usa check_order_status para verificar que el pedido existe. 2. Si no se encuentra el pedido, detente y solicita al cliente el ID de pedido correcto. 

3. Si se encuentra el pedido, utiliza process_refund con order_id y reason. 4. Si el reembolso es exitoso, confirma el importe del reembolso y el número de referencia. 

5. Si el reembolso no se realiza, explica por qué y ofrece derivar el caso al supervisor. """ 

### **Ejemplo completo:** 

from google.adk.agents import LlmAgent 

agent = LlmAgent( model='gemini-2.5-flash', instruction=""" Eres un agente de asistencia al cliente servicial. 

## Selección de herramientas - Utiliza check_order_status cuando el cliente pregunte sobre el estado del pedido. - Utiliza process_refund para solicitudes de reembolso. - Utiliza escalate_to_supervisor para problemas complejos. ## Flujos de trabajo ### Consulta del estado del pedido: 

1. Saluda al cliente. 

2. Utiliza check_order_status con el ID de pedido. 

3. Si no hay errores, proporciona el estado de forma clara. 

4. En caso de errores, orienta al cliente hacia la información correcta. 

### Solicitud de reembolso: 

1. Expresa empatía. 

2. Primero, verifica el pedido con check_order_status. 

3. Si existe un pedido, utiliza process_refund. 

4. Confirma los detalles del reembolso al cliente. 

## Manejo de errores 

- Errores “not_found”: solicita al cliente que verifique la información. - Errores “invalid_format”: explica el formato correcto. - Errores inesperados: utiliza escalate_to_supervisor. 

Sé siempre amable y profesional. """, 

tools=[check_order_status, process_refund, escalate_to_supervisor] ) 

### **Qué se debe tener en cuenta:** 

- **Secciones organizadas:** selección de herramientas, flujos de trabajo, manejo de errores 

- **Orientación específica:** cuándo usar cada herramienta 

- **Paso a paso:** instrucciones secuenciales claras 

- **Manejo de errores:** qué hacer para cada tipo de error 

### **Visualización del flujo de trabajo secuencial:** 

graph TD 

A[Solicitud de usuario: pedido de reembolso] --> B{Razonamiento del agente} B --> C[Herramienta: check_order_status] C --> D{¿Se encontró el pedido?} D -->|No| E[Respuesta de error:<br/>pídele al usuario que verifique] D -->|Sí| F{¿Estado de pedido?} F -->|Entregado| G[Herramienta: process_refund] 

F -->|Procesando| H[Respuesta de error:<br/>aún no se puede reembolsar] F -->|Cancelado| I[Respuesta de error:<br/>ya está cancelado] G --> J{¿Fue exitoso el reembolso?} J -->|Sí| K[Respuesta de éxito:<br/>Confirma al usuario] J -->|No| L[Herramienta: escalate_to_supervisor] H --> M[Derivación de oferta] L --> N[Supervisor asignado] 

style E fill:#ffcccc style H fill:#fff9cc style I fill:#fff9cc style K fill:#ccffcc style L fill:#ffe6cc 

_Las instrucciones estratégicas guían a los agentes a través de flujos de trabajo complejos con un manejo adecuado de errores._ 

## **2. Manejo de errores en las instrucciones** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo hacer referencia a una herramienta en las instrucciones del agente</u>_ 

### **De la documentación del ADK:** 

“Es fundamental instruir claramente al agente sobre cómo manejar los diferentes valores de devolución que una herramienta podría producir. Por ejemplo, si una herramienta devuelve un mensaje de error, tus instrucciones deben especificar si el agente debe reintentar la operación, abandonar la tarea o solicitar información adicional al usuario”. 

### **Estrategias de manejo de errores:** 

### **Estrategia 1: Vuelve a intentarlo frente a desiste** 

instruction=""" 

Lineamientos para el manejo de errores: 

Si check_order_status devuelve “temporary_failure”, haz lo siguiente: 

- Reconoce el problema ante el cliente. 

- Vuelve a intentarlo una vez después de una breve pausa. 

- Si el segundo intento falla, pide disculpas y solicita al cliente que lo intente más tarde. 

Si check_order_status devuelve “not_found”, haz lo siguiente: 

- NO vuelvas a intentarlo con el mismo ID de pedido. 

- Solicita al cliente que verifique el ID de pedido. 

- Ofrece métodos de búsqueda alternativos (por correo electrónico). 

Si check_order_status devuelve “permission_denied”, haz lo siguiente: 

- NO vuelvas a intentarlo ni busques soluciones alternativas. - Pide disculpas y utiliza escalate_to_supervisor de inmediato. """ 

### **Estrategia 2: Acciones específicas para cada error** 

def lookup_order(order_id: str) -> dict: """Busca información del pedido. Devuelve lo siguiente: dict: Información del pedido. En caso de éxito: {'status': 'success', 'order': {...}} En caso de error: {'status': 'error', 'error_type': 'not_found'/'invalid_format'/'permission_denied'} """ 

# Implementación con tipos de errores específicos pass 

agent = LlmAgent( instruction=""" Cuando utilices lookup_order, ten en cuenta lo siguiente: 

Si el tipo de error es “not_found”, haz lo siguiente: 

- `→ Di: "No pude encontrar ese pedido. ¿Podrías verificar el ID de pedido? → Ofrece realizar la búsqueda por correo electrónico o teléfono. → NO hagas suposiciones.` 

Si error_type es “invalid_format”, haz lo siguiente: 

- `→ Di: "Los IDs de pedido deben tener el formato ORD-12345".` 

- `→ Solicita al cliente que proporcione el formato correcto.` 

- `→ Muestra un ejemplo.` 

Si error_type es “permission_denied”, haz lo siguiente: 

- `→ Di: "No tengo acceso a ese pedido. Te voy a comunicar con un supervisor". → Utiliza escalate_to_supervisor de inmediato. → NO intentes enfoques alternativos.` """, 

tools=[lookup_order, escalate_to_supervisor] ) 

### **Estrategia 3: Degradación elegante** 

instruction=""" 

Este es el orden de prioridad para la búsqueda de clientes: 

1. Primero, prueba lookup_by_order_id (más rápido, más directo). 

2. Si eso falla con “not_found”, intenta con lookup_by_email. 

3. Si eso falla, intenta con lookup_by_phone. 

4. Si todas las búsquedas fallan, utiliza escalate_to_supervisor. 

En cada paso, ten en cuenta lo siguiente: 

- Explica lo que estás haciendo. 

- Solicita información de manera amable. 

- Nunca continúes sin datos válidos. """ 

**Principio clave:** los diferentes tipos de errores requieren distintas estrategias de manejo. Especifica exactamente lo que debe hacer el agente en cada caso. 

### **Árbol de decisión para el manejo de errores:** 

#### flowchart TD 

A[Error de herramienta recibido] --> B{¿Tipo de error?} B -->|temporary_failure| C[Reconoce<br/>ante el cliente] C --> D[Vuelve a intentarlo una vez] 

D --> E{¿Tuvo éxito?} 

E -->|Sí| F[Continúa con el flujo de trabajo] 

E -->|No| G[Pide disculpas y solicita que<br/>lo intente más tarde] 

B -->|not_found| H[Solicita al usuario que<br/>verifique la entrada] H --> I[Ofrece métodos<br/>de búsqueda alternativos] 

B -->|invalid_format| J[Explica el<br/>formato correcto] J --> K[Brinda<br/>ejemplos de formatos] 

B -->|permission_denied| L[Deriva el asunto<br/>de inmediato] 

B -->|system_error| M[Pide disculpas<br/>sinceramente] M --> N[Error de registro<br/>para el equipo] N --> O[Ofrece<br/>devolver la llamada] 

style L fill:#ffcccc style G fill:#fff9cc style H fill:#fff9cc style J fill:#fff9cc style M fill:#ffcccc style F fill:#ccffcc 

_Los diferentes tipos de errores requieren distintas respuestas del agente: especifica el manejo exacto en las instrucciones_ 

## **3. Patrón de agente como herramienta (vista previa)** 

_Cobertura completa: futuros cursos sobre la coordinación de varios agentes_ 

### **¿Qué es el agente como herramienta?** 

En lugar de escribir una herramienta de función, puedes utilizar otro agente especializado como herramienta. Esto permite que el agente principal delegue subtareas complejas a agentes especializados. 

### **Cuándo utilizar el agente como herramienta:** 

- ✅ **La subtarea requiere un razonamiento especializado** (no solo lógica predefinida). 

   - ✅ **Se necesitan instrucciones diferentes** para la subtarea. 

- 

   - ✅ **Flujos de trabajo complejos** dentro de la subtarea. 

- 

### **Este es un ejemplo sencillo:** 

from google.adk.agents import LlmAgent from google.adk.tools.agent_tool import AgentTool 

# Agente especializado para asistencia técnica tech_agent = LlmAgent( model='gemini-2.5-flash', name='tech_support', instruction="Eres un especialista en asistencia técnica. Diagnostica problemas y brinda una solución a estos." ) 

- # El agente principal utiliza al especialista como herramienta 

main_agent = LlmAgent( model='gemini-2.5-flash', name='customer_service', instruction="Envía los problemas técnicos a la herramienta tech_support. Aborda las preguntas generales directamente.", tools=[AgentTool(agent=tech_agent)] ) 

### **Diferencias clave:** 

|**Aspecto**|**Herramienta de función**|**Agente como herramienta**|
|---|---|---|
|**Implementa**|Lógica predefinida|Razonamiento y toma de<br>decisiones|
|**Ideal para**|Cálculos, búsquedas, llamadas a<br>la API|Subtareas complejas que<br>requieren discernimiento|
|**Ejemplo**|calculate_shipping()|Especialista en asistencia técnica|



**Nota:** La coordinación de varios agentes, los patrones de delegación y el uso avanzado del agente como herramienta se abordan en futuras lecciones sobre patrones de varios agentes. 

## **4. Prácticas recomendadas para la coordinación de herramientas** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo definir las funciones de las herramientas de manera eficaz</u>_ 

### **De la documentación del ADK:** 

“Cuando cumples con estos lineamientos, le proporcionas al LLM la claridad y la estructura que necesita para utilizar eficazmente tus herramientas de funciones personalizadas, lo que genera un comportamiento del agente más capaz y confiable”. 

### **Resumen de prácticas recomendadas:** 

### **1. Diseño de funciones** 

- # ✅ Recomendable: herramientas enfocadas y de un solo propósito def check_order_status(order_id: str) -> dict: """Solo verifica el estado del pedido.""" pass 

def cancel_order(order_id: str) -> dict: """Solo cancela el pedido.""" pass 

- # ❌ No recomendable: herramientas multipropósito que hacen demasiado def manage_order(order_id: str, action: str, params: dict) -> dict: 

"""Lo hace todo: verificar, cancelar, actualizar, etc.""" pass 

### **2. Nomenclatura clara** 

# ✅ Recomendable: patrón verbo-sustantivo, estilo descriptivo get_customer_profile() calculate_shipping_cost() send_confirmation_email() validate_coupon_code() # ❌ No recomendable: nombres poco precisos o poco claros process_data() handle_request() do_thing() execute() 

### **3. Cadenas de documentación completas** 

def process_refund(order_id: str, reason: str) -> dict: """Procesa un reembolso para el pedido de un cliente. Utiliza esta herramienta SOLO después de verificar que el pedido existe y es elegible para el reembolso. Argumentos: order_id (str): el ID de pedido (formato: ORD-12345) reason (str): motivo del cliente para solicitar el reembolso Devuelve lo siguiente: dict: resultado del procesamiento del reembolso En caso de éxito: { 'status': 'success', 'refund_amount': 99.99, 'refund_id': 'REF-67890', 'estimated_days': 5 } En caso de error: { 'status': 'error', 'error_type': 'not_eligible'/'already_refunded'/'not_found', 'error_message': 'Explicación legible por humanos' } """ pass 

### **4. Formato de devolución coherente** 

# ✅ Recomendable: patrón coherente basado en el estado def tool_1() -> dict: return {"status": "success", "data": value} # o return {"status": "error", "error_type": "specific_type", "error_message": "explanation"} 

def tool_2() -> dict: return {"status": "success", "result": value} # o return {"status": "error", "error_type": "specific_type", "error_message": "explanation"} # ❌ No recomendable: devoluciones incoherentes def tool_1() -> dict: return {"ok": True, "value": value} # Formato diferente def tool_2() -> str: return "success" or  "error: message"  # Devuelve una cadena en lugar de un diccionario 

### **5. Instrucciones estratégicas** 

instruction=""" ## Lineamientos de uso de herramientas 

### Selección de herramientas [Cuándo usar cada herramienta] ### Flujos de trabajo [Procedimientos paso a paso] ### Manejo de errores [Qué hacer ante cada tipo de error] ### Derivación [Cuándo y cómo derivar] """ 

### **Completa la lista de verificación:** 

Los nombres de las herramientas son descriptivos (verbo-sustantivo). Todos los parámetros tienen sugerencias de tipo. Las cadenas de documentación explican qué, cuándo, argumentos y devoluciones. Las devoluciones incluyen la clave de estado. Los mensajes de error son fáciles de usar. Las instrucciones hacen referencia a las herramientas por su nombre. Las instrucciones manejan la ejecución correcta y todos los tipos de errores. Los flujos de trabajo secuenciales están claramente definidos. Se especifican las rutas de derivación. 

## **5. Coordina las herramientas con el estado (vista previa)** 

_Conexión con la lección 4: Administra el estado y la memoria_ 

Las herramientas pueden leer y escribir el estado de la sesión para coordinar flujos de trabajo de varios pasos, hacer un seguimiento del uso y proporcionar un comportamiento 

personalizado. Si bien la cobertura completa de tool_context se abordará en futuras lecciones, aquí te presentamos lo que puedes hacer: 

### **Casos de uso para el estado en herramientas:** 

✅ **Flujos de trabajo de varios pasos** : las herramientas guardan los resultados intermedios en el estado para la siguiente herramienta. ✅ **Seguimiento de uso** : haz un recuento de las invocaciones de la herramienta de manera programática. 

✅ **Personalización** : las herramientas leen las preferencias del usuario del espacio de nombres user:. 

✅ **Lógica condicional** : las herramientas comprueban el estado para determinar el comportamiento. 

### **Ejemplo: Flujo de trabajo de varios pasos con coordinación de estado** 

def check_order_status(order_id: str, ctx) -> dict: """Verifica el estado del pedido y lo guarda para otras herramientas. Argumentos: order_id: el ID de pedido a verificar ctx: contexto de la herramienta (proporciona acceso a session.state) Devuelve lo siguiente: dict: información del estado del pedido Nota: El parámetro ctx (tool_context) se aborda en la lección 6. """ # Busca el pedido order = database.get_order(order_id) # Guarda la información del pedido en el estado de la sesión para que la utilicen otras herramientas ctx.session.state['current_order_id'] = order_id ctx.session.state['current_order_status'] = order['status'] # Hace un seguimiento del uso con el estado de la sesión count = ctx.session.state.get('orders_checked', 0) ctx.session.state['orders_checked'] = count + 1 return { "status": "success", "order_id": order_id, "order_status": order['status'], "details": order } def process_refund(order_id: str, reason: str, ctx) -> dict: """Procesa el reembolso utilizando los datos del pedido guardados en el estado. Utiliza el estado de check_order_status para evitar búsquedas redundantes. """ # Lee el estado del pedido desde el estado (guardado por la herramienta anterior) 

saved_order_id = ctx.session.state.get('current_order_id') saved_status = ctx.session.state.get('current_order_status') 

# Verifica que este sea el mismo pedido que acabamos de buscar if saved_order_id == order_id and saved_status: 

# Utiliza el estado almacenado en caché en lugar de volver a consultar if saved_status != 'delivered': return { "status": "error", "error_type": "cannot_refund", "error_message": f"Order status is '{saved_status}', not 'delivered'" } # Procesa el reembolso... refund_id = process_refund_in_system(order_id, reason) 

# Hace un seguimiento del recuento de reembolsos count = ctx.session.state.get('refunds_processed', 0) ctx.session.state['refunds_processed'] = count + 1 

return { "status": "success", "refund_id": refund_id } 

### **Espacios de nombres de estado en herramientas (de la lección 4):** 

# Datos temporales (se descartan después del turno) ctx.session.state['temp:validation_result'] = result 

# Datos de la sesión (persisten a través de los turnos de la conversación) ctx.session.state['orders_checked'] = 5 

# Preferencias del usuario (persisten a través de las sesiones) ctx.session.state['user:preferred_currency'] = 'USD' 

# Configuración global (que comparten todos los usuarios) ctx.session.state['app:max_refund_amount'] = 500.00 

### **Esto permite lo siguiente:** 

- **Coordinación de herramientas:** una herramienta guarda los datos y otra los lee. 

- **Seguimiento exacto:** acceso programático a los recuentos: si state.get('failed_attempts') >= 3: . 

- **Personalización:** las herramientas se adaptan según las preferencias de user: . 

- **Flujos de trabajo condicionales** : las herramientas toman decisiones basadas en valores de estado. 

**Vista previa:** La integración completa con tool_context , el acceso al estado en herramientas personalizadas y los patrones avanzados de coordinación de estado se abordan en la **Lección 6: Devoluciones de llamadas y flujo de control** . 

# 🧪 **Ejemplo práctico** 

## **Crea un agente de asistencia al cliente con herramientas coordinadas** 

**Lo que crearás:** un agente de asistencia al cliente que maneja consultas sobre pedidos, procesa reembolsos y deriva problemas complejos, con manejo de errores integral y coordinación estratégica de herramientas. 

## **Paso 1: Crea el proyecto** 

adk create customer_support cd customer_support 

### **Qué hace:** 

- Crea un nuevo directorio de proyecto del ADK. 

- Configura la estructura básica del agente. 

- Crea agent.py con el código predeterminado. 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" 

Agente de asistencia al cliente con herramientas coordinadas Demuestra la combinación estratégica de herramientas, el manejo de errores y el patrón de agente como herramienta. 

Referencia: https://google.github.io/adk-docs/tools-custom/ """ 

from google.adk.agents import LlmAgent 

# Base de datos simulada ORDERS_DB = { "ORD123": {"status": "shipped", "total": 99.99, "customer": "john@email.com"}, "ORD456": {"status": "processing", "total": 149.99, "customer": "jane@email.com"}, "ORD789": {"status": "delivered", "total": 249.99, "customer": "bob@email.com"}, } 

# Herramienta 1: Verifica el estado del pedido def check_order_status(order_id: str) -> dict: """Comprueba el estado actual del pedido de un cliente. 

Utiliza esto cuando un cliente pregunte por el estado de su pedido o la entrega. 

Argumentos: order_id (str): el ID de pedido (p. ej., "ORD123"). Devuelve lo siguiente: dict: información del estado del pedido. En caso de éxito: {'status': 'success', 'order_status': '...', 'details': {...}} En caso de error: {'status': 'error', 'error_type': 'not_found'/'invalid_format'} """ # Valida el formato if not order_id.startswith("ORD"): return { "status": "error", "error_type": "invalid_format", "error_message": "Los IDs de pedido deben comenzar con 'ORD' (p. ej., ORD123)" } # Busca el pedido if order_id not in ORDERS_DB: return { "status": "error", "error_type": "not_found", "error_message": f"El pedido {order_id} no se encontró en el sistema" } # Caso de éxito order = ORDERS_DB[order_id] return { "status": "success", "order_id": order_id, "order_status": order["status"], "details": order } # Herramienta 2: Procesa el reembolso def process_refund(order_id: str, reason: str) -> dict: """Procesa una solicitud de reembolso de un pedido. Utiliza esto SOLO después de verificar que el pedido existe con check_order_status. Argumentos: order_id (str): el ID de pedido a reembolsar. reason (str): motivo del cliente para pedir el reembolso. Devuelve lo siguiente: dict: resultado del procesamiento del reembolso. En caso de éxito: {'status': 'success', 'refund_amount': X, 'reference': 'REF###'} En caso de error: {'status': 'error', 'error_type': 'order_not_found'/'cannot_refund'} 

""" # Verifica si existe un pedido if order_id not in ORDERS_DB: return { "status": "error", "error_type": "order_not_found", "error_message": f"No se puede procesar el reembolso: no se encontró el pedido {order_id}" } order = ORDERS_DB[order_id] # Verifica si el pedido es apto para recibir el reembolso if order["status"] == "delivered": # Simula un reembolso exitoso return { "status": "success", "refund_amount": order["total"], "reference": f"REF{order_id[3:]}", "estimated_days": 5, "message": "Reembolso procesado de manera exitosa" } else: # No se pueden reembolsar los pedidos que aún no se entregaron return { "status": "error", "error_type": "cannot_refund", "error_message": f"No se puede reembolsar el pedido en el estado '{order['status']}'. Solo se podrán reembolsar los pedidos entregados." } # Herramienta 3: Deriva el asunto al supervisor def escalate_to_supervisor(issue_summary: str, order_id: str) -> dict: """Deriva problemas complejos a un supervisor humano. Utiliza esto cuando no puedas resolver el problema del cliente con las herramientas disponibles o cuando el cliente solicita explícitamente hablar con un supervisor. Argumentos: issue_summary (str): breve resumen del problema (1-2 oraciones). order_id (str): ID de pedido relacionado, si corresponde. Devuelve lo siguiente: dict: confirmación de la derivación. Siempre devuelve: {'status': 'success', 'ticket_id': 'TICKET###'} """ # Genera el ID del ticket ticket_id = f"TICKET{hash(issue_summary) % 10000:04d}" 

return { "status": "success", "ticket_id": ticket_id, "message": "Problema derivado al supervisor", 

"estimated_response": "en 2 horas", "order_id": order_id if order_id else "N/A" } 

# Crea un agente de asistencia al cliente con instrucciones estratégicas root_agent = LlmAgent( model='gemini-2.5-flash', name='customer_support_agent', description='Maneja consultas de clientes sobre pedidos y reembolsos con manejo de errores integral.', instruction=""" 

Eres un agente de asistencia al cliente servicial y empático para una empresa de comercio electrónico. 

# Tus capacidades 

Tienes tres herramientas disponibles: 

1. check_order_status(order_id): verifica el estado de un pedido. 

2. process_refund(order_id, reason): procesa las solicitudes de reembolso. 3. escalate_to_supervisor(issue_summary, order_id): deriva los problemas complejos. 

- # Lineamientos para el flujo de trabajo 

## Para consultas sobre el estado del pedido: 

1. Saluda al cliente de manera cálida. 

2. Utiliza check_order_status con el ID de pedido que te proporcionen. 

3. Maneja el resultado de la siguiente manera: 

- Si status='success': proporciona una actualización de estado clara con detalles. 

- Si error_type='not_found': solicita de manera amable al cliente que verifique el ID de pedido. 

- Si error_type='invalid_format': explica que los IDs de pedido comienzan con "ORD" (ejemplo: ORD123). 

## Para las solicitudes de reembolso: 

1. Expresa empatía por su situación. 

2. PRIMERO usa check_order_status para verificar que el pedido exista. 

3. Si no se encuentra el pedido, no se puede proceder con el reembolso; solicita al cliente que verifique el ID de pedido. 

4. Si existe un pedido, utiliza process_refund con el order_id y el motivo del cliente. 

5. Actúa en función del resultado del reembolso: 

- Si status='success': confirma el reembolso con el número de referencia, el importe y el plazo. 

- Si error_type='cannot_refund': explica por qué (estado de pedido) y ofrece alternativas o una derivación. 

- Si error_type='order_not_found': esto no debería suceder si el paso 2 se realizó correctamente, pero pide disculpas y verifica. 

## Estrategia de manejo de errores: 

En caso de errores 'not_found', haz lo siguiente: 

- Solicita al cliente que vuelva a verificar el ID de pedido. 

- Ofrece realizar la búsqueda por correo electrónico si lo tiene. 

- Sé paciente y servicial. 

En caso de errores 'invalid_format', haz lo siguiente: 

- Explica de manera amable el formato correcto: "ORD" seguido de números. 

- Proporciona un ejemplo: ORD123. 

- Pídele que proporcione el ID de pedido en el formato correcto. 

En caso de errores 'cannot_refund', haz lo siguiente: 

- Explica claramente la política (solo se pueden reembolsar los pedidos entregados). 

- Muestra empatía por su frustración. 

- Ofrece derivar el asunto al supervisor si desea una excepción. 

- ## Cuándo realizar una derivación 

Utiliza escalate_to_supervisor en los siguientes casos: 

- El cliente está frustrado o enojado y solicita hablar con un supervisor. 

- El problema no se puede resolver con las herramientas disponibles. 

- El cliente solicita una excepción a la política. 

- Varios intentos de usar la herramienta fallaron. 

- El cliente solicita específicamente hablar con un gerente. 

Después de la derivación, haz lo siguiente: 

- Proporciona el ID del ticket. 

- Informa al cliente el tiempo de respuesta esperado. 

- Agradece al cliente por su paciencia. 

- # Estilo de comunicación 

- Sé siempre educado, profesional y empático. 

- Utiliza el nombre del cliente si lo conoces. 

- Indica los próximos pasos de manera clara. 

- Reconoce los sentimientos del cliente (frustración, preocupación). 

- Agradece al cliente por su paciencia. 

- Nunca hagas promesas que no puedas cumplir. """, 

tools=[check_order_status, process_refund, escalate_to_supervisor] ) 

### **Qué se debe tener en cuenta:** 

En este ejemplo, se muestran los conceptos clave de esta parte: 

1. **Tres herramientas personalizadas** con propósitos claros y específicos, y cadenas de documentación completas 

2. **Devolución de errores estructurados** con clave status y valores específicos de error_type 

3. **Instrucciones estratégicas** organizadas en secciones: capacidades, flujos de trabajo, manejo de errores, derivación 

4. **Orientación sobre el flujo de trabajo secuencial** en las instrucciones: "PRIMERO, verifica el pedido y, LUEGO, procesa el reembolso" 

5. **Manejo específico de errores** para cada tipo de error ( not_found , invalid_format , cannot_refund ) 

6. **Rutas de derivación** claramente definidas tanto en la herramienta como en las instrucciones 

## **Paso 3: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

## **Paso 4: Situaciones de prueba** 

Usa estos casos de prueba para ver cómo las instrucciones estratégicas guían la coordinación de herramientas y el manejo de errores: 

**Prueba 1: Manejo de errores con validación de formato** 

Tú: Verifica el pedido 123 por mí 

**Esperado:** El agente llama a check_order_status("123") , recibe el error invalid_format , explica el formato "ORD" correcto con un ejemplo y solicita el ID de pedido corregido. 

**Concepto clave:** La orientación sobre instrucciones específicas para cada error da como resultado una respuesta útil y educativa. 

### **Prueba 2: Flujo de trabajo secuencial de varias herramientas** 

Tú: Me gustaría pedir el reembolso del pedido ORD789 porque el producto no cumplió con mis expectativas 

**Esperado:** El agente hace lo siguiente de forma secuencial: 

1. Llama a check_order_status("ORD789") para verificar la existencia y el estado del pedido. 

2. Llama a process_refund("ORD789", reason) con la información del pedido. 

3. Confirma el reembolso con el importe, el número de referencia y el cronograma. 

**Concepto clave:** Las instrucciones guían la secuencia correcta de herramientas; verifica ANTES de actuar. 

### **Prueba 3: Manejo de errores con la ruta de derivación** 

Tú: Quisiera el reembolso de mi pedido ORD456 _(Nota: ORD456 está "en proceso", no "entregado")_ 

**Esperado:** El agente llama a check_order_status , luego a process_refund , recibe el error cannot_refund , explica la política (solo pedidos entregados) y ofrece la derivación al supervisor. 

**Concepto clave:** Las instrucciones definen las rutas de derivación cuando las herramientas no pueden resolver el problema. 

# **Conclusiones principales** 

### **Patrones de diseño de instrucciones:** 

- **Guía de selección de herramientas:** “Usa X cuando ocurra la situación Y”. 

- **Manejo de resultados:** “Si status='success' entonces..., si es error entonces...". 

- **Flujos de trabajo secuenciales:** “Primero usa X para verificar, luego usa Y para actuar”. 

- **Acciones específicas para cada error:** manejo diferente para cada tipo de error. 

### **Estrategia de manejo de errores:** 

- **Identifica tipos de errores** en el diseño de herramientas (not_found, invalid_format, cannot_refund). 

- **Especifica acciones** para cada tipo de error en las instrucciones. 

- **Brinda orientación** a los clientes (explicar, mostrar ejemplos, ofrecer alternativas). 

- **Define las rutas de derivación** para problemas que no se pueden resolver. 

### **Prácticas recomendadas de coordinación de herramientas:** 

- **Haz referencia a las herramientas por nombre** en las instrucciones. 

- **Maneja todos los resultados** (éxito, cada tipo de error, casos extremos). 

- **Guía las secuencias** cuando las herramientas se deben usar en un orden específico. 

- **Define** los criterios y procesos de la derivación. 

### **Patrón de agente como herramienta:** 

- **Utiliza agentes especializados** para tareas de razonamiento complejas. 

- **Delega subtareas** que requieren experiencia en el dominio. 

- **Preocupaciones separadas:** el agente principal redirecciona, los agentes especialistas ejecutan. 

- **Importa AgentTool:** from google.adk.tools.agent_tool import AgentTool . 

- **Ideal para:** tareas que requieren juicio frente a operaciones determinísticas. 

### **Lista de verificación de calidad:** 

# Diseño de herramientas 

✓ Nombres de funciones descriptivos (verbo-sustantivo) 

✓ Sugerencias de tipo para todos los parámetros 

- ✓ Cadenas de documentación completas (qué, cuándo, argumentos y devoluciones) ✓ Las devoluciones incluyen la clave de estado 

✓ Tipos de errores específicos en las devoluciones 

- # Diseño de instrucciones 

- ✓ Orientación sobre la selección de herramientas (cuándo utilizar cada una) 

- ✓ Pasos del flujo de trabajo (procedimientos secuenciales) 

- ✓ Manejo de errores (acciones para cada tipo de error) 

- ✓ Criterios de derivación (cuándo y cómo) 

- # Coordinación 

- ✓ Lógica secuencial definida ✓ Flujos de trabajo de varias herramientas documentados 

- ✓ Especificación de integración de resultados 

- ✓ Lineamientos de estilo de comunicación 

