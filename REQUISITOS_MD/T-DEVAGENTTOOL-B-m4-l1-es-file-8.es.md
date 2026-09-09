# **La solución: Herramientas de funciones personalizadas** 

## **Escribe funciones de Python y obtén capacidades de agente** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas de funciones</u>_ 

### **De la documentación del ADK:** 

“Transformar una función de Python en una herramienta es una forma sencilla de integrar lógica personalizada en tus agentes. Cuando asignas una función a la lista de tools de un agente, el framework la encapsula automáticamente como FunctionTool ”. 

### **Cómo funciona:** 

1. **Escribes:** la función estándar de Python con tu lógica empresarial 

2. **El ADK inspecciona:** el nombre de la función, la cadena de documentación, los parámetros y las sugerencias de tipo 

3. **El ADK genera:** un esquema que describe la herramienta para el LLM 

4. **El agente usa:** una herramienta basada en el esquema y la cadena de documentación 

### **Este es un ejemplo sencillo:** 

from google.adk.agents import LlmAgent 

# Paso 1: Escribe una función de Python def calculate_shipping_cost(weight_kg: float, country: str) -> dict: """Calcula el costo de envío según el peso del paquete y el destino.""" rates = {"usa": 10, "canada": 12, "uk": 15} 

if country.lower() not in rates: return {"status": "error", "error_message": f"No realizamos envíos a {country}"} 

cost = weight_kg * rates[country.lower()] return {"status": "success", "cost_usd": cost} # Paso 2: Agrega una función a la lista tools del agente agent = LlmAgent( model='gemini-2.5-flash', instruction="Ayudas a los clientes con las estimaciones de los costos de envío.", tools=[calculate_shipping_cost]  # El ADK la encapsula automáticamente como FunctionTool ) 

### **Esto permite lo siguiente:** 

- ✅ **Integrar tu lógica empresarial** directamente en las capacidades del agente 

- ✅ **Acceder a tus sistemas propios** a través del código de Python 

- ✅ **Implementar cálculos específicos del dominio** exclusivos para tu negocio 

   - ✅ **Control total** sobre la implementación y el comportamiento 

- 

- ✅ **Generación automática de esquemas** a partir de la firma de tu función 

### **Cómo se integran las herramientas personalizadas con los agentes:** 

sequenceDiagram participant User participant Agent participant Tool as Custom Tool participant System as Your System/API 

User->>Agent: "Calcula el envío a Canadá" Agent->>Agent: Analiza la solicitud y selecciona la herramienta Agent->>Tool: calculate_shipping_cost(weight=5, country="Canada") Tool->>System: Consulta las tarifas en la base de datos System-->>Tool: datos de tarifas Tool->>Tool: calcula: 5 kg × $12/kg Tool-->>Agent: {"status": "success", "cost_usd": 60} Agent-->>User: "El costo de envío es USD 60" 

Nota sobre Agent, Tool: El LLM decide CUÁNDO llamar;<br/>Tool ejecuta QUÉ hacer 

_Las herramientas personalizadas permiten a los agentes acceder a tu lógica empresarial y sistemas_ 

# **Conceptos básicos** 

## **1. Las firmas de funciones son importantes** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas de funciones</u>_ 

### **De la documentación del ADK:** 

“La firma de la función, incluidos los tipos de parámetros y el tipo de datos que se devuelve, es crucial. El ADK utiliza esta información para generar el esquema que ve el LLM”. 

### **Elementos fundamentales:** 

### **1. Nombre de la función (descriptivo)** 

El LLM utiliza el nombre de la función para comprender lo que hace la herramienta. 

> # ✅ Recomendable: estilo descriptivo, patrón verbo-sustantivo def get_shipping_cost(weight: float, destination: str) -> dict: """Recupera el costo de envío de un paquete"."" pass 

- def calculate_loyalty_points(purchase_amount: float) -> dict: """Calcula los puntos de lealtad obtenidos por una compra.""" 

pass 

def search_available_flights(destination: str, date: str) -> dict: """Busca vuelos disponibles a un destino.""" pass 

# ❌ No recomendable: nombres genéricos y poco claros def process(data: float) -> dict:  # ¿Qué procesar? pass def do_stuff(x: str) -> dict:  # ¿Qué cosas? pass def handler(amount: float) -> dict:  # ¿Qué manejar? pass 

### **2. Sugerencias de tipo (obligatorio)** 

Las sugerencias de tipo le indican al ADK qué tipos debe proporcionar el LLM. 

# ✅ Recomendable: sugerencias de tipo para todos los parámetros y el retorno def lookup_order(order_id: str, user_id: int) -> dict: """Busca información del pedido.""" pass 

def calculate_discount(price: float, customer_tier: str) -> dict: """Calcula el descuento según el nivel del cliente.""" pass 

- # ❌ No recomendable: no hay sugerencias de tipo; el LLM no sabrá qué tipos proporcionar def lookup_order(order_id, user_id):  # ¿Qué tipos son estos? pass 

def calculate_discount(price, customer_tier):  # Tipos desconocidos pass 

### **3. Tipos de parámetros** 

Utiliza tipos serializables en JSON que los LLM comprendan: 

- ✅ **Compatibles:** str , int , float , bool , list , dict 

- ❌ **Evita:** clases personalizadas complejas, objetos y controladores de archivos 

# ✅ Recomendable: tipos simples que pueden serializarse con JSON def book_flight( destination: str, departure_date: str, passengers: int ) -> dict: pass 

# ❌ No recomendable: tipos personalizados complejos from datetime import datetime from custom_models import Customer 

def book_flight( destination: str, departure_date: datetime,  # No serializable en JSON customer: Customer  # Clase personalizada ) -> dict: pass 

### **4. Parámetros obligatorios frente a los opcionales** 

### **De la documentación del ADK:** 

“No establezcas valores predeterminados para los parámetros. Los modelos subyacentes no admiten ni utilizan los valores predeterminados de forma confiable”. 

**Recomendación:** Utiliza todos los parámetros obligatorios. 

# ✅ Recomendado: todos los parámetros son obligatorios def book_flight(destination: str, date: str, passengers: int) -> dict: """Reserva un vuelo.""" pass 

# ⚠ No recomendado: es posible que los valores predeterminados no funcionen de manera confiable def search_flights( destination: str, max_price: float = 1000.0,  # El valor predeterminado puede ignorarse class_type: str = "economy"  # El valor predeterminado puede ignorarse ) -> dict: """Busca vuelos.""" pass 

## **2. Las cadenas de documentación son fundamentales** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre cómo definir las funciones de las herramientas de manera eficaz</u>_ 

### **De la documentación del ADK:** 

“La cadena de documentación de tu función sirve como descripción de la herramienta y se envía al LLM. Por lo tanto, una cadena de documentación bien escrita y completa es fundamental para que el LLM comprenda cómo usar la herramienta de manera eficaz”. 

### **Plantilla de cadena de documentación:** 

def tool_name(param1: type1, param2: type2) -> dict: """[Resumen de una línea de lo que hace esta herramienta] 

- [Opcional: contexto adicional sobre cuándo utilizar esta herramienta] 

Argumentos: param1 (type1): [Descripción del param1] param2 (type2): [Descripción del param2] Devuelve lo siguiente: dict: [descripción de la estructura de retorno] En caso de éxito: {'status': 'success', 'key': value} En caso de error: {'status': 'error', 'error_message': 'explanation'} """ # Implementación pass 

**Ejemplo completo:** 

def calculate_shipping_cost(weight_kg: float, country: str) -> dict: """Calcula el costo de envío según el peso del paquete y el país de destino. Utiliza esta herramienta cuando un cliente pregunte sobre los costos de envío de su pedido. Argumentos: weight_kg (float): el peso del paquete en kilogramos. country (str): el nombre del país de destino. Devuelve lo siguiente: dict: información sobre los costos de envío. En caso de éxito: {'status': 'success', 'cost_usd': 25.50, 'delivery_days': 5} En caso de error: {'status': 'error', 'error_message': 'País no admitido'} """ shipping_rates = { "usa": {"rate_per_kg": 10, "days": 3}, "canada": {"rate_per_kg": 12, "days": 5}, "uk": {"rate_per_kg": 15, "days": 7}, } country_key = country.lower() if country_key not in shipping_rates: return { "status": "error", "error_message": f"El envío a {país} no se admite actualmente." } rate_info = shipping_rates[country_key] cost = weight_kg * rate_info["rate_per_kg"] return { "status": "success", "cost_usd": round(cost, 2), "delivery_days": rate_info["days"], "destination": country } 

### **Lo que ve el LLM:** 

Tool: calculate_shipping_cost 

Descripción: 

Calcula el costo de envío según el peso del paquete y el país de destino. Utiliza esta herramienta cuando un cliente pregunte sobre los costos de envío de su pedido. 

Parámetros: 

- weight_kg (float): el peso del paquete en kilogramos - country (str): el nombre del país de destino 

Devuelve lo siguiente: 

Diccionario con información sobre el estado y el envío 

### **El LLM utiliza esto para decidir:** 

- **Cuándo llamar:** “El cliente pregunta por los costos de envío” 

- **¿Qué parámetros?:** weight_kg (float), country (str) 

- **Qué esperar:** diccionario con cost_usd y delivery_days 

### **Cómo el ADK convierte tu función en un esquema de LLM:** 

graph TB A[Tu función de Python] --> B[Nombre de la función] A --> C[Sugerencias de tipo] A --> D[Cadena de documentación] A --> E[Tipo de retorno] B --> F[Generación de esquemas de LLM] C --> F D --> F E --> F F --> G[Nombre de la herramienta] F --> H[Descripción de la herramienta] F --> I[Tipos de parámetros] F --> J[Resultado esperado] G --> K[Selección de herramientas del LLM] H --> K I --> K J --> K K --> L[El agente llama a la herramienta<br/>con los parámetros correctos] 

style F fill:#ffeb99 style K fill:#e1f5ff 

_El ADK genera automáticamente un esquema de LLM a partir de los metadatos de tu función; no es necesario realizar ninguna configuración manual_ 

## **3. Devuelve diccionarios con estado** 

_Referencia:_ _<u>Artículo de la documentación del ADK sobre las herramientas de funciones</u>_ 

### **De la documentación del ADK:** 

“El tipo de datos que se devuelve preferido para una herramienta de función es un diccionario en Python... Es una práctica muy recomendable incluir una clave status (p. ej., 'success' , 'error' , 'pending' ) para indicar claramente al modelo el resultado de la ejecución de la herramienta”. 

### **Patrón:** 

# Caso de éxito return { "status": "success", "data_key": value, "another_key": another_value } # Caso de error return { "status": "error", "error_message": "Explicación legible por humanos de lo que salió mal" } 

### **¿Por qué es importante?:** 

- **Comprensión del LLM:** un estado claro ayuda al LLM a saber si la herramienta tuvo éxito 

- **Siguiente acción:** el LLM decide qué hacer según el estado (continuar, reintentar, disculparse) 

- **Manejo de errores:** los mensajes de error guían la respuesta del LLM al usuario 

- **Datos estructurados:** un formato coherente hace que las respuestas del LLM sean más confiables 

### **Ejemplo:** 

def lookup_product(product_id: str) -> dict: """Busca información del producto por ID. Argumentos: product_id (str): el ID de producto a buscar. Devuelve lo siguiente: dict: información del producto. En caso de éxito: {'status': 'success', 'product': {...}} En caso de error: {'status': 'error', 'error_message': 'explanation'} """ # Base de datos simulada products = { "PROD001": {"name": "Widget Pro", "price": 99.99, "in_stock": True}, 

"PROD002": {"name": "Gadget Plus", "price": 149.99, "in_stock": False} } # Caso de éxito if product_id in products: return { "status": "success", "product_id": product_id, "product": products[product_id] } # Caso de error return { "status": "error", "error_message": f"El producto {product_id} no se encontró en la base de datos." } 

### **Cómo utiliza esto el LLM:** 

Usuario: "Cuéntame sobre el producto PROD999" 

Llamada del agente: lookup_product("PROD999") 

La herramienta devuelve: {"status": "error", "error_message": "El producto PROD999 no se encontró en la base de datos."} El LLM ve el estado="error" y responde: "Lo siento, pero no pude encontrar el producto PROD999 en nuestro sistema. ¿Podrías verificar el ID del producto?" 

### **Patrón clave:** 

def your_tool(params) -> dict: """Tu cadena de documentación.""" # Valida la entrada if validation_fails: return { "status": "error", "error_message": "Explicación clara para el usuario" } # Realiza la operación try: result = do_something() return { "status": "success", "result_key": result, "additional_info": other_data } except Exception as e: return { "status": "error", 

"error_message": f"Falló la operación: {str(e)}" } 

## **4. Usa el estado en las herramientas personalizadas (vista previa)** 

_Conexión con la lección 4: Administra el estado y la memoria_ 

Las herramientas personalizadas pueden acceder y modificar el estado de la sesión para proporcionar un comportamiento personalizado y adaptado al contexto. Si bien la mecánica de tool_context se abordará en futuras lecciones, aquí te presentamos lo que puedes hacer: 

### **Ejemplo: Herramienta que utiliza el estado para la personalización** 

def recommend_products(category: str, ctx) -> dict: """Recomienda productos según las preferencias del usuario a partir del estado. Argumentos: category: categoría de producto a buscar ctx: contexto de la herramienta (proporciona acceso al estado de la sesión) Devuelve lo siguiente: dict: productos recomendados con información de personalización Nota: El parámetro ctx (tool_context) se aborda en la lección 6. """ # Accede a las preferencias del usuario desde el estado user_tier = ctx.session.state.get('user:tier', 'standard') user_preferences = ctx.session.state.get('user:preferences', {}) # Personaliza las recomendaciones según el nivel y las preferencias if user_tier == 'premium': products = get_premium_products(category, user_preferences) discount = 0.15 else: products = get_standard_products(category) discount = 0.05 return { "status": "success", "products": products, "tier": user_tier, "discount_applied": discount } 

### **Cuándo utilizar el estado en las herramientas:** 

### ✅ **Personalización basada en las preferencias del usuario** 

# Accede a user:language para proporcionar resultados localizados language = ctx.session.state.get('user:language', 'en') 

### ✅ **Contexto de llamadas a herramientas anteriores** 

# Verifica si la operación anterior se completó prev_status = ctx.session.state.get('temp:last_operation_status') 

### ✅ **Flujos de trabajo de varios pasos que requieren datos intermedios** 

# Guarda los resultados intermedios para la siguiente herramienta ctx.session.state['temp:calculation_result'] = computed_value 

### ✅ **Configuración específica del usuario** 

# Usa las unidades preferidas del usuario units = ctx.session.state.get('user:preferred_units', 'imperial') 

### **Espacios de nombres de estado en herramientas (de la lección 4):** 

- temp: : datos temporales, descartados después del turno 

- Sin prefijo: datos de sesión que se descartan una vez finalizada la conversación 

- user: : preferencias del usuario que persisten en todas las sesiones 

- app: : configuración global que comparten todos los usuarios 

### **Ejemplo: Flujo de trabajo de varios pasos con estado** 

def start_order_process(product_id: str, ctx) -> dict: """Inicia el proceso de pedido y lo guarda en el estado.""" # Guarda los datos intermedios en el estado de la sesión ctx.session.state['temp:current_order'] = { 'product_id': product_id, 'step': 'initiated', 'timestamp': time.time() } return {"status": "success", "message": "Pedido iniciado"} 

def add_shipping_address(address: dict, ctx) -> dict: """Agrega la dirección de envío al pedido en curso.""" # Recupera los datos intermedios del estado order_data = ctx.session.state.get('temp:current_order') if not order_data: return {"status": "error", "error_message": "No hay ningún pedido activo"} # Actualiza el pedido en el estado order_data['shipping_address'] = address order_data['step'] = 'address_added' ctx.session.state['temp:current_order'] = order_data return {"status": "success", "message": "Dirección agregada"} 

def finalize_order(ctx) -> dict: """Completa el pedido con los datos del estado.""" # Recupera los datos completos del pedido order_data = ctx.session.state.get('temp:current_order') 

if not order_data or order_data['step'] != 'address_added': return {"status": "error", "error_message": "El pedido no está listo"} 

# Procesa el pedido (llamada a la API, base de datos, etc.) order_id = process_order_in_system(order_data) 

# Limpia el estado temporal del ctx.session.state['temp:current_order'] 

return {"status": "success", "order_id": order_id} 

### **Lo que esto demuestra:** 

- Las herramientas pueden leer las preferencias del usuario desde el espacio de nombres user: . 

- Las herramientas pueden guardar o recuperar datos intermedios con el espacio de nombres temp: . 

- Varias herramientas se coordinan a través de un estado compartido. 

- El estado permite flujos de trabajo complejos y con estado. 

**Vista previa:** La integración completa de herramientas con la administración de estados, incluido el parámetro ctx y tool_context , se aborda en futuras lecciones sobre devoluciones de llamadas y protecciones de seguridad. 

## **5. Varias herramientas en colaboración** 

### **Patrón: Enumera múltiples funciones en el parámetro tools** 

Los agentes pueden utilizar varias herramientas para realizar tareas complejas: 

from google.adk.agents import LlmAgent 

def check_inventory(product_id: str) -> dict: """Comprueba si un producto está en stock.""" # Implementación return {"status": "success", "in_stock": True, "quantity": 5} 

def get_product_price(product_id: str) -> dict: """Obtiene el precio actual de un producto.""" # Implementación return {"status": "success", "price_usd": 99.99} 

def calculate_shipping(weight_kg: float, country: str) -> dict: """Calcula el costo de envío.""" # Implementación return {"status": "success", "cost_usd": 25.50} 

def calculate_total(product_price: float, shipping_cost: float) -> dict: """Calcula el costo total, que incluye el producto y el envío.""" total = product_price + shipping_cost 

return { "status": "success", "subtotal": product_price, "shipping": shipping_cost, "total": total } # Agente con varias herramientas agent = LlmAgent( model='gemini-2.5-flash', instruction=""" Cuando un usuario pregunta sobre el costo total: 

1. Primero verifica el inventario con check_inventory. 

2. Si está en stock, obtén el precio con get_product_price. 

3. Calcula el envío con calculate_shipping. 

4. Utiliza calculate_total para proporcionar el precio final. 

Presenta el desglose de forma clara al cliente. """, tools=[check_inventory, get_product_price, calculate_shipping, calculate_total] ) 

### **Cómo organiza el agente:** 

Usuario: "¿Cuál es el costo total del producto PROD001 enviado a Canadá?" 

Razonamiento del agente: 

```
1. Llama a check_inventory("PROD001") → in_stock: True
2. Llama a get_product_price("PROD001") → price: $99.99
3. Llama a calculate_shipping(weight, "Canada") → shipping: $25.50
4. Llama a calculate_total(99.99, 25.50) → total: $125.49
```

El agente responde: "¡El producto PROD001 está disponible! El precio es $99.99, el envío a Canadá cuesta $25.50, lo que da un total de $125.49". 

### **Puntos clave:** 

- **Llamadas secuenciales:** el agente llama a las herramientas en orden lógico 

- - **Encadenamiento de resultados:** utiliza el resultado de una herramienta como contexto para la siguiente 

- **Organización automática:** el agente decide qué herramientas usar y cuándo 

- **Síntesis natural:** combina todos los resultados en una respuesta coherente 

# 🧪 **Ejemplo práctico** 

## **Crea un agente de viajes con herramientas personalizadas** 

**Lo que crearás:** un agente de viajes que ayude a los usuarios a planificar viajes buscando vuelos, hoteles y calculando presupuestos. 

## **Paso 1: Crea el proyecto** 

adk create travel_agent cd travel_agent 

### **Qué hace:** 

- Crea un nuevo directorio de proyecto del ADK. 

- Configura la estructura básica del agente. 

- Crea agent.py con el código predeterminado. 

## **Paso 2: Escribe el agente** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Agente de viajes con herramientas de funciones personalizadas Demuestra varias herramientas personalizadas que funcionan en conjunto. 

Referencia: https://google.github.io/adk-docs/tools-custom/function-tools/ """ 

from google.adk.agents import LlmAgent 

# Herramienta 1: Busca vuelos def search_flights(destination: str, departure_date: str) -> dict: """Busca vuelos disponibles a un destino en una fecha específica. 

Utiliza esta herramienta cuando un cliente quiera saber las opciones de vuelo. Argumentos: destination (str): la ciudad de destino (p. ej., "París", "Tokio"). departure_date (str): fecha de salida en formato AAAA-MM-DD. Devuelve lo siguiente: dict: resultados de la búsqueda de vuelos. En caso de éxito: {'status': 'success', 'flights': [...], 'count': N} En caso de error: {'status': 'error', 'error_message': 'explanation'} """ # Datos de vuelo simulados available_flights = { "paris": [ {"flight_number": "AF123", "price_usd": 450, "duration_hours": 8}, {"flight_number": "BA456", "price_usd": 480, "duration_hours": 7.5}, ], "tokyo": [ {"flight_number": "JL789", "price_usd": 850, "duration_hours": 13}, {"flight_number": "ANA101", "price_usd": 820, "duration_hours": 12.5}, 

], } dest_key = destination.lower() if dest_key not in available_flights: return { "status": "error", "error_message": f"No se encontraron vuelos a {destination}. Prueba París o Tokio." } return { "status": "success", "destination": destination, "departure_date": departure_date, "flights": available_flights[dest_key], "count": len(available_flights[dest_key]) } 

# Herramienta 2: Busca hoteles def search_hotels(city: str, check_in_date: str) -> dict: """Busca hoteles disponibles en una ciudad para una fecha de entrada específica. Utiliza esta herramienta cuando un cliente necesite alojamiento. 

Argumentos: city (str): el nombre de la ciudad (p. ej., "París", "Tokio"). check_in_date (str): la fecha de entrada en formato AAAA-MM-DD. Devuelve lo siguiente: dict: resultados de la búsqueda de hoteles. En caso de éxito: {'status': 'success', 'hotels': [...], 'count': N} En caso de error: {'status': 'error', 'error_message': 'explanation'} """ # Datos de hoteles simulados available_hotels = { "paris": [ {"name": "Hotel Eiffel", "price_per_night_usd": 150, "rating": 4.5}, {"name": "Louvre Inn", "price_per_night_usd": 120, "rating": 4.2}, ], "tokyo": [ {"name": "Shibuya Grand", "price_per_night_usd": 180, "rating": 4.7}, {"name": "Tokyo Bay Hotel", "price_per_night_usd": 140, "rating": 4.3}, ], } city_key = city.lower() if city_key not in available_hotels: return { "status": "error", "error_message": f"No se encontraron hoteles en {city}. Prueba París o Tokio." } 

return { "status": "success", "city": city, "check_in_date": check_in_date, "hotels": available_hotels[city_key], "count": len(available_hotels[city_key]) } # Herramienta 3: Calcula el presupuesto del viaje def calculate_trip_budget(flight_price: float, hotel_price: float, num_nights: int) -> dict: """Calcula el presupuesto total del viaje, lo que incluye vuelos y alojamiento. Utiliza esto después de encontrar los precios de los vuelos y hoteles para darle al cliente una estimación total. 

Argumentos: flight_price (float): costo del vuelo de ida y vuelta en USD. hotel_price (float): costo del hotel por noche en USD. num_nights (int): número de noches de hospedaje. 

Devuelve lo siguiente: dict: Desglose del presupuesto. Siempre devuelve: {'status': 'success', 'total_usd': X, 'breakdown': {...}} """ hotel_total = hotel_price * num_nights total = flight_price + hotel_total return { "status": "success", "total_usd": round(total, 2), "breakdown": { "flight_cost": flight_price, "hotel_cost_per_night": hotel_price, "num_nights": num_nights, "hotel_total": round(hotel_total, 2) } } # Crea un agente de viajes con las tres herramientas root_agent = LlmAgent( model='gemini-2.5-flash', name='travel_agent', description='Ayuda a los usuarios a planificar viajes buscando vuelos y hoteles.', instruction=""" Eres un asesor de viajes servicial. Tus capacidades: - Buscar vuelos con search_flights(destination, departure_date) - Buscar hoteles con search_hotels(city, check_in_date) - Calcular presupuestos de viaje con calculate_trip_budget(flight_price, hotel_price, num_nights) 

Cuando ayudes a los usuarios: 

1. Si preguntan por vuelos, utiliza search_flights. 

2. Si preguntan por hoteles, utiliza search_hotels. 

3. Si desean una estimación completa del viaje, utiliza ambas herramientas de búsqueda y, a continuación, calculate_trip_budget. 

4. Presenta siempre las opciones de manera clara con los precios. 

5. Si una herramienta devuelve un error, pide disculpas y sugiere destinos disponibles (París o Tokio). 

- ¡Sé amable y ayuda a los usuarios a planificar su viaje perfecto! """, 

tools=[search_flights, search_hotels, calculate_trip_budget] ) 

### **Explicación del código:** 

### **Líneas 10 a 50: Herramienta search_flights** 

- Nombre descriptivo: search_flights (patrón verbo-sustantivo) 

- Sugerencias de tipo: str , str → dict 

- Cadena de documentación completa que explica qué, cuándo, argumentos y retornos 

- - Devuelve un diccionario estructurado con la clave status 

- Manejo de errores para destinos no compatibles 

### **Líneas 52 a 91: Herramienta search_hotels** 

- Patrón similar a search_flights 

- Diferentes estructuras de datos (hoteles frente a vuelos) 

- Manejo de errores coherente con status y error_message 

### **Líneas 93 a 116: Herramienta calculate_trip_budget** 

- Toma la salida de otras herramientas como entrada (flight_price, hotel_price) 

- - Realiza cálculos 

- Devuelve un desglose detallado 

- Siempre tiene éxito (status: success) 

### **Líneas 118 a 142: Agente con varias herramientas** 

- Las tres herramientas en la lista tools 

- La instrucción orienta sobre cuándo utilizar cada herramienta 

- - Explica cómo manejar errores 

- Guía el uso secuencial para solicitudes complejas 

## **Paso 3: Ejecuta y prueba** 

adk web 

Desde tu navegador, ve a http://localhost:8000 . 

## **Paso 4: Situaciones de prueba** 

### **Prueba 1: Búsqueda de vuelos** 

Tú: Quiero volar a París el 15-12-2025 

### **Comportamiento esperado:** 

- El agente llama a search_flights(destination="Paris", departure_date="2025-12-15") . 

- La herramienta devuelve 2 opciones de vuelo. 

- El agente presenta las opciones con números de vuelos, precios y duraciones. 

### **Qué se debe tener en cuenta:** 

- El agente extrajo automáticamente el destino y la fecha a partir del lenguaje natural. 

- - La herramienta devolvió datos estructurados con varias opciones de vuelo. 

- El agente formateó los resultados de forma natural para el usuario. 

### **Prueba 2: Planificación completa del viaje** 

Tú: Planifica un viaje de 3 noches a Tokio a partir del 20-12-2025 

### **Comportamiento esperado:** 

1. El agente llama a search_flights(destination="Tokyo", departure_date="2025-12-20") . 

2. El agente llama a search_hotels(city="Tokyo", check_in_date="2025-12-20") . 

3. El agente elige un vuelo y un hotel razonables entre las opciones. 

4. El agente llama a calculate_trip_budget(flight_price, hotel_price, 3) . 

5. El agente presenta un plan de viaje completo con un desglose del costo total. 

### **Qué se debe tener en cuenta:** 

- El agente organizó tres llamadas a herramientas diferentes. 

- Las herramientas trabajaron en conjunto de forma secuencial. 

- La respuesta final sintetiza toda la información. 

- Presentación en lenguaje natural de datos estructurados. 

### **Prueba 3: Manejo de errores** 

Tú: Busca hoteles en Londres 

### **Comportamiento esperado:** 

- El agente llama a search_hotels(city="London", check_in_date=...) . 

- La herramienta devuelve el error: {"status": "error", "error_message": "No se encontraron hoteles en Londres. Prueba París o Tokio."} . 

- El agente se disculpa de manera amable. 

- El agente sugiere destinos disponibles. 

### **Qué se debe tener en cuenta:** 

- El manejo de errores es ordenado. 

- El agente no alucina datos de hoteles para una ciudad no admitida. 

- Orientación clara sobre qué destinos están disponibles. 

- Tono profesional mantenido incluso con errores. 

### **Prueba 4: Solo cálculo de presupuesto** 

Tú: ¿Cuál es el costo total de un vuelo de $450 y una noche de hotel de $150 por 4 noches? 

### **Comportamiento esperado:** 

- El agente llama a calculate_trip_budget(flight_price=450, hotel_price=150, num_nights=4) . 

- 

   - La herramienta devuelve el desglose. 

- El agente presenta: vuelo $450 + hotel $600 (4 noches × $150) = total $1,050. 

### **Qué se debe tener en cuenta:** 

- El agente seleccionó la herramienta adecuada para la tarea. 

- No llamó a las herramientas de búsqueda de manera innecesaria. 

- Herramienta centrada en una tarea clara (cálculo). 

- El desglose ayuda al usuario a comprender el total. 

# **Conclusiones principales** 

### **Elementos esenciales de la herramienta de función:** 

- **Nombres de funciones descriptivos:** Utiliza el patrón verbo-sustantivo (get , calculate__ , search_*). 

- **Sugerencias de tipo obligatorias:** ADK las utiliza para generar el esquema para el LLM. 

- **Cadena de documentación completa:** Explica qué hace la herramienta, cuándo 

usarla, los argumentos y los retornos. 

- **Devolver diccionarios:** Incluye siempre la clave state para la comprensión del LLM. 

### **Patrón de prácticas recomendadas:** 

def tool_name(param: type) -> dict: """Resumen claro de una línea. Contexto adicional sobre cuándo utilizar esta herramienta. Argumentos: param (type): descripción del parámetro. Devuelve lo siguiente: dict: descripción del retorno. En caso de éxito: {'status': 'success', 'data': value} En caso de error: {'status': 'error', 'error_message': 'explanation'} """ # Valida la entrada if error_condition: return {"status": "error", "error_message": "Explicación clara"} # Realiza la operación return {"status": "success", "result_key": computed_value} 

### **Varias herramientas:** 

- **Enumera todas las funciones:** tools=[tool1, tool2, tool3] 

- **El agente selecciona automáticamente:** según el contexto y las cadenas de documentación 

- **Uso secuencial:** las herramientas pueden basarse en los resultados de las demás 

- **Referencia en las instrucciones:** guía al LLM sobre cuándo usar cada herramienta 

### **Generación de esquemas:** 

ADK crea automáticamente un esquema de herramientas a partir de: 

1. Nombre de la función 

2. Nombres de parámetros y sugerencias de tipo 3. Cadena de documentación 

4. Tipo de datos que se muestra 

### **Cuándo utilizar herramientas personalizadas:** 

- ✅ Cálculos específicos del negocio (costos de envío, descuentos, impuestos) 

   - ✅ Búsquedas en bases de datos propias (pedidos, inventario, clientes) 

- 

   - ✅ Integraciones de API personalizadas (tus servicios internos) 

- 

   - ✅ Lógica específica del dominio (sistemas de reserva, reglas de fijación de precios) 

- 

   - ✅ Cualquier tarea exclusiva de tu aplicación 

- 

### **Diferencias clave:** 

|**Aspecto**|**Herramientas integradas**|**Herramientas de funciones**<br>**personalizadas**|
|---|---|---|
|**Configuración**|Importar y utilizar|Escribir la implementación de la<br>función|
|**Mantenimiento**|El equipo de ADK se encarga del<br>mantenimiento|Tú te encargas del<br>mantenimiento|
|**Personalización**|Limitada a las funciones de la<br>herramienta|Control total|
|**Uso**|Capacidades comunes|Lógica específica del negocio|



