from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline,Pie
from streamlit_echarts import st_pyecharts
import streamlit as st
import sqlite3
import pandas as pd
from pyecharts.commons.utils import JsCode


conn = sqlite3.connect("daaa.db")
c = conn.cursor()
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS tabelavendasss(ano NUMBER, mes NUMBER,valor NUMBER)') 
def add_user_data(ano,mes,valor):
    c.execute('INSERT INTO tabelavendasss(ano,mes,valor) VALUES (?,?,?)', (ano,mes,valor))
    conn.commit()
def view_all_users():
    c.execute('SELECT * FROM tabelavendasss')
    data = c.fetchall()
    return data
create_table()
from st_on_hover_tabs import on_hover_tabs
import streamlit as st
st.set_page_config(layout="wide")

st.markdown("""<style> section[data-testid='stSidebar'] {
    background-color: #111;
    flex-shrink: unset !important;
    
}

@media(hover:hover) and (min-width: 600px) and (max-width: 769px){

    header[data-testid="stHeader"] {
        display:none;
    }

    section[data-testid='stSidebar'] {
        height: 100%;
        min-width:95px !important;
        width: 95px !important;
        margin-left: 305px;
        position: relative;
        z-index: 1;
        top: 0;
        left: 0;
        background-color: #111;
        overflow-x: hidden;
        transition: 0.5s ease;
        padding-top: 60px;
        white-space: nowrap;
    }

    section[data-testid='stSidebar']:hover{
        min-width: 330px !important;
        }

    button[kind="header"] {
        display: none;
    }

    div[data-testid="collapsedControl"]{
        display: none;
    }

}

@media(hover: hover) and (min-width: 769px){

    header[data-testid="stHeader"] {
        display:none;
    }

    section[data-testid='stSidebar'] {
        height: 100%;
        min-width:95px !important;
        width: 95px !important;
        transform:translateX(0px);
        position: relative;
        z-index: 1;
        top: 0;
        left: 0;
        background-color: #111;
        overflow-x: hidden;
        transition: 0.5s ease;
        padding-top: 60px;
        white-space: nowrap;
    }

    section[data-testid='stSidebar']:hover{
        min-width: 330px !important;
        }

    button[kind="header"] {
        display: none;
    }

    div[data-testid="collapsedControl"]{
        display: none;
    }
}</style>""", unsafe_allow_html=True)


with st.sidebar:
     tabs = on_hover_tabs(tabName=['Dashboard', 'Análise geral', 'Incluir venda'], 
                         iconName=['query_stats', 'lists', 'done'], default_choice=0)
dados = pd.DataFrame(view_all_users(),columns=["ano", "mes","Vlr_LiqItem"])
dados = dados.sort_values(by = ["mes"])
if tabs =='Dashboard':
    def main():
        tl = Timeline()
        def add(z,x=[],y=[]):
            bar = (
                    Bar()
                    .add_xaxis(x)
                    .add_yaxis("Vendas", y)
                    .set_global_opts(title_opts=opts.TitleOpts(is_show=False),legend_opts=opts.LegendOpts(is_show=False))
                    .reversal_axis()
                )
            tl.add(bar,z)
        
        anos = dados["ano"].value_counts().index.sort_values()
        def xsss(i):
            g = dados[["mes","Vlr_LiqItem"]].loc[dados["ano"] == i]
            g = pd.DataFrame(g)
            s = g[["mes","Vlr_LiqItem"]].groupby("mes").sum()
            return list(s["Vlr_LiqItem"])
        mesess = list(dados["mes"].value_counts().index.sort_values())
        def meses(i):
            g = dados[["mes","Vlr_LiqItem"]].loc[dados["ano"] == i]
            g = pd.DataFrame(g)
            s = g[["mes","Vlr_LiqItem"]].groupby("mes").sum()
            return list(s.groupby("mes").groups)
        def anoss(z):
            g = dados[["ano","Vlr_LiqItem"]].loc[dados["mes"] == z]
            g = pd.DataFrame(g)
            s = g[["ano", "Vlr_LiqItem"]].groupby("ano").sum()
            return list(s["Vlr_LiqItem"])
        def anoxs(z):
            g = dados[["ano","Vlr_LiqItem"]].loc[dados["mes"] == z]
            g = pd.DataFrame(g)
            s = g[["ano", "Vlr_LiqItem"]].groupby("ano").sum()
            return list(s.groupby("ano").groups)
        tl2 = Timeline()
        tl2.add_schema(pos_left="30px", pos_right="30px", pos_bottom="5px")
        tl.add_schema(pos_left="20px", pos_right="70px", pos_bottom="5px")
        def addpie(h,x=[],y=[]):
            pie = (
                Pie()
                .add(
                    "Vendas",
                    [list(z) for z in zip(x, y)],
                    rosetype="radius",
                    radius=["30%", "50%"],
                    center=["50%","50%"],
                    label_opts=opts.LabelOpts(
                        position="outside",  
                    ),
                ) 
                .set_global_opts(title_opts=opts.TitleOpts(title=""),legend_opts=opts.LegendOpts(is_show=False),tooltip_opts=opts.TooltipOpts()))
            tl2.add(pie,h)
        meta = 1000000
        meta_daniel = 300000
        total_daniel = 100000
        meta_gabriel = 300000
        total_gabriel = 150000
        total_time = 700000
        lista1 = [
    {"value": (meta - total_time), "percent": (meta - total_time)/(meta)},
    {"value":(meta_daniel - total_daniel),"percent": (meta_daniel-total_daniel)/ (meta_daniel)},
    {"value":(meta_gabriel- total_gabriel),"percent": (meta_gabriel - total_gabriel)/ (meta_gabriel)}
]
        lista2 = [
    {"value": total_time, "percent": total_time/(meta)},
    {"value":total_daniel,"percent": total_daniel/ (meta_daniel)},
    {"value":total_gabriel,"percent": total_gabriel/ (meta_gabriel)}
]
        ca = (
        Bar()
        .add_xaxis(["meta","daniel","gabriel"])
        .add_yaxis(["valor vendido","valor vendido","valor vendido"], lista2, stack="stack1", category_gap="50%")
        .add_yaxis(["quanto falta para bater a meta","quanto falta para bater a meta","quanto falta para bater a meta"],lista1, stack="stack1",category_gap="50%")
        .set_global_opts(title_opts=opts.TitleOpts(is_show=False))
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}")),
            legend_opts=opts.LegendOpts(is_show=False)
))

        for i in anos:
            add(i,meses(i),xsss(i))
        for x in mesess:
            addpie(x,anoxs(x),anoss(x))
        col1, col2 = st.columns([1.5,1])
        with col1:
            with st.expander(label="Comparação meses",expanded=True):
                st_pyecharts(tl2,width="550px",height="270px")
           
            with st.expander(expanded=True,label="Meta vendedores"):
                st_pyecharts(ca,key="bar",height="200px", width="650px")
        with col2:
            with st.expander(expanded=True,label="Vendas por mês"):
                st_pyecharts(tl,height="560px",width="460px") 



        

    if __name__ == "__main__":
        main()



elif tabs == 'Incluir venda':
    with st.form(key="incluir"):
        ano = st.number_input("Ano", step=1, format="%d")
        mes = st.selectbox("Mês", range(1,13))
        valor = st.number_input("Valor de venda")
        botao = st.form_submit_button("Enviar")
    if botao:
        if ano and mes and valor:
            add_user_data(ano,mes,valor)
            st.success("Venda cadastrada com sucesso")
        else:
            st.error("preencha todos os campos")
elif tabs == "Análise geral":
    col1, col2 = st.columns(2)
    anos = dados["Ano"].value_counts().index.sort_values()
    mess = dados["Mês"].value_counts().index.sort_values()
    ano = col1.selectbox("Ano",anos)
    dados_anos = dados[dados["Ano"] == ano]
    mes = col2.selectbox("Mês",mess)
    dados_mes = dados[dados["Mês"] == mes]
    dados_final = dados_anos[dados_anos["Mês"] == mes]
    botao = col1.checkbox("Todas as opções",key="botao1",value=True)
    botao2 = col2.checkbox("Todas as opções",key="botao2",value=True)
    if botao == True and botao2 == True:
        st.dataframe(dados.sort_values(by="Ano"))
    elif botao == True and botao2 == False:
        st.dataframe(dados_mes.sort_values(by = "Ano"))
    elif botao == False and botao2 == True:
        st.dataframe(dados_anos.sort_values(by="Ano"))
    else:
        st.dataframe(dados_final.sort_values(by="Ano"))
