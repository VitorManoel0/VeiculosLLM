from rich.console import Console
from rich.table import Table
import sys
import os

from src.client.main import MCPOpenAIClient

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.models.vehicle_model import VehicleModel

console = Console()


async def start_agent(client: MCPOpenAIClient):
    """Start the virtual agent with MCP client support.

    Args:
        client: MCP client instance.
    """

    console.print(
        f"[green]Olá sou seu assistente de busca ao carro desejado. o que você deseja procurar?[/]\n"
        f"[orange]Caso queira sair a qualquer momento voce pode digitar sair ou exit[/]",

    )

    while True:
        user_input = input("Você: ")
        if ("sair" or "exit") in user_input.lower():
            break

        with console.status("[yellow]Buscando...[/]", spinner="line"): # Você pode mudar "line" para outro spinner se preferir (ex: "dots", "dots2", etc.)
            response, text_ = await client.process_query(user_input)

        display_results(response)

        console.print(f"[bold green]Agente Virtual:[/] {text_[0].text}")


def display_results(vehicles: list[VehicleModel]):
    """Print a list of vehicles on table format."""
    if not vehicles:
        console.print("[bold orange]Nenhum resultado para exibir.[/]")
        console.print(
            "[bold red]bold orange:[/] Não conseguir achar nenhum veículos com base na sua pesquisa."
        )
        return

    table = Table(title="Resultados da Busca")

    expected_columns = [
        "Marca",
        "Modelo",
        "Ano",
        "Motor",
        "Combustivel",
        "Cor",
        "Quilometragem",
        "Portas",
        "Cambio",
        "Preço",
        "Categoria",
    ]

    for col_name in expected_columns:
        table.add_column(col_name)

    for vehicle in vehicles:
        try:
            brand = vehicle.marca
            model = vehicle.modelo
            year = str(vehicle.ano)
            engine = vehicle.motor
            fuel = vehicle.combustivel
            color = vehicle.cor
            miles = vehicle.quilometragem
            doors = vehicle.portas
            gearbox = vehicle.cambio
            price = vehicle.preco
            price_str = f"R$ {price:.2f}" if isinstance(price, (int, float)) else "N/A"
            category = vehicle.categoria

            table.add_row(
                brand,
                model,
                year,
                engine,
                fuel,
                color,
                str(miles),
                str(doors),
                gearbox,
                price_str,
                category,
            )
        except Exception as row_e:
            console.print(
                f"[bold red]Erro ao processar linha da tabela:[/]{row_e} - Dados: {vehicle}"
            )
            table.add_row("Erro" * (len(expected_columns) - 1))

    console.print(table)
