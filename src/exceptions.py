"""
Módulo para excepciones personalizadas de la aplicación.
"""

class APIException(Exception):
    """Clase base para las excepciones de la API."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class InvalidAPIKeyError(APIException):
    """Excepción para una API Key inválida o mal formada."""
    def __init__(self, detail: str = "API Key inválida o no proporcionada."):
        super().__init__(status_code=401, detail=detail)

class EndpointNotFoundError(APIException):
    """Excepción para cuando un endpoint no se encuentra."""
    def __init__(self, endpoint_id: str):
        detail = f"Endpoint con id '{endpoint_id}' no encontrado."
        super().__init__(status_code=404, detail=detail)

class ForbiddenAccessError(APIException):
    """Excepción para intentos de acceso no autorizados a recursos."""
    def __init__(self, detail: str = "No tienes permiso para acceder a este recurso."):
        super().__init__(status_code=403, detail=detail)

class InsufficientCreditsError(APIException):
    """Excepción para cuando un usuario no tiene créditos suficientes."""
    def __init__(self, required: int):
        detail = f"Créditos insuficientes. Se requieren {required} créditos para esta operación."
        super().__init__(status_code=402, detail=detail) # 402 Payment Required

class FileProcessingError(APIException):
    """Excepción para errores durante el procesamiento de archivos."""
    def __init__(self, detail: str = "Error al procesar el archivo."):
        super().__init__(status_code=500, detail=detail)

class DatabaseError(APIException):
    """Excepción para errores genéricos de base de datos."""
    def __init__(self, detail: str = "Error interno en la base de datos."):
        super().__init__(status_code=500, detail=detail)

class OpenAIError(APIException):
    """Excepción para errores relacionados con la API de OpenAI."""
    def __init__(self, detail: str = "Error en el servicio de análisis de IA."):
        super().__init__(status_code=503, detail=detail) # 503 Service Unavailable
