from app.scraper.indeed import fetch_indeed_offers
from app.scraper.infojobs import fetch_infojobs_offers


REQUIRED_OFFER_FIELDS = {"titulo", "empresa", "ubicacion", "enlace", "fuente"}


def assert_valid_offer_structure(offers):
    assert isinstance(offers, list)
    assert offers

    offer = offers[0]
    assert REQUIRED_OFFER_FIELDS.issubset(offer.keys())

    for field in REQUIRED_OFFER_FIELDS:
        assert isinstance(offer[field], str)
        assert offer[field]


def test_infojobs_devuelve_estructura_valida_sin_llamada_real(monkeypatch):
    monkeypatch.delenv("INFOJOBS_CLIENT_ID", raising=False)
    monkeypatch.delenv("INFOJOBS_CLIENT_SECRET", raising=False)

    offers = fetch_infojobs_offers(query="python", limit=2)

    assert_valid_offer_structure(offers)
    assert offers[0]["fuente"] == "InfoJobs"
    assert len(offers) <= 2


def test_indeed_devuelve_estructura_valida_con_mock(monkeypatch):
    class FakeResponse:
        status_code = 403
        text = ""

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.scraper.indeed.requests.get", fake_get)

    offers = fetch_indeed_offers(query="python", limit=2)

    assert_valid_offer_structure(offers)
    assert offers[0]["fuente"] == "Indeed"
    assert len(offers) <= 2
