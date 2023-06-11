from fastapi.responses import JSONResponse

ERRO_CAMPO = JSONResponse(
        status_code=404,
        content={"message": "Erro: Campos não foram corretamente preenchidos"})

ERRO_NAO_ESPERADO = JSONResponse(status_code=900,
                                 content={"message": "Erro não esperado"}
                                )
