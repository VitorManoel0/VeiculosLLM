from pydantic import BaseModel, Field
from datetime import date


class VehicleModel(BaseModel):
    id: int = Field(..., description="ID único do veículo")
    marca: str = Field(..., description="Marca do veículo")
    modelo: str = Field(..., description="Modelo do veículo")
    ano: int = Field(..., description="Ano de fabricação")
    motor: str = Field(..., description="Detalhes do motor")
    combustivel: str = Field(..., description="Tipo de combustível")
    cor: str = Field(..., description="Cor do veículo")
    quilometragem: int = Field(..., description="Quilometragem do veículo")
    portas: int = Field(..., description="Número de portas")
    cambio: str = Field(..., description="Tipo de câmbio")
    preco: float = Field(..., description="Preço do veículo")
    categoria: str = Field(..., description="Categoria do veículo")

    model_config = {"from_attributes": True}
