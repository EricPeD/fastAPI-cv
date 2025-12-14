from pydantic import BaseModel, Field, HttpUrl
from typing import List
from uuid import UUID


class Experiencia(BaseModel):
    puesto: str | None = Field(None, description="Puesto o cargo ocupado.")
    empresa: str | None = Field(None, description="Empresa donde se trabajó.")
    periodo: str | None = Field(
        None, description="Período de tiempo en el puesto (ej. '2018 - 2022')."
    )
    descripcion: str | None = Field(
        None, description="Descripción de las responsabilidades y logros."
    )


class Educacion(BaseModel):
    titulo: str | None = Field(None, description="Título o grado obtenido.")
    institucion: str | None = Field(None, description="Institución educativa.")
    periodo: str | None = Field(
        None, description="Período de tiempo de estudio (ej. '2014 - 2018')."
    )


class CVInfo(BaseModel):
    name: str | None = Field(None, description="Nombre completo del candidato.")
    email: str | None = Field(None, description="Correo electrónico de contacto.")
    phone: str | None = Field(None, description="Número de teléfono de contacto.")
    resumen: str | None = Field(
        None, description="Resumen profesional o perfil del candidato."
    )
    experiencia: List[Experiencia] | None = Field(
        [], description="Lista de experiencias laborales."
    )
    educacion: List[Educacion] | None = Field(
        [], description="Lista de formaciones académicas."
    )
    habilidades: List[str] | None = Field(
        [], description="Lista de habilidades técnicas o 'hard skills'."
    )
    soft_skills: List[str] | None = Field(
        [], description="Lista de habilidades blandas o 'soft skills'."
    )
    full_text: str | None = Field(
        None, description="El texto completo extraído del CV."
    )


class CallbackBody(BaseModel):
    callback_url: HttpUrl = Field(
        ..., description="URL a la que se enviará el resultado del procesamiento."
    )


class AuthActor(BaseModel):
    user_id: str
    key_id: UUID


class InputTokensDetails(BaseModel):
    cached_tokens: int = 0

class OutputTokensDetails(BaseModel):
    reasoning_tokens: int = 0

class Usage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_tokens_details: InputTokensDetails | None = Field(default_factory=InputTokensDetails)
    output_tokens_details: OutputTokensDetails | None = Field(default_factory=OutputTokensDetails)

    def __add__(self, other: 'Usage'):
        if not isinstance(other, Usage):
            return NotImplemented

        # Aggregate basic token counts
        total_input = self.input_tokens + other.input_tokens
        total_output = self.output_tokens + other.output_tokens
        total_tokens = self.total_tokens + other.total_tokens

        # Aggregate detailed token counts, handling potential None values
        self_input_details = self.input_tokens_details or InputTokensDetails()
        other_input_details = other.input_tokens_details or InputTokensDetails()
        total_cached = self_input_details.cached_tokens + other_input_details.cached_tokens

        self_output_details = self.output_tokens_details or OutputTokensDetails()
        other_output_details = other.output_tokens_details or OutputTokensDetails()
        total_reasoning = self_output_details.reasoning_tokens + other_output_details.reasoning_tokens

        return Usage(
            input_tokens=total_input,
            output_tokens=total_output,
            total_tokens=total_tokens,
            input_tokens_details=InputTokensDetails(cached_tokens=total_cached),
            output_tokens_details=OutputTokensDetails(reasoning_tokens=total_reasoning)
        )
