import importlib
import sys
from unittest.mock import Mock, patch

import pytest
import requests


def criar_resposta(status_code=200, items=None, total_pages=1):
    resposta = Mock()
    resposta.status_code = status_code
    resposta.json.return_value = {
        "total_pages": total_pages,
        "items": items or [],
    }
    return resposta


@pytest.fixture(scope="module")
def modulo_extracao():
    """Importa o módulo sem permitir chamadas reais à API."""
    resposta_vazia = criar_resposta()
    with patch("requests.get", return_value=resposta_vazia):
        sys.modules.pop("etl.extracao_api", None)
        return importlib.import_module("etl.extracao_api")


def test_paginacao_usa_total_pages(modulo_extracao):
    respostas = [
        criar_resposta(total_pages=3),
        criar_resposta(items=[{"id": 1}], total_pages=3),
        criar_resposta(items=[{"id": 2}], total_pages=3),
        criar_resposta(items=[{"id": 3}], total_pages=3),
    ]

    with patch.object(modulo_extracao.requests, "get", side_effect=respostas) as get:
        modulo_extracao.extrair_dados("/clientes")

    paginas = [chamada.kwargs["params"]["page"] for chamada in get.call_args_list]
    assert paginas == [1, 1, 2, 3]


def test_reune_registros_de_todas_as_paginas(modulo_extracao):
    respostas = [
        criar_resposta(total_pages=2),
        criar_resposta(items=[{"id": 10}, {"id": 11}], total_pages=2),
        criar_resposta(items=[{"id": 12}], total_pages=2),
    ]

    with patch.object(modulo_extracao.requests, "get", side_effect=respostas):
        registros = modulo_extracao.extrair_dados("/pedidos")

    assert registros == [{"id": 10}, {"id": 11}, {"id": 12}]


def test_trata_falha_de_conexao_na_primeira_requisicao(modulo_extracao):
    with patch.object(
        modulo_extracao.requests,
        "get",
        side_effect=requests.exceptions.ConnectionError("API indisponível"),
    ):
        registros = modulo_extracao.extrair_dados("/clientes")

    assert registros == []


def test_trata_erro_http_404_durante_a_paginacao(modulo_extracao):
    respostas = [
        criar_resposta(total_pages=2),
        criar_resposta(items=[{"id": 20}], total_pages=2),
        criar_resposta(status_code=404, total_pages=2),
    ]

    with patch.object(modulo_extracao.requests, "get", side_effect=respostas):
        registros = modulo_extracao.extrair_dados("/pedidos")

    assert registros == [{"id": 20}]
