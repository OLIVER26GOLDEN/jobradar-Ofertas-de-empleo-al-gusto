import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database import SessionLocal
from app.models import Oferta
from components.filters import render_offer_filters
from components.metrics import render_offer_metrics
from components.tables import render_offers_table


st.set_page_config(
    page_title="jobradar Dashboard",
    layout="wide",
)


def load_offers() -> pd.DataFrame:
    """Carga las ofertas guardadas en la base de datos configurada por la API."""
    db = SessionLocal()
    try:
        offers = db.query(Oferta).order_by(Oferta.creado_en.desc()).all()
        rows = [
            {
                "id": offer.id,
                "titulo": offer.titulo,
                "empresa": offer.empresa,
                "ubicacion": offer.ubicacion,
                "modalidad": offer.modalidad,
                "salario": offer.salario,
                "descripcion": offer.descripcion,
                "enlace": offer.enlace,
                "fuente": offer.fuente,
                "estado": offer.estado,
                "fecha_publicacion": offer.fecha_publicacion,
                "creado_en": offer.creado_en,
            }
            for offer in offers
        ]
        return pd.DataFrame(rows)
    finally:
        db.close()


def apply_filters(
    offers: pd.DataFrame,
    keyword: str,
    empresa: str,
    ubicacion: str,
) -> pd.DataFrame:
    """Aplica filtros locales usando los nombres reales del modelo Oferta."""
    filtered = offers.copy()

    if keyword:
        keyword_mask = (
            filtered["titulo"].fillna("").str.contains(keyword, case=False, na=False)
            | filtered["descripcion"].fillna("").str.contains(keyword, case=False, na=False)
        )
        filtered = filtered[keyword_mask]

    if empresa != "Todas":
        filtered = filtered[filtered["empresa"] == empresa]

    if ubicacion != "Todas":
        filtered = filtered[filtered["ubicacion"] == ubicacion]

    return filtered


def main() -> None:
    st.title("jobradar")
    st.caption("Dashboard de ofertas guardadas")

    offers = load_offers()

    if offers.empty:
        render_offer_metrics(offers)
        st.info("Todavia no hay ofertas guardadas en la base de datos.")
        return

    keyword, empresa, ubicacion = render_offer_filters(offers)
    filtered_offers = apply_filters(offers, keyword, empresa, ubicacion)

    render_offer_metrics(filtered_offers)
    render_offers_table(filtered_offers)


if __name__ == "__main__":
    main()
