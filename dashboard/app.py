from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data" / "gold"

st.set_page_config(
	page_title="Observatorio de Energía y Clima",
	page_icon="⚡",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	[data-testid="stMetricValue"] { color: #0b7285; }
	[data-testid="stMetricValue"] > div {
		font-size: clamp(1rem, 2.4vw, 1.8rem) !important;
		white-space: normal !important;
		overflow: visible !important;
		overflow-wrap: anywhere !important;
		text-overflow: clip !important;
	}
	[data-testid="stMetric"] { min-width: 0 !important; }
	[data-testid="stMetricLabel"] { color: #495057; }
	h1 { color: #073b4c; }
	h2, h3 { color: #0b7285; }
	.insight-card {
		background: #163b4d;
		border-left: 5px solid #ef476f;
		border-radius: 8px;
		color: #f4f7f9;
		margin: 8px 0;
		padding: 12px 16px;
	}
	.chart-note {
		background: #264653;
		border-left: 4px solid #ffd166;
		border-radius: 6px;
		color: #f4f7f9;
		font-size: 0.92rem;
		margin: -4px 0 10px;
		padding: 8px 12px;
	}
	</style>
	""",
	unsafe_allow_html=True,
)


@st.cache_data
def load_gold() -> tuple[pd.DataFrame, pd.DataFrame]:
	market_path = GOLD / "fact_mercado_mensual.parquet"
	sales_path = GOLD / "fact_ventas_mensual.parquet"
	missing = [path.name for path in (market_path, sales_path) if not path.exists()]
	if missing:
		raise FileNotFoundError(", ".join(missing))

	market = pd.read_parquet(market_path)
	sales = pd.read_parquet(sales_path)
	market["mes"] = pd.to_datetime(market["mes"])
	sales["periodo"] = pd.to_datetime(sales["periodo"])
	return market, sales


def format_cop(value: float) -> str:
	return f"${value:,.0f}".replace(",", ".")


def style_chart(chart):
	chart.update_layout(
		template="plotly_dark",
		height=360,
		margin=dict(l=10, r=10, t=18, b=10),
		paper_bgcolor="#102a43",
		plot_bgcolor="#163b4d",
		font=dict(color="#f4f7f9", family="Arial"),
		legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
	)
	chart.update_xaxes(showgrid=False, linecolor="#457b8c", tickfont=dict(color="#d9edf2"))
	chart.update_yaxes(gridcolor="#28586a", zerolinecolor="#457b8c", tickfont=dict(color="#d9edf2"))
	return chart


def build_insights(market_data: pd.DataFrame, sales_data: pd.DataFrame) -> list[str]:
	insights = []

	if len(market_data) >= 2:
		ordered_market = market_data.sort_values("mes")
		first_price = ordered_market["precio_bolsa_promedio"].iloc[0]
		last_price = ordered_market["precio_bolsa_promedio"].iloc[-1]
		price_change = ((last_price - first_price) / first_price * 100) if first_price else 0
		direction = "aumentó" if price_change >= 0 else "disminuyó"
		insights.append(
			f"El precio promedio de bolsa {direction} **{abs(price_change):.1f}%** "
			f"entre {ordered_market['mes'].iloc[0]:%b %Y} y {ordered_market['mes'].iloc[-1]:%b %Y}."
		)

		first_demand = ordered_market["demanda_mensual_total"].iloc[0]
		last_demand = ordered_market["demanda_mensual_total"].iloc[-1]
		demand_change = ((last_demand - first_demand) / first_demand * 100) if first_demand else 0
		demand_direction = "creció" if demand_change >= 0 else "cayó"
		insights.append(
			f"La demanda del sistema {demand_direction} **{abs(demand_change):.1f}%** "
			"entre el primer y el último mes visibles."
		)

	if not market_data.empty:
		climate_summary = (
			market_data.groupby("fenomeno_climatologico", as_index=False)["precio_bolsa_promedio"]
			.mean()
			.sort_values("precio_bolsa_promedio", ascending=False)
		)
		if not climate_summary.empty:
			most_expensive = climate_summary.iloc[0]
			insights.append(
				f"El fenómeno asociado al mayor precio promedio es **{most_expensive['fenomeno_climatologico']}**, "
				f"con {format_cop(most_expensive['precio_bolsa_promedio'])} por kWh."
			)

	if not sales_data.empty:
		sales_summary = sales_data.groupby("tipo_compra", as_index=False)["energia_kwh"].sum()
		leading_sale = sales_summary.sort_values("energia_kwh", ascending=False).iloc[0]
		share = leading_sale["energia_kwh"] / sales_summary["energia_kwh"].sum() * 100
		insights.append(
			f"La modalidad **{leading_sale['tipo_compra']}** concentra la mayor energía vendida, "
			f"con una participación del **{share:.1f}%** en el periodo filtrado."
		)

	return insights


st.title("Observatorio de Energía y Clima")
st.caption("Mercado eléctrico, ventas y señales climáticas de la capa Oro")

try:
	market, sales = load_gold()
except FileNotFoundError as error:
	st.error("Todavía no existen los archivos de la capa Oro.")
	st.code("python -m src.transformar\npython -m src.exportar_oro")
	st.info(f"Archivos faltantes: {error}")
	st.stop()

min_date = min(market["mes"].min(), sales["periodo"].min()).date()
max_date = max(market["mes"].max(), sales["periodo"].max()).date()

with st.sidebar:
	st.header("Filtros")
	selected_dates = st.date_input(
		"Periodo",
		value=(min_date, max_date),
		min_value=min_date,
		max_value=max_date,
	)
	phenomena = sorted(market["fenomeno_climatologico"].dropna().unique())
	selected_phenomena = st.multiselect(
		"Fenómeno climático",
		options=phenomena,
		default=phenomena,
	)
	purchase_types = sorted(sales["tipo_compra"].dropna().unique())
	selected_purchase_types = st.multiselect(
		"Tipo de compra",
		options=purchase_types,
		default=purchase_types,
	)

if len(selected_dates) == 2:
	start_date, end_date = pd.to_datetime(selected_dates).date
else:
	start_date = end_date = selected_dates[0]

market_filtered = market[
	market["mes"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))
	& market["fenomeno_climatologico"].isin(selected_phenomena)
].copy()
sales_filtered = sales[
	sales["periodo"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))
	& sales["tipo_compra"].isin(selected_purchase_types)
].copy()

avg_price = market_filtered["precio_bolsa_promedio"].mean()
total_demand = market_filtered["demanda_mensual_total"].sum()
total_energy = sales_filtered["energia_kwh"].sum()
total_value = sales_filtered["valor_cop"].sum()

metric_columns = st.columns(4)
metric_columns[0].metric("Precio bolsa promedio", format_cop(avg_price) if pd.notna(avg_price) else "Sin datos")
metric_columns[1].metric("Demanda acumulada", f"{total_demand / 1_000_000:,.2f} GWh")
metric_columns[2].metric("Energía vendida", f"{total_energy / 1_000_000:,.2f} GWh")
metric_columns[3].metric("Valor de ventas", format_cop(total_value))

st.divider()

st.subheader("Lectura automática")
insights = build_insights(market_filtered, sales_filtered)
if insights:
	for insight in insights:
		st.markdown(f'<div class="insight-card">{insight.replace("**", "")}</div>', unsafe_allow_html=True)
else:
	st.info("Selecciona un periodo y al menos una categoría para generar una lectura automática.")

market_left, market_right = st.columns(2)
with market_left:
	st.subheader("Precio promedio de bolsa")
	st.plotly_chart(
		style_chart(px.line(
			market_filtered,
			x="mes",
			y="precio_bolsa_promedio",
			markers=True,
			color_discrete_sequence=["#ef476f"],
			labels={"mes": "Mes", "precio_bolsa_promedio": "COP/kWh"},
		)),
		use_container_width=True,
	)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> evolución del precio promedio del mercado en cada mes seleccionado.</div>', unsafe_allow_html=True)
with market_right:
	st.subheader("Demanda mensual del sistema")
	demand_chart = px.area(
		market_filtered,
		x="mes",
		y="demanda_mensual_total",
		color_discrete_sequence=["#118ab2"],
		labels={"mes": "Mes", "demanda_mensual_total": "kWh"},
	)
	style_chart(demand_chart)
	st.plotly_chart(demand_chart, use_container_width=True)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> meses de mayor consumo y tendencia general de la demanda del sistema.</div>', unsafe_allow_html=True)

climate_left, climate_right = st.columns(2)
with climate_left:
	st.subheader("Precio por fenómeno climático")
	climate_chart = px.box(
		market_filtered,
		x="fenomeno_climatologico",
		y="precio_bolsa_promedio",
		color="fenomeno_climatologico",
		color_discrete_sequence=["#06d6a0", "#ffd166", "#ef476f", "#118ab2"],
		labels={"fenomeno_climatologico": "Fenómeno", "precio_bolsa_promedio": "COP/kWh"},
	)
	climate_chart.update_layout(showlegend=False)
	style_chart(climate_chart)
	st.plotly_chart(climate_chart, use_container_width=True)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> compara los precios entre fenómenos; la línea central representa la mediana.</div>', unsafe_allow_html=True)
with climate_right:
	st.subheader("Mercado y clima en el tiempo")
	climate_line = px.scatter(
		market_filtered,
		x="mes",
		y="precio_bolsa_promedio",
		color="fenomeno_climatologico",
		size="demanda_mensual_total",
		color_discrete_sequence=["#06d6a0", "#ffd166", "#ef476f", "#118ab2"],
		labels={"mes": "Mes", "precio_bolsa_promedio": "COP/kWh", "fenomeno_climatologico": "Fenómeno"},
	)
	style_chart(climate_line)
	st.plotly_chart(climate_line, use_container_width=True)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> cada punto es un mes; su tamaño representa demanda y su color identifica el fenómeno.</div>', unsafe_allow_html=True)

sales_left, sales_right = st.columns(2)
with sales_left:
	st.subheader("Energía vendida por modalidad")
	energy_chart = px.bar(
		sales_filtered.groupby(["periodo", "tipo_compra"], as_index=False)["energia_kwh"].sum(),
		x="periodo",
		y="energia_kwh",
		color="tipo_compra",
		barmode="group",
		color_discrete_sequence=["#073b4c", "#06d6a0"],
		labels={"periodo": "Mes", "energia_kwh": "kWh", "tipo_compra": "Modalidad"},
	)
	style_chart(energy_chart)
	st.plotly_chart(energy_chart, use_container_width=True)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> energía vendida por modalidad y modalidad líder en cada mes.</div>', unsafe_allow_html=True)
with sales_right:
	st.subheader("Valor mensual de las ventas")
	value_chart = px.bar(
		sales_filtered.groupby(["periodo", "tipo_compra"], as_index=False)["valor_cop"].sum(),
		x="periodo",
		y="valor_cop",
		color="tipo_compra",
		barmode="stack",
		color_discrete_sequence=["#ef476f", "#118ab2"],
		labels={"periodo": "Mes", "valor_cop": "COP", "tipo_compra": "Modalidad"},
	)
	style_chart(value_chart)
	st.plotly_chart(value_chart, use_container_width=True)
	st.markdown('<div class="chart-note"><strong>Qué muestra:</strong> aporte de Bolsa y Contrato al valor comercial de cada mes.</div>', unsafe_allow_html=True)
