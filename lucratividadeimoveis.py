# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf

# Definindo a função que calcula o valor das parcelas


def calcular_parcela(valor_imovel, valor_entrada, valor_reforco, qtde_reforco, prazo_pagamento, reajuste_mensal):
    valor_financiado = valor_imovel - valor_entrada
    valor_reforco_total = valor_reforco * qtde_reforco
    valor_financiado -= valor_reforco_total
    qtde_parcelas = prazo_pagamento - qtde_reforco
    valor_parcela = npf.pmt(reajuste_mensal/100,
                            qtde_parcelas, -valor_financiado, 0, when='begin')
    # Note que foi corrigido o nome do parâmetro da função npf.pmt()

    return valor_parcela

# Definindo a função que calcula a lucratividade


def calcular_lucratividade(valor_imovel, valor_entrada, valor_reforco, qtde_reforco, prazo_pagamento, reajuste_mensal, valor_venda):
    valor_parcela = calcular_parcela(
        valor_imovel, valor_entrada, valor_reforco, qtde_reforco, prazo_pagamento, reajuste_mensal)
    valor_total = valor_parcela * \
        (prazo_pagamento - qtde_reforco) + \
        valor_entrada + valor_reforco * qtde_reforco
    lucro = valor_venda - valor_total
    porcentagem_lucro = lucro / valor_total * 100
    return porcentagem_lucro


# Configurando o layout da página
st.set_page_config(page_title='Investimentos Imobiliários', layout='wide')

# Adicionando o título da página
st.title('Investimentos Imobiliários')

# Criando o formulário para inserir os valores
col1, col2 = st.columns(2)

with col1:
    valor_imovel = st.number_input('Valor do imóvel na planta')
    valor_entrada = st.number_input('Valor da entrada')
    valor_reforco = st.number_input('Valor dos reforços')
    qtde_reforco = st.number_input('Quantidade de reforços')
    prazo_pagamento = st.number_input('Prazo de pagamento (em meses)')
    reajuste_mensal = st.number_input('Reajuste mensal das parcelas')

with col2:
    inicio_obra = st.date_input('Início da obra')
    termino_obra = st.date_input('Término da obra')
    valor_venda = st.number_input('Valor de venda')

# Chamando a função que calcula a lucratividade
lucratividade = calcular_lucratividade(
    valor_imovel, valor_entrada, valor_reforco, qtde_reforco, prazo_pagamento, reajuste_mensal, valor_venda)

# Mostrando os resultados na página
st.write('### Resultados')
st.write(f'Lucratividade: {lucratividade:.2f}%')
