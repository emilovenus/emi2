# 📨 Sistema de Notificaciones — Patrones de Diseño (Observer y Factory Method)

## 📘 Introducción

Este proyecto consiste en el desarrollo de un **Sistema de Notificaciones** que permite enviar mensajes a los usuarios a través de diferentes medios, como **correo electrónico**, **SMS** o **notificaciones push**.

El propósito principal es aplicar **patrones de diseño orientados a objetos**, en particular los patrones **Observer** y **Factory Method**, además de seguir los **principios SOLID** para lograr un código limpio, extensible y mantenible.

Este ejercicio busca fortalecer la comprensión del diseño orientado a objetos, la **comunicación entre clases** y la **aplicación práctica de patrones de diseño** utilizados en entornos profesionales de desarrollo de software.

---

## 🧩 Marco Teórico

### 🔹 Patrón Observer

El **Patrón Observer (u Observador)** define una relación **uno a muchos** entre objetos.
Cuando un objeto (denominado *Sujeto*) cambia su estado, **todos sus observadores son notificados automáticamente**.

En este caso, el **Sujeto** es la clase `Notificacion`, que mantiene una lista de usuarios suscritos y les envía actualizaciones.
Los **Observadores** son los objetos `Usuario`, que implementan una interfaz para recibir las notificaciones.

**Estructura del patrón:**

* **Sujeto (Subject):** Mantiene una lista de observadores y les notifica cuando hay un cambio o evento.
* **Observador (Observer):** Define la interfaz que recibe las actualizaciones.

**Ejemplo aplicado:**
Cuando se publica un nuevo mensaje (por ejemplo, “Nueva actualización disponible”), todos los usuarios suscritos son notificados automáticamente.

---

### 🔹 Patrón Factory Method

El **Patrón Factory Method** permite **crear objetos sin especificar la clase concreta** del objeto que se creará.
Este patrón se utiliza para **encapsular la lógica de creación** y permitir que el sistema sea extensible.

En este proyecto, se aplica para crear diferentes tipos de notificaciones:

* `EmailNotificacion`
* `SMSNotificacion`
* `PushNotificacion`

La clase `NotificacionFactory` se encarga de devolver la instancia correcta según el tipo solicitado.

De esta forma, si en el futuro se desea agregar una nueva forma de notificación (por ejemplo, **WhatsApp**), se puede hacer sin modificar el código existente, cumpliendo el **principio Open/Closed** de SOLID.

---

### 🔹 Principios SOLID

Los principios **SOLID** son un conjunto de buenas prácticas para el diseño orientado a objetos:

1. **S – Single Responsibility:**
   Cada clase tiene una única responsabilidad.

   * `Usuario` solo representa datos del usuario.
   * `Notificacion` solo gestiona la suscripción y aviso a los observadores.
   * `NotificacionFactory` solo crea instancias de notificaciones.

2. **O – Open/Closed:**
   El sistema está abierto a la extensión (se pueden agregar nuevos tipos de notificaciones) pero cerrado a la modificación (no es necesario cambiar las clases existentes).

3. **L – Liskov Substitution:**
   Las subclases (`EmailNotificacion`, `SMSNotificacion`, `PushNotificacion`) pueden sustituir a la interfaz `INotificacion` sin alterar el comportamiento esperado.

4. **I – Interface Segregation:**
   Las interfaces son específicas: `IObservador` solo contiene `actualizar()`, e `INotificacion` solo tiene `enviar()`.

5. **D – Dependency Inversion:**
   Las dependencias se basan en **abstracciones**, no en implementaciones concretas.
   Por ejemplo, la clase `Usuario` depende de `INotificacion`, no de una clase concreta como `EmailNotificacion`.

---

## 🏗️ Estructura del Sistema

El sistema se compone de las siguientes clases principales:

| Clase                                                      | Descripción                                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **IObservador**                                            | Interfaz que define el método `actualizar(mensaje)` para recibir notificaciones.     |
| **Usuario**                                                | Representa a un usuario del sistema y actúa como observador.                         |
| **Notificacion**                                           | Actúa como el sujeto (Subject) que mantiene la lista de observadores y los notifica. |
| **INotificacion**                                          | Interfaz para definir el método `enviar(mensaje)`.                                   |
| **EmailNotificacion / SMSNotificacion / PushNotificacion** | Implementaciones concretas que definen cómo se envía la notificación.                |
| **NotificacionFactory**                                    | Fábrica que crea instancias del tipo de notificación solicitado.                     |

---

## 🧠 Funcionamiento del Código

1. Se crean varios objetos de tipo `Usuario`.
2. Cada usuario puede suscribirse al sistema de notificaciones mediante el método `agregarObservador()`.
3. El sistema (la clase `Notificacion`) envía un mensaje.
4. Todos los usuarios suscritos son notificados automáticamente.
5. A través del **Factory Method**, cada usuario puede recibir el mensaje por un canal diferente: email, SMS o push.

---

## 🧰 Ejemplo de Ejecución

### Código principal (`main.py`)

```python
if __name__ == "__main__":
    sistema = Notificacion()

    usuario1 = Usuario("Emily", "emily@gmail.com", "123456789")
    usuario2 = Usuario("Carlos", "carlos@gmail.com", "987654321")

    sistema.agregarObservador(usuario1)
    sistema.agregarObservador(usuario2)

    sistema.notificarObservadores("Nueva actualización disponible en la app")
```

### Salida esperada en consola

```
Enviando EMAIL a Emily (emily@gmail.com): Nueva actualización disponible en la app
Enviando EMAIL a Carlos (carlos@gmail.com): Nueva actualización disponible en la app
```

Si se modificara el tipo de notificación en la fábrica a `SMS` o `PUSH`, el sistema seguiría funcionando sin alterar la estructura de las clases.

---

## 🧱 Aplicación de los Patrones

| Patrón             | Implementación en el Proyecto                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **Observer**       | La clase `Notificacion` (sujeto) mantiene una lista de observadores (`Usuario`) y les notifica automáticamente los mensajes. |
| **Factory Method** | La clase `NotificacionFactory` decide qué tipo de notificación crear (email, SMS o push).                                    |
| **SOLID**          | Se cumple al tener clases con una sola responsabilidad, interfaces específicas y dependencias basadas en abstracciones.      |

---

## 🚀 Conclusión

Este proyecto demuestra cómo los **patrones de diseño** y los **principios SOLID** ayudan a construir sistemas **flexibles, mantenibles y extensibles**.

Gracias al uso de **Observer**, se logró una comunicación eficiente entre el sujeto y los observadores, mientras que **Factory Method** permitió crear distintos tipos de notificaciones sin alterar el código existente.

En conjunto, ambos patrones hacen que el sistema sea fácil de **ampliar**, **probar** y **reutilizar** en otros proyectos.

---

## 📂 Archivos del Proyecto

```
SistemaNotificaciones/
│
├── main.py
├── README.md
└── notificacion.py  # Contiene todas las clases e interfaces
```

---

## ✍️ Autor

**Nombre:** *EMILY VALLE*
**Materia:** Programación Orientada a Objetos
**Tema:** Patrones de Diseño – Observer y Factory Method
**Lenguaje:** Python