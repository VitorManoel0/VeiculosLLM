import asyncio

from rich.console import Console

from src.agent.virtual_agent import start_agent
from src.client.main import MCPOpenAIClient
from src.database import db_session


console = Console()

# Initialize database populator
db_populator = db_session.db_session


async def main():
    # Initialize and populate database
    db_populator.clean_database()  # Clear existing data
    db_populator.seed_database()  # Populate with new data
    try:
        client = await MCPOpenAIClient().start_session()

        try:
            await start_agent(client)

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Operação interrompida pelo usuário.[/]")
        finally:
            await client.close()

    except Exception as e:
        console.print(f"[bold red]Erro fatal ao iniciar o agente:[/]{e}")


if __name__ == "__main__":
    asyncio.run(main())
