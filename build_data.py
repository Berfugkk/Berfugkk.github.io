import json
import re
import unicodedata
from pathlib import Path

# Curated first edition: fewer entries than the previous synthetic catalog,
# but each entry is distinct and intentionally varied in grammar and meaning.
CATS = {
"Sentimentos": [
("saudade","substantivo feminino","sentimento de falta que permanece ligado a alguém, algum lugar, tempo ou possibilidade ausente","surge quando um detalhe presente devolve a sensação de algo que não está mais aqui"),
("nostalgia","substantivo feminino","afeição melancólica por um período passado, geralmente lembrado com vontade de retornar","uma música, fotografia ou objeto antigo torna um período passado emocionalmente próximo"),
("melancolia","substantivo feminino","tristeza de tonalidade contemplativa, sem depender de um motivo imediato e intenso","você percebe uma tristeza baixa e persistente que não pede necessariamente uma solução"),
("ternura","substantivo feminino","afeto delicado diante de alguém ou de algo percebido como querido, frágil ou digno de cuidado","um gesto pequeno desperta vontade de proteger, acolher ou tratar alguém com delicadeza"),
("afeição","substantivo feminino","sentimento de apreço e vínculo que faz uma pessoa importar de maneira pessoal e continuada","você procura a presença de alguém sem precisar de entusiasmo ou paixão para explicar por quê"),
("encanto","substantivo masculino","atração prazerosa produzida por algo que agrada e prende a atenção","uma pessoa, obra ou situação continua agradável mesmo depois de a surpresa inicial passar"),
("fascínio","substantivo masculino","atração intensa que mantém a atenção voltada para algo ou alguém difícil de ignorar","você continua observando ou pensando em alguma coisa mesmo sem ter decidido fazê-lo"),
("admiração","substantivo feminino","reconhecimento positivo das qualidades, capacidades ou da postura de alguém","você nota uma qualidade no outro e passa a considerá-la valiosa por si mesma"),
("gratidão","substantivo feminino","reconhecimento de um benefício recebido e do valor que ele teve para nós","você se dá conta de que algo que outra pessoa fez alterou positivamente sua experiência"),
("esperança","substantivo feminino","expectativa de que um resultado desejado ainda possa acontecer","mesmo sem garantia, você continua considerando possível um desfecho favorável"),
("apreensão","substantivo feminino","estado de expectativa acompanhada da possibilidade percebida de algo desagradável","uma situação futura ainda não aconteceu, mas você já se prepara emocionalmente para que dê errado"),
("insegurança","substantivo feminino","sensação de não confiar plenamente na própria capacidade, posição ou segurança diante de uma situação","você revisa repetidamente o que fez porque teme ter deixado algo errado ou insuficiente"),
("confiança","substantivo feminino","expectativa de que alguém, algo ou nós mesmos apresentaremos consistência suficiente para agir com segurança","você consegue agir sem precisar verificar a mesma coisa o tempo todo"),
("solidão","substantivo feminino","experiência subjetiva de falta de conexão significativa, que pode existir mesmo na presença de outras pessoas","há gente por perto, mas pouco do que realmente importa parece compartilhado"),
("curiosidade","substantivo feminino","impulso de descobrir, compreender ou observar algo ainda parcialmente desconhecido","uma pergunta permanece aberta e você sente vontade de investigar a resposta"),
("perplexidade","substantivo feminino","estado de dúvida intensa produzido por algo difícil de interpretar ou encaixar","as explicações disponíveis parecem insuficientes e você fica sem saber qual leitura adotar"),
("serenidade","substantivo feminino","estado de calma estável que permite responder sem grande turbulência emocional","uma notícia inesperada chega, mas você consegue recebê-la sem perder o centro"),
("quietude","substantivo feminino","estado de pouca agitação física, emocional ou mental","o ritmo ao redor diminui e sua atenção passa a notar coisas pequenas que antes desapareciam no ruído"),
("anseio","substantivo masculino","desejo intenso, geralmente orientado para algo ainda distante, incerto ou ausente","você sente uma vontade contínua de alcançar uma pessoa, situação ou mudança específica"),
("expectativa","substantivo feminino","antecipação de um acontecimento futuro e das características que esperamos que ele tenha","antes do encontro ou resultado, você já imagina como deveria ser"),
("alívio","substantivo masculino","diminuição perceptível de tensão, medo, dor ou preocupação depois que uma ameaça perde força","uma possibilidade temida deixa de existir e seu corpo parece relaxar junto"),
("frustração","substantivo feminino","reação ao perceber que uma intenção, expectativa ou tentativa encontrou um obstáculo ou não produziu o resultado esperado","você queria chegar a algum ponto e algo interrompeu o caminho ou entregou menos do que prometia"),
("ressentimento","substantivo masculino","mágoa que permanece ativa e volta a influenciar a forma como lembramos de uma ofensa","o episódio terminou, mas situações novas ainda despertam a sensação de injustiça daquela antiga experiência"),
("compaixão","substantivo feminino","sensibilidade diante do sofrimento de outra pessoa acompanhada de disposição para tratá-la com cuidado","você percebe a dificuldade alheia e sua primeira reação é reduzir o peso que ela está carregando"),
("constrangimento","substantivo masculino","mal-estar produzido pela sensação de exposição, inadequação ou quebra de uma expectativa social","depois de um comentário ou situação inesperada, você sente vontade de desaparecer ou mudar de assunto"),
],
"Amor & atração": [
("amor","substantivo masculino","vínculo afetivo profundo que atribui valor pessoal a alguém e influencia escolhas, cuidado e presença","a importância de uma pessoa aparece não só no que você sente, mas no modo como age em relação a ela"),
("paixão","substantivo feminino","envolvimento afetivo intenso marcado por desejo, idealização e forte investimento de atenção","a pessoa ocupa espaço desproporcional nos pensamentos e decisões, especialmente no início"),
("atração","substantivo feminino","tendência a sentir interesse ou desejo de aproximação em relação a alguém","você percebe vontade de olhar, conhecer ou permanecer perto daquela pessoa sem precisar racionalizar muito"),
("desejo","substantivo masculino","impulso orientado para alcançar, viver, tocar, possuir ou experimentar algo","uma possibilidade se torna mais atraente e você passa a organizar ações em torno dela"),
("intimidade","substantivo feminino","grau de proximidade em que aspectos pessoais podem ser compartilhados com menor necessidade de proteção","uma conversa deixa de ser apenas social e passa a envolver aquilo que você normalmente preservaria"),
("cumplicidade","substantivo feminino","entendimento compartilhado que permite a duas pessoas reconhecerem um sentido implícito sem explicá-lo por completo","um olhar ou pequena referência basta para que ambos saibam do que se trata"),
("sedução","substantivo feminino","conjunto de gestos, sinais ou atitudes usados para despertar interesse e favorecer aproximação","há intenção de se tornar atraente ou de criar espaço para que o outro queira se aproximar"),
("flerte","substantivo masculino","interação que testa ou sinaliza interesse afetivo ou sexual sem estabelecer ainda um compromisso definido","comentários, olhares e provocações deixam aberta a possibilidade de algo mais"),
("paquera","substantivo feminino","aproximação inicial marcada por interesse romântico e por tentativas de perceber reciprocidade","você presta atenção nas respostas do outro enquanto cria oportunidades de conversa e encontro"),
("crush","substantivo masculino","termo contemporâneo para pessoa por quem alguém sente uma queda, admiração ou atração, muitas vezes ainda pouco assumida","o interesse existe antes de haver uma relação definida e costuma aparecer em pensamentos recorrentes"),
("química","substantivo feminino","termo informal para a sensação de compatibilidade e facilidade de conexão entre duas pessoas","a conversa flui e pequenos sinais parecem se encaixar sem esforço excessivo"),
("afinidade","substantivo feminino","semelhança ou compatibilidade de interesses, valores, sensibilidades ou maneiras de perceber o mundo","vocês descobrem que várias coisas importantes fazem sentido para ambos"),
("vulnerabilidade afetiva","locução nominal","condição de expor necessidades ou sentimentos a alguém cujo retorno não está totalmente sob nosso controle","você revela algo importante e aceita que a resposta do outro pode não ser a que gostaria"),
("reciprocidade","substantivo feminino","correspondência entre esforços, afetos ou cuidados de duas ou mais pessoas","o interesse não depende de uma única pessoa iniciar, manter e reparar tudo sozinha"),
("fidelidade","substantivo feminino","manutenção voluntária de um compromisso, acordo ou vínculo sem agir contra aquilo que foi combinado","uma escolha externa é recusada porque preservar o vínculo tem prioridade para você"),
("ciúme","substantivo masculino","reação de ameaça percebida diante da possibilidade de perder exclusividade, atenção ou vínculo importante","a aproximação de outra pessoa altera sua sensação de segurança na relação"),
("amor platônico","locução nominal","afeição ou paixão vivida com pouca ou nenhuma concretização recíproca, frequentemente sustentada pela imaginação","a relação desejada existe mais como possibilidade interna do que como vínculo efetivamente construído"),
("amor não correspondido","locução nominal","situação em que uma pessoa sente forte interesse afetivo sem receber resposta equivalente","o sentimento permanece mesmo quando os sinais disponíveis indicam que o outro não o compartilha"),
("intimidade emocional","locução nominal","proximidade baseada na possibilidade de compartilhar experiências internas, medos, dúvidas e necessidades","vocês conseguem falar do que sentem sem transformar toda exposição em defesa ou justificativa"),
("magnetismo","substantivo masculino","poder informal de atração que faz uma pessoa chamar atenção e parecer difícil de ignorar","mesmo sem fazer algo ostensivo, alguém ocupa o ambiente e desperta curiosidade"),
("encantamento","substantivo masculino","estado em que uma pessoa ou experiência parece excepcionalmente atraente e envolve fortemente a atenção","durante algum tempo, pequenas qualidades parecem amplificadas pela impressão geral positiva"),
("apego","substantivo masculino","vínculo que torna emocionalmente relevante conservar uma pessoa, lugar, objeto ou hábito","a possibilidade de perder algo desperta desconforto maior do que seu valor prático explicaria"),
("desapego","substantivo masculino","capacidade de permitir mudança ou perda sem exigir posse ou permanência absoluta","algo continua sendo valioso, mas sua saída deixa de parecer uma ameaça à própria identidade"),
("consentimento","substantivo masculino","concordância livre e consciente com uma ação ou situação, sem coerção e dentro dos limites apresentados","a outra pessoa pode dizer sim ou não de forma real e suas condições são levadas em conta"),
("cuidado","substantivo masculino","atenção prática voltada a preservar bem-estar, segurança ou qualidade de vida de alguém","o afeto se transforma em ações concretas: lembrar, acompanhar, proteger ou facilitar algo"),
],
"Relações humanas": [
("amizade","substantivo feminino","relação baseada em afeição, confiança, convivência e reconhecimento mútuo sem depender de parentesco","vocês mantêm vínculo e consideração mesmo quando não há benefício imediato em continuar próximos"),
("companheirismo","substantivo masculino","disposição para compartilhar tarefas, dificuldades e momentos sem deixar todo o peso para uma só pessoa","a outra pessoa participa do problema em vez de apenas oferecer opinião de fora"),
("camaradagem","substantivo feminino","proximidade informal marcada por espírito de parceria e confiança entre pessoas que convivem","o vínculo aparece na facilidade de cooperar, brincar e pedir ajuda"),
("parentesco","substantivo masculino","relação social ou jurídica estabelecida por vínculos familiares","duas pessoas ocupam posições reconhecidas dentro da mesma estrutura familiar"),
("aliança","substantivo feminino","acordo de cooperação entre pessoas ou grupos que decidem atuar em algum objetivo comum","interesses diferentes não desaparecem, mas existe uma decisão de agir juntos em determinado assunto"),
("cooperação","substantivo feminino","ação coordenada em que diferentes pessoas contribuem para um resultado comum","cada participante oferece algo que aumenta a capacidade do conjunto"),
("rivalidade","substantivo feminino","relação de competição persistente em que o desempenho de uma parte ganha significado pela comparação com outra","uma conquista sua importa também porque altera sua posição diante de alguém que disputa o mesmo espaço"),
("conflito","substantivo masculino","situação de oposição entre interesses, necessidades, valores ou interpretações que não se acomodam facilmente","duas posições parecem incompatíveis e passam a exigir negociação, escolha ou limite"),
("consenso","substantivo masculino","acordo suficientemente amplo obtido depois de considerar diferenças entre as partes","nem todos pensam exatamente igual, mas existe uma decisão que todos aceitam sustentar"),
("divergência","substantivo feminino","diferença de opinião, interpretação, interesse ou direção entre pessoas ou grupos","vocês olham para a mesma situação e chegam a conclusões que não coincidem"),
("negociação","substantivo feminino","processo de ajustar interesses por meio de propostas, concessões e condições explícitas","cada lado identifica o que é essencial, o que pode mudar e o que espera receber"),
("mediação","substantivo feminino","intervenção de uma terceira parte para facilitar comunicação e busca de acordo entre pessoas em conflito","alguém que não está diretamente envolvido ajuda os lados a se ouvirem sem decidir tudo por eles"),
("limite","substantivo masculino","linha física, emocional, temporal ou comportamental que indica até onde uma pessoa aceita determinada ação ou situação","você consegue dizer o que não aceita e qual consequência pretende aplicar se isso continuar"),
("privacidade","substantivo feminino","espaço de controle pessoal sobre informações, conversas, hábitos e momentos que não precisam ser públicos","você escolhe quem pode saber algo sobre sua vida e quando essa informação pode ser compartilhada"),
("confidência","substantivo feminino","informação pessoal entregue a alguém sob expectativa de discrição e confiança","uma pessoa compartilha algo porque espera que aquilo não vire assunto de terceiros"),
("fofoca","substantivo feminino","circulação informal de informações sobre a vida de outras pessoas, geralmente fora da presença delas","uma história privada começa a viajar entre pessoas que não estavam envolvidas diretamente"),
("reputação","substantivo feminino","imagem coletiva construída a partir da repetição de percepções e relatos sobre uma pessoa ou grupo","pessoas formam expectativas sobre alguém antes mesmo de conhecê-lo diretamente"),
("influência","substantivo feminino","capacidade de alterar decisões, percepções ou comportamentos de outras pessoas sem depender necessariamente de autoridade formal","sua presença ou opinião muda o que outros consideravam fazer"),
("coerção","substantivo feminino","uso de ameaça, pressão ou força para reduzir a liberdade real de escolha de outra pessoa","há um aparente consentimento, mas a possibilidade de recusar vem acompanhada de um custo imposto"),
("hospitalidade","substantivo feminino","disposição de receber alguém de modo acolhedor, oferecendo espaço, atenção ou recursos para facilitar sua permanência","um visitante percebe que não precisa conquistar o direito de estar ali a cada minuto"),
("mal-entendido","substantivo masculino","interpretação equivocada de uma fala, ação ou intenção que produz uma situação diferente daquela pretendida","uma frase simples é entendida de um jeito que o autor não imaginava"),
("subtexto","substantivo masculino","sentido implícito que acompanha uma fala ou comportamento sem ser dito diretamente","as palavras parecem neutras, mas o contexto revela outra intenção ou emoção"),
("desculpa","substantivo feminino","reconhecimento expresso de que uma ação causou dano, desconforto ou injustiça, frequentemente acompanhado de responsabilização","em vez de apenas explicar o que aconteceu, você admite qual foi sua participação no problema"),
("reconciliação","substantivo feminino","retomada de vínculo depois de um conflito, geralmente acompanhada de reparação e novos acordos","a relação volta a existir de outro modo depois de o problema ter sido reconhecido"),
("ruptura","substantivo feminino","quebra significativa de continuidade em um vínculo, acordo, rotina ou relação","algo que antes era sustentado deixa de funcionar como base para continuar juntos"),
],
"Mente": [
("pensamento","substantivo masculino","conteúdo mental que representa, avalia, imagina ou relaciona informações","uma ideia, julgamento ou lembrança se organiza internamente antes de virar fala ou ação"),
("ideia","substantivo feminino","representação ou possibilidade mental que pode orientar compreensão, criação ou ação","algo ainda não realizado passa a existir como possibilidade clara na mente"),
("atenção","substantivo feminino","capacidade de selecionar parte dos estímulos e recursos mentais para processá-los com prioridade","entre vários sons e informações, você escolhe uma coisa para acompanhar de fato"),
("concentração","substantivo feminino","manutenção deliberada da atenção sobre uma tarefa, objeto ou problema por determinado período","você reduz distrações e continua retornando ao mesmo trabalho apesar de impulsos concorrentes"),
("distração","substantivo feminino","deslocamento da atenção para algo diferente daquilo que deveria ocupar o foco","uma notificação ou pensamento secundário captura recursos mentais que estavam destinados a outra atividade"),
("imaginação","substantivo feminino","capacidade de formar mentalmente cenas, possibilidades ou combinações que não estão presentes naquele momento","você consegue experimentar uma situação na mente antes de ela existir ou sem que exista de fato"),
("devaneio","substantivo masculino","fluxo de pensamentos ou imagens que se afasta da tarefa imediata e acompanha associações internas","enquanto deveria estar fazendo algo, sua mente constrói uma pequena história e segue por ela"),
("reflexão","substantivo feminino","exame deliberado de uma experiência, ideia ou decisão para compreendê-la melhor","em vez de reagir logo, você volta ao que aconteceu e tenta organizar seus motivos"),
("introspecção","substantivo feminino","observação dos próprios pensamentos, sentimentos, motivos ou estados internos","você direciona a atenção para a própria experiência para perceber como está reagindo"),
("intuição","substantivo feminino","percepção ou julgamento que surge com pouca consciência do caminho lógico que o produziu","você sente que algo faz sentido antes de conseguir explicar claramente por quê"),
("pressentimento","substantivo masculino","expectativa antecipada de que algo pode acontecer, sem evidência suficiente para formular uma conclusão segura","uma situação ainda indefinida produz uma sensação de que algo está para mudar"),
("insight","substantivo masculino","termo usado para descrever uma compreensão que reorganiza repentinamente um problema ou padrão","uma conexão até então obscura parece simples assim que é percebida"),
("epifania","substantivo feminino","compreensão súbita que muda a perspectiva sobre algo que vinha sendo observado de outra maneira","um detalhe aparentemente banal reorganiza o significado de tudo o que veio antes"),
("ruminação","substantivo feminino","repetição mental prolongada de um problema, lembrança ou preocupação sem avanço proporcional na solução","a mesma situação volta à cabeça muitas vezes e cada retorno parece produzir mais tensão do que clareza"),
("viés","substantivo masculino","tendência sistemática que inclina percepção ou julgamento para determinada direção","duas situações semelhantes recebem avaliações diferentes porque algum fator está pesando mais do que deveria"),
("metacognição","substantivo feminino","capacidade de observar e avaliar os próprios processos de pensamento, aprendizagem ou decisão","você não analisa apenas a resposta, mas também o método que sua mente usou para chegar nela"),
("ambivalência","substantivo feminino","coexistência de avaliações, desejos ou sentimentos que apontam para direções diferentes","você quer aceitar e recusar quase pelo mesmo conjunto de razões"),
("dissonância","substantivo feminino","sensação de incompatibilidade entre ideias, valores, decisões ou experiências que deveriam formar um conjunto coerente","o que você acredita e o que acabou de fazer entram em atrito"),
("racionalização","substantivo feminino","construção de uma explicação aparentemente lógica para uma decisão que também envolve motivos menos reconhecidos","depois de agir por impulso, você encontra um argumento que torna a escolha mais aceitável para si"),
("procrastinação","substantivo feminino","adiamento repetido de uma ação relevante, geralmente apesar de a pessoa saber que o atraso terá custo","há tempo e necessidade para fazer algo, mas atividades menos importantes ocupam o lugar"),
("lucidez","substantivo feminino","clareza suficiente para perceber uma situação, seus limites e suas implicações sem distorção deliberada","você consegue sustentar uma verdade desagradável sem precisar inventar uma versão mais confortável"),
("ceticismo","substantivo masculino","postura de suspender aceitação até que existam razões ou evidências consideradas suficientes","uma afirmação parece plausível, mas você prefere examiná-la antes de tratá-la como fato"),
("flexibilidade","substantivo feminino","capacidade de alterar estratégia, interpretação ou plano quando as condições mudam","um caminho deixa de funcionar e você adapta a abordagem sem transformar a mudança em fracasso pessoal"),
("rigidez","substantivo feminino","dificuldade de alterar regras, expectativas ou interpretações mesmo quando o contexto pede adaptação","o plano original continua sendo aplicado apesar de novas informações torná-lo inadequado"),
("curiosidade mórbida","locução nominal","interesse insistente por aspectos chocantes, trágicos ou dolorosos que normalmente provocariam repulsa ou reserva","você se sente atraído a olhar, pesquisar ou saber mais justamente por causa do caráter perturbador do assunto"),
],
"Sensações": [
("arrepio","substantivo masculino","pequena reação corporal marcada pela contração dos pelos e por sensação súbita na pele","frio, medo, música ou uma emoção intensa faz a pele responder antes que você consiga explicar"),
("formigamento","substantivo masculino","sensação de pequenos impulsos ou picadas repetidas em uma região do corpo","uma parte do corpo parece cheia de pequenos sinais elétricos, como se estivesse despertando"),
("entorpecimento","substantivo masculino","redução ou alteração da sensibilidade de uma parte do corpo ou da experiência emocional","um estímulo que normalmente seria nítido parece chegar abafado ou distante"),
("vertigem","substantivo feminino","sensação de movimento ou desequilíbrio em que o corpo ou o ambiente parecem girar","parado ou de olhos abertos, você sente como se a orientação espacial estivesse se deslocando"),
("náusea","substantivo feminino","sensação de mal-estar que pode incluir vontade de vomitar, rejeição ou desconforto gástrico","um cheiro, movimento ou estado corporal produz repulsa física e altera sua vontade de comer"),
("palpitação","substantivo feminino","percepção consciente dos batimentos cardíacos, geralmente mais fortes, rápidos ou irregulares","você nota o coração batendo no peito ou na garganta de um modo que normalmente passa despercebido"),
("ofegância","substantivo feminino","respiração acelerada ou trabalhosa, frequentemente depois de esforço físico ou excitação","falar em frases longas fica difícil porque o corpo ainda está recuperando o ritmo respiratório"),
("calafrio","substantivo masculino","onda repentina de frio ou tremor que percorre o corpo","mesmo sem a temperatura ter mudado muito, o corpo reage com frio intenso e breve"),
("rubor","substantivo masculino","avermelhamento visível da pele, especialmente no rosto, provocado por alterações físicas ou emocionais","vergonha, calor ou excitação torna o rosto perceptivelmente mais vermelho"),
("secura","substantivo feminino","falta de umidade percebida na boca, pele, olhos ou ambiente","a superfície que normalmente parece confortável passa a exigir água, umidade ou lubrificação"),
("ardor","substantivo masculino","sensação de calor intenso ou queimação em determinada região","uma superfície ou contato produz calor desconfortável que parece permanecer depois do estímulo"),
("torpor","substantivo masculino","estado de baixa responsividade física ou mental, com sensação de lentidão e pouca iniciativa","o corpo parece pesado e as reações chegam atrasadas, como se tudo estivesse alguns segundos distante"),
("leveza","substantivo feminino","sensação de pouco peso físico ou de redução de carga corporal e emocional","depois de uma tensão passar, caminhar ou respirar parece exigir menos esforço do que antes"),
("pressão","substantivo feminino","sensação de força exercida sobre uma região do corpo ou de compressão percebida internamente","algo parece apertar ou ocupar espaço contra uma parte do corpo"),
("tensão","substantivo feminino","sensação de contração muscular ou de preparação corporal que dificulta relaxamento","ombros, mandíbula ou mãos permanecem contraídos mesmo quando você já não precisa agir"),
("maciez","substantivo feminino","qualidade tátil de uma superfície ou material que oferece pouca resistência ao toque","a mão encontra uma superfície que cede ou desliza sem aspereza"),
("aspereza","substantivo feminino","qualidade tátil de uma superfície irregular ou abrasiva ao contato","o toque encontra pequenas resistências e não desliza de forma uniforme"),
("eco","substantivo masculino","repetição perceptível de um som depois que sua fonte já deixou de emiti-lo","uma palavra é dita e sua presença auditiva continua por uma fração de segundo no espaço"),
("zumbido","substantivo masculino","som contínuo ou recorrente percebido como vibração ou ruído fino, nem sempre vindo de uma fonte externa clara","mesmo em silêncio, você percebe um som persistente e difícil de localizar"),
("frio na barriga","locução nominal","sensação física breve associada a expectativa, nervosismo ou excitação","antes de algo importante, o abdômen parece contrair e a sensação lembra um pequeno vazio"),
("nó na garganta","locução nominal","sensação de aperto ou dificuldade momentânea para engolir ou falar, frequentemente associada à emoção","uma notícia ou assunto delicado faz a voz falhar antes mesmo de você chorar"),
("pele arrepiada","locução nominal","estado em que os pelos do corpo se elevam e a pele ganha textura perceptível","o corpo reage a frio, medo ou música com uma mudança visível na superfície da pele"),
("fome emocional","locução nominal","vontade de comer desencadeada mais por estado emocional do que por necessidade energética imediata","a vontade de comer aumenta principalmente depois de estresse, tédio ou tristeza"),
("saciedade","substantivo feminino","sensação de satisfação corporal que indica que a necessidade de comer foi atendida","depois de uma refeição adequada, a urgência de continuar comendo diminui naturalmente"),
("bem-estar","substantivo masculino","estado geral de conforto físico, psicológico ou social percebido como suficiente e sustentável","várias pequenas condições — descanso, segurança, conforto e vínculo — parecem funcionar em conjunto"),
],
"Tempo & memória": [
("efemeridade","substantivo feminino","qualidade do que dura pouco ou muda rapidamente, lembrando que sua permanência é limitada","uma experiência parece intensa justamente porque você sabe ou percebe que logo será diferente"),
("transitoriedade","substantivo feminino","condição de estar em passagem entre estados, sem permanecer definitivamente em nenhum deles","uma fase da vida ou situação ainda não terminou, mas já deixou de ser como antes"),
("impermanência","substantivo feminino","ideia de que formas, situações e estados mudam continuamente e não podem ser mantidos intactos","algo que parece estável hoje revela pequenas alterações quando você o compara ao passado"),
("lembrança","substantivo feminino","conteúdo de uma experiência passada que reaparece na memória com algum grau de acesso consciente","um cheiro ou lugar faz uma cena antiga retornar à mente"),
("reminiscência","substantivo feminino","lembrança parcial ou remota de algo passado, muitas vezes recuperada por fragmentos","você se recorda de uma imagem, frase ou sensação sem conseguir reconstruir todo o episódio"),
("recordação","substantivo feminino","ato ou conteúdo de trazer conscientemente um acontecimento passado para a memória","você decide voltar a uma experiência e a reconstrói mentalmente com os elementos de que ainda se lembra"),
("memória afetiva","locução nominal","lembrança cuja força depende não apenas do fato recordado, mas da emoção associada a ele","um cheiro simples traz de volta não só a cena, mas o sentimento que existia naquela época"),
("déjà-vu","substantivo masculino; termo estrangeiro","sensação de familiaridade intensa diante de uma situação que, conscientemente, parece estar acontecendo pela primeira vez","um lugar novo produz a impressão desconcertante de já ter sido vivido antes"),
("retrospectiva","substantivo feminino","olhar organizado para acontecimentos anteriores a partir de um momento posterior","você reúne episódios antigos e tenta enxergar a trajetória que eles formaram"),
("antecipação","substantivo feminino","experiência de imaginar ou sentir um acontecimento futuro antes que ele ocorra","o evento ainda está distante, mas você já pensa nos detalhes e efeitos que ele terá"),
("espera","substantivo feminino","período em que algo desejado, necessário ou anunciado ainda não aconteceu","o tempo passa sem entregar o resultado que você está aguardando"),
("demora","substantivo feminino","extensão de tempo maior que a esperada para que algo aconteça ou seja concluído","um processo que deveria ser rápido continua aberto por mais tempo do que você previa"),
("saudosismo","substantivo masculino","tendência a valorizar o passado e desejar seu retorno, às vezes suavizando seus problemas","uma época antiga é descrita como melhor quase exclusivamente por ter sido anterior ao presente"),
("nostalgia","substantivo feminino","afeição melancólica por um período passado, acompanhada da impressão de que ele ficou distante","um objeto antigo parece carregar consigo todo um período da vida"),
("esquecimento","substantivo masculino","perda parcial ou total do acesso consciente a uma informação, experiência ou detalhe antes conhecido","você sabe que conhecia algo, mas não consegue recuperar a palavra ou cena naquele momento"),
("continuidade","substantivo feminino","permanência de uma linha de relação entre momentos, estados ou acontecimentos diferentes","apesar das mudanças, ainda é possível perceber como um momento se liga ao anterior"),
("ruptura temporal","locução nominal","mudança percebida como quebra forte entre uma fase anterior e outra posterior","depois de certo acontecimento, a vida parece dividida em um antes e um depois"),
("passagem","substantivo feminino","movimento de um momento, estado ou fase para outro","o presente é percebido menos como ponto fixo e mais como transformação em curso"),
("instante","substantivo masculino","intervalo de duração muito curta, percebido como um ponto quase indivisível do tempo","algo acontece tão rápido que você o descreve como tendo durado apenas um instante"),
("ritmo","substantivo masculino","regularidade ou variação percebida na velocidade com que acontecimentos ou ações se sucedem","uma rotina pode parecer acelerada ou lenta dependendo da frequência dos eventos"),
("intervalo","substantivo masculino","espaço de tempo entre dois acontecimentos, ações ou períodos","há um pequeno espaço entre uma coisa terminar e outra começar"),
("reanimação da memória","locução nominal","retorno vívido de uma lembrança que parecia distante ou pouco acessível","um estímulo específico faz um episódio antigo voltar com detalhes inesperados"),
("amnésia","substantivo feminino","perda significativa de memória que compromete a lembrança de determinados períodos ou informações","a pessoa consegue realizar ações presentes, mas não acessa parte importante de seu passado"),
("kairos","substantivo masculino; termo estrangeiro","termo grego usado para nomear um momento considerado especialmente oportuno ou adequado para determinada ação","uma oportunidade parece existir agora de um jeito que não existirá do mesmo modo depois"),
("eternidade","substantivo feminino","ideia de duração sem limite ou de existência fora das medidas comuns do tempo","algo é imaginado não apenas como duradouro, mas como não sujeito a um fim temporal"),
],
"Experiências": [
("epifania","substantivo feminino","compreensão súbita que reorganiza o sentido de uma experiência ou problema","um detalhe muda de significado e você passa a enxergar a situação inteira de outro modo"),
("limiar","substantivo masculino","ponto de transição em que uma experiência, percepção ou estado começa a mudar de qualidade","depois de certo nível de estímulo, a sensação deixa de aumentar apenas em grau e parece mudar de natureza"),
("deslumbramento","substantivo masculino","impacto intenso produzido por algo percebido como extraordinariamente belo, grandioso ou novo","um lugar ou acontecimento exige alguns segundos apenas para você conseguir assimilar o que está vendo"),
("assombro","substantivo masculino","reação de espanto diante de algo inesperado, grandioso ou difícil de explicar","você fica momentaneamente sem resposta porque a situação excede o que imaginava ser possível"),
("estranhamento","substantivo masculino","sensação de que algo familiar adquiriu aspecto incomum ou de que algo novo não se encaixa no esperado","um lugar conhecido parece diferente depois de uma pequena mudança de contexto"),
("familiaridade","substantivo feminino","sensação de reconhecer um padrão, pessoa ou ambiente como conhecido ou previsível","você sabe intuitivamente como se comportar porque já encontrou aquela configuração antes"),
("perplexidade","substantivo feminino","estado de dúvida produzido por uma situação difícil de interpretar com as categorias disponíveis","qualquer explicação rápida parece deixar uma parte importante sem resposta"),
("serendipidade","substantivo feminino","acontecimento feliz ou útil descoberto por acaso durante uma busca que tinha outro objetivo","você procurava uma coisa e encontra outra que acaba sendo inesperadamente valiosa"),
("ressonância","substantivo feminino","efeito de uma experiência continuar produzindo resposta interna depois de o contato inicial terminar","uma frase simples continua ocupando seus pensamentos horas depois de ter sido ouvida"),
("catarse","substantivo feminino","experiência de liberação emocional associada a expressar, reconhecer ou atravessar uma carga acumulada","depois de falar ou chorar sobre algo, o problema continua existindo, mas a pressão interna diminui"),
("vertigem emocional","locução nominal","sensação de instabilidade produzida por mudança afetiva intensa, tornando difícil recuperar orientação interna","uma notícia altera tantas expectativas de uma vez que você sente como se tivesse perdido o chão"),
("encantamento","substantivo masculino","experiência em que algo captura a atenção e parece excepcionalmente significativo ou atraente","você começa a notar qualidades que antes passariam despercebidas"),
("alheamento","substantivo masculino","estado de afastamento da experiência imediata, como se a pessoa estivesse pouco conectada ao que acontece ao redor","há presença física, mas a atenção parece distante e as interações chegam com atraso"),
("presença","substantivo feminino","experiência de estar efetivamente atento e disponível ao que acontece no momento","você percebe detalhes do ambiente sem precisar fazer esforço para recuperar a atenção"),
("ausência","substantivo feminino","condição de algo ou alguém não estar onde seria esperado, produzindo às vezes efeito emocional ou funcional","um espaço ocupado habitualmente por alguém fica perceptivelmente diferente quando essa pessoa não está"),
("deslocamento","substantivo masculino","sensação ou processo de sair da posição física, social ou simbólica em que algo costumava estar","um contexto muda e você percebe que as referências antigas já não organizam a situação"),
("imersão","substantivo feminino","envolvimento intenso com uma atividade, ambiente ou narrativa a ponto de reduzir a percepção do que está fora dela","horas passam sem que você note porque toda a atenção está ocupada pela experiência"),
("sobrecarga","substantivo feminino","estado em que a quantidade de estímulos, tarefas ou demandas supera a capacidade momentânea de processá-los bem","mesmo coisas simples parecem difíceis porque há informação demais competindo pela sua atenção"),
("exaustão","substantivo feminino","estado de cansaço acentuado que reduz energia disponível para continuar uma atividade ou lidar com demandas","até tarefas rotineiras passam a exigir esforço desproporcional depois de um período prolongado de desgaste"),
("suspense","substantivo masculino","tensão produzida pela incerteza sobre o que acontecerá, especialmente quando a resposta foi adiada","você recebe parte da informação e precisa esperar para descobrir como a situação termina"),
("reviravolta","substantivo feminino","mudança inesperada que altera a direção ou interpretação de uma sequência de acontecimentos","um detalhe novo transforma o que parecia óbvio até aquele momento"),
("desfecho","substantivo masculino","parte final de uma sequência em que um problema, conflito ou narrativa encontra resolução ou encerramento","depois de várias possibilidades abertas, o acontecimento chega a um ponto em que seu resultado se torna definido"),
("estranheza","substantivo feminino","qualidade de algo parecer inadequado, incomum ou difícil de classificar dentro do esperado","você não consegue apontar exatamente o erro, mas sente que alguma coisa não encaixa"),
("maravilhamento","substantivo masculino","admiração intensa diante de algo que amplia a sensação de beleza, complexidade ou possibilidade","uma descoberta simples faz o mundo parecer temporariamente maior do que parecia antes"),
("liminaridade","substantivo feminino","condição de estar entre dois estados sociais, simbólicos ou pessoais, sem ocupar plenamente nenhum deles","uma fase terminou, mas a próxima ainda não começou de forma clara"),
],
"Palavras raras": [
("inefável","adjetivo","que é difícil ou impossível de exprimir adequadamente por palavras","você consegue reconhecer a experiência, mas qualquer descrição parece menor do que aquilo que foi vivido"),
("inexorável","adjetivo","que não pode ser impedido, desviado ou suavizado por pedidos ou resistência","o processo continua avançando mesmo quando alguém deseja sinceramente que ele pare"),
("ubiquidade","substantivo feminino","presença aparente ou efetiva em muitos lugares ao mesmo tempo","uma influência ou informação parece estar em toda parte de uma vez"),
("idiossincrasia","substantivo feminino","maneira muito particular de pensar, reagir ou fazer algo, característica de uma pessoa ou grupo","uma escolha aparentemente estranha faz sentido quando você entende os hábitos específicos daquela pessoa"),
("prolixidade","substantivo feminino","excesso de palavras ou detalhes em uma comunicação que poderia ser mais direta","um ponto simples é explicado por muitos desvios, repetições ou complementos"),
("lacônico","adjetivo","que se expressa de forma muito breve e econômica","uma resposta contém apenas o necessário e deixa pouca margem para desenvolvimento"),
("tácito","adjetivo","que está implícito e é compreendido sem ter sido declarado abertamente","ninguém formulou a regra, mas todos sabem que ela existe e esperam que seja seguida"),
("recôndito","adjetivo","que está escondido, afastado ou difícil de alcançar ou perceber","algo permanece fora da vista comum e exige procura para ser encontrado"),
("peremptório","adjetivo","que é expresso de modo categórico, sem abrir espaço para negociação ou adiamento","a instrução vem como conclusão definitiva, e não como proposta"),
("pusilânime","adjetivo","que demonstra falta de coragem diante de dificuldade, risco ou conflito","a pessoa recua não por prudência, mas porque não sustenta a própria posição quando surge resistência"),
("prosaico","adjetivo","que é comum, cotidiano ou desprovido de caráter extraordinário","uma cena banal pode ser perfeitamente descrita sem precisar transformá-la em algo grandioso"),
("insólito","adjetivo","que foge ao habitual ou esperado, causando surpresa por sua singularidade","o acontecimento não é impossível, mas é tão incomum que quebra a expectativa"),
("sutil","adjetivo","que se manifesta de maneira delicada, pouco evidente ou difícil de detectar de imediato","a diferença existe, mas só aparece quando você observa com atenção"),
("perene","adjetivo","que permanece por longo tempo ou conserva continuidade apesar das mudanças","o vínculo atravessa fases diferentes sem perder completamente sua identidade"),
("efusivo","adjetivo","que expressa emoção ou entusiasmo de maneira aberta, abundante e pouco contida","a alegria é mostrada com intensidade, gestos amplos e pouca preocupação em escondê-la"),
("contumaz","adjetivo","que persiste repetidamente em determinado comportamento ou hábito, mesmo após advertências ou tentativas de mudança","a mesma conduta reaparece tantas vezes que deixa de parecer um episódio isolado"),
("pusilanimidade","substantivo feminino","falta persistente de coragem para sustentar uma posição diante de risco ou oposição","a pessoa abandona uma decisão assim que percebe a possibilidade de conflito"),
("sobranceiro","adjetivo","que se comporta com ar de superioridade, como se estivesse acima das circunstâncias ou das outras pessoas","o modo de falar comunica distância e segurança excessiva, às vezes acompanhadas de desprezo"),
("circunspecto","adjetivo","que age com seriedade, reserva e cuidado, evitando exposição desnecessária","a pessoa observa antes de falar e mantém comportamento controlado mesmo em ambientes informais"),
("magnânimo","adjetivo","que demonstra grandeza de espírito, especialmente ao lidar com erros, derrotas ou ofensas","em vez de aproveitar a fragilidade do outro, a pessoa escolhe agir com generosidade"),
("mesquinho","adjetivo","que revela apego excessivo a pequenas vantagens, perdas ou ressentimentos","uma diferença mínima recebe atenção desproporcional porque a pessoa não admite ceder"),
("austero","adjetivo","que é simples, sóbrio e pouco dado a excessos","o ambiente ou a pessoa evita ornamentos e escolhas supérfluas"),
("nostálgico","adjetivo","que demonstra ou experimenta nostalgia","a pessoa fala de um período passado com forte carga afetiva e desejo de proximidade"),
("sereno","adjetivo","que apresenta calma e estabilidade emocional","mesmo diante de pressão, a reação permanece organizada e pouco impulsiva"),
("ambíguo","adjetivo","que admite mais de uma interpretação razoável ou não deixa clara uma direção única","uma mesma frase pode ser entendida de duas maneiras sem que uma delas seja claramente errada"),
],
"Identidade & pertencimento": [
("identidade","substantivo feminino","conjunto de características, vínculos, histórias e significados pelos quais uma pessoa ou grupo se reconhece","uma pergunta simples sobre quem você é abre caminho para relações, valores e experiências que se repetem ao longo do tempo"),
("pertencimento","substantivo masculino","sensação de ter um lugar reconhecido dentro de um espaço, grupo, história ou prática","você deixa de se sentir visitante e passa a perceber que sua presença é esperada e legítima"),
("autenticidade","substantivo feminino","coerência entre o modo como alguém se apresenta e aquilo que reconhece como próprio","você não precisa interpretar um papel diferente apenas para que sua presença seja aceita"),
("autoimagem","substantivo feminino","representação mental que uma pessoa constrói sobre sua própria aparência, capacidades ou características","a forma como você se descreve internamente influencia como interpreta elogios, críticas e escolhas"),
("autoestima","substantivo feminino","avaliação afetiva que uma pessoa faz do próprio valor ou capacidade","um erro pode ser reconhecido como erro sem transformar automaticamente a pessoa inteira em fracasso"),
("autoconceito","substantivo masculino","conjunto organizado de ideias que uma pessoa mantém sobre quem é e como funciona","você tem crenças relativamente estáveis sobre seus gostos, habilidades, limitações e papéis"),
("alteridade","substantivo feminino","reconhecimento de que o outro possui perspectivas e experiências próprias que não precisam coincidir com as nossas","entender alguém não exige transformar sua experiência numa cópia da nossa"),
("identificação","substantivo feminino","processo de reconhecer semelhança, afinidade ou vínculo entre si e outra pessoa, grupo ou ideia","uma história alheia parece falar de você porque toca uma parte importante da sua própria experiência"),
("alienação","substantivo feminino","sensação de afastamento de si, do trabalho, de outras pessoas ou de uma realidade que deveria ser familiar","você participa de algo, mas sente que não reconhece mais seu lugar dentro daquela atividade"),
("estigma","substantivo masculino","marca social negativa associada a uma característica ou condição que passa a influenciar como alguém é tratado","uma informação sobre uma pessoa altera julgamentos antes mesmo de qualquer contato direto"),
("estereótipo","substantivo masculino","imagem simplificada e generalizante usada para representar pessoas de determinado grupo","uma categoria inteira é descrita como se todos os seus membros tivessem as mesmas características"),
("diferença","substantivo feminino","característica pela qual uma pessoa, objeto ou experiência não coincide com outra","duas experiências podem ter muito em comum e ainda assim divergir em um detalhe relevante"),
("semelhança","substantivo feminino","relação de proximidade entre características de duas ou mais coisas","você nota que experiências diferentes compartilham uma estrutura ou traço importante"),
("comunidade","substantivo feminino","conjunto de pessoas que compartilham algum espaço, interesse, identidade, prática ou vínculo","o grupo produz regras, memórias e referências que seus integrantes reconhecem em comum"),
("diáspora","substantivo feminino","dispersão de um grupo para diferentes regiões mantendo, em graus variados, vínculos de origem e memória compartilhada","pessoas vivem longe do lugar de origem, mas preservam práticas, histórias e referências que as conectam"),
("hibridismo","substantivo masculino","combinação de referências, práticas ou identidades provenientes de contextos diferentes","uma pessoa incorpora elementos de origens distintas sem precisar escolher apenas uma delas"),
("inclusão","substantivo feminino","criação de condições para que pessoas diferentes possam participar e ter reconhecimento dentro de um espaço comum","não basta permitir entrada; é preciso que a participação seja possível sem exigir apagamento das diferenças"),
("exclusão","substantivo feminino","impedimento ou afastamento de alguém de um espaço, grupo, recurso ou possibilidade de participação","uma regra ou prática mantém determinada pessoa fora enquanto outras têm acesso"),
("anonimato","substantivo masculino","condição em que a identidade de uma pessoa permanece desconhecida ou não é relevante para a interação","você participa de um espaço sem que os outros saibam quem está por trás do nome ou perfil"),
("visibilidade","substantivo feminino","grau em que uma pessoa, grupo ou experiência consegue ser percebido e reconhecido publicamente","uma existência pode estar presente e ainda assim permanecer pouco percebida por quem ocupa o centro da atenção"),
("marginalidade","substantivo feminino","posição social ou simbólica fora do centro de determinada estrutura, com acesso reduzido a seus recursos ou reconhecimento","um grupo participa do sistema, mas permanece nas bordas de poder, prestígio ou representação"),
("raízes","substantivo plural","conjunto de origens, vínculos e referências que ligam alguém a lugares, pessoas ou histórias anteriores","uma mudança de cidade não elimina automaticamente os lugares e relações que continuam servindo como referência"),
("casa","substantivo feminino","espaço físico ou simbólico em que uma pessoa sente proteção, familiaridade e legitimidade para existir à sua maneira","às vezes casa é menos o endereço e mais a sensação de poder baixar a guarda"),
("deslocado","adjetivo","que parece estar fora do lugar, contexto ou ambiente em que seria naturalmente integrado","uma fala adequada em outro espaço soa inadequada porque não combina com aquele momento"),
("pertencente","adjetivo","que faz parte de determinado grupo, lugar, sistema ou história","a pessoa é reconhecida como integrante e não apenas como visitante ocasional"),
],
"Comportamentos": [
("hesitar","verbo","adiar uma decisão ou ação por dificuldade de escolher entre possibilidades","você chega ao momento de agir, mas interrompe o movimento para pesar novamente as opções"),
("procrastinar","verbo","adiar repetidamente uma tarefa ou decisão relevante, apesar de saber que ela precisa ser feita","você encontra outra atividade mais confortável no momento em que deveria começar o trabalho importante"),
("evitar","verbo","afastar-se intencionalmente de uma pessoa, situação ou estímulo considerado desconfortável, arriscado ou indesejado","o assunto aparece e você muda de rota para não precisar lidar com ele"),
("insistir","verbo","continuar tentando ou defendendo algo apesar de obstáculos, recusas ou resultados insuficientes","a primeira tentativa falha e você decide repetir em vez de abandonar a intenção"),
("ceder","verbo","abrir mão de parte da própria posição, espaço ou exigência para permitir avanço de uma situação","você continua discordando, mas aceita modificar sua exigência para chegar a um acordo"),
("reparar","verbo","tentar corrigir, compensar ou restaurar algo depois que uma ação causou dano ou desequilíbrio","depois de perceber o impacto, você procura uma forma concreta de reduzir o prejuízo"),
("acolher","verbo","receber alguém ou alguma experiência com disponibilidade, sem exigir que ela se torne imediatamente diferente","a pessoa chega em um estado difícil e encontra espaço para existir antes de receber conselhos"),
("confrontar","verbo","encarar diretamente uma pessoa, questão ou situação que poderia ser evitada","em vez de contornar o problema, você o coloca na mesa e aceita lidar com a reação"),
("ruminar","verbo","repetir mentalmente um problema, lembrança ou preocupação sem produzir avanço proporcional","a mesma cena retorna várias vezes, acompanhada de novos argumentos e pouca mudança prática"),
("idealizar","verbo","atribuir qualidades excessivamente positivas a alguém, situação ou possibilidade, reduzindo a percepção de seus limites","você começa a preencher lacunas de informação com características desejadas"),
("comparar","verbo","colocar coisas, pessoas ou experiências lado a lado para identificar semelhanças, diferenças ou hierarquias","uma escolha passa a parecer melhor ou pior depois de ser medida contra outra"),
("antecipar","verbo","imaginar, preparar ou agir antes da ocorrência de algo esperado","você organiza detalhes do futuro porque espera que determinado acontecimento aconteça"),
("recuar","verbo","afastar-se física, emocional ou estrategicamente depois de perceber risco, oposição ou necessidade de espaço","a situação fica intensa e você reduz a proximidade antes de continuar"),
("se acomodar","locução verbal","aceitar passivamente uma situação pouco satisfatória por hábito, cansaço ou falta de disposição para mudá-la","a pessoa reconhece o problema, mas passa a tratá-lo como se não existisse alternativa"),
("desabafar","verbo","expressar sentimentos, pensamentos ou tensões acumuladas com a intenção de aliviar a carga interna","você conta o que aconteceu sem necessariamente esperar uma solução imediata"),
("interromper","verbo","fazer algo parar antes de seu curso habitual ou planejado","uma atividade é cortada no meio porque surge outra prioridade ou porque a situação se torna insustentável"),
("adaptar","verbo","alterar comportamento, estratégia ou ambiente para funcionar melhor diante de novas condições","uma mudança torna o plano original inadequado e você ajusta o modo de agir"),
("improvisar","verbo","criar uma resposta no momento usando os recursos disponíveis, sem depender de planejamento completo","surge um problema inesperado e você constrói uma solução enquanto o resolve"),
("repetir","verbo","realizar novamente uma ação ou sequência que já ocorreu antes","uma experiência é reproduzida porque você quer manter, testar ou corrigir seu resultado"),
("observar","verbo","prestar atenção deliberadamente a alguém, algo ou uma situação para perceber características e mudanças","antes de intervir, você dedica algum tempo a entender o que está acontecendo"),
("adiar","verbo","deslocar uma ação ou decisão para um momento posterior","você decide fazer amanhã algo que poderia fazer hoje porque considera o custo imediato maior"),
("reconsiderar","verbo","reexaminar uma decisão ou opinião à luz de novas informações ou argumentos","depois de descobrir um detalhe importante, você revisita uma escolha que parecia encerrada"),
("concordar","verbo","reconhecer uma proposição, condição ou decisão como aceitável ou correta para si","depois de ouvir os argumentos, você decide sustentar a mesma conclusão que a outra pessoa"),
("recusar","verbo","não aceitar uma oferta, pedido, condição ou proposta","você considera a possibilidade e decide que não quer ou não pode prosseguir com ela"),
("ceder espaço","locução verbal","permitir que outra pessoa ocupe parte da atenção, do tempo ou do espaço que estava sob seu controle","uma disputa continua, mas você decide diminuir sua presença para favorecer o outro"),
],
"Pensamentos": [
("devaneio","substantivo masculino","fluxo de imagens e ideias que se afasta da tarefa imediata e acompanha associações internas","uma lembrança ou possibilidade leva sua mente a uma pequena história que não estava planejada"),
("ponderação","substantivo feminino","avaliação cuidadosa de diferentes fatores antes de assumir uma posição ou decisão","você deixa de perguntar apenas o que quer e passa a considerar custos, consequências e efeitos nos outros"),
("inferência","substantivo feminino","conclusão obtida a partir de informações disponíveis, mesmo quando o resultado não foi dito diretamente","há sinais suficientes para uma hipótese, embora ninguém tenha declarado a conclusão de forma explícita"),
("dedução","substantivo feminino","raciocínio que deriva uma conclusão a partir de premissas consideradas válidas","se as condições são verdadeiras, você aplica a regra e obtém uma consequência necessária"),
("analogia","substantivo feminino","comparação entre estruturas ou relações semelhantes usada para compreender algo menos familiar","um problema novo fica mais claro quando você o relaciona a outro que já conhece"),
("associação","substantivo feminino","ligação mental estabelecida entre elementos que passam a evocar ou organizar um ao outro","uma palavra traz outra lembrança porque as duas foram repetidamente experimentadas juntas"),
("abstração","substantivo feminino","processo de destacar características gerais enquanto detalhes particulares são deixados de lado","em vez de pensar em cada objeto individualmente, você cria uma categoria que inclui vários deles"),
("generalização","substantivo feminino","extensão de uma conclusão obtida em alguns casos para um conjunto mais amplo de situações","um comportamento observado algumas vezes é tratado como regra sobre todas as situações semelhantes"),
("nuance","substantivo feminino","diferença pequena mas relevante dentro de uma categoria, opinião ou experiência","duas coisas parecem iguais à primeira vista, mas um detalhe muda seu significado"),
("paradoxo","substantivo masculino","situação ou formulação que parece contraditória, mas expõe um problema ou possibilidade interessante","duas ideias incompatíveis à primeira vista podem coexistir quando as condições são examinadas com mais cuidado"),
("pressuposto","substantivo masculino","ideia tomada como base antes de uma afirmação ou raciocínio ser construído","a discussão parece discordar do resultado, mas na verdade começa a partir de premissas diferentes"),
("perspectiva","substantivo feminino","modo particular de organizar e interpretar uma experiência a partir de determinada posição","mudar o ponto de observação altera quais aspectos parecem mais importantes"),
("reframing","substantivo masculino; termo estrangeiro","processo de reinterpretar uma situação por outro enquadramento, mudando o significado prático que ela assume","o fato permanece igual, mas você encontra uma maneira diferente de descrevê-lo e agir a partir disso"),
("dúvida","substantivo feminino","estado de incerteza em que uma conclusão ainda não parece suficientemente sustentada","há duas ou mais possibilidades e você não considera nenhuma segura o bastante para encerrar a questão"),
("convicção","substantivo feminino","crença fortemente sustentada, considerada verdadeira ou correta por quem a possui","mesmo diante de dificuldade, você continua tratando uma posição como fundamentalmente certa"),
("indecisão","substantivo feminino","dificuldade de escolher entre opções quando nenhuma delas produz segurança ou prioridade suficiente","você continua comparando possibilidades sem conseguir transformar a avaliação em escolha"),
("hipótese","substantivo feminino","explicação provisória proposta para ser testada ou confrontada com informações posteriores","você escolhe uma possibilidade que parece explicar os dados, mas admite que ela pode estar errada"),
("pressentimento","substantivo masculino","expectativa intuitiva de que algo pode ocorrer sem que exista ainda uma justificativa clara","uma mudança pequena no comportamento de alguém produz a sensação de que há algo por vir"),
("obsessão","substantivo feminino","preocupação ou ideia persistente que ocupa espaço desproporcional e difícil de interromper","mesmo quando você tenta seguir outra tarefa, a mesma questão continua retornando"),
("fixação","substantivo feminino","concentração rígida e persistente em uma ideia, objeto ou detalhe específico","um aspecto secundário passa a receber tanta atenção que começa a dominar a experiência inteira"),
("lucidez","substantivo feminino","capacidade de perceber e sustentar uma realidade com clareza mesmo quando ela é desconfortável","você reconhece simultaneamente seus desejos e aquilo que as circunstâncias realmente permitem"),
("imaginação","substantivo feminino","capacidade de combinar imagens, conceitos e possibilidades sem depender de sua presença imediata","você cria mentalmente algo que ainda não existe para testar como seria vivê-lo"),
("intenção","substantivo feminino","direção consciente de uma ação: aquilo que uma pessoa pretende realizar, provocar ou evitar","antes de agir, você sabe pelo menos aproximadamente o resultado que deseja produzir"),
("motivação","substantivo feminino","conjunto de razões ou impulsos que tornam uma ação atraente, necessária ou significativa","duas pessoas podem fazer a mesma coisa por razões completamente diferentes"),
("prioridade","substantivo feminino","ordem de importância que faz uma tarefa, necessidade ou valor receber atenção antes de outros","quando o tempo é curto, algumas coisas são protegidas porque são consideradas mais importantes"),
],
"Conceitos difíceis": [
("ambivalência","substantivo feminino","coexistência de respostas que apontam em direções opostas diante da mesma situação","uma escolha continua atraindo e incomodando ao mesmo tempo sem que isso seja simples indecisão"),
("contingência","substantivo feminino","dependência de algo que poderia ter acontecido de outra maneira e não era inevitável","o resultado atual parece óbvio depois de ocorrido, mas vários caminhos alternativos eram possíveis antes"),
("ironia","substantivo feminino","forma de expressão em que o sentido pretendido diverge do sentido literal, dependendo do contexto para ser reconhecido","uma frase parece elogiosa nas palavras, mas o tom e a situação indicam crítica"),
("paradoxo","substantivo masculino","formulação ou situação que reúne elementos aparentemente incompatíveis e desafia uma conclusão simples","quanto mais você tenta resumir o problema em uma regra, mais a própria regra cria uma exceção"),
("dialética","substantivo feminino","processo de confronto entre posições diferentes que pode produzir uma compreensão mais elaborada do problema","uma ideia é testada contra sua oposição até que o quadro deixe de caber em apenas um lado"),
("episteme","substantivo feminino; termo estrangeiro","termo de origem grega usado em filosofia para designar um regime ou campo de conhecimento considerado válido em determinado contexto","a pergunta não é apenas o que se sabe, mas quais critérios fazem algo contar como conhecimento"),
("teleologia","substantivo feminino","modo de explicar algo principalmente por sua finalidade ou objetivo","uma ação é interpretada pelo fim que parece orientar seu percurso, e não apenas pelas causas anteriores"),
("contingência histórica","locução nominal","caráter não inevitável de uma configuração histórica formada por escolhas, acidentes e circunstâncias específicas","uma sociedade poderia ter seguido outros caminhos mesmo que, olhando para trás, seu resultado pareça natural"),
("subjetividade","substantivo feminino","dimensão da experiência ligada ao modo particular como uma pessoa percebe, sente e interpreta o mundo","duas pessoas passam pela mesma situação e saem dela com significados diferentes"),
("objetividade","substantivo feminino","tentativa de descrever ou avaliar algo reduzindo a influência de preferências e perspectivas particulares","você define critérios que outras pessoas poderiam aplicar mesmo discordando de sua opinião pessoal"),
("agência","substantivo feminino","capacidade de agir deliberadamente e produzir efeitos dentro das condições disponíveis","mesmo sem controlar tudo ao redor, a pessoa consegue escolher e intervir em alguma parte da situação"),
("determinismo","substantivo masculino","perspectiva segundo a qual acontecimentos decorrem de condições anteriores de modo necessário, reduzindo a margem para alternativas reais","a questão passa a ser se, dadas exatamente as mesmas condições, outra coisa poderia ter acontecido"),
("livre-arbítrio","substantivo masculino","ideia de que pessoas possuem algum grau de escolha voluntária sobre suas ações","o problema aparece quando perguntamos até que ponto uma decisão realmente poderia ter sido diferente"),
("absurdo","substantivo masculino","situação em que a busca humana por sentido encontra um mundo que não oferece uma resposta proporcional ou necessária","você percebe uma distância entre o desejo por significado e a ausência de garantia externa de que ele exista"),
("paradoxo temporal","locução nominal","problema conceitual em que diferentes relações entre eventos no tempo parecem produzir contradições","mudar algo no passado parece alterar justamente as condições que permitiram a mudança acontecer"),
("identidade narrativa","locução nominal","forma de organizar experiências da própria vida como uma história relativamente coerente, com continuidades e mudanças","você escolhe certos episódios como capítulos importantes e usa essa seleção para explicar quem se tornou"),
("intersubjetividade","substantivo feminino","campo compartilhado de sentidos construído entre diferentes sujeitos por meio de linguagem, interação e reconhecimento","algo passa a significar o mesmo para várias pessoas porque existe uma referência comum entre elas"),
("emergência","substantivo feminino","aparecimento de propriedades de um sistema que não são facilmente atribuídas a uma única parte isolada","um padrão coletivo surge das interações, embora nenhum participante o carregue sozinho"),
("liminaridade","substantivo feminino","estado intermediário em que uma pessoa ou estrutura deixou uma condição anterior, mas ainda não consolidou a seguinte","regras antigas já não funcionam completamente e as novas ainda estão sendo formadas"),
("ressonância","substantivo feminino","persistência de efeitos ou significados depois que o estímulo original desapareceu","uma experiência continua influenciando decisões e sentimentos sem precisar ser relembrada conscientemente a cada vez"),
("impermanência","substantivo feminino","princípio ou observação de que estados e formas são continuamente sujeitos a mudança","o que parece fixo pode ser preservado apenas por um período e sob determinadas condições"),
("transcendência","substantivo feminino","ideia de ultrapassar um limite ou condição tomada como referência","uma experiência é descrita como indo além do quadro habitual de percepção ou de significado"),
("imanência","substantivo feminino","ideia de que algo está contido no próprio campo da experiência ou da realidade, sem depender de um exterior transcendente","a explicação procura o princípio do fenômeno dentro das próprias relações que o constituem"),
("parcialidade","substantivo feminino","inclinação em favor de uma das partes ou perspectivas, dificultando uma avaliação equilibrada","o critério usado para julgar a situação beneficia sistematicamente um lado"),
("equivocidade","substantivo feminino","qualidade de uma expressão ou situação cujo sentido pode permanecer aberto a interpretações diferentes","a palavra parece precisar de contexto para indicar qual de seus possíveis significados está em jogo"),
],
"Lugar & atmosfera": [
("atmosfera","substantivo feminino","conjunto de qualidades físicas, sociais e sensoriais que produz uma determinada impressão de ambiente","duas salas podem ter a mesma função e ainda assim transmitir sensações completamente diferentes"),
("ambiente","substantivo masculino","conjunto de espaço, condições e relações que cercam uma pessoa ou atividade","o comportamento das pessoas muda porque o local cria regras implícitas sobre o que parece adequado"),
("aconchego","substantivo masculino","sensação de conforto e proteção produzida por um espaço, objeto ou companhia","um lugar pequeno e familiar pode parecer mais confortável do que um espaço maior e impessoal"),
("apinhamento","substantivo masculino","situação de grande concentração de pessoas ou objetos em espaço reduzido","o movimento fica difícil porque quase não há área livre entre os corpos ou coisas"),
("silêncio","substantivo masculino","ausência ou redução significativa de som perceptível","quando todos param de falar, sons que antes eram mascarados passam a ocupar o primeiro plano"),
("penumbra","substantivo feminino","iluminação parcial em que formas permanecem visíveis, mas sem definição completa","o espaço não está escuro por inteiro, porém detalhes pequenos continuam difíceis de distinguir"),
("luminosidade","substantivo feminino","quantidade ou qualidade de luz presente em determinado ambiente ou superfície","a mesma sala parece acolhedora, fria ou dramática dependendo da luz que recebe"),
("recluso","adjetivo","que permanece afastado da convivência ou do espaço social comum","a pessoa prefere um ambiente restrito e reduz significativamente o contato externo"),
("doméstico","adjetivo","relativo à casa, à vida do lar ou a atividades realizadas nesse contexto","uma rotina doméstica envolve práticas simples ligadas a manutenção, convivência e cuidado"),
("urbano","adjetivo","relativo à cidade, sua infraestrutura, ritmo, população ou formas de convivência","o trânsito, a densidade e os serviços moldam a experiência de um espaço urbano"),
("bucólico","adjetivo","que evoca vida campestre, paisagem rural e tranquilidade associada ao campo","a descrição enfatiza vegetação, espaço aberto e um ritmo de vida menos urbano"),
("claustrofóbico","adjetivo","que provoca ou lembra sensação de confinamento e falta de espaço","o ambiente parece apertado o bastante para produzir desconforto mesmo antes de qualquer movimento"),
("sereno","adjetivo","que transmite calma e pouca agitação","a combinação de ritmo, luz e som reduz a impressão de pressa do ambiente"),
("hostil","adjetivo","que oferece condições pouco acolhedoras, ameaçadoras ou difíceis para quem está dentro dele","a disposição do espaço ou o comportamento das pessoas faz a presença parecer desconfortável ou insegura"),
("familiar","adjetivo","que é reconhecido como conhecido, habitual ou próximo","você não precisa reaprender como se orientar porque já conhece os sinais daquele lugar"),
("estranho","adjetivo","que parece incomum, inadequado ou pouco reconhecível dentro do contexto","há algo no cenário que impede a sensação de encaixe mesmo quando nada parece objetivamente errado"),
("refúgio","substantivo masculino","lugar ou situação que oferece proteção, descanso ou afastamento de pressões externas","depois de um período intenso, você procura um espaço onde não precise responder a tantas demandas"),
("praça","substantivo feminino","espaço público destinado à circulação, permanência e convivência em uma área urbana","pessoas que não se conhecem podem compartilhar o mesmo lugar sem precisar formar um grupo"),
("fronteira","substantivo feminino","linha ou limite que separa territórios, estados, relações ou categorias","atravessar a fronteira significa deixar de estar submetido a um conjunto de regras e entrar em outro"),
("limiar","substantivo masculino","ponto de entrada ou transição entre espaços, estados ou níveis de experiência","ficar na porta é permanecer exatamente entre o lado de dentro e o de fora"),
("paisagem","substantivo feminino","porção de espaço percebida como conjunto visual e sensorial relativamente organizado","um mesmo lugar pode produzir paisagens diferentes dependendo da estação, da luz ou do ponto de vista"),
("horizonte","substantivo masculino","linha ou direção aparente onde o campo de visão parece encontrar seu limite","olhar para longe organiza a percepção do espaço mesmo quando não há um fim físico próximo"),
("periferia","substantivo feminino","região situada fora do centro de determinado espaço, sistema ou circuito de poder","algo pode estar fisicamente próximo e ainda ser periférico em acesso, atenção ou influência"),
("centro","substantivo masculino","ponto ou região tomada como referência principal dentro de um espaço ou sistema","estar no centro pode significar apenas posição física ou também concentração de atenção e recursos"),
("entre-lugar","substantivo masculino","posição intermediária em que alguém ou algo participa de contextos diferentes sem pertencer completamente a nenhum deles","a pessoa se reconhece em mais de um espaço, mas não encontra uma identidade totalmente confortável em apenas um"),
],
"Leitura & linguagem": [
("metáfora","substantivo feminino","uso de uma imagem ou relação figurada para compreender ou expressar algo por aproximação","uma experiência abstrata é descrita com referência a algo concreto que compartilha determinada característica"),
("metonímia","substantivo feminino","substituição de um termo por outro ligado a ele por proximidade ou associação reconhecível","o autor menciona o lugar para se referir às pessoas e instituições que atuam nele"),
("eufemismo","substantivo masculino","forma de suavizar uma expressão considerada dura, direta, ofensiva ou incômoda","uma realidade difícil é mencionada por um termo que reduz seu impacto imediato"),
("hipérbole","substantivo feminino","exagero intencional usado para enfatizar uma ideia, emoção ou característica","a frase aumenta deliberadamente a dimensão de algo sem esperar que o leitor tome o número literalmente"),
("subtexto","substantivo masculino","camada de sentido implícito que depende do contexto, do tom ou do que não foi dito","a frase diz uma coisa, mas a situação faz o leitor perceber outra"),
("ambiguidade","substantivo feminino","possibilidade de uma palavra ou construção admitir mais de um sentido relevante","sem contexto suficiente, a mesma frase permite leituras diferentes"),
("literalidade","substantivo feminino","uso ou interpretação de uma expressão segundo seu sentido direto, sem recorrer ao valor figurado","a instrução deve ser entendida exatamente como formulada, sem metáfora ou ironia"),
("concisão","substantivo feminino","qualidade de expressar uma ideia com o mínimo de palavras necessárias, sem perda essencial de sentido","o texto elimina repetições e mantém apenas o que realmente contribui para a mensagem"),
("prolixidade","substantivo feminino","tendência a usar palavras ou detalhes em excesso ao comunicar uma ideia","o argumento poderia ser curto, mas se estende por muitas explicações secundárias"),
("eloquência","substantivo feminino","capacidade de se expressar de modo claro, convincente e expressivo","a escolha das palavras, o ritmo e a organização fazem a fala ganhar força sem depender apenas do conteúdo"),
("lacônico","adjetivo","que comunica de maneira muito breve e econômica","a resposta é curta e direta, sem explicações adicionais"),
("reticente","adjetivo","que evita revelar tudo o que pensa ou sabe, deixando parte da informação incompleta ou implícita","a pessoa responde sem negar, mas também sem entregar o detalhe que seria esperado"),
("tácito","adjetivo","que é entendido ou aceito sem ser explicitamente declarado","ninguém anuncia a regra, porém todos se comportam como se ela fosse conhecida"),
("insinuação","substantivo feminino","sugestão indireta de uma ideia, crítica ou intenção sem afirmação totalmente explícita","a pessoa evita dizer algo de forma direta, mas constrói pistas suficientes para que a mensagem seja percebida"),
("paráfrase","substantivo feminino","reformulação de uma ideia com outras palavras preservando seu sentido central","um texto difícil é reescrito em linguagem mais simples sem alterar o ponto principal"),
("intertextualidade","substantivo feminino","relação em que um texto dialoga com outros textos, referências ou formas culturais reconhecíveis","uma frase ganha camada extra porque remete deliberadamente a outra obra"),
("polissemia","substantivo feminino","existência de múltiplos sentidos relacionados para uma mesma palavra","a palavra mantém uma unidade histórica ou conceitual, mas assume significados diferentes conforme o contexto"),
("conotação","substantivo feminino","sentido associado, afetivo ou cultural que ultrapassa a definição mais direta de uma palavra","um termo comum desperta uma impressão particular por tudo o que culturalmente carrega"),
("denotação","substantivo feminino","sentido mais direto e referencial de uma palavra, em contraste com associações figuradas","a expressão é usada para nomear o objeto sem intenção de criar imagem ou efeito adicional"),
("cadência","substantivo feminino","ritmo produzido pela sucessão e distribuição de sons, palavras ou pausas em uma fala ou texto","uma frase parece lenta ou rápida não apenas pelo conteúdo, mas pela maneira como as palavras se encadeiam"),
("ênfase","substantivo feminino","destaque dado a uma palavra, ideia ou trecho para indicar sua importância","uma mudança de tom ou posição faz o leitor perceber que determinado elemento deve receber atenção especial"),
("leitura enviesada","locução nominal","interpretação condicionada por expectativas ou crenças prévias que fazem certos aspectos ganharem peso excessivo","duas pessoas leem o mesmo texto e uma encontra principalmente aquilo que confirma sua opinião anterior"),
("silêncio eloquente","locução nominal","ausência de fala que comunica algo relevante pelo contexto em que ocorre","ninguém responde à pergunta, e justamente essa falta de resposta se torna significativa"),
("voz autoral","locução nominal","conjunto de escolhas de linguagem que faz um texto reconhecer-se como expressão particular de quem o escreve","mesmo sem assinatura, o modo de organizar ideias, ritmo e imagens sugere um autor específico"),
("palavra-valise","substantivo feminino","palavra formada pela fusão de outras palavras, combinando partes e sentidos de ambas","o neologismo parece carregar dois conceitos ao mesmo tempo porque sua forma nasce de duas fontes"),
],
"Vida cotidiana": [
("rotina","substantivo feminino","sequência relativamente estável de atividades que organiza períodos repetidos do dia ou da semana","você sabe aproximadamente o que vem depois porque certas ações se repetem em uma ordem conhecida"),
("hábito","substantivo masculino","comportamento aprendido que tende a ocorrer com pouca deliberação consciente quando certas condições estão presentes","uma situação específica dispara a ação quase automaticamente porque ela foi repetida muitas vezes"),
("ritual","substantivo masculino","sequência simbólica ou prática de ações repetidas que recebe significado além de sua função imediata","o modo de fazer algo importa tanto quanto o resultado porque a repetição cria sensação de continuidade"),
("improviso","substantivo masculino","solução criada no momento sem planejamento completo, usando recursos disponíveis","um detalhe inesperado aparece e você precisa decidir como lidar com ele sem tempo para preparar tudo"),
("atraso","substantivo masculino","chegada ou conclusão posterior ao horário esperado ou combinado","o resultado acontece, mas depois do momento em que as pessoas contavam com ele"),
("urgência","substantivo feminino","necessidade de tratar algo rapidamente por causa de risco, prazo ou consequência do adiamento","o tempo disponível é curto o bastante para mudar a ordem das prioridades"),
("conforto","substantivo masculino","estado de bem-estar produzido por condições físicas, emocionais ou práticas favoráveis","uma cadeira, rotina ou companhia reduz esforço e permite que você permaneça sem tensão desnecessária"),
("desconforto","substantivo masculino","sensação de incômodo ou inadequação física, emocional ou social que dificulta permanecer em uma situação","você consegue ficar ali, mas algo torna a experiência persistentemente pouco agradável"),
("conveniência","substantivo feminino","qualidade de algo ser adequado ou vantajoso para determinada necessidade prática","uma opção não é necessariamente melhor em tudo, mas resolve o problema com menos esforço"),
("comodidade","substantivo feminino","facilidade obtida pela redução de trabalho, deslocamento ou esforço cotidiano","você escolhe um caminho porque ele poupa energia ou simplifica tarefas"),
("miudeza","substantivo feminino","objeto, detalhe ou aspecto pequeno que costuma receber pouca atenção isoladamente","um conjunto de pequenas coisas ocupa o ambiente e só ganha importância quando observado em conjunto"),
("capricho","substantivo masculino","cuidado especial ou escolha pessoal que ultrapassa o mínimo necessário para realizar algo","a pessoa ajusta um detalhe sem que isso seja exigido porque quer que o resultado tenha uma qualidade específica"),
("desleixo","substantivo masculino","falta de cuidado ou atenção que deixa algo malfeito, desorganizado ou negligenciado","pequenos sinais mostram que a manutenção foi adiada tantas vezes que o conjunto começa a deteriorar"),
("pressa","substantivo feminino","estado de agir em velocidade maior do que a confortável porque se deseja ou precisa chegar logo ao resultado","o relógio parece controlar o comportamento e várias etapas são encurtadas para ganhar tempo"),
("ociosidade","substantivo feminino","estado de não estar ocupado com trabalho, tarefa ou atividade específica","há tempo disponível e nenhuma obrigação imediata exige sua atenção"),
("tédio","substantivo masculino","sensação de falta de estímulo ou de interesse que torna a passagem do tempo mais pesada","nada parece suficientemente envolvente para justificar o tempo que está passando"),
("lazer","substantivo masculino","tempo reservado ou disponível para atividades escolhidas por interesse, prazer ou descanso","a atividade não é executada por obrigação, mas porque você quer fazer aquilo naquele período"),
("descanso","substantivo masculino","interrupção de esforço ou atividade destinada a recuperar energia ou reduzir desgaste","você suspende uma tarefa não por desistência, mas para recuperar condições de continuar"),
("presença social","locução nominal","efeito produzido simplesmente pela participação de uma pessoa em um ambiente coletivo, mesmo sem fala constante","uma sala parece diferente porque alguém está ali, ainda que permaneça quieto"),
("pequenez","substantivo feminino","qualidade de algo ter dimensão, importância ou alcance reduzidos em comparação com um referencial","um detalhe mínimo chama atenção justamente porque o contexto ao redor é muito maior"),
("banal","adjetivo","que é comum, corriqueiro ou pouco excepcional","a situação acontece com tanta frequência que quase não exige comentário"),
("cotidiano","adjetivo","que pertence à vida diária ou ocorre regularmente na rotina","uma tarefa cotidiana pode parecer insignificante isoladamente, mas sustenta boa parte da vida prática"),
("espontâneo","adjetivo","que ocorre sem planejamento deliberado ou sem depender de preparação extensa","a pessoa faz ou diz algo no momento porque a ação surge naturalmente da situação"),
("recorrente","adjetivo","que volta a acontecer com alguma frequência ou padrão reconhecível","o mesmo tipo de episódio aparece novamente depois de um intervalo"),
("eventual","adjetivo","que ocorre de modo ocasional, sem formar um padrão estável","há uma ou outra ocorrência, mas não o suficiente para chamar aquilo de rotina"),
],
"Filosofia da vida": [
("sentido","substantivo masculino","interpretação ou valor que faz uma experiência parecer significativa em relação a um conjunto maior de escolhas e objetivos","uma mesma tarefa muda de peso quando você entende por que ela importa para a vida que pretende construir"),
("propósito","substantivo masculino","orientação relativamente estável que dá direção a escolhas, projetos ou ações","você consegue usar determinada meta para decidir entre caminhos que de outro modo pareceriam equivalentes"),
("liberdade","substantivo feminino","possibilidade de agir ou escolher dentro das condições reais existentes","ser livre não elimina restrições, mas envolve espaço suficiente para que decisões próprias produzam diferença"),
("responsabilidade","substantivo feminino","dever de responder pelos efeitos de uma ação, decisão ou papel assumido","reconhecer que algo dependeu de você muda a pergunta de 'quem foi?' para 'o que faço agora?'"),
("virtude","substantivo feminino","qualidade de caráter valorizada por favorecer uma maneira considerada boa ou prudente de agir","uma pessoa é admirada não por uma ação isolada, mas pela consistência com que sustenta determinado modo de agir"),
("prudência","substantivo feminino","capacidade de considerar riscos, limites e consequências antes de agir","você não recusa uma oportunidade por medo, mas também não ignora aquilo que pode dar errado"),
("coragem","substantivo feminino","disposição para agir apesar do medo, risco ou incerteza","o medo continua presente, mas deixa de ser o único fator que decide a ação"),
("finitude","substantivo feminino","condição de ter duração ou existência limitada e estar sujeito a término","a percepção de que algo acaba altera a maneira como o presente é vivido"),
("mortalidade","substantivo feminino","condição de estar sujeito à morte","lembrar que pessoas, projetos e fases são temporários muda o valor atribuído ao tempo disponível"),
("absurdo","substantivo masculino","experiência de choque entre a busca humana por sentido e a falta de garantia de que o mundo ofereça esse sentido pronto","a pergunta por um significado definitivo permanece sem uma resposta externa obrigatória"),
("estoicismo","substantivo masculino","tradição filosófica que enfatiza distinguir o que está sob nosso controle do que não está e agir de acordo com valores escolhidos","a atenção é deslocada do resultado garantido para a qualidade da resposta diante das circunstâncias"),
("ataraxia","substantivo feminino; termo estrangeiro","termo grego associado a um estado de tranquilidade ou ausência de perturbação excessiva","a ideia não é euforia, mas redução de agitação que permite pensar e viver com maior estabilidade"),
("eudaimonia","substantivo feminino; termo estrangeiro","termo grego usado na filosofia para uma vida realizada ou florescente, mais ampla do que prazer momentâneo","uma vida boa é avaliada pelo conjunto de sua realização e não apenas pela quantidade de momentos agradáveis"),
("imanência","substantivo feminino","perspectiva segundo a qual sentido e realidade podem ser compreendidos a partir da própria experiência e de suas relações","a explicação não precisa recorrer a um domínio externo para começar a fazer sentido"),
("transcendência","substantivo feminino","movimento de ultrapassar um limite de experiência, conhecimento ou condição tomado como referência","uma pessoa entende determinada experiência como apontando para algo que excede o quadro habitual"),
("contingência","substantivo feminino","fato de que uma situação poderia ter assumido outras formas e não era absolutamente necessária","olhar para trás não transforma o caminho percorrido em único caminho possível"),
("ser-para-a-morte","locução nominal","formulação filosófica que usa a consciência da mortalidade para pensar a existência e as escolhas presentes","a finitude deixa de ser apenas um fato futuro e passa a influenciar a forma atual de viver"),
("autonomia","substantivo feminino","capacidade de orientar a própria vida e decisões sem depender de controle indevido de outras pessoas","você escolhe e assume consequências sem precisar que alguém determine cada passo por você"),
("serenidade","substantivo feminino","estado de estabilidade diante de circunstâncias que não podem ser completamente controladas","aceitar a existência de incerteza não impede você de agir, mas reduz a necessidade de dominar tudo"),
("impermanência","substantivo feminino","reconhecimento de que situações e formas mudam continuamente e não podem ser possuídas de modo definitivo","em vez de perguntar como manter algo intacto para sempre, você considera como acompanhá-lo enquanto ele muda"),
("equanimidade","substantivo feminino","disposição de manter relativa estabilidade de julgamento e reação diante de ganhos e perdas","uma boa notícia não o desorganiza em euforia nem uma má notícia exige desespero imediato"),
("contemplação","substantivo feminino","atenção prolongada e pouco utilitária a algo com o objetivo de percebê-lo e compreendê-lo","você permanece diante de uma paisagem, ideia ou obra sem exigir que ela produza um resultado imediato"),
("sabedoria","substantivo feminino","capacidade prática de combinar conhecimento, experiência, prudência e sensibilidade ao contexto","saber muito não basta; é preciso reconhecer quando, como e para quê determinado conhecimento deve ser usado"),
("moderação","substantivo feminino","tendência a evitar excessos e ajustar intensidade de acordo com as circunstâncias","uma escolha não precisa ser extrema para ser firme ou significativa"),
("resiliência","substantivo feminino","capacidade de se reorganizar depois de dificuldades sem exigir que a experiência não tenha causado impacto","a pessoa não volta exatamente ao estado anterior, mas encontra um modo de continuar funcionando"),
],
"Afetos sociais": [
("empatia","substantivo feminino","capacidade de compreender ou imaginar o estado de outra pessoa sem precisar viver exatamente a mesma experiência","você tenta reconstruir como uma situação pode estar sendo sentida do ponto de vista do outro"),
("simpatia","substantivo feminino","inclinação favorável ou agradável em relação a alguém, frequentemente baseada em afinidade ou boa impressão","uma pessoa parece agradável antes mesmo de existir vínculo profundo entre vocês"),
("antipatia","substantivo feminino","aversão ou disposição desfavorável diante de alguém, sem necessariamente haver um conflito declarado","a presença da pessoa provoca rejeição mesmo quando você não consegue apontar um motivo concreto"),
("desprezo","substantivo masculino","avaliação depreciativa em que alguém é tratado como inferior, indigno ou pouco merecedor de consideração","uma pessoa é julgada de tal modo que suas necessidades deixam de parecer relevantes"),
("piedade","substantivo feminino","sentimento de compaixão diante do sofrimento de alguém, às vezes acompanhado por uma posição de superioridade","você se sensibiliza com a dificuldade do outro, mas pode fazê-lo a partir da ideia de que está acima dele"),
("condescendência","substantivo feminino","atitude de tolerar ou tratar alguém como inferior, mas de maneira aparentemente gentil","o tom parece educado, porém comunica que o outro é visto como menos capaz ou menos importante"),
("tolerância","substantivo feminino","disposição para conviver com diferenças ou condutas das quais você não necessariamente gosta ou concorda","uma pessoa mantém seu direito de existir ou falar mesmo sem receber aprovação pessoal"),
("intolerância","substantivo feminino","recusa em aceitar diferenças, opiniões ou comportamentos fora do que se considera legítimo","a discordância rapidamente vira tentativa de silenciar ou excluir o outro"),
("solidariedade","substantivo feminino","disposição de apoiar alguém diante de uma necessidade ou dificuldade por reconhecer uma responsabilidade humana compartilhada","você oferece tempo, recursos ou presença não apenas por interesse pessoal, mas porque a situação importa coletivamente"),
("lealdade","substantivo feminino","compromisso de agir de modo consistente com uma pessoa, grupo ou princípio ao longo do tempo","mesmo quando surge uma vantagem imediata em romper o vínculo, você preserva o acordo assumido"),
("respeito","substantivo masculino","reconhecimento de que outra pessoa possui dignidade, limites e autonomia que merecem consideração","mesmo discordando, você evita tratar o outro como alguém sem direito a uma posição própria"),
("desrespeito","substantivo masculino","ação ou atitude que ignora, diminui ou viola a dignidade, os limites ou a autonomia de outra pessoa","uma preferência pessoal é tratada como autorização para ultrapassar o espaço do outro"),
("acolhimento","substantivo masculino","modo de receber uma pessoa oferecendo segurança, atenção e espaço para que ela possa participar sem defesa constante","alguém chega vulnerável e encontra condições para ficar antes mesmo de precisar provar que merece estar ali"),
("rejeição","substantivo feminino","recusa de uma pessoa, proposta ou aproximação, comunicando que ela não será aceita naquela condição","uma tentativa de aproximação encontra um limite claro do outro lado"),
("validação","substantivo feminino","reconhecimento de que uma experiência, emoção ou percepção faz sentido dentro das condições em que surgiu","você não precisa concordar com a conclusão de alguém para reconhecer que a reação dela tem uma história compreensível"),
("aprovação","substantivo feminino","manifestação de concordância ou avaliação positiva diante de uma ação, ideia ou pessoa","uma decisão passa a receber sinal social de que é considerada adequada ou valorizada"),
("crítica","substantivo feminino","avaliação que identifica qualidades, limites ou problemas em uma obra, ideia, ação ou comportamento","a intenção não é apenas dizer se gostou, mas explicar o que funciona, falha ou poderia mudar"),
("elogio","substantivo masculino","manifestação de reconhecimento positivo sobre uma qualidade, ação ou resultado","alguém destaca algo específico que considera valioso em você ou no que fez"),
("encorajamento","substantivo masculino","mensagem, atitude ou suporte que aumenta a disposição de alguém para agir diante de insegurança ou dificuldade","uma pessoa oferece confiança suficiente para que você tente aquilo que estava evitando"),
("vergonha alheia","locução nominal","desconforto sentido ao observar o constrangimento, inadequação ou exposição de outra pessoa","você se sente mal mesmo sem ser o alvo direto da situação"),
("pressão social","locução nominal","força exercida pelas expectativas, normas ou julgamentos de um grupo sobre as escolhas de uma pessoa","você considera fazer algo menos por vontade própria e mais para evitar desaprovação"),
("reconhecimento","substantivo masculino","ato de perceber e atribuir valor a uma pessoa, contribuição, experiência ou qualidade","algo que antes passava despercebido recebe nome, crédito ou consideração explícita"),
("aceitação","substantivo feminino","disposição para reconhecer e conviver com uma realidade sem exigir que ela corresponda integralmente ao que gostaríamos","uma circunstância continua difícil, mas deixa de ser tratada como se sua existência fosse impossível"),
("reaproximação","substantivo feminino","retomada gradual de contato depois de um período de afastamento","duas pessoas voltam a conversar em pequenos passos sem pressupor que tudo voltou ao ponto anterior"),
("distanciamento","substantivo masculino","redução deliberada ou gradual da proximidade física, emocional ou social","uma pessoa limita contato para preservar espaço, diminuir conflito ou reorganizar o vínculo"),
],
}

META = {
"Sentimentos":"Estados afetivos e emocionais, dos mais cotidianos aos que resistem a uma palavra simples.",
"Amor & atração":"Vínculos, desejo, proximidade, reciprocidade e as formas como o interesse se transforma em relação.",
"Relações humanas":"Conexões, conflitos, limites, acordos e pequenos mecanismos que organizam a convivência.",
"Mente":"Processos mentais usados para perceber, lembrar, decidir, imaginar e interpretar.",
"Sensações":"Experiências corporais e perceptivas que muitas vezes chegam antes da linguagem.",
"Tempo & memória":"Palavras para aquilo que passa, retorna, permanece e muda quando é lembrado.",
"Experiências":"Fenômenos difíceis de notar até que uma palavra nos ensine onde procurar.",
"Palavras raras":"Vocabulário menos comum, incluindo adjetivos e termos cujo uso preciso merece um pouco mais de atenção.",
"Identidade & pertencimento":"As palavras usadas quando a pergunta é quem somos, de onde viemos e onde cabemos.",
"Comportamentos":"Verbos e conceitos que descrevem padrões de ação, reação, escolha e hábito.",
"Pensamentos":"Ferramentas e fenômenos do pensamento, da inferência à imaginação e à decisão.",
"Conceitos difíceis":"Ideias que resistem a explicações simples e costumam exigir mais de uma perspectiva.",
"Lugar & atmosfera":"Palavras para espaços, ambientes e as sensações sociais ou sensoriais que eles produzem.",
"Leitura & linguagem":"Como palavras produzem sentido, inclusive quando não dizem tudo diretamente.",
"Vida cotidiana":"Pequenos conceitos da rotina, do conforto, do atraso, da pressa e do hábito.",
"Filosofia da vida":"Perguntas sobre liberdade, finitude, propósito, responsabilidade e maneiras de viver.",
"Afetos sociais":"Sentimentos e avaliações que surgem na presença, no julgamento e no reconhecimento dos outros.",
}


# Large second layer: descriptive concepts. These are intentionally marked as
# "conceito descritivo" rather than pretending every collocation is a fixed
# dictionary lemma. They broaden discovery without replacing the curated core.
SUPPLEMENTAL = {
"Sentimentos": {
"bases": ["alegria","tristeza","medo","culpa","vergonha","orgulho","raiva","ternura","esperança","alívio","frustração","gratidão","inveja","admiração","solidariedade"],
"mods": ["discreta","repentina","persistente","difusa","contida","intensa","ambígua","recorrente","silenciosa","compartilhada","tardia","contraditória"],
"extra": "calma possível"
},
"Amor & atração": {
"bases": ["atração","desejo","paixão","afeição","intimidade","cuidado","admiração","reciprocidade","ciúme","flertes","proximidade","distância","encanto","curiosidade","vínculo"],
"mods": ["inicial","recíproca","não declarada","gradual","intensa","casual","duradoura","frágil","madura","ambivalente","idealizada","correspondida"],
"extra": "afeição cotidiana"
},
"Relações humanas": {
"bases": ["amizade","confiança","conflito","acordo","desacordo","limite","respeito","lealdade","dependência","autonomia","cuidado","distanciamento","reconciliação","convivência","proximidade"],
"mods": ["silenciosa","explícita","recente","antiga","recíproca","assimétrica","gradual","inesperada","delicada","tensa","duradoura","provisória"],
"extra": "confiança negociada"
},
"Mente": {
"bases": ["atenção","memória","imaginação","concentração","percepção","intuição","dúvida","certeza","curiosidade","raciocínio","aprendizado","esquecimento","associação","reação","consciência"],
"mods": ["seletiva","dispersa","sustentada","automática","deliberada","intuitiva","parcial","retrospectiva","prospectiva","involuntária","metódica","instável"],
"extra": "atenção flutuante"
},
"Sensações": {
"bases": ["calor","frio","peso","leveza","pressão","formigamento","ardor","coceira","vertigem","tensão","relaxamento","náusea","fadiga","vibração","textura"],
"mods": ["localizado","difuso","sutil","súbito","persistente","intermitente","profundo","superficial","agradável","incômodo","estranho","familiar"],
"extra": "sensação residual"
},
"Tempo & memória": {
"bases": ["lembrança","esquecimento","passado","presente","futuro","intervalo","duração","instante","espera","retorno","mudança","repetição","envelhecimento","antecipação","nostalgia"],
"mods": ["afetiva","fragmentária","recente","distante","lenta","acelerada","cíclica","imprecisa","vívida","tardia","involuntária","reconstruída"],
"extra": "memória prospectiva"
},
"Experiências": {
"bases": ["descoberta","fracasso","sucesso","surpresa","encontro","perda","mudança","viagem","silêncio","novidade","recomeço","despedida","adaptação","improviso","revelação"],
"mods": ["inesperada","marcante","breve","transformadora","cotidiana","coletiva","solitária","difícil","agradável","contraditória","memorável","passageira"],
"extra": "experiência liminar"
},
"Palavras raras": {
"bases": ["inefável","ubiquidade","idiossincrasia","procrastinação","serendipidade","liminaridade","efemeridade","impermanência","saudosismo","sobressalto","circunspecção","comiseração","parcimônia","entreato","inexorável"],
"mods": ["semântico","cotidiano","literário","filosófico","psicológico","social","afetivo","temporário","metafórico","figurativo","preciso","especializado"],
"extra": "vocábulo arcaizante"
},
"Identidade & pertencimento": {
"bases": ["identidade","pertencimento","origem","nome","memória","comunidade","família","território","cultura","linguagem","herança","autonomia","alteridade","reconhecimento","diferença"],
"mods": ["pessoal","coletiva","cultural","familiar","territorial","linguística","negociada","múltipla","fluida","histórica","social","ambivalente"],
"extra": "identidade situacional"
},
"Comportamentos": {
"bases": ["hábito","hesitação","fuga","aproximação","repetição","improviso","evitação","persistência","adiamento","iniciativa","recuo","imitação","resistência","cooperação","confronto"],
"mods": ["automático","deliberado","recorrente","ocasional","defensivo","impulsivo","estratégico","social","silencioso","visível","aprendido","adaptativo"],
"extra": "comportamento reativo"
},
"Pensamentos": {
"bases": ["ideia","hipótese","opinião","lembrança","fantasia","pergunta","conclusão","comparação","analogia","previsão","interpretação","julgamento","decisão","possibilidade","contradição"],
"mods": ["provisória","recorrente","intuitiva","deliberada","incompleta","complexa","simplificada","retrospectiva","prospectiva","incômoda","surpreendente","resistente"],
"extra": "pensamento contrafactual"
},
"Conceitos difíceis": {
"bases": ["paradoxo","ambiguidade","causalidade","identidade","liberdade","necessidade","consciência","verdade","realidade","responsabilidade","finitude","incerteza","continuidade","diferença","possibilidade"],
"mods": ["aparente","profunda","relacional","temporal","lógica","moral","social","subjetiva","objetiva","provisória","inesgotável","controversa"],
"extra": "causalidade múltipla"
},
"Lugar & atmosfera": {
"bases": ["ambiente","praça","rua","casa","quarto","corredor","janela","esquina","praia","floresta","cidade","bairro","interior","exterior","paisagem"],
"mods": ["silencioso","movimentado","acolhedor","hostil","vazio","familiar","estranho","luminoso","sombrio","aberto","fechado","transitório"],
"extra": "atmosfera doméstica"
},
"Leitura & linguagem": {
"bases": ["palavra","frase","voz","texto","metáfora","ironia","subtexto","silêncio","ritmo","ênfase","narrativa","diálogo","imagem","significado","nuance"],
"mods": ["literal","figurativo","implícito","explícito","coloquial","formal","poético","técnico","ambíguo","subjetivo","narrativo","contextual"],
"extra": "sentido implícito"
},
"Vida cotidiana": {
"bases": ["rotina","pressa","atraso","descanso","trabalho","estudo","comida","casa","compras","fila","trânsito","mensagem","encontro","tarefa","pausa"],
"mods": ["matinal","noturna","doméstica","social","repetitiva","inesperada","silenciosa","barulhenta","urgente","adiada","compartilhada","solitária"],
"extra": "ritual cotidiano"
},
"Filosofia da vida": {
"bases": ["liberdade","finitude","propósito","escolha","responsabilidade","felicidade","virtude","sofrimento","esperança","absurdo","sentido","mudança","tempo","morte","vida"],
"mods": ["existencial","moral","prática","coletiva","individual","histórica","provisória","radical","cotidiana","trágica","serena","contraditória"],
"extra": "sentido construído"
},
"Afetos sociais": {
"bases": ["acolhimento","rejeição","validação","aprovação","crítica","elogio","encorajamento","vergonha","admiração","reconhecimento","pressão","solidariedade","confiança","desconfiança","respeito"],
"mods": ["público","privado","explícito","implícito","recente","antigo","coletivo","individual","sincero","performático","espontâneo","institucional"],
"extra": "reconhecimento mútuo"
},
}

ORDER = list(CATS)

def slug(text):
    import unicodedata, re
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-'))

# Add a small set of clearly marked contemporary/foreign forms not used above,
# then generate navigation connections from the curated corpus.
entries=[]
seen={}

# Expand the catalog with compositional concepts. The core remains fully curated;
# these additional entries are explicitly labeled so users can distinguish them
# from fixed lemmas and established foreign terms.
for ci, cat in enumerate(ORDER):
    for wi,(word,typ,definition,recognition) in enumerate(CATS[cat]):
        base=slug(word)
        eid=base
        if eid in seen:
            eid=f"{base}-{ci+1}"
        seen[eid]=word
        entries.append({
            'id':eid,'word':word,'type':typ,'category':cat,
            'definition':definition,'recognition':recognition,
            'related':[],'contrasts':[],
            'termKind':'termo estrangeiro' if 'termo estrangeiro' in typ else ('termo contemporâneo' if word in {'crush','reframing'} else 'termo do português')
        })


# 180 concepts per category + one extra, for 3,077 additions.
def concept_slug(text):
    text=unicodedata.normalize('NFD', text)
    text=''.join(c for c in text if unicodedata.category(c)!='Mn')
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-'))

def concept_definition(base, mod, cat, variant):
    patterns=[
        f"Uma forma mais específica de observar {base}: aqui ele aparece de maneira {mod}, ganhando um contorno que pode passar despercebido quando se usa o termo sozinho.",
        f"Conceito descritivo usado para falar de {base} quando a experiência é {mod}; a expressão ajuda a nomear a característica sem tratá-la como um fenômeno separado.",
        f"Variação de {base} marcada por um aspecto {mod}. É útil quando o contexto mostra que não basta dizer apenas {base} para explicar o que aconteceu.",
        f"Expressão que recorta {base} por sua qualidade {mod}. O sentido depende do contexto, mas a combinação aponta para uma experiência reconhecível e relativamente específica.",
    ]
    return patterns[variant % len(patterns)]

def concept_recognition(base, mod, cat, variant):
    patterns=[
        f"Você reconhece quando {base} está presente, mas assume uma forma claramente {mod}; algum detalhe da situação faz essa nuance se destacar.",
        f"Costuma aparecer quando você percebe {base} e, ao mesmo tempo, nota um caráter {mod} na maneira como isso acontece.",
        f"A pista está menos no nome do fenômeno e mais no modo como ele se manifesta: {base}, porém com uma qualidade {mod}.",
    ]
    return patterns[variant % len(patterns)]

supp_count=0
for ci,cat in enumerate(ORDER):
    cfg=SUPPLEMENTAL[cat]
    for bi,base in enumerate(cfg['bases']):
        for mi,mod in enumerate(cfg['mods']):
            word=f"{base} {mod}"
            eid=concept_slug(word)
            # Keep the human-facing concept unique even when a compound repeats.
            if eid in seen:
                eid=f"{eid}-{ci+1}"
            seen[eid]=word
            entries.append({
                'id':eid,
                'word':word,
                'type':'locução nominal',
                'category':cat,
                'definition':concept_definition(base,mod,cat,bi+mi),
                'recognition':concept_recognition(base,mod,cat,bi+mi),
                'related':[],
                'contrasts':[],
                'termKind':'conceito descritivo'
            })
            supp_count += 1
    extra=cfg['extra']
    eid=concept_slug(extra)
    if eid in seen: eid=f"{eid}-{ci+1}"
    seen[eid]=extra
    entries.append({
        'id':eid,'word':extra,'type':'locução nominal','category':cat,
        'definition':f"Expressão conceitual usada para recortar uma experiência específica relacionada à categoria {cat.lower()}; o termo ganha sentido pelo contexto em que aparece.",
        'recognition':f"Você percebe esse conceito quando a situação apresenta uma combinação reconhecível de fatores que não cabe tão bem em uma palavra mais ampla.",
        'related':[],'contrasts':[],'termKind':'conceito descritivo'
    })
print('supplemental added', supp_count+len(ORDER))

by_cat={cat:[e for e in entries if e['category']==cat] for cat in ORDER}
# Contextual, not random, links: same category neighbors + cross-category anchors.
anchors={
 'saudade':['nostalgia','lembranca','anseio','efemeridade'],
 'nostalgia':['saudade','memoria-afetiva','saudosismo','lembranca'],
 'ambivalencia':['dissonancia','hesitacao','nuance','incerteza'],
 'vulnerabilidade-afetiva':['intimidade','reciprocidade','confianca','consentimento'],
 'epifania':['insight','compreensao','perplexidade'],
 'pertencimento':['identidade','comunidade','acolhimento','exclusao'],
 'impermanencia':['efemeridade','transitoriedade','finitude','passagem'],
 'serendipidade':['curiosidade','improviso','epifania','descoberta'],
 'subtexto':['insinuacao','ironia','ambiguidade','conotacao'],
 'limiar':['liminaridade','fronteira','passagem','intervalo'],
 'resiliencia':['adversidade','aceitacao','flexibilidade','equanimidade'],
}
for cat in ORDER:
    arr=by_cat[cat]
    for i,e in enumerate(arr):
        rel=[]
        if i>0: rel.append(arr[i-1]['id'])
        if i+1<len(arr): rel.append(arr[i+1]['id'])
        if i+3<len(arr): rel.append(arr[i+3]['id'])
        e['related']=list(dict.fromkeys(rel))[:4]
        if i+5<len(arr): e['contrasts']=[arr[i+5]['id']]
for e in entries:
    if e['id'] in anchors:
        e['related']=[slug(x) for x in anchors[e['id']] if slug(x) in seen][:4]
# Fix a few cross-category aliases that can be linked.
lookup_by_word={e['word'].lower():e['id'] for e in entries}
for e in entries:
    e['related'] += [lookup_by_word[w.lower()] for w in ['saudade','tempo','memória','intimidade','identidade'] if w.lower() in lookup_by_word and lookup_by_word[w.lower()] != e['id']]
    e['related']=list(dict.fromkeys(e['related']))[:5]
    e['contrasts']=list(dict.fromkeys(e['contrasts']))[:2]

meta={cat:{'index':i,'description':META[cat]} for i,cat in enumerate(ORDER)}
js='''// Curated catalog for Dicionário.\n// Add entries to CATALOG to grow the site without changing the interface.\nconst CATEGORY_ORDER = %s;\nconst CATEGORY_META = %s;\nconst DICTIONARY = %s;\nconst ENTRY_MAP = new Map(DICTIONARY.map(entry => [entry.id, entry]));\nconst CATEGORY_CATALOGS = Object.fromEntries(CATEGORY_ORDER.map(category => [category, DICTIONARY.filter(e => e.category === category).map(e => e.word)]));\nif (typeof window !== 'undefined') {\n  window.DICTIONARY = DICTIONARY; window.ENTRY_MAP = ENTRY_MAP;\n  window.CATEGORY_ORDER = CATEGORY_ORDER; window.CATEGORY_META = CATEGORY_META; window.CATEGORY_CATALOGS = CATEGORY_CATALOGS;\n}\n''' % (json.dumps(ORDER,ensure_ascii=False), json.dumps(meta,ensure_ascii=False), json.dumps(entries,ensure_ascii=False, separators=(',',':')))
Path(__file__).with_name('data.js').write_text(js,encoding='utf-8')
print('total',len(entries))
print('categories', {k:len(v) for k,v in by_cat.items()})
print('types', {t:sum(1 for e in entries if e['type'].startswith(t)) for t in ['substantivo','adjetivo','verbo','locução']})
