"""
sistema_notificaciones.py

Mini-proyecto: Sistema de Notificaciones (Single-file)
Patrones: Observer + Factory Method
Principios SOLID: explicados en comentarios y aplicados en la estructura.

Ejecución: python sistema_notificaciones.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ---------------------------
# INTERFACES / ABSTRACCIONES
# ---------------------------

class IObservador(ABC):
    """Interfaz Observador (IObservador)
    Define el contrato para cualquier observador que quiera recibir notificaciones.
    (Aplica Dependency Inversion - SOLID: dependemos de abstracciones.)
    """
    @abstractmethod
    def actualizar(self, mensaje: str) -> None:
        raise NotImplementedError


class INotificacion(ABC):
    """Interfaz para distintos tipos de notificación (email, sms, push).
    Cada implementación concreta debe definir enviar(mensaje, destino).
    (Aplica Interface Segregation: interfaz específica para notificaciones.)
    """
    @abstractmethod
    def enviar(self, mensaje: str, destino: str) -> None:
        raise NotImplementedError


# ---------------------------
# IMPLEMENTACIONES CONCRETAS (NOTIFIERS)
# ---------------------------

class EmailNotificacion(INotificacion):
    """Simula el envío de un email."""
    def enviar(self, mensaje: str, destino: str) -> None:
        print(f"  [Email] -> Enviando email a {destino}: '{mensaje}'")


class SMSNotificacion(INotificacion):
    """Simula el envío de un SMS."""
    def enviar(self, mensaje: str, destino: str) -> None:
        print(f"  [SMS]   -> Enviando SMS a {destino}: '{mensaje}'")


class PushNotificacion(INotificacion):
    """Simula el envío de una notificación push."""
    def enviar(self, mensaje: str, destino: str) -> None:
        print(f"  [Push]  -> Enviando push a {destino}: '{mensaje}'")


# ---------------------------
# FACTORY METHOD
# ---------------------------

class NotificacionFactory:
    """Factory Method simple que devuelve una instancia de INotificacion según el tipo.
    - Permite añadir nuevos tipos sin cambiar el código cliente (Open/Closed).
    - Si no se reconoce el tipo, devuelve None (podría devolver un Null Object).
    """
    @staticmethod
    def crear_notificacion(tipo: str) -> Optional[INotificacion]:
        t = tipo.strip().lower()
        if t == "email":
            return EmailNotificacion()
        if t == "sms":
            return SMSNotificacion()
        if t == "push":
            return PushNotificacion()
        return None


# ---------------------------
# OBSERVER: SUBJECT (NOTIFICACION)
# ---------------------------

class Notificacion:
    """Sujeto (Subject) del patrón Observer.
    Mantiene una lista de observadores y los notifica cuando ocurre un evento.
    (Single Responsibility: esta clase solo gestiona suscriptores y notificaciones.)
    """
    def __init__(self):
        self._observadores: List[IObservador] = []

    def agregar_observador(self, obs: IObservador) -> None:
        if obs not in self._observadores:
            self._observadores.append(obs)
            print(f"[System] Observador agregado: {obs}")

    def eliminar_observador(self, obs: IObservador) -> None:
        if obs in self._observadores:
            self._observadores.remove(obs)
            print(f"[System] Observador eliminado: {obs}")

    def notificar_observadores(self, mensaje: str) -> None:
        print(f"\n[System] Notificando a {len(self._observadores)} observadores: '{mensaje}'")
        for obs in list(self._observadores):
            try:
                obs.actualizar(mensaje)
            except Exception as e:
                print(f"  Error notificando {obs}: {e}")


# ---------------------------
# OBSERVER: USUARIO (IMPLEMENTA IObservador)
# ---------------------------

class Usuario(IObservador):
    """Clase Usuario que implementa IObservador.

    Atributos:
      - nombre: nombre del usuario (usado como identificador para push en este ejemplo)
      - email: dirección de correo (puede estar vacía)
      - telefono: número de teléfono (puede estar vacío)
      - canales_preferidos: lista de cadenas: 'email', 'sms', 'push'

    Responsabilidad única: representar al usuario y saber cómo recibir notificaciones.
    (Si se necesitara lógica de envío real, la responsabilidad de 'enviar' está en las clases
     que implementan INotificacion, no en Usuario.)
    """
    def __init__(self, nombre: str, email: str = "", telefono: str = "", canales_preferidos: Optional[List[str]] = None):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        # Default: email si no se especifica
        self.canales_preferidos = canales_preferidos or ["email"]

    def __repr__(self) -> str:
        return f"Usuario({self.nombre}, canales={self.canales_preferidos})"

    def actualizar(self, mensaje: str) -> None:
        """Método llamado por el Subject cuando haya una notificación.
        Aquí el usuario decide (según sus canales) cómo recibir el mensaje:
        usa la fábrica para crear el 'notifier' correspondiente (Dependency Inversion).
        """
        print(f"\n[Usuario] {self.nombre} recibe actualización: '{mensaje}'")
        for canal in self.canales_preferidos:
            notifier = NotificacionFactory.crear_notificacion(canal)
            if notifier is None:
                print(f"  - Canal desconocido para {self.nombre}: {canal}")
                continue

            # Seleccionamos el 'destino' según el canal (simulado)
            if canal.lower() == "email":
                destino = self.email or f"{self.nombre.lower()}@example.com"
            elif canal.lower() == "sms":
                destino = self.telefono or "0000000000"
            elif canal.lower() == "push":
                destino = self.nombre  # podría ser un device_id en un caso real
            else:
                destino = self.nombre

            notifier.enviar(mensaje, destino)


# ---------------------------
# EJEMPLO / SIMULACIÓN (main)
# ---------------------------

def main():
    sistema = Notificacion()

    # Crear usuarios con preferencias distintas
    alice = Usuario("Alice", email="alice@example.com", telefono="+5215550001111", canales_preferidos=["email", "push"])
    bob = Usuario("Bob", email="bob@example.com", telefono="+5215550002222", canales_preferidos=["sms"])
    carla = Usuario("Carla", email="carla@example.com", telefono="+5215550003333", canales_preferidos=["email", "sms", "push"])
    diego = Usuario("Diego", canales_preferidos=["push"])  # sin email ni teléfono, demo de valores por defecto

    # Suscribimos usuarios
    sistema.agregar_observador(alice)
    sistema.agregar_observador(bob)
    sistema.agregar_observador(carla)
    sistema.agregar_observador(diego)

    # Enviar una notificación
    sistema.notificar_observadores("Nueva actualización disponible: versión 1.2.0")

    # Eliminar a Bob y enviar otra notificación
    sistema.eliminar_observador(bob)
    sistema.notificar_observadores("Recordatorio: tu suscripción vence en 3 días")

    # Demostrar caso de canal desconocido (extensión sin modificar clientes)
    diego.canales_preferidos.append("telegram")  # canal que la fábrica no reconoce
    sistema.notificar_observadores("Prueba canal desconocido")

    # Mostrar que se puede añadir un nuevo Notifier sin cambiar Usuario/Notificacion:
    # (en la práctica añadiríamos la clase nueva y registraríamos en la fábrica)
    print("\n[Demo] Fin de la simulación.")


if __name__ == "__main__":
    main()
