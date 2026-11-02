# Tradução de Re:Zero para português brasileiro

As orientações editoriais estão em [AGENTS.md](AGENTS.md). O projeto trabalha com a **web novel**; referências de outras versões precisam de correspondência confirmada antes de fundamentar alterações.

## Onde consultar

- [Acompanhamento dos capítulos](ACOMPANHAMENTO.md): fontes japonesa e inglesa, etapas de revisão e trabalho em aberto.
- [Pendências e anonimato](PENDÊNCIAS.md): dúvidas de atribuição e ocorrências de identidade ainda oculta, sem notas adicionais na narrativa.
- [Glossário](GLOSSÁRIO.md): terminologia, decisões e fontes verificadas.
- [Referências de voz](VOZES.md): exemplos contextualizados de seis personagens, conferidos no japonês.
- [Links auxiliares](LINKS.md): índices e manual de estilo, com seus limites de aplicação.

## Conferência automática

Requer Python 3.10 ou superior, apenas com a biblioteca padrão. Executar na pasta do projeto:

```powershell
python tools/verificar_projeto.py
```

O comando confere cabeçalhos, correspondência entre título e arquivo, fonte e data registradas, separadores nas extremidades, colchetes, marcações suspeitas, possíveis rótulos repetidos na narração e as variantes terminológicas explicitamente cadastradas. Também verifica se cada `???` foi classificado e se os índices correspondem ao registro atual.

Os alertas terminológicos são candidatos à revisão, não substituições automáticas. A lista de variantes é deliberadamente explícita e não cobre todos os sinônimos, flexões ou erros possíveis. Consultar a entrada do glossário antes de acrescentar uma variante; uma citação ou um contexto diferente pode justificar a ocorrência.

Para atualizar os índices depois de editar [projeto.json](projeto.json):

```powershell
python tools/verificar_projeto.py --atualizar-indices --estrito
```

A opção de atualização escreve **somente** `ACOMPANHAMENTO.md` e `PENDÊNCIAS.md`. Não altera capítulos, glossário, regras ou estados de revisão. Erros objetivos impedem a geração das vistas. A execução comum apenas lê arquivos.

Códigos de saída: **0** = sem erros; **1** = avisos com `--estrito`; **2** = erro de estrutura, registro ou leitura. Pendências editoriais já registradas são informadas separadamente e não fazem a conferência estrutural falhar. Aprovação do script não confirma atribuições, fidelidade, naturalidade, ausência de omissões ou correspondência entre versões; essas verificações exigem leitura das fontes. Os links são conferidos no registro, sem teste de disponibilidade pela rede.

## Atualizar o acompanhamento

`projeto.json` é a fonte dos dois índices gerados. Cada capítulo registra caminho relativo, fontes, publicação e crédito inglês e quatro etapas: fidelidade, naturalidade, falantes e formato. Usar datas no formato `AAAA-MM-DD`, somente quando a etapa foi realmente executada. Se a fonte não informar uma data de publicação, usar `null` e indicar a ausência no cabeçalho; não inventar uma data para satisfazer o verificador.

- `registrada` identifica revisão histórica documentada; a observação deve explicar a evidência e o escopo. Não representa uma nova revisão feita pelo gerador.
- `pendente` ou `iniciada` mantém explícito o trabalho ainda necessário. `concluida`, `conferida` e `ajustado` descrevem etapas efetivamente realizadas; `com_pendencias` indica falantes ainda em investigação.
- Uma renomeação autorizada exige atualizar o campo `arquivo`. Os símbolos ✔️/✖️ não atualizam as etapas automaticamente.
- Para um novo capítulo, adicionar uma entrada com ID único e fontes conferidas, sem copiar datas de revisão concluída de outro capítulo. Regenerar as vistas após preencher os dados.

Em `ocorrencias_anonimas`, registrar o texto exato de cada fala, sem o rótulo e os colchetes, e classificar como `anonimato_narrativo` ou `atribuicao_pendente`. O primeiro preserva o efeito da cena; o segundo inclui original japonês, candidatos, motivo e próximo passo. Duas falas idênticas no mesmo capítulo precisam de dois registros com IDs diferentes, pois o verificador também confere a quantidade.

Para resolver uma atribuição, registrar `estado: "resolvida"` e uma `resolucao` com a evidência e sua fonte, atualizar a fala e a etapa de falantes e regenerar as vistas. Preservar o registro da decisão. O verificador detecta divergências, mas não decide se uma evidência é suficiente.

## Verificar alterações no próprio verificador

```powershell
python -B -m unittest discover -s tools -p 'test_*.py' -v
```

Os testes usam exemplos artificiais e uma pasta temporária; não modificam os capítulos reais. Cobrem falas simultâneas, citações e falas incorporadas, cabeçalhos, aspas de títulos no Windows, fontes e datas, colchetes, variantes, classificação de `???` e atualização dos índices.
