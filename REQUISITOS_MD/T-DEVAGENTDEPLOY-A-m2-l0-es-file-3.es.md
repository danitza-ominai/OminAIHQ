

# El problema: La complejidad de la implementación es un obstáculo es un obstáculo 

De localhost a Agent Engine 

En la parte 1, configuraste tu entorno de Google Cloud. Ahora, implementarás tu primer agente en producción. Estado actual: 

Cuenta de Google Cloud lista 

APIs habilitadas (Vertex AI y Cloud Run) 

- gcloud CLI autenticada 

SDK de Vertex AI instalado 

Estado futuro: 

Ninguno Desa ~~rr~~ o ~~ll~~ o ~~l~~ oca ~~l~~ :   adk web → h ~~tt~~ p:// ~~l~~ oca ~~l~~ hos ~~t~~ :8000 ↓ Agen ~~t E~~ ng ~~i~~ ne:      adk dep ~~l~~ oy agen ~~t-~~ eng ~~i~~ ne → h ~~tt~~ ps://agen ~~t-~~ xyz.goog ~~l~~ eap ~~i~~ s.com 

Tarea que debes realizar: Transforma tu agente de localhost en un servicio de producción con un solo comando. 







## El problema: La complejidad de la implementación es un obstáculo 

La implementación tradicional en la nube es compleja: 

- Escribir Dockerfiles 

- Configurar Kubernetes 

- Configurar bases de datos para el estado de la sesión 

- Administrar la infraestructura 

- Manejar el escalamiento y el balanceo de cargas 

#### Los estudiantes son desarrolladores de agentes, no ingenieros de DevOps 

#### Ejemplo concreto: 

Py ~~t~~ hon 

- ~~# Fl~~ u ~~j~~ o de ~~tr~~ aba ~~j~~ o mu ~~lti~~ agen ~~t~~ e de ~~l~~ cu ~~r~~ so 8 ( ~~f~~ unc ~~i~~ ona de ~~f~~ o ~~r~~ ma ~~l~~ oca ~~l~~ ) ~~fr~~ om goog ~~l~~ e.adk.agen ~~t~~ s ~~i~~ mpo ~~rt~~ Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ , Pa ~~r~~ a ~~ll~~ e ~~l~~ Agen ~~t~~ , LoopAgen ~~t~~ 



wo ~~r~~ k ~~fl~~ ow ~~=~~ Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ ( name ~~=~~ 'con ~~t~~ en ~~t~~ <u>_qa_sys</u> ~~t~~ em', sub_agen ~~t~~ s ~~=~~ [ ~~i~~ n ~~t~~ ake, ~~f~~ ac ~~t~~ <u>_check_wo</u> ~~r~~ k ~~fl~~ ow, qua ~~lit~~ y_ ~~l~~ oop] ) 

~~#~~ P ~~r~~ uebas ~~l~~ oca ~~l~~ es: adk web ✅ 

~~# I~~ mp ~~l~~ emen ~~t~~ ac ~~i~~ ón en p ~~r~~ oducc ~~i~~ ón: ??? ❌ 

~~#~~ Neces ~~i~~ dad: Docke ~~r~~ , Kube ~~r~~ ne ~~t~~ es, bases de da ~~t~~ os, ~~i~~ n ~~fr~~ aes ~~tr~~ uc ~~t~~ u ~~r~~ a... 

### El problema principal 

Los estudiantes necesitan la implementación con un solo comando sin complejidad de infraestructura. 



2 

