import json
from typing import Dict, Tuple

from fastmcp import FastMCP, Context

mcp = FastMCP("Car search assistant")


@mcp.tool()
async def generate_json(user_input: str, context: Context) -> Dict[str, any]:
    """Gerar um json com os valores que servirão de filtro para os carros"""

    response = await context.sample(
        f"Crie um json com os valores que você encontrar no input: {user_input}",
        system_prompt="""
                    você deve procurar valores no input que se encaixe nos seguintes campos presentes no filters
                    responda apenas com o json de resposta
                    
                    Preste atenção ao input para diferenciar os campos data_de_fabricacao e ano são duas colunas diferentes
                    
                    caso os campos for [ano, preco, quilometragem, qtd_portas, data_de_fabricacao] identificado que o valor:
                     - deve ser maior ou igual use como do exemplo: {"ano": "$gte: 2015"}
                     - deve ser maior use algo como do exemplo: {"ano": "$gt: 2015"}
                     - deve ser menor ou igual use como do exemplo: {"ano": "$lte: 2015"}
                     - deve ser menor use como do exemplo: {"ano": "$lt: 2015"}
                     
                    caso os campos seja 'marca','modelo','motor','combustivel','cor','cambio','categoria'
                     - deve ser como o exemplo {campo: $like: valor}
                    
                    filters: Um dicionário com os critérios de filtro. Os campos possíveis são:
                        - marca: marca do veículo (ex: 'Fiat', 'Volkswagen')
                        - modelo: modelo do veículo (ex: 'Palio', 'Gol')
                        - ano: ano do veículo (ex: 2022)
                        - preco: preço do veículo (ex: 50000)
                        - motor: especificação do motor (ex: '1.0', '2.0')
                        - combustivel: tipo de combustível (ex: 'Gasolina', 'Flex')
                        - cor: cor do veículo (ex: 'Azul', 'Preto')
                        - quilometragem: quilometragem do veículo (ex: 30000)
                        - portas: quantidade de portas (ex: 2, 4)
                        - cambio: tipo de câmbio (ex: 'Manual', 'Automático')
                        - categoria: categoria do veículo (ex: 'Sedan', 'SUV')
                        
                        
                    caso não for identificado nenhum campo diferente de null, apenas um dicionário vazio assim: {}
                    não escreve nada a mais, apenas: {}
                    """,
    )
    return json.loads(response.text)


@mcp.tool()
async def generate_sql_select(json_car_filters: Dict, context: Context) -> str:
    """
    Gera uma query SQL SELECT baseada nos filtros de carro fornecidos.

    Esta função recebe um dicionário de filtros no formato {"campo": "$operador: valor"}
    e converte para uma consulta SQL válida. Por exemplo: {"cor": "$eq: Azul"} será
    convertido em "SELECT * FROM vehicle WHERE cor = 'Azul'".

    Operadores suportados:
    - $eq: Igual (=)
    - $gt: Maior que (>)
    - $lt: Menor que (<)
    - $gte: Maior ou igual (>=)
    - $lte: Menor ou igual (<=)
    - $like: Contém (LIKE '%valor%')

    Args:
        json_filtros_carro: Dicionário com os campos e operadores de filtro
        context: Contexto da execução do MCP

    Returns:
        Uma string contendo a consulta SQL gerada

    Exemplos:
        {"cor": "$eq: Azul"} → "SELECT * FROM vehicle WHERE cor = 'Azul'"
        {"ano": "$gte: 2020"} → "SELECT * FROM vehicle WHERE ano >= 2020"
        {"modelo": "$like: Gol"} → "SELECT * FROM vehicle WHERE modelo LIKE '%Gol%'"
        :param context:
        :param json_car_filters:
    """

    response = await context.sample(
        f"Crie uma query de SELECT com seguinte input: {json_car_filters}",
        system_prompt="""
                        Você é um especialista em gerar consultas SQL precisas.
        
                        O input será um dicionário com campos e operadores no formato {"campo": "$operador: valor"}.
                        
                        Operadores e sua tradução para SQL:
                        - $eq: = (igual)
                        - $gt: > (maior que)
                        - $lt: < (menor que)
                        - $gte: >= (maior ou igual)
                        - $lte: <= (menor ou igual)
                        - $like: LIKE (contém, adicionar %valor%)
                        
                        Construa uma query SQL SELECT * FROM vehicle com uma cláusula WHERE que reflita precisamente 
                        os filtros fornecidos. Para múltiplos filtros, conecte-os com AND.
                        
                        Responda APENAS com a query SQL completa, sem explicações adicionais.
                    """,
    )
    return response.text


@mcp.tool()
async def generate_prompt_request(properties: Tuple, context: Context) -> str:
    """ """

    properties, properties_exist = properties

    response = await context.sample(
        f"Informe ao usuario que para ter uma resposta mais direta e completa ele deverá fornecer mais "
        f"infomações e essas informações poderá ser qualquer um dos campos prensentes nessa lista {str(set(properties)-set(properties_exist))} e "
        f"peça novamente as opções que ele já enviou, que são os campos presentes nesta lista: {str(properties_exist)}",
        system_prompt="""
                        Você é um assistente que procura carros presentes dentro de um SQLite.
                        
                        peça para ele adicionar mais informações e repetir oque já foi passado mais as perguntas que 
                        serão feitas"
                        
                        O input será uma lista com campos que você devera fazer as perguntas.
                        
                        o output sempre deverá conter o lembrete de que ele tem que repetir os campos já informados 

                        faça perguntas solicitando sempre os campos, caso não foi informado nenhuma informação na lista
                        retorne apenas a pergunta pedindo informações sobre o carro de acordo com os campos, que você 
                        teve contexto
                        
                        me retorne apenas a pergunta sem informar que está retonando algo                    
                    """,
    )
    return response.text
