# @11 de agosto de 2026 23:08 

### Resumen 

## Descripción General 

- Sesión práctica sobre Google Agent Development Kit LADK2M, toolkit open source para construir agentes con código en múltiples lenguajes y modelos ‣ 

- El objetivo del taller es construir un entrenador de maratón como caso de uso, explorando distintos patrones de orquestación de forma incremental ‣ 

- El laboratorio de código se ejecuta en Cloud Shell dentro de un proyecto de Google Cloud aprovisionado temporalmente ‣ 

- Las sesiones cubren 9 niveles LL0^L4M organizados en tres pilares: Graph, Collaborative y Dynamic ‣ 

## Conceptos Clave de ADK2 

- Un agente se compone de: modelo, instrucción (opcional) y herramientas (opcional) ‣ 

- Los nodos son la unidad básica de construcción y pueden ser: funciones, agentes o humanos en el loop ‣ 

- Regla clave: si es determinista **→** función; si requiere razonamiento **→** agente (ahorra tokens, latencia y costo) ‣ 

- Los nodos se comunican mediante node input y event output con esquemas de datos validados LPydantic) ‣ 

- El Runner + EventLoop es el runtime de ADK que ejecuta el agente de forma asíncrona y emite un stream de eventos ‣ 

## Pilar 0 – Mega Prompt (Prologue) 

- Un solo agente con un prompt gigante genera salida, pero los datos son inventados, no determinista y difícil de probar o intercambiar componentes ‣ 

- Cada pieza de razonamiento paga tokens innecesariamente ‣ 

- Sirve como punto de partida para justificar los patrones más avanzados ‣ 

@11 de agosto de 2026 23:08 

1 

## Pilar 0 – Agente con Herramientas (L0) 

- Se añade una herramienta (función Python de pace splitting) al agente ‣ 

- El modelo invoca la herramienta solo si la pregunta lo requiere; de lo contrario responde con su conocimiento ‣ 

- Establece la base de cómo conectar datos reales vía herramientas ‣ 

## Pilar 1 – Flujos de Trabajo Graph (L1, L2A, L2B) 

- L1 ^ Secuencial: nodo función LFetchConditions, 0 LLMM → nodo agente LAdviceM; flujo lineal simple ‣ ‣ 

- L2A ^ Fan-Out Paralelo + Join: FetchWeather, AnalyzeCourse y PullFitness corren en paralelo, se unen en un JoinNode y el resultado se entrega a un único agente Strategy ‣ ‣ 

   - Ventaja: velocidad significativamente mayor al ejecutar en paralelo ‣ 

- L2B ^ Router Determinista: tras el join, un router basado en temperatura (función, no LLM) enruta hacia agente de estrategia para calor, frío o normal ‣ ‣ 

   - Solo hay un llamado LLM en toda la pipeline ‣ 

## Pilar 2 – Agentes Colaborativos (L3) 

- Patrón para cuando no se sabe de antemano qué agentes se necesitarán; un agente coordinador/concierge decide a cuáles especialistas invocar según la pregunta ‣ ‣ 

- Modos de subagente disponibles: Single-turn LSingleton), Task mode (va y viene con preguntas de seguimiento) y Chat mode ‣ ‣ 

- L3A: pregunta "¿debería correr hoy?" → el concierge consulta hasta 4 especialistas en paralelo (modo singleton) y sintetiza la respuesta ‣ ‣ 

- L3B ^ Task mode: "necesito un chaleco de hidratación" → el agente de equipamiento pausa, solicita talla, el usuario responde, el agente completa y confirma el pedido ‣ ‣ 

## Pilar 3 – Flujos Dinámicos (L4A, L4B) 

- La forma del grafo depende de la entrada en tiempo de ejecución (runtime), no se puede dibujar en diseño ‣ 

@11 de agosto de 2026 23:08 

2 

- L4A ^ Runtime-Sized Fan-Out: un agente decompositor divide la pregunta en 3^7 sub-preguntas → se lanzan N workers en paralelo → agente sintetizador produce el resumen ‣ ‣ 

   - Ejemplo: "Dime todo sobre el maratón de Boston" → descompuesto en 5 sub-preguntas → 5 research agents en paralelo ‣ ‣ 

- L4B ^ Recursivo LDeep Research): los workers pueden descomponerse a mayor profundidad de forma recursiva; se debe controlar ancho y profundidad máximos para evitar costos elevados en tokens ‣ ‣ 

## Guía para Elegir el Patrón Correcto 

- Solo funciones si es determinista (sin LLM necesario) ‣ 

- Graph workflow si el flujo se puede dibujar antes de que lleguen los datos ‣ 

- Collaborative si hay un equipo de agentes conocido pero no se sabe cuántos se invocarán ‣ 

- Dynamic/Programmatic si la forma del grafo depende completamente de la entrada; se controla con Python (recursión, fan-out width, max depth) ‣ 

## Q&A – Puntos Destacados 

- ¿Cuándo usar subagentes vs. un solo agente con muchas herramientas? Factores: aislamiento de contexto, paralelismo, facilidad de prueba, y capacidad de mezclar modelos por subagente ‣ ‣ 

- ADK2 vs ADK1: en ADK1 todo era un agente; en ADK2 hay funciones, agentes, humanos en el loop, join nodes, task mode, singleton mode como construcciones de primera clase ‣ ‣ 

- ¿Se puede usar PHP? ADK soporta actualmente Python, Go, TypeScript y Java; las herramientas externas llamadas por el agente pueden estar en cualquier lenguaje ‣ ‣ 

## Próximas Sesiones 

Asistir a las próximas sesiones de la serie sobre agentes: temas de persistencia, memoria y aprendizaje de experiencias ‣ Notas 

@11 de agosto de 2026 23:08 

3 

### Transcripción 

La IA de Naución está transcribiendo esta reunión. Luego construiré algunos de los conceptos de ADK2 y luego saldremos a la laboratoria de código. Por supuesto, el Kit de Desarrollo de Agentes es sólo un refresco muy rápido. es Google's open source toolkit for building agents. It's code first, available in multiple languages, works with multiple models. And key thing about it is orchestration, right? These are those workflows, whether sequential, loop, parallel, and all of those things that we can use in order to build out. 

diferentes escenarios. Y, por supuesto, ADK también viene con una herramienta, donde te permite probar estas cosas en tu computadora. Por ejemplo, tiene una consola web donde puedes probarlas. También tiene formas por las que puedes desplegar a tus agentes al mundo real. 

Así que esto podría ser, por ejemplo, en Google Cloud Platform. en Cloud Run o Agent Engine o incluso GKE. Así que estas herramientas también son parte del ADK. Ahora, un agente, como saben, es tres cosas, y habrías visto esto varias veces. Tiene su modelo, puede tener una instrucción, y quizás uno o más herramientas para alcanzar a... 

para integrar datos reales con tus APIs o solo algunas funciones que cumplen la instrucción y lo que el usuario le ha pedido. Ahora, en ADK también tenemos este concepto de un operador. Así que básicamente tiene acceso al ADK Runtime And then it takes whatever is the agent logic code that you have to or which you have written and executes it basically, right? So just a little visual representation of what we talked about. So. 

Por ejemplo, cuando un usuario proporciona el prompt, va al agente, que luego va a interpretar y también descifrar o básicamente entender el intento del usuario. Ahora, como parte de eso, el modelo también puede decidir que tiene acceso a estos herramientas que han sido configurados y puede llamar a un herramienta específica. 

No es necesario que cada vez llame a una herramienta o dos, pero dependiendo de la intención, puede mapear a una o dos herramientas que estén disponibles y luego, por supuesto, el modelo interpreta la respuesta y luego la devuelve, es formado y devuelve a la 

That's typically the flow that we expect while we are building out agents. Now, a few constructs that I wanted to share before we get going with the Codelab. es, cuando se trata de ADK2, ¿cómo picturizamos o cómo pensamos cuando construimos estos flujos? 

@11 de agosto de 2026 23:08 

4 

Así que piensa en un nivel alto en el que estarías construyendo nodos, básicamente estos podrían ser nodos secuenciales. Estás viendo nodo A, luego estaremos haciendo algo en B, luego estaremos haciendo algo en C. Ahora, ¿cómo el flujo de datos entre todos ellos? Puedes pensar a un nodo como teniendo un nodo de entrada y teniendo un nodo de salida, ¿verdad? Entonces, el entrado podría ser cualquiera de los datos que vienen desde el nodo anterior upstream. Puedes tener solo estrellas, puedes tener incluso... 

en el que se pueden hacer modelos idénticos y tener datos muy estructurados que van adentro y fuera de los sistemas. Pueden tener una ruta en la que los fans salen, o incluso, perdón, que van a una ruta específica, listas podrían ser producidas. La cosa clave aquí para entender, y también llegaremos al siguiente, es que en ADK]2, mientras que vis a vis ADK]1, 

Los nodos pueden ser cualquier cosa, puede ser una función, puede ser un agente, puede ser un humano en el loop, y así sucede, ¿verdad? Así que se sigue una manera bastante estándar en la que puedes mezclar cosas y, lo más importante, no todo necesita ser un agente. 

Puedes tener Node A como una función, puede tener Node B como un agente, y eventualmente puede tener Node C como un humano en el loop, pero realmente el flujo es bastante estándar, que cada uno de los nodos obtiene un input de nodo, que es un evento. o, ¿sabes?, enviado desde el nodo de arriba y, de manera similar, tiene una salida de evento que luego va a los nodos de abajo y así sucesivamente, ¿cierto? Así que solo manténgase este modelo en mente porque. 

Cuando ves el código después, eso es lo que pasa desde el punto de vista del código. Pero ten en cuenta que es un dato muy estructurado que podrías tener como esquema de input y esquema de salida en el nodo, para asegurarte de que los datos que vienen y que salen son actuales. 

es validado. Ahora, solo quiero retratar esto de nuevo, que es que, como viste, el nodo podría ser una función, podría ser un agente. It could be a human in the loop, you kind of standardize these things into a node. So the way you would want to read this code is if you just look at the bottom, right, it just says there's a start. 

luego hay un FetchWeather y luego hay un AdWord, es como un flujo secuencial que tenemos. Entonces, si miras después del comienzo, lo primero es un FetchWeather, es simplemente una función. Tiene un input de nodo, crea un objeto de datos de tiempo y simplemente lo ejecuta. Eso se envía al advisor, 

@11 de agosto de 2026 23:08 

5 

que es un agente, y el agente lo define en su manera estándar. Tiene un modelo, puede tener una instrucción, puede tener herramientas y así sucesivamente. 

Así que si puedes ver aquí, ¿verdad? Solo quería reiterar el concepto que vimos antes. Son solo nodos. Estos nodos pueden ser funciones, pueden ser agentes y tal. Y va de ese modo. Ahora, ten en cuenta que no todo necesita ser un agente en ADK2, y eso es importante por varias razones, no sólo simplifica algunas cosas. 

Pero también, si algo es determinista, no debe ir a la parte de la razón de un agente que ayuda tanto en términos de velocidad de latencia y también en términos de costes, porque ahora no vas a la parte de la razón de los tokens que se generan para So keep these things in mind and we'll reiterate it several times that when do we use what? If it's deterministic, ideally it should be a function. And if it needs reasoning, it should be a function. 

Dejemos que sea un agente, ¿verdad? Así que esto jugaría un gran papel después cuando se trata de ser eficiente en el uso de tokens y también podríamos ver los resultados, la capacidad de probar ciertos pasos. Tiene algunos. de beneficios claros aquí. Muy rápidamente, mencioné esto un poco antes, pero RUNNER y EVENTLOOP, ¿verdad? Así que esto es realmente cómo vamos a ejecutar nuestras aplicaciones o los agentes hoy, y lo verás en el laboratorio de código también. 

No estaremos usando el ADK web, pero realmente estaremos usando el runner aquí. Este es todo el runtime de ADK, junto con tu agente ejecutado. Así que la manera en que funciona es que el runner toma... de lo que necesitas, el agente o el nodo de ruta que quieres ejecutar, luego empieza a ejecutarlo, obtiene un stream de eventos, ya sea la salida o una función que se llame. 

So and so forth. So you'll see a lot of boilerplate code in your code labs, which is nothing but the runner loop just running. So we will not spend too much part there, but. As you can see from the code, right, it's primarily, you know, you give it to the runner, the runner then starts in an asynchronous fashion and then it just streams a sequence of events, could be the output, could be tools to be called, just the whole. 

Así que, dado todo esto, el contexto, nuevamente, nuestro objetivo es construir un entrenador de maratón. y ver diferentes aproches, desde construir un gran prompto y luego lentamente lo dividir en diferentes patrones. Ahora, este es tu 

@11 de agosto de 2026 23:08 

6 

gran imagen de los varios, diría, ejemplos que hemos tenido en toda la laboratorio de código que estarás ejecutando. 

Ahora, esto es más como una guía para mostrarte que está dividido a través de, puedes decir, nueve niveles o nueve, sabes, diferentes pruebas de código que te mostrarán en adición a uno o dos extraones. Pero realmente hemos clasificado esto a través de pilares. Así que en el primer pilar aprenderás cómo ciertas cosas se pueden lograr usando un flujo gráfico. Pero luego también vamos a sorprender cómo. 

es posiblemente una buena idea ahora romper estas cosas en subagentes y dejar que sean elegidos de los que el subagente puede hacer su trabajo. Así que vamos a mirar los trabajos colaborativos que están en el segundo pilar. Y el tercero es muy codificado, pero es dinámico en el sentido de que no sabes hasta el tiempo de ronda cuantos agentes necesitarás, cuantos nodos necesitarás. 

¿Cuántos nodos deberían hacer algún tipo de descomposición o profundidad a la que deberían ir y hacerlo? Por ejemplo, si te digo que vas a investigar un cierto tópico, podrías decir, ok, un tópico, veré los artículos sobre él, cualquiers papeles sobre él, quizás cualquier video de YouTube sobre él. 

Solo te estoy dando algunos ejemplos. Así que podrías querer romperlo en múltiples tareas y entonces esas podrían ir recursivamente, casi como tareas de investigación profunda, si lo has conocido, así que ese es el patrón que veremos. en Pillar 3, right at the end, okay? Now, having said this context, note that in the code lab, once we launch it in a minute or two, 

también verán estos números que se llaman L0, L1, etc. Todos esos detalles están ahí en el código. Así que vamos a seguir con, también lo lanzaré desde mi sitio. Esta es la laboratorio de código que tenemos que hacer aquí. Voy a abrir esto y verás el tipo de environmiento en el que trabajamos. 

I'll come back to this task one and the other task that we have to do. But for now, the way I would want to or you would want to run this code lab is you go to this particular. link and that sort of opens up, you know, this the ADK to orchestration patterns code lab that we'll be seeing over here. 

Ahora, este es un ambiente en el que estarás ejecutando la laboratorio, así que tienes que hacer clic en el botón de empezar. Pero antes de eso, recuerda que toda la laboratoria de la mesa es, ya sabes, algunas de las cosas que hemos discutido hasta ahora. 

@11 de agosto de 2026 23:08 

7 

as well as every single step that you have to run is pretty much there over here as instructions. So I'm just going to click on this start button right now. Esto proviene de un ambiente para ti, proviene de un proyecto de Google Cloud para ti, con los APIs requeridos y todo, todo preparado para que sea más fácil para ti. 

I do the code labs. As you can see over here right now, it's provisioning some of the resources for the lab. It should be like probably in a minute or so. you will see a form that shows you that the provisioning is complete. And it also will show you the Google Cloud Project, a temporary username, password, et cetera. 

that you have to use to log into this. So that's what you see here. It says Open Cloud Console. And ideally, this would be a good thing to launch. You know, as you can see in an incognito window, that's important so that it doesn't probably clash with some of this because you'll be logging in with the username and password that we see here. 

So I'm going to launch this now in an incognito window. So that's coming up right now. 

I'll just go ahead with the steps to accept some of the terms and conditions and you will be led into the Google Cloud Console. Voy a aceptar esto y continúo. Entonces, lo que tenemos aquí es una consola de Google Cloud. Y, bastante, tienes acceso al proyecto de Google Cloud, el ambiente. 

That has been provisioned. So if I just, you know, go back to the the code lab steps which were there, right? So basically, if I if I just go through this, what we'll be doing in this code lab is we are going to be going through these three orchestration. 

¿sabes? patrones. Y para construir un maratón, levantan a su entrenador. Ahora, aquí, lo que vamos a hacer es, como les dije, tenemos nueve de los ejemplos, tenemos tres pilares, el gráfico, colaborativo y funcionamiento dinámico. Y, por supuesto, junto a esto, aprenderemos 

lo que significa usar cada uno de estos patrones. Entonces, si solo miro abajo. Entonces, nuevamente, hemos cubierto un poco de esto, donde veremos todos estos patrones juntos, patrones fan-out. patterns, dynamic patterns, but really speaking to run this code lab, we need to have a project that's already provisioned to you and everything pretty much runs in Cloud Shell. So just to go through these steps, we've already done that, we've started the code lab. 

@11 de agosto de 2026 23:08 

8 

etcétera. Cloud Shell es nada más que un VM que se te da, te da un ambiente y es por eso que vamos a estar ejecutando algunos de nuestros codes. Así que déjame hacerlo. Básicamente, verás un botón de activar Cloud Shell justo en la parte superior aquí. 

ven, ven entra 

Le ponemos tres. ¿Qué te sirvió, papito? Ve. 

Entra, entra gordito, entra, amorcito entra. Ok, so here we are at our cloud shell and we are right at the terminal from where we can start giving our commands. Ahora, también verás que, por ahora, un proyecto ha sido provisional para ti, y eso es lo que ves aquí, justo en la parte superior, pero si vuelvo a lo que son las próximas cosas que podríamos confirmar. 

es que te dice que ya estás autorizado, eso debería estar bien, en caso de que tengas que hacer eso, puedes ejecutar algunos de estos comandos que se muestran allí y tal vez podamos ejecutar solo uno de estos comandos para you know, configure the, just confirm that our project is all set up correctly. So I will just come over here and put a gcloud config list. 

And that gives a project ID to you. And you will see that this project ID is pretty much similar to the one that you find on. This is the check that you do. So now that this is there, what are the things we need to do next? So as per the code lab that's out here. 

Es solo que te dice configurar un par de cosas en tu environmento, así que vamos a estar usando, tú sabes, a Vertex AI o la plataforma de agentes para, tú sabes, hacer toda la integración con los APIs Gemini detrás de las escenas o modelos. También establece la ubicación del proyecto ID. 

etcétera en play. So just this is an extremely important step. Make sure that these environment variables are all set up. So I'm just going to go ahead and. y una vez que todo esté hecho, hemos diseñado un par de variables ambientales que se utilizan a través de la laboratorio, así que eso es bueno. 

As you can see, the next steps are to create the right Python environment and install the libraries, especially the ADK2 and any other ones that we need. So I'm just going to go through these three steps quickly. So one is to simply, you know, clone the tutorial source code and go into that directory. So we are there. 

Then the next step is to activate or create a Python virtual environment in which will be running all of these things. So. Vamos a hacer eso también. Y una vez 

@11 de agosto de 2026 23:08 

9 

que el ambiente Python esté en lugar, todo lo que necesitamos hacer es simplemente instalar. 

the libraries that I mentioned. It's a quiet install, as you can see. So we'll just copy this and. 

So once this is done, basically what we have is the environment, the source code is all there, the environment is created and you are now ready to run all of your. So I'll just go, while this goes on, I'll just go for a moment back to the task. So the first thing we want to just see is that, OK, you're telling us about these different ADK orchestration patterns which are there. 

¿Cómo podemos volver a la manera en la que escribimos agentes, típicamente? Y no es algo cierto o malo. Siempre lo hacemos como un primer paso. Why don't I just write it in one big prompt and, you know, see that run. And that's also an approach that we start off with. So, for example, I'll just show you. They tell us to run this particular program which is out there. So, let me just first run it for you and then I'll show you the source code also. 

And then we'll discuss as the code lab says, what could be some of the problems, right? So this is a traditional way in which we say one agent gives this large prompt and it should do its magic. So it. As you can see here, at every step, right, you will see which application it tells you to try out. So I'm just going to go there. 

Share it, OK. So this is all done. And I'll just also, in parallel, open up this editor so that we can switch between the source code, and I can show you that. So you can see here that in ADK tutorial. Si lo has clonado sucesivamente, tienes todos los ejemplos y el primero que vamos a usar es el Prologue. 

Ok, déjame crear un poco más de espacio aquí. Entonces, lo que hace este prologue es básicamente un gran programa. Y antes de que lo ejecutemos... Oh, perdón, déjame ejecutarlo. Así que vamos aquí y estamos en la dirección correcta, en el ambiente, en el ambiente virtual. Apenas asegúrese de que todas estas cosas están ahí y aquí vamos. 

van a estar ejecutando un prologue.py en este momento y básicamente aquí estamos diciendo, oye, sólo ayúdame con mi estrategia de Raze Day. para el maratón de Chicago. Vamos a ver el código en un rato, pero básicamente lo que está sucediendo detrás de las escenas es que tenemos un gran promedio, lo hemos dado, y vamos a ver qué es la salida que viene. 

Ahora, mientras esto sucede, déjame mostrarte el código muy rápidamente. Y este es el mismo código que se llama Draw. Como les dije, lo ejecutamos todo 

@11 de agosto de 2026 23:08 

10 

en el Runner, así que no tenemos que ir demasiado a cada una de esas cosas, pero verás que hacia el final siempre hay un... 

Little bit of a template code that runs the application and so on. Now, if you look at this over here, right, the main node is the mega coach. And what does the mega coach do? It's just one agent. It's using a specific model. And if you notice over here, one large prompt. That's it. 

de que tienes un sistema de estrategia de maratón completo, tienes acceso, tienes acceso a esto y eso, y ahora lo reportas y lo analizas y así sucesivamente. Pero la primera cosa que debería golpearte es. Just by giving out this, let's see if you got some output. And here you go. So it's literally given us whatever we asked for by just one single prompt, which is that. 

Ok, esta es la estrategia del día de la carrera, luego se te da el asesoramiento de la salud. Se ha ido muy bien y se ha hecho. Hay algunos consejos aquí y eso es importante. Hay algunas preguntas. ¿De dónde vinieron las temperaturas? ¿De dónde vinieron los niveles del mar? ¿De dónde vinieron las leyes de entrenamiento? Entonces, la primera cosa que debería golpearte, y de nuevo, no hay nada malo o bien, solo estamos tratando de... 

en una forma incremental. Un gran prompt, un megaprompt, sin herramientas, pero todavía tenemos alguna salida del modelo. De nuevo, esto claramente muestra que el modelo va a hacer lo mejor que puede. you know, made it even reach out to any real world data, but it's still given us something. So basically the problem is, while you may still feel that some of these things are okay, 

It has got some problems, right? And what could be some of the problems? You will see that also very clearly in the code lab description. Es decir, mientras se ve una estrategia muy confiable, específica, bien formada, los números son inventados, todo está hecho. En otras palabras, no se puede confiar en ello. 

You can't easily test this stuff because it's all there. Maybe it's not even deterministic. Every time you run it, you might get some different kind of data. You can't simply swap something in an easy fashion. Y más importante, puede haber algunas cosas que solo hubieran sido una llamada de función, y no necesariamente hay que ir por toda la raza y cosas así. 

Several problems you might have also seen it as you got some experience building agents that these are the inherent problems if you try to fit everything into one agent. y un gran megaprompter sin acceso a herramientas y así sucesivamente. Así que ese fue el propósito de nuestro primer. Solo para establecer la premisa de por qué no un gran. 

@11 de agosto de 2026 23:08 

11 

Así que hemos visto algunos de estos. Ahora, si vamos al siguiente, dice que empecemos a construir nuestro primer agente, tal vez con un poco de herramientas, No puede ser completo, pero es como construir lo que ya sabes que un agente tiene un modelo, un set de instrucciones y uno o dos herramientas. 

Ahora, le estamos dando un ejemplo de función Python. Esto es probablemente ya conocido a la mayoría de ustedes, que si ejecutas este particular, te mostraré lo que el primer agente con algunos herramientas empieza a ver como. Así que es algo así que. 

y luego el agente decidirá que si la búsqueda del usuario tiene un necesidad de invocar una herramienta que hemos definido, usará la herramienta o no usará la herramienta. Así que es por eso que veis dos... samples o sample applications, sample ways in which we're telling you to run this application, which is you just run this first. Let's see the code and understand what's going on, right? 

So this is the L0 first agent. Let me again switch back to you know, the code that we had. So I'm going to close this and I'm just going to navigate it here so that you also know what we are going to show. Esto es, perdón, nuestro agente primero L0, y si ves al agente, veámos qué está pasando en el código. Entonces, en la parte de abajo, déjame ir primero, como te dije, va a lanzar la cosa. 

Ahora, antes de que lleguemos al código, veámos el agente, ¿verdad? Hay una pequeña diferencia entre el anterior. De hecho, ahora le hemos dado uno en particular. And this is something that the model may call this, depending upon the question. So basically, it's not that we have fixed all of these things. For example, it's just got a function right now that helps you split your timing. If you want to do it in three hours, it says how you should pace it. 

Pero todo lo demás, si no hay herramienta para ello, el agente va a llegar con las respuestas. Así que básicamente dice que eres un entrenador amigable. But answer the runner's question, be specific. If the runner mentions, call the function. But otherwise, if you ask some other question, it's not going to work out. So if I go back to. 

The, you know, examples we are telling you to run. See, the first one is saying that just go ahead and, you know, run this. And you've seen the default code that we've got some timing that is being asked for. But if you ask some other question and it's not going to be using the tool in any case. So, for example, if I 

@11 de agosto de 2026 23:08 

12 

just copy this one and say so. So if I just show you how the code may eventually run. 

It's clearly saying if you don't pass anything as a parameter, which is what we are doing, it says very specifically I want to run it in this much. So basically it should use our function that we've created. So let me clear this and run this for you. So this ideally will end up invoking the paste setting, the tool that we've created, right? 

Eso es básicamente lo que es. Como pueden ver aquí, se llama el PlaySplits, el tool de PlaySplits, el tool ha registrado algún dato y luego el entrenador lo ha sintetizado muy bien. And just used exactly what it got from the function to do that. But as is pointed out in the what you call example, if you if you do this, I mean, if you give this value. 

No hay nada sobre el ajuste del ritmo o nada, así que va a volver a su manera de tratar de responder a lo mejor de su conocimiento, no hay herramienta. en este caso. De nuevo, podrías haber ya construido agentes con herramientas, pero esto es solo para establecer las cosas. Así que, sí, no se ha invocado ninguna herramienta, pero ha venido con una respuesta en particular. Así que, eventualmente, lo que intentamos conseguir es 

In order to make the agent useful, you would anyways build out a set of tools which connects to your real world data. So now let's go back to. en la laboratorio de código. Así que eso es básicamente lo que es el paso L0, que es como cuando tenemos a nuestro primer agente ADK con herramientas. Eventualmente llamará a las herramientas si están ahí, pero si no es capaz de... 

la respuesta y tal. Así que esa es esta parte. Ahora, la próxima cosa es donde empezaremos a saltar a nuestro gráfico de workflows. And before we start looking at the code, I mean, we could go through all of the code immediately, but let me set some context to you with a few slides and then we'll jump into this L1 workflow. 

So I'm back at my slides, we've already done this code lab and we've set up the environment. Mega prompt we already do just to reiterate a few things we've done so far. Hemos mirado el megaprompter, hemos dicho un agente, un código grande, obviamente muy difícil de confiar en o probarlo también, y estás pagando por casi cada pieza de razonamiento con la que estás haciendo el modelo. 

También vimos donde añadimos un tool y vimos cómo un modelo podría invocar un tool si lo necesitaba. Así que hemos realizado esto. ejemplo 

@11 de agosto de 2026 23:08 

13 

también. Así que ahora vamos a ir a nuestro primer pilar, que es el pilar gráfico. Y ahí vamos a hablar ahora de lo que significa crear funcionamientos basados en gráficos en ADK2. 

a un nivel alto, ¿verdad? Piénsalo de esta manera. Usted ya ha definido cómo debería ir el flujo. Así que eso es lo que significa el artículo, que es que se dibuja el flujo de trabajo antes de que alcance algún ingreso. Pero en otras palabras, Es solo que realmente sabes cómo debería ir. Por ejemplo, lo que ves en el diagrama es un ejemplo, un escenario que tal vez quieras que suceda. Así que significa invocar una función primero, dependiendo de la, tú sabes, el valor de. 

la función o lo que vuelve con ella. Puedes querer que un humano la chequee o simplemente la denuncie, o puedes ir a otra función y así. Entonces aquí literalmente ves un conjunto de nodos. some parts possible, you know, routing that's happening possible. Who knows? We will see as later on we could even combine outputs from several nodes and then synthesize, join and go forward. Right? So. 

todos estos escenarios podrían ser construidos usando estos gráficos y eso es lo que estamos viendo. La cosa clave aquí y lo cubrimos un poco antes, pero es bueno leerlo. Hablamos de nodos y dijimos que esto podría ser una función si es determinista o puede ser un agente si necesita respuesta. Ahora, eso es una buena cosa para hacer porque no necesitas llamar a un agente para cada cosa. Si es solo una función, si es solo una decisión de ruta, tal vez todo lo que necesitas es un código determinista. 

No necesitas a un agente para responder y por eso. también puedes guardar un montón de tokens. Así que, de nuevo, la estrategia es empujar el trabajo determinista a funciones y, si es necesario, traer el DLL. Por eso, en este diagrama verás algo en la parte superior. Uno dice función, el otro es el inputo humano. 

Otra es una herramienta, otra es un LLM y así sucesivamente, ¿verdad? Así que asegúrate de elegir las cosas correctas para el proceso completo. Eso realmente ayudará, no solo a acelerar, sino también a salvar. Ahora, lo que vamos a hacer en los próximos ejemplos, ¿verdad? Es bastante claro, es algo de este tipo, que vimos L0 y L1, que son 

pero ahora en L1, L2, A y B, los tres más ejemplos que están ahí en este pilar, en realidad veremos varias cosas. ¿Podemos crear un flujo secuencial? Primero, ¿puedo extraer algo de una función? And then we advise, then we'll 

@11 de agosto de 2026 23:08 

14 

also see, can we do things in a parallel way and then join and then so on, give a strategy, we'll also see a router. 

En caso de que la temperatura sea caliente en el día para la carrera de maratón, entonces dános una estrategia que nos ayude a encontrar condiciones calientes o a manejar las condiciones calientes. pero en caso de que sea frío. Así que no necesariamente necesitas una raza para que suceda. Por eso, estas son todas las formas interesantes por las que se combinarán y luego lo reunirán juntos al final. 

Así que esos son los ejemplos que vamos a ver. Así que el primero que vamos a ver aquí es lo siguiente. Y voy a cambiar a la laboratorio de código en un rato, que es la tasa L1. So we are going to be building out basically a very basic graph workflow which has a start node, it has got a function node and then it's got an agent node. Basically we'll fetch some conditions via simply a function. 

y luego le dirá a su agente. Si ves el código en el botón de abajo, es bastante claro, lee desde el fondo, que tienes un flujo de trabajo, ¿verdad? Y tiene... Es básicamente una lista de tuples y un tuple es una cosa secuencial. Así que tienes un nodo de comienzo, condiciones de búsqueda y un consejo. 

So after start it simply goes to fetch conditions. As I told you, it could have a node input and an event output. How the data is passed between fetch conditions and advice would be via. you know, the input output node. So all we are doing in fetch conditions is get some dummy conditions. We output that to the next node, which gets fed to advise. And then advise, we have an input schema we could apply, which is a good thing that thereby you don't get all the verbose text also. 

que salen. Simplemente, por ejemplo, si hay un agente y luego le das a un nodo de función, el nodo de función simplemente puede obtener una esquema muy específica que salva en, exactamente los bills, los tokens y más, ¿verdad? Y además el dato está validado. Así que este es el más simple de los trabajos que podemos hacer y lo veremos y luego volveremos otra vez aquí. 

So let me go back to the code lab. So I'm in the first workflow code lab, which you're seeing over here. y básicamente todo lo que vamos a hacer es un escenario que se ve así, que es empezar algo, vamos a buscar algunas condiciones y consejos. Esta es la secuencia. 

Y presten atención al hecho de que dice función y también dice agente. El primer nodo es simplemente una función. El segundo nodo... es un agente. La función dice que es 0 LLM porque simplemente no estamos usando el LLM 

@11 de agosto de 2026 23:08 

15 

para hacer nada aquí, mientras que este es un LLM y puede sintetizar y hacer nada con el 

dependiendo de la instrucción que tengas. De nuevo, entre los nodos, como les dije, hay un input de nodo que se recibe, y cuando recibes una salida de un evento, From an upstream node, that's what is passed as a node input to the following, that's how you want to sort of visualize. So now let's see the code and what it tells us to do. Right. So basically all it's saying over here, if you see the code. 

es que tenemos un simple flujo de trabajo que tiene Start, Fetch Conditions y Advance. Y en Fetch Conditions tienes un nodo de función. Zero LLM being called over here, but in the next one you can see that it's the standard way we define our agent, which is the name, the model. 

Vamos a ver después, mientras lo cubrimos, qué significa Singleton, chat y otras cosas. No te preocupes por eso. Tiene un esquema de ingresos y algunas instrucciones basadas en eso. ¿Correcto? Entonces, nuevamente, los detalles de la laboratorio de código tienen un montón de, diría yo, explicaciones, etc. también, ¿verdad? Entonces, vamos a intentar ejecutar esto y ver cómo funciona todo. 

Así que lo que nos está diciendo hacer es, si yo solo me voy, es ejecutar este L1 Graph Basics Workflow, veremos el código también mientras me muevo allí. Así que voy a. Un saludo. 

Share this. OK, I'm just going to clear this before I run it. Let's see the code. So we are in L1, Graph Basics and Workflow. Ok, so again, if I just go back to the, go down over there, the standard runner stuff as I mentioned is just going to be. ah running your main root node, which are given in this case. Our node is the workflow node. If I look at the workflow node, what does it have? The same thing as I mentioned. 

Tiene un comienzo, tiene condiciones de pérdida y tiene advertencia. ¿Qué tienen las condiciones de pérdida? Eso es nada más una función de avión, ¿verdad? Y en el mundo real podría dar un API y obtener el datos. Así que puedes ver. ¿Cuánto fácil sería incluso probar esto? ¿Cuánto fácil sería incluso intercambiar diferentes API si necesitas, o desde una API dummy a una API real? Veamos la compartilización de todo esto. 

And secondly, you know, we've not sort of made any kind of reasoning that's going on over here. Here, all it does is it builds out a Pydantic class and it simply uses the model.dump in order to... pase a todo ese dato estructural al 

@11 de agosto de 2026 23:08 

16 

agente, que lo obtiene y sólo dice, debido a las condiciones del día de hoy, déjalo basado en esto y referencia la actual temperatura y viento. 

You see that? So that's how it's actually referencing any of the temperature, wind, and other conditions that you can always specify in the instructions. Así que dado esto, voy de vuelta al terminal y si solo ejecuto este trabajo de GraphBasics, eso es bastante lo que esperaremos. 

que se llama ahora las condiciones de búsqueda y ese nodo de función ha dado ese valor en particular y luego de inmediato encuentras que el siguiente, que es el agente de consejo, ya ha combinado. las recomendaciones o cualquiera que sea la salida que tuvo como input de nodo del anterior y se hizo su trabajo, ¿verdad? Así que básicamente es así. 

construimos un muy simple flujo de trabajo gráfico con un nodo de comienzo, un nodo de función y luego un nodo de agente. Ahora, continuemos construyendo esto. Así que voy a volver al laberinto de código. ¿Y qué es lo siguiente que nos dice? Nos dice que vamos a aprender algo llamado 

Parallel fan out and a joint node. Now, what does this mean really? So let me just zoom in first to a nice diagram out here. Sorry, just let me have some water. Vamos a volver a lo que estábamos diciendo que vamos a construir, el entrenamiento de maratón. And in that, if you recollect, we had to do several things, one is to get weather conditions, maybe analyze the course, even get fitness data for the current participant and so on, right? 

y usar toda esa información para sintetizar y dar una respuesta en términos de una estrategia. Esa es la cosa a nivel alto que queríamos hacer. Lo vimos inicialmente como un mega-prompt, que podíamos dar todo en un prompt, y luego dependiendo del LLM, o si ya tenías herramientas conectadas a él, 

It might be able to combine it and give you data, but we saw the problems with it. So now what we are going to be looking at is we saw a sequential, one of the patterns is very simple sequential graph workflow. Ahora, piensa de esta manera, podría usar el mismo flujo de trabajo secundario y decir, primero el clima, luego analizar el curso y luego la salud total. 

And then maybe combine all of this data and somehow give a strategy, right? That's one way you could do that also. But you know that these pieces of information are independent of each other. If I say just analyze the Chicago Marathon and the course that is there, I could do that separately, whether it could be fetched separately. 

@11 de agosto de 2026 23:08 

17 

FITNESS data could be pressed separately. So what you're seeing over here is a new construct which helps you run all of these things in parallel. So you're literally saying I want to run FetchWeather, AnalyzeScore, FullFitness in parallel. Let that thing be joined or basically combine all of that data or maybe map it based on what function return what right into a joint node and that payload. 

es entonces dado a una estrategia que podría ser un agente. Así que puedes ver aquí, literalmente el agente viene solo al final. Tienes estas construcciones ya disponibles en ADK2. que te permite ejecutar funciones en paralelo. Luego tienes un nodo junto que lo combinará. Espera a que cada uno de estos nodos termine y hazlo. Esto tiene varios beneficios, no solo desde el punto de vista de prueba. 

pero también el hecho de que podrías hacer estas cosas en Parallel, ¿verdad? Así que, si ves aquí, estas tres funciones, están funcionando en Parallel. No estás esperando que una termine con la otra. Literalmente, se hará mucho más rápido. Secondly, you got join node, that's a beautiful way by which you could wait for all three of them to complete and then put it into one tight payload. 

que se le da a la estrategia, que es el único agente que tendremos en este puzzle que lo usará para luego llegar a una estrategia. Así que. Y algunas de las cosas que ven aquí también mencionan que todos los tres en realidad empiezan juntos, lo que significa que todos los tres de estos literalmente empiezan juntos, por lo que el que toma más tiempo puede acabar siendo tu puerta, pero de otra manera, en ese particular ámbito de tiempo, 

que podríamos completar todas estas cosas, ¿verdad? Así que veámos todo eso, veámos el código también una vez más y luego podremos ejecutar esta particular cosa que nos está diciendo. So let's copy this one for now and then it will be either the hot or the cold strategy, etc. So I'm going to go back to. 

y vamos a la jornada paralela. Vamos a mirar el código. Solo unos minutos. Disculpa. Así que déjame ir a la parte correcta donde el flujo de trabajo es definido. Este es nuestro flujo de trabajo. And you can see it's a fan out. So things are happening in parallel. Then we are joining and then we've got one particular agent. So. How are we defining these writers? I told you these are is nothing but a list of couples. 

y tienes el nodo de comienzo que dice, hey, vete y, ¿sabes qué? analiza el clima, analiza la salud, todas estas cosas suceden juntos. Todos ellos eventualmente. End up at joining right and what's the joint input. So we can 

@11 de agosto de 2026 23:08 

18 

actually see it's a joint node and then finally the joint inputs will be given to something called a strategy. 

And this strategy is our agent, which is just it says the input schema is the bundled data, of course, there's also output schema that we have defined. And then the instruction clearly says we you receive bundled data from these three things we ran in parallel and produce a race strategy that adapts to it. So just to, I mean, again, visualize it, all we've done is you've defined a thing that starts. 

se ejecutan tres de estas funciones en parálisis, las unen juntas y luego el resultado de la unión, un dato bundado, es dado a una única estrategia de agente que luego usa esa información para crear eso. So I'm just going to go back to our terminal and let me just clear this. And then. And again, we are passing. 

Así que, como pueden ver aquí, comenzamos un timer, y si han visto que se han acabado, y luego este es el dato de ronda de carreras que ha sido proporcionado, ¿verdad? And then it uses that information to then create your strategy around it. So as you can see over here, total time, you will see if you try to do these things in sequence. 

Probablemente habrá mucho más tiempo que va a salir, tal vez si pusieras todo en un agente para resolver, eso también podría haber tomado mucho más tiempo. Así que hicimos un fan-out, hicimos un join. Y luego, finalmente, hicimos un llamado LLM que trajo todas estas cosas juntos para hacer ese flujo, ¿verdad? Entonces, si voy de vuelta a nuestro laboratorio de código por un momento. 

So that's what we pretty much did in this L2A, which is parallel and joint node. Now, here's an interesting thing that we'll be doing next in L2B, which will then complete that particular pillar. Ahora, mirenlo de este modo, dependiendo del clima, puede que sea caliente o frío, ¿verdad? Y queremos que suceda algún tipo de ruta adicional para que nos de un calor caliente. 

de la estrategia del clima o de las condiciones del clima o si va a ser frío, déjanos una estrategia basada en eso. Primero, déjame mostrarte el diagrama para que puedas entender lo que intentamos hacer. Entonces, en lugar de darlo a un agente y luego determinar si es caliente, si es esta temperatura, y dejando que el agente lo haga, nosotros simplemente implementamos otro router aquí. 

que dice que todo es lo mismo que antes. Entonces tienes 3 de estas cosas que están siendo llevadas a un nodo adjoint. Pero luego, estamos 

@11 de agosto de 2026 23:08 

19 

introduciendo un router. Y el router dice que desde el FetchWeather Usa la temperatura, y si es caliente, déjalo a un agente que sepa sobre una estrategia de carrera caliente, o una estrategia de carrera normal, o en caso de que sea frío, ¿qué podría ser la estrategia de carrera? 

Así que es bastante interesante, en un sentido, la ruta es solo otra función, no es un LLM. En nuestro ejemplo anterior, si tuvieramos que hacer una ruta caliente o una ruta constante, Y probablemente estaríamos dependiendo nuevamente de un agente para determinar basado en los valores y luego darnos una estrategia o dos diferentes. Pero ahora, miren esto, hemos descompuesto más adelante. Esto te ayuda realmente a cambiar, cambiar, cualquier cosa en cualquier punto en particular. 

pero tienes un código muy determinista de ruta que está sucediendo. Entonces, ¿qué es lo que parece un rutaje? La forma en que quieres verlo, esta es la ruta por si toma un input de nodo. El input del nodo es nada más que el fecho, así que donde quiera que tenga este fecho, la temperatura, sólo lo usa para determinar si el valor de la ruta está caliente, fría o normal. 

And then this is the key thing. When you output an event, instead of just throwing out the data, it's also giving a route. And depending upon the route... Puedes ver que hay un nodo más que dice que si está caliente, déjalo al agente de estrategia caliente, y si está normal, a este agente. Veamos el código y luego ejecutaremos todo esto. Es bastante interesante. 

I'll just copy this so that we have it ready. I'm going to switch to our code. I'm going to go to let me just clear this. I'll go to open editor. Y vamos a ir a un L2. Este es el último en este pilar. Así que vamos a workflow, que está ahí afuera. Again, first thing that I just want to concentrate on is how we have defined the workflow. So if you see the workflow, the three start nodes are the same. Sorry, the three... 

Parallel nodes from the start at the same patch, weather, analyze course, pull, fitness. These all go to join inputs. And the join inputs now go to a route by weather. ¿Qué hace la ruta por el clima? Como les dije, sólo verifica. Es una ruta determinista. No es el modelo. Esa es otra gran ventaja. Tienes tu condición de ruta aquí. 

y simplemente va a establecer un parámetro que es el valor, si es caliente, frío o no. Y luego, si vuelvo al flujo de trabajo, dice que si es un diccionario. Así que si es caliente, por favor, vámonos a este agente. Si es normal, vámonos a este. Ahora, veámos la estrategia caliente. Así que ahí es donde el agente entra y 

@11 de agosto de 2026 23:08 

20 

dice, tú eres un coche de maratón, caminando en condiciones calientes, el calor es un riesgo, descansa, hidratea. 

So and so, right? So a nice way by which you can actually create this. So they go back to the terminal, run this. 

So, again, you may not need the parameter, you could just possibly change the code and let, again, the thing is we have to simulate what's coming, so that's why. Están pasando este parámetro para que, porque no estamos mirando la condición de vida, así que es solo para crear el salto para el router y luego, sabes, el router va a ese particular. 

una estrategia de agentes de carrera y luego te da una estrategia diferente a base de eso. Y, de nuevo, puedes ver la velocidad con la que todo esto está sucediendo. Debería ser la primera cosa que te ataca. versus if you had put all of this in some mega prompt or if you even had agents, sorry, nodes, which were agents and you made them do the reasoning. You just saw over here, if I just. 

Vamos a volver a nuestro laboratorio de código. Verás aquí que, de nuevo, el router es algo determinado. Todo esto en paralelo que está funcionando, de nuevo, funciona. una de estas tres, esta es la única vez en la que el agente actualmente viene, ¿verdad? Así que voy a volver a nuestros slides y luego vamos a estar mirando el siguiente pilar, que es el agente colaborativo. Así que, espero que lo tengas ahora. Así que lo que hemos hecho hasta ahora es... 

Hemos completado este tipo de pilar aquí ahora mismo. Hemos construido un agente, hemos añadido una herramienta, hemos visto nuestro primer flujo de trabajo secuencial. Luego hicimos un intercambio paralelo y finalmente hicimos algún routing también. So, let me go back to the slides and just again, to quickly refresh in this L1, we did a sequential workflow, then we also saw... 

de todo el paro, que es, de nuevo, todavía un solo llamado LLM, ¿verdad? Entonces, y luego, finalmente, vimos todo el pilar, que es que Nosotros fuimos en paralelo para obtener el datos, lo unimos y luego usamos un router basado en funciones deterministas para definir a qué agente en particular debería ir. Así que si ves aquí, los puentes LLM. 

para toda la pipelínea, todavía solo hay una, ¿de acuerdo? Así que ahora, pasamos al siguiente pilar. De nuevo, de nuevo, estos son sólo momentos de pilar uno para cuidar. Pero la siguiente, que es colaborativa. Ahora, piensa de esta manera. Hasta ahora, hemos estado preguntando algunas preguntas sobre la estrategia de la elección y tal vez 

@11 de agosto de 2026 23:08 

21 

Decidimos que tenemos un flujo de trabajo gráfico que obtendrá todas estas tres informaciones y luego se unirá y te dará el dato. Eso es genial. Pero ahora piensa de esta manera. It is possible that a user who is using or talking to your agent might just say, you know, I'm having a knee problem, or someone might just say, you know, I'm not feeling so good to run to class. 

mañana o algo de ese tipo. Ahora, ¿cómo se compone básicamente el proyecto para eso? Ahora, obviamente no sabes, como mencionamos, los gráficos son cosas por las que sabes alrededor de antes, antes de que el datos lleguen hasta cómo se va a ejecutar. Pero en escenarios como este, no sabes lo que el usuario te va a preguntar, por lo que no sabes 

de cómo exactamente, ¿sabes?, rastrear nuestra lógica de rastreo. Así que es por eso que la cosa colaborativa viene, y la idea es que no hay edificios declarados como tal, básicamente se va a un, diría coordinador o un concierge, ¿verdad? Este es un LLM que decide que, basado en su pregunta, 

Yo tengo un montón de subagentes o especialistas. Uno podría ser un especialista médico. Uno podría ser un especialista del clima. Uno podría ser un especialista de pacientes, un especialista de nutrición. Así que dependiendo de lo que pidas, yo podría elegir uno o más agentes. 

entonces enviar su solicitud para obtener la información de ellos y luego sintetizar y darles la respuesta. Esa es la idea de todo el trabajo colaborativo, pero hay algunas nuences aquí. ¿Va a ser que solo puedo enviar las cosas? Porque en ADK]1, si tuvieras subagentes y solo transferirías a los agentes, ellos solo entrarían y esa conversación acabaría allí. 

Pero en este caso, tal vez tenga una necesidad de enviar una solicitud a un médico y un agente de carrera o un agente médico. Combinar todo esto, porque dependiendo de tu cuenta, podría llamar a todos tres de ellos. o solo llamar a uno o solo llamar a dos, ¿verdad? Y necesito las respuestas para que pueda combinar y continuar la conversación requerida con el usuario, ¿verdad? Y a veces también puede haber un necesito por el que. 

No has dado toda la información que es suficiente para que el subagente responda. Así que puede que haya un poco de modo de charla o de modo de tarea. me dan toda la información que necesito para que pueda responder esto para ti. Hay turno solo, hay modo de charla, hay modo de tarea. Vamos a verlo, pero la imagen más grande es... 

que en este patrón tienes un agente coordinador que decide a base de la búsqueda, porque no sabes de afuera cuántos o qué agentes vas a necesitar 

@11 de agosto de 2026 23:08 

22 

para hablar con. Pero todavía tengo acceso a un grupo de subagentes y puedo posiblemente llamarlos, recoger el datos y luego sintetizar y dar la respuesta de vuelta. 

So that's basically what's going to be happening over here. So as you can see, as an example, there's a coordinator and six specialists. But most importantly, it's the question that determines who fires or who gets executed. So, for example, if it's what should I eat? 

Pero por ejemplo, si mi pie duele en mi 18, podría necesitar un poco más de información de la parte médica de las cosas, tal vez de la parte de aquí, o lo que sea. Así que puedes ver que si se trata de un ajuste de equipos, necesito zapatillas, tal vez en ese escenario, como te dije, es como un modo de tarea que es, sí, puedo darlo al agente de equipos, pero el agente de equipos puede incluso preguntarte, ¿de qué tamaño? 

Y así termina. Básicamente hay varias maneras. Puedo llamar a un agente y obtener el dato o el agente puede ir en modo de tarea y volver y volver para obtener las respuestas y así sucesivamente. Básicamente, la cosa interesante aquí es que no sabemos en adelante cuántos agentes necesitaremos, pero dejaremos esa decisión a este agente coordinador. Y así es como parece. 

de la base. Así que tenemos, este es un ejemplo diferente, pero tenemos un agente, un planeador de viajes. Tiene subagentes llamados agentes del clima y agentes de vuelo. Y nuevamente, esos son configurados en nuestro modo estándar. Pero dependiendo de lo que preguntes al planeador de viajes, podrías decir, ¿cómo está el clima allí? O podrías decir, estoy planeando tomar algunos vuelos en esta temporada a la ciudad. En ese caso, podría llamar. 

por los agentes, ¿verdad? Así que lo dejamos a ellos. Y de nuevo, para resumir aquí rápidamente, no necesitas saber todo de esto en este punto en el tiempo, pero ten en cuenta. que idealmente estaríamos lanzando a los subagentes en cualquiera de estos módulos, que es el módulo de chat, el módulo de tarea o el módulo de un solo paso. Ahora, el módulo de tarea, perdón, el módulo de chat es algo que podríamos. 

ah, you know, probably not be looking at because in one one if you give it to a subagent subagent, this was that does it and you lose the control because the control is now finally with the subagent. y se cierra la conversación. Pero estaremos mirando las tareas y Singleton. Y Singleton es más como, sabes, le das la tarea al subagente, vuelve y estas también podrían ser operadas en paralelo. 

@11 de agosto de 2026 23:08 

23 

Pero una tarea es algo que quizás quieras tener un par de preguntas hasta que todo esté respondido. Es solo un parámetro muy sencillo que colocas en el nodo y lo verás en un momento. So basically we will be looking at the first example now in our, you know, in the second pillar, which is the examples that, so we got this one, then we got the finish line and so on. 

So let's go on now to our code lab and begin over there again. So in task number 7, which is L3A, Lo que vamos a hacer es algo de este tipo y yo solo copiaré este comando aquí, pero o quizás hagámoslo. Vamos a hacer este, que no queremos ver el modo de charla, aunque puedes probarlo después. 

Idealmente, vamos a mirar esta pregunta, ¿debería levantarme hoy? ¿Y qué significa eso? Puedes ver la complejidad o la manera en que esta pregunta ha sido preguntada, ¿debería levantarme hoy? ¿Qué significa eso? ¿A qué agente debería darlo? Y eso es precisamente lo que esta diagrama sorprende, que tienes este coordinador en general, que es el concierge de la carrera. 

Y dependiendo de la pregunta, el concierge puede llamar a cualquiera de estos especialistas en un solo turno y luego sintetiza la respuesta. Así que no sabemos, puede llamar, dependiendo de, aquí es como, ¿debería llamar hoy? Pero podría ser cualquier otra pregunta que te requiera llamar a la médica. Puede necesitar llamar a la nutrición, tal vez el clima y así. Así que nuevamente, vamos a usar el modo singleton. 

That's pretty much how it's going to turn out to be. So I'm going to just take this. I'm going to go back to our. Sample here, sorry, the environment and before I even run this code, which is out here, let us first, as we've been doing. Look at the L3 collaborative, you know, example, the concierge. What does the concierge really look like? Once again, I'm just going to go right till the end. 

la cosa en la que se construye el agente, un minuto, perdón, el todo, el flujo inicial. Así que esto es un mensaje de construcción. 

Ok. So basically this is like, you know, we are just running this method called ask question and what does that do, right? Así que básicamente, si ves aquí, hay algo que se llama el coordinador. Hay una función de equipo de construcción aquí. Vamos a ver qué está pasando. Porque después el corredor llega. 

y construye la coordinación. Entonces, ¿qué está pasando en el equipo de construcción? Por el momento, veámoslo. Básicamente, aquí estamos construyendo un nuevo equipo, ¿verdad? Así que estamos diciendo que para tantos especialistas, ya hemos definido cuántos especialistas hay, seis de ellos. 

@11 de agosto de 2026 23:08 

24 

So for as many specialists that are there, look, it's actually creating a list of agents. So basically return back or, you know, the whole. un equipo de un equipo que tiene a todos estos agentes en él, así que tiene el modelo, etcétera, el equipo que se ha construido y así sucesivamente. 

Una vez esto esté hecho, básicamente el equipo ha sido construido con el Reyes Concierge. Ahora, perdón. Esto, sí. Una vez esto esté hecho. It's going to then go and hit each of these subagents that are there. So if I go to this building, sorry, one second. So we ask and then it says, depending upon this runner. 

What are the sub-questions and what are the questions that it's going to be giving each one of them. And then it sort of, it won't do the transfer to agent, but in this case it will do a... el subagente y regresar con la respuesta. Así que si lo ejecutas, empieza a ser un poco más claro. 

Así que tenemos un equipo de agentes, tenemos una pregunta que ha sido dada al concierge y el concierge luego determina lo que está pasando. Así que es como, ¿debería votar hoy? y todos los subagentes han sido lanzados en un modo de una sola vuelta. Así que si ves aquí, ¿debería correr hoy? Se ha ido en realidad y dijo, tal vez, voy a ir y preguntar a estos cuatro, ¿sabes? 

Oops, what happened? 

Ok, maybe at times it also does a retry in case there is any kind of an issue. So if I just go back to the flow, it's got these four subagents that it wants to call out to. Y a cada uno de estos, básicamente dice, ok, ¿debería reanudar hoy? ¿Qué quieres volver con como respuesta? De hecho, dado que todos estos chicos han respondido de alguna manera, 

a los especialistas que fueron elegidos para esta tarea o así, y dado ahora. Ok, de nuevo, llega con algo de lo que se llama escenarios. Esto no es datos reales. Si ves el código. Hemos construido ciertos escenarios, y dependiendo del escenario aquí, dice que médicos y especialistas de temperatura te dicen contra la carrera hoy. 

las condiciones extremas, por favor, priorícate y así sucesivamente. Así que realmente se ha considerado, ¿debería caminar hoy? Y dijeron, tal vez, veamos primero el clima, si es demasiado caliente o algo así, o si el escenario dice que tu data de entrenamiento no ha sido muy buena. 

Así que si solo voy a volver al escenario que hicimos aquí. Así que tened en cuenta esto, esto es lo que realmente hemos hecho. Hicimos, ¿debería correr hoy? y miramos a estos diferentes subagentes y luego los subagentes 

@11 de agosto de 2026 23:08 

25 

respondieron cada uno de ellos con lo que tenían que hacer y luego una sola respuesta fue sintetizada. La siguiente, si ves, que es, y de nuevo hay muchas descripciones que puedes leer siempre, 

es que también tenemos algún tipo de finalización. Esto es como una conversación de métodos de trabajo, ¿verdad? Así que les mostraré el ejemplo que se usa aquí. So it's over here. If there is nothing being asked, it's fine. But if you ask something of this sort, which is I need a hydration vest. So in this case, yes. 

Puede que haya un agente que pueda responder tu pregunta, pero todavía puede necesitar una pregunta seguida que vuelva. Así que básicamente tenemos una respuesta que también vuelve. No hemos puesto a un humano en una lupa o algo así. Pero verás que un par de interacciones ocurren. Envia la pregunta a un subagente. El subagente responde, ok, ¿qué tamaño? etc. Y luego también... 

Share this, share this. 

Ok, so this is actually now a task mode. It's not just a single turn thing. So the user says I need a hydration vest. Let's see which sub-agent it actually... No se preocupe por la cosa de la pausa, yo me acerco a eso. Así que puedes ver que hay un ajustador de ruedas. Este es el subagente al que se ha ido. 

El montador ha vuelto. ¿Cuál es el tamaño? Y luego se ha convertido en un estado de pausa. Y el cambio, que es del usuario, esa es la respuesta que le pusimos, que dice que es de 2 litros medio. That again goes back to a gear fitter, it says I finished my task and then finally the synthesized answer is your order is this and it has been placed, right? So. 

Puedes ver aquí la descripción, que es que todo se hizo por la consultoría, mirando tu pregunta, diciendo que el agente de montaje debería ser llamado. y el agente de equipamiento va a regresar y te va a preguntar una pregunta con la que respondes de regreso y todo el orden de equipamiento validado se vuelve a una línea final final y nos vemos. 

you know, place the order. So hopefully this is again, if I look at the code that's in your task desk over here and again, it follows same ones. lo que vimos, todo lo que estaba funcionando, que sólo va a un agente de montaje específico, que es éste, y luego... 

Si, como la mesa de carreras y tiene subagentes, solo pide este. Esto es simplificado para hacer el código un poco más fácil de seguir. Entonces, le diste tu cuenta al agente de carreras, pero luego le dieron a el subagente. el 

@11 de agosto de 2026 23:08 

26 

subagente, la moda, fue una tarea y eso se volvió y se volvió. Y porque fue especificado, debes saber que puedes preguntar una pregunta terrificante y así sucesivamente. Así es como el flujo. 

So let me go back to our code lab and that sort of covers the second pillar, which is about collaborative things. So if I go back to our slides. un momento, déjame solo reiterar. Lo que vimos en este pilar fue que vimos diferentes modos por los que los subagentes, por ejemplo, si voy de vuelta a este diagrama. 

diferent subagents that could be invoked by a concierge. And the examples that we saw were like, you know, single term. It just collects data from multiple. agents and we also saw one very specific, you know, geared as the agent being invoked, sorry, the agent being invoked, which is it delegates to it. It goes into a pause mode, ask you a follow up question. 

The user replies, it resumes, finish, and then it goes on in that fashion. So that is how you could have both concierge talking to subagents, getting data from each one of them. But also in case one of the agents needs to go into a mode by which it wants to ask you, it's paused, the questions go back and forth and then it completes, right? 

El último pilar que tenemos ahora mismo es el pilar dinámico. Y lo que hemos visto hasta ahora, hemos visto esos trabajos gráficos, Parallel, fan out, routing and so on. But that was when you know that, you know, how the flow is determined. The flow is determined so you could draw it before time, design time. 

pero antes de que lleguen los datos. En el segundo pilar, el colaborativo, que vimos justo ahora, antes de esto, el dinámico, no sabemos cuántos agentes necesitamos hablar con Pero esa es la cosa colaborativa, donde tenemos subagentes configurados y uno de los consejeros o agente coordinador puede hablar con cualquiera de los subagentes para cumplir las obligaciones. 

Ahora, el tercero es el más flexible, pero, por supuesto, está orientado al código. Y esto tiene que ver con el hecho de que, a través del código, te permite decidir ¿sabes cuántos agentes o cuántos nodos quieres ejecutar? ¿Quieres hacer eso en paralelo? ¿Quieres colectar datos de eso? ¿Sabes, quieres hacer que uno de ellos trabajadores vaya más profundo, más y más a ello? 

Es casi como un agente de investigación profunda, donde, por ejemplo, si yo digo, hey, investiga este tópico para mí, o en este caso, en el que ves a Rana 

@11 de agosto de 2026 23:08 

27 

Rass, investiga el mejor maratón. ¿Qué significa eso? Eso significa que ahora puedes dibujar este gráfico porque no sabes que cuando quieras estudiar las mejores estrategias nutricionales del maratón, puede haber tantas cosas. Podría haber cosas alrededor, como veremos, sobre qué tipo de nutrición podría haber allí, qué tipo de estrategias de combustión, etcétera, etcétera, ¿verdad? Y, de nuevo, Puedes ir a una página y decir, hey, tengo estos cinco artículos que necesito leer o cinco otros temas que necesito investigar. Entonces, literalmente tienes cosas por las que tener que romper. 

de esta declaración. Las mejores estrategias nutricionales de maratón podrían ser rompidas en múltiples trabajadores que puedan ir y hacer su investigación independiente sobre lo que lo rompieron. You can define how many you want in terms of workers, but what you're seeing over here is just one part where you said decompose it and parallelly let them go and fetch the data and synthesize it. 

Pero también puedes tener que un trabajador puede ir más profundo y más profundo, ¿verdad? Así que no es solo el tamaño, pero como puedes ver aquí, incluso podría ser la profundidad. So, for example, one is the flat fan out, which is what we are seeing decompose five topics and come back with it, but it could also be a recursive tree, which could be a bit more complicated. So, for example, look at decomposing to carb loading and gels, but carb loading may further decompose into another depth, which is glycogen and timing. 

Let's research on that or that could go on. So again you have to be very careful with these things because these could end up not just amount of time but also a significant amount of tokens while doing the research. la longitud y la profundidad, cuando se multiplican juntos, puede significar bastante tokens. Pero, por supuesto, dependiendo del tipo de tareas o del todo el dinamismo que necesites aquí. 

Y esto podría ser definitivamente un flujo que ustedes podrían querer pasar. Así que esto es lo que ahora vamos a ir pasando en esto. Ahora, en un nivel alto, ¿verdad? Antes de que me ponga en el por. Just think of it this way. Start right at the bottom, which is I've got a workflow and I'm just saying I need to run this my workflow. Now I told you dynamic stuff is the programmatic way. 

So, you can see over here that we've created one decorator called add node that lets it function as a node and then which could then spawn or basically, you know, instantiate further nodes also. So, you can see inside of my workflow. que no solo te da acceso a los contextos, una salida similar que va 

@11 de agosto de 2026 23:08 

28 

adelante, pero dentro de eso, ves que también estoy ejecutando otro nodo. Así que está completamente a tu gusto. Puedes tener una lista aquí y ejecutar múltiples nodos dependiendo de las preguntas que tengas. 

Puedes tener condiciones aquí, dependiendo de las que puedas ejecutar uno o más nodos. Así que es completamente programático. Aquí solo ves un nodo ejecutado dentro de Workflow, pero dependiendo de tu... dependiendo de tu loop, dependiendo de cuántos quieres, podrías programáticamente ejecutar todos estos nodos, obtener el resultado, y luego regresar. 

o básicamente ir al nodo de abajo que está ahí afuera. Así que, de nuevo, esto es otro, solo para mostrarte dos de ellos. Así que puedes ver que estoy empezando mi funcionamiento, pero en mi funcionamiento puedes ver que estoy llamando a resultados. Y luego le estoy llamando a un nodo formado de resultado también, así que le estoy llamando a dos nodos completamente dinámicos, pero completamente en mi código. Así que de nuevo, parece que es un código duro de dos líneas. 

invocaciones ya, but this could be in a loop, this could be based on conditions, and you could have and run as many nodes as you want in your own. So what we're going to be seeing now is two more examples, which is. Y creo que vamos a ir con uno de ellos. El siguiente es nada más que los nodos profundos si se necesita ir a un modo recursivo. Así que un ejemplo debería ser suficiente para nosotros. 

para entender este patrón. Básicamente tenemos solo trabajadores finales. Si lo miro, voy a hacer el uno a la izquierda, voy a descomponer la llamada. And this will be happening into one or more workers that will get executed. So let me go back to our code lab. 

And that's the pattern. Let me see the diagram over here. So this is basically a run time sized fan out. Why is it called a run time sized fan out? Porque el LLM decidirá cuántas preguntas subterráneas. ¿De dónde se obtienen las preguntas subterráneas? De hecho, tomará la pregunta que el usuario le dio y luego tendrá algunas instrucciones. 

que dirá, oye, rompa esta pregunta del usuario en tres o cuatro subpreguntas. Piense en la investigación, ¿verdad? Entonces, si estás haciendo investigación, dirías, ok, tengo que hacerlo en este tópico, pero quizás estas son tres o cuatro áreas en este tópico, o estas son tres o cuatro tipos de, vamos a obtener videos, vamos a obtener artículos, vamos a obtener blog posts. 

@11 de agosto de 2026 23:08 

29 

of a topic and then do that. You could decompose in different ways depending upon your instruction. So basically we're going to be decomposing it. Each decomposition would be one specific research task, which is then given to a parallel worker. Y luego, una vez que se completen, se puede sintetizar todo el briefing aquí, ¿verdad? Así que esto es... Ahora parece diferente porque... 

Puedes decir que esto parece algo como el gráfico para mí. Parece que hay una función y luego algo en paralelo. Puede parecer así visualmente, pero no es así, porque la parte de la decomposición es completamente dinámica. We don't know how many sub-questions might come in, we can't draw this at design time, this is all happening at run time depending upon the question you ask and how many workers we may need to. 

ah, you know, ah, launch. So if I look at the code that's telling us to do, we just have to do this L4 flat research and the flat research is just number of workers. No vamos a hacer que cada uno de los trabajadores vaya a la profundidad. No vamos a hacer 4B, que les mostraré aquí, que es nada más que a veces la investigación puede involucrar preguntas más profundas o, ¿sabes?, profundidad. 

Así que es una cosa similar, pero de nuevo, el código es el mismo tipo de concepto en el que podrías tener respaldos recursivos también. En nuestro caso aquí, hoy vamos a enfocarnos en este 3B1, que es el panel de tamaño de tiempo de rueda. Así que voy a volver a... 

A ver por. Let me close this. And the flat research one. So deep research. Now over here again, if I just go back to the thing at the start, so basically what you've got is, this is our workflow, do a decomposition. y luego hacer investigación y luego sintetizar. Básicamente toma tu pregunta y descompone. ¿Qué está pasando en descomponer? Veámoslo. En descomponer básicamente se extrae tu respuesta. 

And then depending upon that, you can see it's running this decomposed agent which is saying you're a research coordinator. Break the user's open ended question into three to seven specific. subcuestions. This gives back, you know, some kind of a list, which is then, as you can see, depending upon the subquestions. 

And then each of the sub questions results in a parallel workup which then takes that particular question and then says, OK, go ahead and you research agent. So you go and do your work. So you are a specialist, given one specific 

@11 de agosto de 2026 23:08 

30 

research question, produce a finding. So each one of these goes and then does the sub-question that it has been asked to. 

And returns back and then synthesize agent just takes in all the, you know, listings of findings and create some kind of a summary. So if we just run this, it should. para hacer todo claro. Así que, de nuevo, por el momento dirás Hey, pero ¿qué es la pregunta que me has preguntado? Lo siento, debería haber mostrado eso. Así que si vas hasta el final de esto, dice Dime todo 

que yo debería saber sobre la carrera de la maratón de Boston, la fuerza, el clima, las paredes, el espacio, qué se usa, etc. Esa es la pregunta que vamos a estar publicando ahí. Así que ahí vamos. 

So this is my query and now you will see that look, it's actually decomposed, that agent decomposed into five sub questions, right? ¿Y cuáles son las tipografías claves? Vuelvan con estas, basadas en lo que les pidieron. Se han lanzado 5 subagentes de investigación en paralelo, o nodos en paralelo. 

que van a estar respondiendo a esas preguntas. Y una vez que lo haga, ahora va a mezclar todos estos en paralelo, para que puedan ver cómo. de cómo fue y cómo lo hizo. Así que es bastante directo, donde la pregunta original solo queda como es, pero la decomposición la divide en dos partes. 

you know, you depend, you can set even a max of number of the width you want to go to, that many questions. And then each of those questions, it has spawned a research agent as you can see. y luego se sintetiza todo esto, se unen todos, en una sola respuesta final. 

El diagrama debería ser bastante directo. Nuestra pregunta original me dice todo sobre el maratón en estas áreas. Se decompuso en cuatro preguntas. Cinco preguntas creo. And then it's created this research question, I mean, sorry, workers and then synthesize. For me, I don't think we need to run this right now. It's really just an extension of it, which is, in a sense, I told you we could even go. 

a una profundidad, así que incluso podrías decir que la investigación, en caso de que quieras romperla, puedes romperla más y así sucede, ¿verdad? Pero ten en cuenta que puede causar tokens y cosas como esas. Así que, si vuelvo a mi pantalla por un momento, eso fue el L4A que hicimos, el L4B, como les dije, es... 

Puedes ir más profundo también, ¿verdad? Hasta un máximo. Son cosas recursivas. Pero ten en cuenta que estas cosas pueden costarte tus tokens, porque todos empezarán a romperlo en una manera dinámica. Y aunque, 

@11 de agosto de 2026 23:08 

31 

recuerda, puedes establecer el máximo al mismo tiempo, también podrías decir, ¿Puedo condicionalmente en mi código establecer algunas formas por las que no puedo ir más allá de esto o que necesito parar en ese momento? Sí, puedes hacer todo eso también. 

porque esta cosa dinámica está completamente cortada. Sí, así que tal vez si vuelvo por un momento a la laboratorio de código. en esa particular cosa. Eso es bastante, ya sabes, ahora estamos llegando al final de qué patrón deberíamos usar y eso es cómo eventualmente el laboratorio de código 

So nothing more in the code laboratory. So going back to my slides just to summarize what pattern we should be using. Keep in mind that, look, we said at the beginning that it's very important that we don't make everything, you know, an agent. We should definitely see what are the deterministic things that you could do. 

Y en ese caso, probablemente no necesitas realmente usar cualquier tipo de gráfico o cosas así. Ahora, si puedes dibujar el flujo antes de que llegue la entrada, ya sabemos que este será el flujo. Estas son las maneras en las que los agentes o los nodos o las funciones necesitan hacer su trabajo. Si lo conoces antes, eso se convierte en un flujo de trabajo gráfico y ese es el pilar L2 que vimos. 

Similarmente, no sabemos en el tiempo de diseño cuál es la forma, pero sabemos que hay un equipo de agentes que puede resolverlo y quizás uno o más de ellos puedan hacer el trabajo. En ese caso, eso se convierte en el patrón colaborativo que vimos. Y finalmente, tenemos algo donde decimos que no sabemos, basado en la pregunta, 

¿Cuántas cosas más se pueden dividir? Porque la forma en sí depende de la entrada. Eso es lo que significa. Vimos un ejemplo de una búsqueda abierta. y luego se dividió en tareas o tópicos de investigación individuales, y luego eso espantó a los trabajadores para hacer su trabajo y terminarlo. Ese fue el patrón dinámico. Vimos 4A y 4B, que eran los mismos, pero que incluso iban a una profundidad recursiva. 

So again, this is just a reference, the number of examples that we saw so far from the first one, which talked about. you know, one large prompt and everything being inside of that. So to summarize, right, just keep these points in mind, which is that, you know, Y, obviamente, las funciones preparan el contexto, las fronteras son las funciones de trabajo y, por supuesto, el router es para la parte de atrás y el modelo es la respuesta. 

@11 de agosto de 2026 23:08 

32 

De la manera en que quieres leer esto, idealmente, es que... Y probablemente veas que algunas de estas cosas son deterministas, solo funciones. No necesitas necesariamente un modelo para hacer la raza cada vez, eso salva tiempo. tiempo, latencia, tokens y más. 

De nuevo, si lo sabes antes, si puedes dibujarlo, es conocido en el tiempo de diseño, así que puedes usar un gráfico. Pero si no puedes hacerlo en el tiempo de diseño, pero sabes que este es el equipo de agentes que puede hacerlo, el patrón colaborativo puede ser una manera de ir. 

And if it completely depends on the input, dynamic programmatic may might be the way to go. And again, you know, you have to do it via Python code. en términos del último patrón que vimos, si vamos de manera dinámica y programática, entonces recursión depth, fan out width, etcétera, esas son las cosas que puedes controlar en tu código de Python, dependiendo de 

logic or some conditional variables or some count or max or whatever you want to define based on your logic. Yeah, that's pretty much what I had from my side. a ver si hay algunas preguntas específicas que necesito tomar. También tenemos algunas, déjame ver si... 

Yo creo que probablemente algunas de las preguntas estén respuestas. Sí, también podría tomar un par de preguntas, en una de anteriores. That have come one or two questions from that. So just give me a minute. 

Sí, así que dos o tres preguntas y yo las tomaré a un nivel que ayudará a solidificar lo que hemos aprendido hoy. A veces la pregunta es, ¿cómo decidimos cuántos agentes podrían estar ahí? ¿Será un número de herramientas que decidan cuántos agentes? ¿Por qué buscamos subagentes? ¿Podríamos poner todos los herramientas en un único agente? ¿Cuáles podrían ser las criterias? Así que hay ciertos factores que vienen en juego. 

Uno podría ser también cosas como si tuvieras diferentes, digamos, contextos para cada uno de los agentes. No quieres que uno sepa sobre el otro o se corrompa o se influya por eso. Así que dependiendo de ese contexto de isolación. You might want to think about letting each sub-agent do its task, what it's meant for, and just returns back the data. That could be one particular thing. Sometimes the way the modality of execution could be there, which is you want to do it in a parallel fashion. 

en cualquier caso es mejor romperlo en subagentes o como vimos algunos de los patrones para romperlo separadamente para que puedas enfriarlo y luego combinarlo en uno y así sucesivamente, ¿verdad? Sometimes testing those 

@11 de agosto de 2026 23:08 

33 

things out could also become a bit easier if you've got separate functionalities and things of that sort. So I would say. 

y tal vez otro punto puede ser que también quieras mezclar y mezclar modelos para los subagentes, dependiendo de la lógica o la complejidad que hay ahí. Entonces, varios factores, no puede ser solo uno que decide si necesitas subagentes, pero algunos de estos puntos. 

que mencionamos. La otra cosa es que hoy hablamos de ADK2, y 

generalmente si vienes de un mundo de ADK1, Puedes tener un par de cosas en mente cuando empiezas a aprender sobre ADK2. Vimos algunos de los patrones que son construcciones de primera clase. Ahora en ADK2 se simplifican muchas cosas. 

lo que ADK]1 podría hacer. No estoy diciendo que algunas de estas cosas no podrías hacer, pero tendría que haber un modo más paitánico para hacerlo y algunas cosas no eran posibles. Todo era un agente en 1x, pero ahora básicamente puedes ver, puedes tener funciones, puedes tener agentes, puedes tener a un humano en el loop. 

All of these things are nodes that help you do that. Even when it comes to subagents, you saw different modes that are there. We just had a transfer agent to transfer to the agent in OneX. Pero ahora tenemos eso junto con, como vimos, un modo de tarea. Tenemos un modo de turno solo que hace las cosas más fáciles. Hay un nodo de unirse y muchas otras cosas que hacen todo el aspecto de programación. O diría que la forma en que lo construyes. 

mucho más fácil, más flexible y apoyo de primera clase en ADK R2. Sí, creo que aparte de eso, tal vez también hay una pregunta alrededor de. ¿Puedo usar el idioma PHP? Josef ha preguntado eso en el proyecto Hackathon. Creo que la manera en la que querrías mirar esto es mirar el tipo de apoyo de idioma que tenemos actualmente para ADK. 

So we've got support for Python, Go, TypeScript and Java, to the best of my knowledge, these four. So if you've got to use ADK, my best guess is you'd have to use one of these. But of course, you know. If your agent is calling some tools or external APIs which are hosted elsewhere, those as well could be in any text tag, any language framework. 

of your preference that you may want to post this. 

Así que eso es todo desde mi punto de vista. Muchas gracias por unirse a esta sesión. Espero que haya sido útil. un par de, quiero decir, tres más sesiones en esta serie que te llevan a través de conceptos más avanzados para construir 

@11 de agosto de 2026 23:08 

34 

agentes en el mundo real, rangido desde la persistencia, desde la memoria, cómo los agentes aprenden. 

de sus experiencias. Así que estas serían muy buenas sesiones para atender para construir algunos de los conocimientos fundamentales a través de estos patrones que aprendiste en esta primera sesión de hoy. Así que. Definitivamente espero que se unan para las otras sesiones. Sí, eso es de mi lado. Sabes, que tengas un gran día. Gracias. 

Ya lo hice, papu. 

A ver, no, no, no, no nos distraigamos, no nos distraigamos. 

A ver, estoy a correr una parte de las asas, pero no lo cuento, de hecho. 

No dice, ¿por qué? 

¡Nooo! Me salí. 

@11 de agosto de 2026 23:08 

35 

