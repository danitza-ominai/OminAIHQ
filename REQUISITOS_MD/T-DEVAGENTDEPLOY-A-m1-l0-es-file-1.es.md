

El problema: Los agentes de localhost no se pueden compartir no se pueden compartir 

# Introducción 

## Creaste agentes sofisticados: 

- Cursos del 1 al 3: Agentes básicos con modelos, herramientas e instrucciones 

- Curso 4: Administración de estados con 4 espacios de nombres 

- Curso 5: Integración avanzada de herramientas 

- Curso 6: Protecciones con devoluciones de llamada 

- Curso 7: Coordinación de varios agentes 

- Curso 8: Flujos de trabajo complejos con el protocolo A2A (localhost) 

## Pero hay una limitación fundamental: 

Py ~~t~~ hon 

- ~~#~~ De ~~l~~ os cu ~~r~~ sos ~~1~~ a ~~l~~ 8: ~~T~~ odo se e ~~j~~ ecu ~~t~~ a en ~~l~~ oca ~~l~~ hos ~~t~~ 

- ~~# T~~ e ~~r~~ m ~~i~~ na ~~l 1~~ : adk web 

- ~~#~~ Acceso: h ~~tt~~ p:// ~~l~~ oca ~~l~~ hos ~~t~~ :8000 

- ~~#~~ P ~~r~~ ob ~~l~~ ema: So ~~l~~ o se puede accede ~~r~~ desde ~~T~~ U compu ~~t~~ ado ~~r~~ a 

- ~~#~~ No se pueden compa ~~rtir~~ con e ~~l~~ equ ~~i~~ po o ~~l~~ os usua ~~ri~~ os 



- ~~#~~ Se de ~~ti~~ enen cuando ~~l~~ a compu ~~t~~ ado ~~r~~ a en ~~tr~~ a en modo de suspens ~~i~~ ón 

- ~~#~~ S ~~i~~ n d ~~i~~ spon ~~i~~ b ~~ili~~ dad 24/7 

En este curso, se resuelve la "brecha de localhost" enseñándote los aspectos básicos de la implementación en la nube. 

# El problema: Los agentes de localhost no se pueden compartir 

Considera un agente sofisticado: 

Flujo de trabajo complejo: 

Py ~~t~~ hon 

- ~~#~~ S ~~i~~ s ~~t~~ ema de QA de con ~~t~~ en ~~i~~ do ( ~~f~~ unc ~~i~~ ona de ~~f~~ o ~~r~~ ma ~~l~~ oca ~~l~~ ) ~~fr~~ omgoogl ~~e~~ .adk.agent ~~s~~ i ~~m~~ por ~~tS~~ equenti ~~al~~ A ~~g~~ ent, Para ~~l~~ l ~~el~~ A ~~g~~ ent, LoopAgent 

wo ~~r~~ k ~~fl~~ ow ~~=~~ Sequen ~~ti~~ a ~~l~~ Agen ~~t~~ ( 

sub_agen ~~t~~ s ~~=~~ [ 

- ~~i~~ n ~~t~~ ake, 

- Pa ~~r~~ a ~~ll~~ e ~~l~~ Agen ~~t~~ (sub_agen ~~t~~ s ~~=~~ [va ~~li~~ da ~~t~~ o ~~r~~ <u>_a, va</u> ~~li~~ da ~~t~~ o ~~r~~ <u>_b, va</u> ~~li~~ da ~~t~~ o ~~r~~ <u>_c]),</u> LoopAgen ~~t~~ (sub_agen ~~t~~ s ~~=~~ [qua ~~lit~~ y_check, ~~r~~ e ~~fi~~ ne ~~r~~ ], max_ ~~it~~ e ~~r~~ a ~~ti~~ ons ~~=~~ 5) ] ) 

- ~~#~~ P ~~r~~ uebas: adk web 

- ~~#~~ Acceso: h ~~tt~~ p:// ~~l~~ oca ~~l~~ hos ~~t~~ :8000 

- ~~#~~ P ~~r~~ ob ~~l~~ ema: So ~~l~~ o se puede accede ~~r~~ desde m ~~i~~ compu ~~t~~ ado ~~r~~ a 







2 

## Las limitaciones fundamentales: 

No se pueden compartir con el equipo o los usuarios 

- La URL de localhost (http://localhost:8000) solo funciona en tu máquina. 

- Los miembros del equipo no pueden acceder a tus agentes. 

- Los usuarios no pueden probar ni usar tus agentes. 

### Sin escalabilidad 

   - Hay una única instancia y está en tu computadora. 

   - No pueden manejar varios usuarios simultáneos. 

   - El rendimiento está limitado por la máquina local. 

   - No hay escalado automático 

- No hay forma de integrarlos en los sistemas de producción. 

### Sin disponibilidad 24/7 

- Los agentes se detienen cuando cierras la terminal. 

- Los agentes se detienen cuando la computadora entra en modo de suspensión o se reinicia. 

- No se puede prestar el servicio a usuarios en diferentes zonas horarias. 

### Sin persistencia de producción 

   - InMemorySessionService pierde datos cuando se reinicia. 

   - El estado de la sesión no se conserva en las diferentes implementaciones. 

   - No existe la memoria entre sesiones. 

   - No pueden aprender de las interacciones pasadas. 

- No son confiables para su uso en producción. 

## El problema principal 

El desarrollo en localhost es ideal para crear y probar agentes, pero los sistemas de producción necesitan la implementación en la nube para compartir y obtener confiabilidad y escalabilidad. 



3 

