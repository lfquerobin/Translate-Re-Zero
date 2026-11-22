# Contexto e prioridades

Estamos traduzindo Re:Zero para o português brasileiro. Preservar sentido, ambiguidades intencionais, voz, ritmo e impacto emocional, buscando naturalidade sem acrescentar interpretações nem omitir nuances. Fidelidade não exige copiar a sintaxe inglesa: quando uma solução soar estranha, reformular e comparar de novo com a fonte.

## Sequência de trabalho

1. Consultar os capítulos anteriores, `GLOSSÁRIO.md`, `VOZES.md`, `ACOMPANHAMENTO.md` e `PENDÊNCIAS.md`. As traduções anteriores são referências, não justificativas para repetir erros.
2. Localizar o japonês do mesmo capítulo e da mesma versão da obra e a fonte intermediária, quando houver. Ler os textos-fonte inteiros antes de traduzir, compreendendo acontecimentos, relações, tom e intenção dos diálogos.
3. Traduzir ou revisar seguindo as regras abaixo. Investigar dificuldades de compreensão; preservar indefinições intencionais.
4. Fazer as duas etapas de revisão descritas adiante, atualizar o glossário, as referências de voz quando pertinente e o acompanhamento.
5. Salvar a versão integral no caminho correto, executar `python tools/verificar_projeto.py --atualizar-indices` e conferir os arquivos gerados antes da entrega. O verificador não substitui a leitura nem autoriza marcar uma revisão como concluída.

## Fontes e verificação

Sempre ler e consultar o original japonês e validar o capítulo inteiro contra ele, mesmo quando a tradução partir do inglês e não houver dúvidas aparentes. Comparar também com a fonte intermediária disponível. Se o japonês não puder ser localizado ou acessado, informar a limitação, as partes não validadas e manter a etapa pendente no acompanhamento; não declarar cotejo concluído.

Não presumir que escolhas da tradução intermediária reproduzem diretamente o japonês. Em caso de ambiguidade, inconsistência, perda de nuance ou resultado pouco natural, aprofundar a pesquisa no original, no contexto da obra e, conforme necessário, em fontes sobre expressões, referências culturais e trocadilhos. Não resolver incertezas inventando interpretações.

Consultar as referências de `LINKS.md` com os seguintes limites:

Em cada nova tradução, verificar se o Manual da WCT online mudou em relação à cópia local mais recente de `Referências/WCT`, seguindo as orientações do README dessa pasta. Comparar o conteúdo textual, desconsiderando mudanças apenas de espaços, scripts, estilos e elementos automáticos do Google Docs. Se houver mudanças de conteúdo, guardar nova captura datada em HTML e texto, preservar as anteriores e atualizar os links e o registro da captura. Consultar as mudanças pertinentes ao capítulo sem aplicar automaticamente convenções inglesas ou informações de outra versão. Se o acesso falhar, usar a última cópia local e informar sua data e a limitação da conferência. Fazer essa verificação durante o trabalho de tradução, sem criar tarefa agendada ou automação recorrente.

- O Manual de Estilo da WCT auxilia na terminologia, nos tratamentos e nas particularidades de fala. Distinguir observações sobre o japonês de convenções editoriais inglesas; conferir a aplicação à versão e ao capítulo em trabalho, sem importar regionalismos, formatação ou revelações de arcos posteriores.
- O índice de erros da light novel inglesa serve para localizar possíveis problemas. Um erro da light novel não comprova erro da web novel: conferir o japonês e a versão correspondente antes de aplicar uma correção.

Quando o japonês confirmar um erro no inglês, corrigir o português e registrar brevemente a decisão fora do capítulo, no glossário ou na entrega. Distinguir erro confirmado, adaptação deliberada e interpretação incerta. Não criar relatórios avulsos sem solicitação; os registros permanentes definidos neste projeto fazem parte do acompanhamento autorizado.

## Fidelidade, naturalidade e voz

Preservar pausas, repetições intencionais, hesitações, interrupções, intensidade e grau de formalidade. Não acrescentar gírias, regionalismos, palavrões ou linguagem arcaica sem apoio no original. Considerar o interlocutor e a situação ao escolher pronomes, tratamentos, vocabulário, sarcasmo e intimidade.

Os exemplos de `VOZES.md` são referências contextualizadas, não fórmulas para todas as falas nem provas isoladas de quem fala. Distinguir exemplos conferidos no capítulo de observações auxiliares do manual.

Selecionar as referências de voz e tratamento pertinentes à cena, ao interlocutor e ao que os personagens e o leitor sabem naquele ponto. Para uma retomada ou transição, reler o final do trecho anterior e recuperar apenas os acontecimentos e as decisões terminológicas necessários para a continuidade.

Verificar sujeitos, ações, referentes dos pronomes e relações de causa, consequência, contraste, condição e sequência temporal. Esclarecer referentes apenas quando a fonte permitir. Não explicitar relações, intenções ou informações que ela deixa indefinidas, sobretudo se isso eliminar uma interpretação ou antecipar uma revelação.

Avaliar frases e transições junto das anteriores e seguintes. Evitar literalismos ou soluções burocráticas que destoem do registro, como “a saber” numa passagem informal, sem transformar exemplos em lista de palavras proibidas nem simplificar indiscriminadamente a prosa. Manter construções formais próprias da voz. Nas frases interrompidas, conferir a ligação natural com a continuação ou a fala seguinte, preservando a interrupção.

Corrigir repetições acidentais introduzidas pela tradução; não trocar palavras por sinônimos apenas para variar quando a repetição tiver função narrativa.

## Diálogos e marcações

Nas falas de diálogo em parágrafo próprio, usar `Nome: [fala]`. Substituir apenas os delimitadores externos; preservar citações internas, travessões, pausas e interrupções. Não duplicar a marcação com aspas externas dentro dos colchetes.

**Exceção para fala incorporada à narração:** quando o próprio trecho identifica claramente o falante, manter a fala na mesma posição com os delimitadores originais, sem inserir outro rótulo. Exemplos: `enquanto prosseguia: “Se é assim,”` e `Rom perguntou a Felt, “E a senha?”`. Essa exceção evita construções como `prosseguia: Subaru: [...]`. Não deslocar a fala, criar parágrafo, reescrever a narrativa ou converter uma citação em diálogo independente apenas para aplicar um rótulo. Se uma fala incorporada continuar ambígua, preservar a construção e registrar a pendência fora do capítulo.

Validar as atribuições pela narração, ações, referentes, conversa completa e japonês. Pronomes e peculiaridades de fala são pistas auxiliares, não prova isolada. Não presumir alternância automática: falas consecutivas podem pertencer à mesma pessoa.

Usar somente a identidade que o texto permite reconhecer naquele ponto, respeitando o ponto de vista da cena. Não antecipar nomes verdadeiros, disfarces ou revelações. Se houver apenas uma descrição, usar um rótulo compatível, como `Garota`; preservar nomes provisórios, como `Satella`, enquanto forem o conhecimento disponível. Para falas simultâneas, identificar os participantes confirmados, como `Rom e Felt: [fala]`.

Manter `???: [fala]` tanto para identidade ainda oculta na narrativa quanto para atribuição sem evidência suficiente após a pesquisa. Distinguir os casos no registro interno de `projeto.json`, que gera `PENDÊNCIAS.md`: `anonimato_narrativo` ou `atribuicao_pendente`. Não colocar essa classificação nem hipóteses dentro do capítulo. Registrar cada ocorrência com trecho, motivo e referência; nas pendências, acrescentar as interpretações possíveis e apresentar a dúvida relevante na entrega. Anonimato intencional não bloqueia a conclusão da revisão; dúvida editorial permanece aberta até haver evidência para resolvê-la.

Não confundir pensamento, citação, exemplo ou narração entre aspas com fala pronunciada. Fora das exceções adotadas para identificação de falantes, preservar as marcações da fonte enviada pelo usuário. Evitar caracteres soltos e duplicações como “— ―”. Corrigir aspas invertidas ou duplicações da fonte somente quando comprovadamente acidentais, após conferir contexto e japonês quando necessário. Uma marcação incomum não é automaticamente erro; se houver dúvida, preservá-la e registrá-la separadamente.

## Glossário e registros do projeto

Em toda tradução ou revisão, consultar e atualizar `GLOSSÁRIO.md` antes da entrega. Registrar o que importa para os próximos capítulos: termo original, tradução adotada, japonês efetivamente conferido, contexto, versão, capítulo ou seção e link da verificação. Incluir tratamentos, peculiaridades de voz e decisões relevantes quando pertinente; não preencher dados por suposição nem duplicar entradas.

Corrigir entradas quando a consulta revelar erro, inconsistência, lacuna ou informação nova. Ao mudar uma escolha, explicar brevemente o motivo e a fonte, indicando capítulos anteriores afetados. Separar decisões confirmadas, adaptações deliberadas, dúvidas abertas e referências auxiliares ainda não verificadas. `VOZES.md` reúne exemplos de voz; o glossário pode remetê-los, sem copiar todo o conteúdo.

`projeto.json` é o registro de acompanhamento: caminhos, fontes japonesa e inglesa, versão, etapas de revisão, ocorrências anônimas e variantes terminológicas a verificar. `ACOMPANHAMENTO.md` e `PENDÊNCIAS.md` são vistas geradas desse registro; atualizar os dados e regenerar as vistas, sem manter listas divergentes. Os símbolos nos nomes dos capítulos não substituem as etapas registradas. Não marcar uma etapa como concluída apenas porque um símbolo mudou, o arquivo foi formatado ou o verificador passou.

Registrar somente revisões efetivamente realizadas, com data e escopo. Ao incorporar trabalho anterior, indicar que se trata do registro histórico existente. Alterações de conteúdo exigem rever os trechos afetados contra as fontes; mudanças extensas exigem nova revisão integral. Após mudanças de apresentação, registrar se a releitura contínua final ainda está pendente. Atualizar caminhos no registro quando houver renomeação autorizada, preservando escolhas do usuário.

## Cabeçalho, arquivo e notas

Ao entregar uma tradução, apresentar antes do corpo o cabeçalho completo, com cada linha inteira em negrito:

**Título: <título>**
**Link: <link da fonte>**
**Data de publicação: <data de publicação na fonte>**
**Traduzido por: <crédito de tradução informado pela fonte, indicando o idioma quando necessário>**

Não inventar título ou link: solicitar o que faltar. Para data ou crédito ausentes na fonte, indicar que não foram informados. Não confundir autor da obra ou responsável pela postagem com tradutor. A data do japonês não substitui a da tradução intermediária apresentada no cabeçalho.

Sempre salvar o texto integral revisado, com cabeçalho, dentro de `C:\Users\luizh\OneDrive\Documentos\Traduções\ReZero`, na pasta do arco/fase e no formato existente; entregar no chat não substitui salvar. O nome do arquivo deve conservar o título do cabeçalho, suas aspas internas e externas e sua pontuação. No Windows, substituir aspas retas duplas por aspas tipográficas de abertura e fechamento apenas no nome do arquivo, preservando a hierarquia; essa exceção não vale para o corpo.

Toda nova tradução deve ser salva com **✖️ no início do nome do arquivo**, antes da numeração, seguindo o modelo `✖️ 015. Arco 1, Capítulo 14 – “Na quarta vez é que dá certo”.md`. O símbolo é um prefixo de organização do arquivo, não parte do título da obra no cabeçalho. Não trocar automaticamente por ✔️ ao concluir a tradução ou as revisões; manter ✖️ até orientação do usuário. As etapas efetivamente realizadas continuam registradas separadamente em `projeto.json`.

Não inserir novas notas ou explicações na narrativa sem solicitação. Preservar e traduzir as notas que já pertencem à fonte, distinguindo-as de observações novas da revisão. Para dúvida relevante não resolvida, registrar e apresentar fora do capítulo o original e as interpretações possíveis, sem tratar hipótese como certeza.

## Revisão e entrega

1. **Fidelidade:** comparar integralmente com japonês e fonte intermediária, verificando omissões, acréscimos, negações, sujeitos, referentes, sequência de ações, relações lógicas, intensidade, falantes e marcações. Conferir todos os parágrafos e separadores presentes e em ordem, sem duplicações nem truncamentos; não exigir correspondência mecânica de um parágrafo por idioma.
2. **Naturalidade:** ler o português continuamente, sem consultar a fonte, verificando clareza, ritmo, transições, repetições e coerência de voz. Depois de reformular um trecho, comparar novamente com a fonte para confirmar fidelidade.

No cotejo, usar começo e fim de cenas, separadores e notas da fonte como pontos de referência para conferir a cobertura e a ordem entre japonês, inglês e português. Conferir também o alcance de negações e quantificadores, o grau de certeza, a maneira como uma ação é executada e as fórmulas recorrentes que têm função na narrativa. Diferenças de contagem de parágrafos servem para localizar trechos a verificar.

Para um trecho suspeito, localizar a redação vigente e a evidência na fonte ou na cena. Antes de editar, confirmar se há perda de sentido, problema de leitura ou desvio de voz e distinguir esses casos de uma alternativa igualmente defensável. Preservar a redação quando a evidência não justificar a troca e registrar dúvidas relevantes no acompanhamento existente. Ao corrigir, alterar apenas o trecho necessário e conferir a passagem completa com a fonte. Em revisões em lote, confirmar que o trecho a editar ainda corresponde ao que foi analisado.

Se houver mudança confirmada no texto de uma fonte ou em uma decisão do glossário, identificar os capítulos e as passagens afetadas e conferir o impacto no contexto. Em monitoramentos por comparação textual, considerar o corpo do capítulo e as notas da fonte, desconsiderando mudanças de navegação ou estilo da página. Indícios de alteração ajudam a localizar trechos para revisão. Registrar nova validação somente depois do cotejo efetivo.

Na conferência final, verificar especialmente gritos, falas curtas, interrupções e mudanças de falante; confirmar versão salva, cabeçalho, título/nome do arquivo e registros atualizados. Executar o verificador, avaliar seus alertas pelo contexto e corrigir erros objetivos. Ele confere estrutura e regras explícitas, não comprova qualidade, identidade de falantes ou integridade semântica da tradução. Informar na entrega as alterações principais, pendências relevantes e limitações de validação.


## Sincronização com o GitHub

Por solicitação do usuário, ao concluir qualquer alteração neste projeto, fazer commit de todas as alterações pendentes e enviá-las ao GitHub (remoto `origin`), sem pedir nova confirmação. Conferir o estado do Git após o envio. Se o envio falhar, preservar o trabalho local e informar a limitação; nunca declarar sincronização concluída sem confirmação.
