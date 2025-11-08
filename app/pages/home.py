import streamlit as st

st.set_page_config(
    page_title="SINAPI+ - Sistema de Orçamentos de Obras",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header {
        font-size: 2rem;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #66bb6a;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
    }
    .feature-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    .info-box {
        background-color: #2d2d2d;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .step-number {
        background-color: #4caf50;
        color: #121212;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
    }
    .stSelectbox > div > div {
        background-color: #1e1e1e;
        border: 1px solid #4caf50;
        color: #e0e0e0;
    }
    .stSelectbox > div > div:hover {
        border-color: #66bb6a;
    }
    /* Botões personalizados */
    .stButton > button {
        background-color: #4caf50;
        color: #121212;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #66bb6a;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    /* Divisórias e separadores */
    hr {
        border-color: #4caf50;
        opacity: 0.3;
        margin: 2rem 0;
    }
    /* Texto do rodapé */
    .footer-text {
        color: #b0b0b0;
        text-align: center;
        font-size: 0.9rem;
    }
    /* Cards de categorias com hover */
    .category-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #333;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .category-card:hover {
        border-color: #4caf50;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2);
    }
    /* Container para alinhar as seções */
    .sections-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .section-column {
        flex: 1;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-header"> SINAPI+</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        '<div class="sub-header"> O que é o SINAPI+?</div>', unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="feature-card">
    O <strong>SINAPI+</strong> é uma ferramenta para estimativa de custos de construção civil, 
    baseada nos insumos e referências oficiais do <strong>SINAPI (Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil)</strong>.
    <div>
        <strong>A plataforma permite:</strong>
        <br>
        <ul>
            <li> Realizar orçamentos detalhados por categoria de infraestrutura </li>
            <li> Utilizar composições de custos baseadas no SINAPI </li>
            <li> Simular diferentes cenários de construção </li>
            <li> Gerar relatórios consolidados de custos </li>
        </ul>
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '<div class="sub-header">📍 Selecione seu Estado</div>', unsafe_allow_html=True
    )

    estados_brasil = [
        "SP", "RJ", "MG", "RS", "PR", "SC", "BA", "DF", "GO", "ES", "PE", "CE", 
        "PA", "MA", "MT", "MS", "PB", "AL", "SE", "RN", "RO", "TO", "AC", "AM", "AP", "RR", "PI"
    ]

    estado_selecionado = st.selectbox(
        "Escolha o estado para usar os insumos SINAPI específicos:",
        options=estados_brasil,
        index=0,
        key="input_estado",
    )

    st.markdown(
        f"""
    <div class="info-box">
    <strong>Estado selecionado:</strong> {estado_selecionado}
    <br>
    <small>Os custos serão calculados usando os insumos do SINAPI para este estado.</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


col3, col4 = st.columns(2)

with col3:
    st.markdown(
        '<div class="sub-header">🚀 Como Funciona?</div>', unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="info-box">
    <div><span class="step-number">1</span><strong>Selecione seu Estado:</strong> Escolha a localização para usar os insumos específicos da região</div>
    <br>
    <div><span class="step-number">2</span><strong>Navegue pelas Categorias:</strong> Acesse as páginas específicas para cada tipo de infraestrutura</div>
    <br>
    <div><span class="step-number">3</span><strong>Preencha os Dados:</strong> Insira as quantidades e parâmetros necessários para cada item</div>
    <br>
    <div><span class="step-number">4</span><strong>Consulte Resultados:</strong> Visualize os custos calculados na página de resultados</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        '<div class="sub-header">ℹ️ Informações Úteis</div>', unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="feature-card">
    <strong>📅 Atualização dos Dados:</strong>
    <br>Os insumos são atualizados mensalmente conforme publicação oficial do SINAPI.
    <br>
    Base de preços: Agosto/2025.
    
    <br><br>
    
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "SINAPI+ - Ferramenta de Orçamento | "
    "Desenvolvido para profissionais da construção civil"
    "</div>",
    unsafe_allow_html=True,
)