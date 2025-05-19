import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

# Configurações iniciais
sns.set_theme(style="whitegrid")
plt.style.use('ggplot')

# Função para carregar uma tabela do CSV
def carregar_tabela(nome_arquivo):
    df = pd.read_csv(nome_arquivo)
    return [list(df.columns)] + df.values.tolist()

# Função para formatar a tabela no PDF
def formata_tabela(tabela):
    styles = getSampleStyleSheet()
    return [[Paragraph(str(cell), styles["Normal"]) for cell in row] for row in tabela]

# Função para adicionar uma imagem ao relatório
def adicionar_imagem(nome_arquivo, width=400):
    if os.path.exists(nome_arquivo):
        return Image(nome_arquivo, width=width, height=250)
    else:
        return Paragraph(f"Imagem '{nome_arquivo}' não encontrada.", getSampleStyleSheet()["Normal"])

# Função para criar o relatório PDF
def criar_relatorio_pdf(nome_arquivo_saida):
    doc = SimpleDocTemplate(nome_arquivo_saida, pagesize=letter)
    elements = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]

    # Título do relatório
    elements.append(Paragraph("Relatório Infomaz - Análise de Vendas", title_style))
    elements.append(Spacer(1, 24))

    # Função para adicionar uma seção com título, descrição e tabela
    def adicionar_secao(titulo, descricao, nome_tabela, nome_imagem=None):
        elements.append(Paragraph(titulo, heading_style))
        elements.append(Paragraph(descricao, normal_style))
        elements.append(Spacer(1, 12))

        if os.path.exists(nome_tabela):
            tabela = carregar_tabela(nome_tabela)
            tabela_formatada = formata_tabela(tabela)
            t = Table(tabela_formatada)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph(f"Tabela '{nome_tabela}' não encontrada.", normal_style))
        elements.append(Spacer(1, 12))

        if nome_imagem and os.path.exists(nome_imagem):
            img = adicionar_imagem(nome_imagem)
            elements.append(img)
        elements.append(Spacer(1, 24))

    # Carregar arquivo Excel
    caminho_arquivo_excel = "Case_Infomaz_Base_de_Dados.xlsx"
    xls = pd.ExcelFile(caminho_arquivo_excel)

    # Carregar tabelas
    produtos_df = pd.read_excel(xls, sheet_name="Cadastro Produtos", header=1)
    clientes_df = pd.read_excel(xls, sheet_name="Cadastro Clientes", header=1)
    transacoes_df = pd.read_excel(xls, sheet_name="Transações Vendas", header=1)
    estoque_df = pd.read_excel(xls, sheet_name="Cadastro de Estoque", header=1)
    fornecedores_df = pd.read_excel(xls, sheet_name="Cadastro Fornecedores", header=1)

    # Converter datas
    transacoes_df["DATA NOTA"] = pd.to_datetime(transacoes_df["DATA NOTA"])
    transacoes_df["MES_ANO"] = transacoes_df["DATA NOTA"].dt.to_period('M')
    estoque_df["DATA ESTOQUE"] = pd.to_datetime(estoque_df["DATA ESTOQUE"])

    # Calcular VALOR UNITÁRIO se não existir
    if "VALOR UNITARIO" not in estoque_df.columns:
        estoque_df["VALOR UNITARIO"] = estoque_df["VALOR ESTOQUE"] / estoque_df["QTD ESTOQUE"]

    # ====================
    # Questão 1: Valor Total de Venda por Categoria
    # ====================
    df_vendas_categoria = transacoes_df.merge(
        produtos_df[["ID PRODUTO", "CATEGORIA"]], on="ID PRODUTO"
    )
    valor_total_venda_categoria = df_vendas_categoria.groupby("CATEGORIA")["VALOR NOTA"].sum().reset_index()
    valor_total_venda_categoria.sort_values(by="VALOR NOTA", ascending=False, inplace=True)
    valor_total_venda_categoria.to_csv("questao_1_valor_total_categoria.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x="VALOR NOTA", y="CATEGORIA", data=valor_total_venda_categoria.head(10))
    plt.title("Questão 1 - Valor Total de Venda por Categoria")
    plt.xlabel("Valor Total de Venda")
    plt.ylabel("Categoria")
    plt.tight_layout()
    plt.savefig("grafico_questao_1.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 2: Margem de Lucro por Produto
    # ====================
    produtos_estoque_map = produtos_df[["ID PRODUTO", "ID ESTOQUE"]]
    df_margem = transacoes_df.merge(produtos_estoque_map, on="ID PRODUTO")
    df_margem = df_margem.merge(estoque_df[["ID ESTOQUE", "VALOR UNITARIO"]], on="ID ESTOQUE")
    df_margem["MARGEM"] = df_margem["VALOR ITEM"] - df_margem["VALOR UNITARIO"]

    # Adicionar informações faltando
    if "NOME PRODUTO" not in df_margem.columns or "CATEGORIA" not in df_margem.columns:
        df_margem = df_margem.merge(produtos_df[["ID PRODUTO", "NOME PRODUTO", "CATEGORIA"]], on="ID PRODUTO")

    # Agrupar por ID PRODUTO e calcular média da margem
    margem_produtos = df_margem.groupby("ID PRODUTO").agg(
        MARGEM=("MARGEM", "mean"),
        NOME_PRODUTO=("NOME PRODUTO", "first"),
        CATEGORIA=("CATEGORIA", "first")
    ).reset_index()
    margem_produtos["MARGEM"] = margem_produtos["MARGEM"].round(2)
    margem_produtos.sort_values(by="MARGEM", ascending=False, inplace=True)
    margem_produtos.to_csv("questao_2_margem_produtos.csv", index=False)

    # ====================
    # Questão 3: Ranking de clientes por quantidade de produtos comprados por mês
    # ====================
    ranking_clientes_mensal = transacoes_df.groupby(["ID CLIENTE", "DATA NOTA"])["QTD ITEM"].sum().reset_index()
    ranking_clientes_mensal["MES_ANO"] = pd.to_datetime(ranking_clientes_mensal["DATA NOTA"]).dt.to_period('M')
    ranking_completo = ranking_clientes_mensal.merge(clientes_df[["ID CLIENTE", "NOME CLIENTE"]], on="ID CLIENTE")
    ranking_completo["POSICAO_RANKING"] = ranking_completo.groupby("MES_ANO").cumcount() + 1
    top_clientes_mensal = ranking_completo.sort_values(by=["MES_ANO", "QTD ITEM"], ascending=[True, False]).head(10)
    top_clientes_mensal.to_csv("questao_3_ranking_clientes.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x="QTD ITEM", y="NOME CLIENTE", data=top_clientes_mensal)
    plt.title("Questão 3 - Top 10 Clientes por Quantidade de Produtos Comprados por Mês")
    plt.xlabel("Quantidade de Produtos")
    plt.ylabel("Nome do Cliente")
    plt.tight_layout()
    plt.savefig("grafico_questao_3.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 4: Ranking de fornecedores por quantidade de estoque por mês
    # ====================
    ranking_fornecedores_mensal = estoque_df.groupby(["ID FORNECEDOR", "DATA ESTOQUE"])["QTD ESTOQUE"].sum().reset_index()
    ranking_fornecedores_mensal["MES_ANO"] = pd.to_datetime(ranking_fornecedores_mensal["DATA ESTOQUE"]).dt.to_period('M')
    ranking_fornecedores_mensal.drop(columns=["DATA ESTOQUE"], inplace=True)
    ranking_fornecedores_mensal.sort_values(by=["MES_ANO", "QTD ESTOQUE"], ascending=[True, False], inplace=True)
    ranking_completo_fornecedores = ranking_fornecedores_mensal.merge(fornecedores_df[["ID FORNECEDOR", "NOME FORNECEDOR"]], on="ID FORNECEDOR")
    top_fornecedores_mensal = ranking_completo_fornecedores.head(10)
    top_fornecedores_mensal.to_csv("questao_4_ranking_fornecedores.csv", index=False)

    # ====================
    # Questão 5: Ranking de produtos por quantidade de venda por mês
    # ====================
    ranking_produtos_mensal = transacoes_df.groupby(["ID PRODUTO", "DATA NOTA"])["QTD ITEM"].sum().reset_index()
    ranking_produtos_mensal["MES_ANO"] = pd.to_datetime(ranking_produtos_mensal["DATA NOTA"]).dt.to_period('M')
    ranking_completo_produtos = ranking_produtos_mensal.merge(produtos_df[["ID PRODUTO", "NOME PRODUTO", "CATEGORIA"]], on="ID PRODUTO")
    ranking_completo_produtos["POSICAO_RANKING"] = ranking_completo_produtos.groupby("MES_ANO").cumcount() + 1
    top_produtos_mensal = ranking_completo_produtos.sort_values(by=["MES_ANO", "QTD ITEM"], ascending=[True, False]).head(10)
    top_produtos_mensal.to_csv("questao_5_ranking_produtos_quantidade.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x="QTD ITEM", y="NOME PRODUTO", data=top_produtos_mensal)
    plt.title("Questão 5 - Top 10 Produtos por Quantidade de Venda por Mês")
    plt.xlabel("Quantidade Vendida")
    plt.ylabel("Produto")
    plt.tight_layout()
    plt.savefig("grafico_questao_5.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 6: Ranking de produtos por valor de venda por mês
    # ====================
    ranking_valor_produtos_mensal = transacoes_df.groupby(["ID PRODUTO", "DATA NOTA"])["VALOR ITEM"].sum().reset_index()
    ranking_valor_produtos_mensal["MES_ANO"] = pd.to_datetime(ranking_valor_produtos_mensal["DATA NOTA"]).dt.to_period('M')
    ranking_valor_produtos_mensal.rename(columns={"VALOR ITEM": "TOTAL_VENDIDO"}, inplace=True)
    ranking_valor_produtos_mensal = ranking_valor_produtos_mensal.merge(produtos_df[["ID PRODUTO", "NOME PRODUTO", "CATEGORIA"]], on="ID PRODUTO")
    ranking_valor_produtos_mensal["POSICAO_RANKING"] = ranking_valor_produtos_mensal.groupby("MES_ANO").cumcount() + 1
    top_valor_produtos_mensal = ranking_valor_produtos_mensal.sort_values(by=["MES_ANO", "TOTAL_VENDIDO"], ascending=[True, False]).head(10)
    top_valor_produtos_mensal.to_csv("questao_6_ranking_produtos_valor.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x="TOTAL_VENDIDO", y="NOME PRODUTO", data=top_valor_produtos_mensal)
    plt.title("Questão 6 - Top 10 Produtos por Valor de Venda por Mês")
    plt.xlabel("Valor Total Vendido")
    plt.ylabel("Produto")
    plt.tight_layout()
    plt.savefig("grafico_questao_6.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 7: Média de Valor de Venda por Categoria por Mês
    # ====================
    transacoes_com_categoria = transacoes_df.merge(produtos_df[["ID PRODUTO", "CATEGORIA"]], on="ID PRODUTO")
    transacoes_com_categoria["DATA NOTA"] = pd.to_datetime(transacoes_com_categoria["DATA NOTA"])
    transacoes_com_categoria["MES_ANO"] = transacoes_com_categoria["DATA NOTA"].dt.to_period('M')
    media_venda_categoria_mensal = transacoes_com_categoria.groupby(["CATEGORIA", "MES_ANO"])["VALOR ITEM"].mean().reset_index()
    media_venda_categoria_mensal.rename(columns={"VALOR ITEM": "MEDIA_VALOR_ITEM"}, inplace=True)
    media_venda_categoria_mensal["MES_ANO"] = media_venda_categoria_mensal["MES_ANO"].astype(str)
    media_venda_categoria_mensal["MEDIA_VALOR_ITEM"] = media_venda_categoria_mensal["MEDIA_VALOR_ITEM"].round(2)
    media_venda_categoria_mensal.to_csv("questao_7_media_valor_categoria.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="MES_ANO", y="MEDIA_VALOR_ITEM", hue="CATEGORIA", data=media_venda_categoria_mensal)
    plt.title("Questão 7 - Média de Valor de Venda por Categoria por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Média de Valor de Venda")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafico_questao_7.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 8: Média de margem de lucro por categoria
    # ====================
    df_margem_categoria = transacoes_df.merge(produtos_estoque_map, on="ID PRODUTO")
    df_margem_categoria = df_margem_categoria.merge(estoque_df[["ID ESTOQUE", "VALOR UNITARIO"]], on="ID ESTOQUE")
    df_margem_categoria["MARGEM"] = df_margem_categoria["VALOR ITEM"] - df_margem_categoria["VALOR UNITARIO"]
    df_margem_categoria = df_margem_categoria.merge(produtos_df[["ID PRODUTO", "CATEGORIA"]], on="ID PRODUTO")
    df_margem_categoria["DATA NOTA"] = pd.to_datetime(df_margem_categoria["DATA NOTA"])
    df_margem_categoria["MES_ANO"] = df_margem_categoria["DATA NOTA"].dt.to_period('M')
    ranking_margem_categoria = df_margem_categoria.groupby(["CATEGORIA", "MES_ANO"])["MARGEM"].mean().reset_index()
    ranking_margem_categoria.rename(columns={"MARGEM": "MEDIA_MARGEM"}, inplace=True)
    ranking_margem_categoria["MEDIA_MARGEM"] = ranking_margem_categoria["MEDIA_MARGEM"].round(2)
    ranking_margem_categoria.to_csv("questao_8_ranking_margem_categoria.csv", index=False)
    ranking_margem_categoria["MES_ANO"] = ranking_margem_categoria["MES_ANO"].astype(str)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="MES_ANO", y="MEDIA_MARGEM", hue="CATEGORIA", data=ranking_margem_categoria)
    plt.title("Questão 8 - Média de Margem de Lucro por Categoria por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Média de Margem")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafico_questao_8.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Questão 9: Lista de produtos comprados por clientes
    # ====================
    transacoes_com_produtos = transacoes_df.merge(produtos_df[["ID PRODUTO", "NOME PRODUTO", "CATEGORIA"]], on="ID PRODUTO")
    transacoes_com_produtos = transacoes_com_produtos.merge(clientes_df[["ID CLIENTE", "NOME CLIENTE"]], on="ID CLIENTE")
    top_produtos_cliente = transacoes_com_produtos.groupby(["NOME CLIENTE", "NOME PRODUTO"])["QTD ITEM"].sum().reset_index()
    top_produtos_cliente.sort_values(by="QTD ITEM", ascending=False, inplace=True)
    top_produtos_cliente.to_csv("questao_9_lista_produtos_clientes.csv", index=False)

    # ====================
    # Questão 10: Ranking de produtos por quantidade de estoque
    # ====================
    estoque_com_produtos = estoque_df.merge(produtos_df[["ID ESTOQUE", "NOME PRODUTO", "CATEGORIA"]], on="ID ESTOQUE")
    ranking_estoque_produtos = estoque_com_produtos.groupby(["NOME PRODUTO", "CATEGORIA"])["QTD ESTOQUE"].sum().reset_index()
    ranking_estoque_produtos.rename(columns={"QTD ESTOQUE": "TOTAL_ESTOQUE"}, inplace=True)
    ranking_estoque_produtos.sort_values(by="TOTAL_ESTOQUE", ascending=False, inplace=True)
    top_estoque_produtos = ranking_estoque_produtos.head(20)
    top_estoque_produtos.to_csv("questao_10_ranking_estoque_produtos.csv", index=False)

    # Plotar gráfico
    plt.figure(figsize=(10, 6))
    sns.barplot(x="TOTAL_ESTOQUE", y="NOME PRODUTO", data=top_estoque_produtos)
    plt.title("Questão 10 - Top 20 Produtos por Quantidade de Estoque")
    plt.xlabel("Quantidade de Estoque")
    plt.ylabel("Produto")
    plt.tight_layout()
    plt.savefig("grafico_questao_10.png", dpi=300, bbox_inches='tight')
    plt.close()

    # ====================
    # Criar Relatório PDF
    # ====================
    adicionar_secao(
        "Questão 1 - Valor Total de Venda por Categoria",
        "Esta métrica mostra o faturamento total por categoria de produto.",
        "questao_1_valor_total_categoria.csv",
        "grafico_questao_1.png"
    )

    adicionar_secao(
        "Questão 2 - Margem de Lucro por Produto",
        "Mostra a média de margem calculada como (Valor Item - Valor Unitário) para cada produto.",
        "questao_2_margem_produtos.csv"
    )

    adicionar_secao(
        "Questão 3 - Top 10 Clientes por Quantidade de Produtos Comprados por Mês",
        "Ranking dos clientes com base na quantidade de produtos comprados por mês.",
        "questao_3_ranking_clientes.csv",
        "grafico_questao_3.png"
    )

    adicionar_secao(
        "Questão 4 - Top 10 Fornecedores por Quantidade de Estoque Disponível por Mês",
        "Mostra os fornecedores com maior estoque disponível por mês.",
        "questao_4_ranking_fornecedores.csv"
    )

    adicionar_secao(
        "Questão 5 - Top 10 Produtos por Quantidade de Venda por Mês",
        "Produtos mais vendidos por mês, com base na quantidade.",
        "questao_5_ranking_produtos_quantidade.csv",
        "grafico_questao_5.png"
    )

    adicionar_secao(
        "Questão 6 - Top 10 Produtos por Valor de Venda por Mês",
        "Produtos com maior valor de venda mensal.",
        "questao_6_ranking_produtos_valor.csv",
        "grafico_questao_6.png"
    )

    adicionar_secao(
        "Questão 7 - Média de Valor de Venda por Categoria por Mês",
        "Gráfico mostra a evolução da média de valor de venda por categoria ao longo dos meses.",
        "questao_7_media_valor_categoria.csv",
        "grafico_questao_7.png"
    )

    adicionar_secao(
        "Questão 8 - Média de Margem de Lucro por Categoria por Mês",
        "Mostra a média de margem de lucro por categoria e mês.",
        "questao_8_ranking_margem_categoria.csv",
        "grafico_questao_8.png"
    )

    adicionar_secao(
        "Questão 9 - Top 20 Produtos Mais Comprados por Clientes",
        "Lista dos produtos mais comprados pelos clientes.",
        "questao_9_lista_produtos_clientes.csv"
    )

    adicionar_secao(
        "Questão 10 - Top 20 Produtos por Quantidade de Estoque",
        "Mostra quais produtos possuem mais unidades em estoque.",
        "questao_10_ranking_estoque_produtos.csv",
        "grafico_questao_10.png"
    )

    # Build the PDF
    doc.build(elements)

    print(f"\n✅ Relatório PDF salvo como '{nome_arquivo_saida}'.")
    
criar_relatorio_pdf("relatorio_infomaz.pdf")