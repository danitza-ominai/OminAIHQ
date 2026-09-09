# **La solución: Resultados estructurados con Pydantic** 

## **Aplica JSON con output_schema** 

_Referencia:_ _<u>Documentación del ADK sobre la estructuración de datos</u>_ 

Según la documentación del ADK, utiliza Pydantic BaseModel para definir la estructura exacta que necesitas: 

de pydantic importa BaseModel, Field 

class ProductInfo(BaseModel): product_name: str = Field(description="El nombre del producto") price: float = Field(description="El precio en USD") storage: str = Field(description="La capacidad de almacenamiento") 

structured_agent = LlmAgent( model="gemini-2.5-flash", instruction="""Extrae información del producto y responde con JSON. Formato: {"product_name": "name", "price": 999.99, "storage": "256GB"}""", output_schema=ProductInfo # Aplica esta estructura exacta ) 

### **La documentación del ADK brinda la siguiente información:** 

" **output_schema (opcional):** Define un esquema que represente la estructura deseada del resultado. Si se configura, la respuesta final del agente _debe_ ser una cadena JSON que se ajuste a este esquema". 

# **Conceptos básicos** 

## **1. Define esquemas con Pydantic** 

_Referencia:_ _<u>Ejemplo de Python obtenido de la documentación del ADK</u>_ 

Crea un modelo de Pydantic que represente el resultado deseado: 

de pydantic importa BaseModel, Field 

class CapitalOutput(BaseModel): capital: str = Field(description="La capital del país") 

### **Puntos clave:** 

- **Debe heredar de BaseModel** : No puedes utilizar diccionarios de Python ni clases simples. 

- Cada campo tiene un tipo ( str , float , int , bool , etcétera). 

- Utiliza Field(description=…) para ayudar al LLM a entender cada campo. 

- Pasa la **clase en sí** a output_schema , no a una instancia: output_schema=CapitalOutput . 

**Importante:** Según la documentación del ADK, "el esquema de entrada y salida suele ser del tipo Pydantic BaseModel". Debes definir tu esquema como una clase Pydantic. Los diccionarios como {"name": "string"} no funcionarán. 

## **2. Utiliza output_schema en agentes** 

_Referencia:_ _<u>Documentación del ADK sobre la estructuración de datos</u>_ 

Aplica el esquema a tu agente: 

structured_agent = LlmAgent( model="gemini-2.5-flash", name="capital_finder", instruction="""Eres un agente de información de capitales. Si se proporciona un país, responde SOLO con un objeto JSON que contenga la capital. 

Formato: {"capital": "capital_name"}""", output_schema=CapitalOutput # Aplica el resultado JSON ) 

### **Qué hace:** 

- El agente **debe** devolver un objeto JSON que coincida con el esquema. 

- Las respuestas no válidas se rechazan automáticamente. 

- Tu código obtiene una estructura garantizada. 

## **3. Almacena los resultados con output_key** 

_Referencia:_ _<u>Documentación del ADK sobre output_key</u>_ 

Guarda la respuesta del agente en el estado de la sesión para usarla más adelante: 

structured_agent = LlmAgent( model="gemini-2.5-flash", instruction="Extrae la capital como JSON", output_schema=CapitalOutput, output_key="found_capital" # Almacena la respuesta en session.state["found_capital"] ) 

### **La documentación del ADK brinda la siguiente información:** 

" **output_key (opcional):** Proporciona una clave de cadena. Si se configura, el contenido de texto de la respuesta _final_ del agente se guardará automáticamente en el diccionario de estado de la sesión con esta clave". 

### **Casos de uso:** 

- Transferencia de datos entre agentes en flujos de trabajo 

- Almacenamiento de la información extraída para su posterior procesamiento 

- Creación de canalizaciones de varios pasos 

### **Nota importante sobre los flujos de trabajo de varios agentes:** 

Si bien este módulo muestra output_schema en root_agent , el resultado estructurado es igualmente valioso para los agentes secundarios intermedios en flujos de trabajo de varios agentes (lo que se aborda en el curso 5). Cuando hay varios agentes trabajando juntos, el uso de output_schema en los agentes secundarios garantiza un formato de datos coherente cuando se transmite información de uno a otro. Ejemplo: 

# El agente secundario extrae datos estructurados extraction_agent = LlmAgent( model="gemini-2.5-flash", name="data_extractor", output_schema=ProductInfo, # Resultado estructurado para el próximo agente output_key="extracted_data" ) 

# Otro agente usa esos datos estructurados 

analysis_agent = LlmAgent( 

model="gemini-2.5-flash", 

name="data_analyzer", 

# El agente recibe datos estructurados de extraction_agent a través del estado de la sesión ) 

Puedes utilizar el resultado estructurado en cualquier nivel de agente (raíz o intermedio) dependiendo de dónde necesites formatos de datos garantizados. 

## **4. Esquemas complejos** 

_Referencia:_ _<u>Documentación del ADK sobre la estructuración de datos</u>_ 

Crea estructuras más sofisticadas: 

de pydantic importa BaseModel, Field 

de typing importa List, Optional 

class ProductDetails(BaseModel): name: str = Field(description="Nombre del producto") price: float = Field(description="Precio en USD") 

storage_options: List[str] = Field(description="Capacidades de almacenamiento disponibles") in_stock: bool = Field(description="Si el producto está en stock") discount: Optional[float] = Field(default=None, description="Porcentaje de descuento, si lo hubiera") 

product_agent = LlmAgent( model="gemini-2.5-flash", instruction="""Extrae toda la información del producto como JSON. Incluye name, price, storage_options (lista), in_stock (booleano) y discount (si se menciona).""", output_schema=ProductDetails ) 

### **Tipos compatibles:** 

- Básicos: str , int , float y bool 

- Colecciones: List[T] y Dict[str, T] 

- Opcional: Optional[T] para campos que aceptan valores nulos 

- Anidados: Otras clases de BaseModel 

### **Importante: Integridad del esquema** 

El esquema define la estructura EXACTA del resultado. El LLM SOLO incluirá los campos que definas en tu Pydantic BaseModel. Si necesitas objetos anidados, como metadatos, errores o paginación en el resultado, debes definirlos todos de forma explícita en el esquema: 

de pydantic importa BaseModel, Field de typing importa List, Dict 

class ApiResponse(BaseModel): status: str = Field(description="correcto, error o parcial") status_code: int = Field(description="Código de estado HTTP") data: Dict = Field(description="Datos principales de la respuesta") metadata: Dict = Field(description="Metadatos de la solicitud") # Debe definirse para que aparezca errors: List[str] = Field(default=[], description="Mensajes de error, si los hubiera") 

# Si no se incluye "metadata" en el esquema, el modelo no incluirá metadatos en el resultado 

# El esquema es un contrato: solo los campos definidos aparecen en las respuestas 

Esto garantiza que obtengas exactamente la estructura que necesitas, ni más ni menos. 

# 🧪 **Ejemplo práctico** 

Creemos un agente de extracción de productos completo con resultados estructurados. 

## **Paso 1: Crea el proyecto** 

adk create product_extractor cd product_extractor 

## **Paso 2: Escribe el código del agente con resultados estructurados** 

Reemplaza el contenido de agent.py por lo siguiente: 

""" Agente de extracción de productos con resultados JSON estructurados. Se muestra cómo usar output_schema del ADK con Pydantic BaseModel. """ 

de google.adk.agents importa LlmAgent de pydantic importa BaseModel, Field 

# Paso 1: Define la estructura del resultado con Pydantic class ProductInfo(BaseModel): product_name: str = Field(description="El nombre completo del producto") price: float = Field(description="El precio en USD") storage: str = Field(description="Capacidad de almacenamiento (p. ej., '256GB')") color: str = Field(default="No se especifica", description="Color del producto, si se menciona") 

# Paso 2: Crea un agente con output_schema root_agent = LlmAgent( model="gemini-2.5-flash", name="product_extractor", description="Extrae información del producto de los mensajes del usuario y devuelve un objeto JSON estructurado", instruction="""Eres un extractor de información de productos. 

Tu tarea: 

- Lee el mensaje del usuario sobre un producto 

- Extrae product_name, price, storage y color (si se mencionan) 

- Responde SOLO con un objeto JSON válido que coincida con este formato: 

{ "product_name": "product name here", "price": 999.99, "storage": "256GB", "color": "titanio negro" } 

Reglas: 

- El precio debe ser un número (sin signos de dólar) 

- El almacenamiento debe incluir la unidad (como GB o TB) 

- Si no se menciona el color, se debe utilizar "No se especifica" 

- SOLO se debe devolver el objeto JSON como resultado, sin ningún texto explicativo""", output_schema=ProductInfo, # Aplica esta estructura exacta output_key="extracted_product" # Almacena el resultado en el estado de la sesión 

) 

## **Paso 3: Ejecuta y prueba** 

adk web 

Visita http://localhost:8000 y prueba estos datos de entrada: 

### **Prueba 1: Información completa** 

Tú: "Quiero el iPhone 15 Pro de 256 GB en titanio negro por $999" 

### **Resultado JSON esperado:** 

{ "product_name": "iPhone 15 Pro", "price": 999.0, "storage": "256GB", "color": "titanio negro" } 

### **Prueba 2: Color faltante** 

Tú: "Samsung Galaxy S24 con 512 GB por $1,199" 

### **Resultado JSON esperado:** 

{ "product_name": "Samsung Galaxy S24", "price": 1199.0, "storage": "512GB", "color": "No se especifica" } 

### **Prueba 3: Formato diferente** 

Tú: "Consígueme una MacBook Pro de 1 TB por un precio de $2,499" 

### **Resultado JSON esperado:** 

{ "product_name": "MacBook Pro", "price": 2499.0, "storage": "1TB", "color": "No se especifica" } 

### **Qué debes tener en cuenta:** 

- ✅ El resultado es **siempre** un objeto JSON válido. 

   - ✅ Se usa **siempre** la misma estructura. 

- 

   - ✅ Los campos faltantes obtienen valores predeterminados. 

- 

- ✅ Es fácil de analizar en tu aplicación. 

# **Conclusiones principales** 

- **output_schema** aplica un resultado JSON estructurado con Pydantic BaseModel. 

- **Pasa la clase** (no una instancia): output_schema=ProductInfo . 

- **output_key** almacena los resultados en el estado de la sesión para la integración de flujos de trabajo. 

- **Las instrucciones deben guiar el formato JSON** : Indica al agente qué debe generar. 

- **La validación es automática** : Las respuestas no válidas se rechazan. 

- **Usa descripciones de campos** : Ayuda al LLM a comprender el propósito de cada campo. 

