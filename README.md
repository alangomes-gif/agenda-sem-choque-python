# Agenda Sem Choque

Ferramenta local para conferir se compromissos se sobrepõem. Exemplo: estudo das 9h às 10h e revisão das 9h30 às 10h30 geram conflito das 9h30 às 10h. Funciona apenas no terminal e não altera calendários.

## Executar
Python 3.10+, sem dependências externas:

```sh
python agenda.py exemplo.json
python -m unittest -v
```

Cada evento precisa de nome único, início e fim em `AAAA-MM-DDTHH:MM`. Use todos os horários no mesmo fuso local. A saída JSON lista pares em conflito e os intervalos exatos. Eventos que apenas encostam (um termina quando outro começa) não conflitam. Datas inválidas e duração nula ou negativa são rejeitadas antes do relatório.

## Limites
Demonstração de portfólio com agenda fictícia. Não conecta a Google Calendar ou Outlook, não envia lembretes, não considera recorrências, deslocamento, fusos ou horário de verão. A verificação é por pares e se destina a agendas pequenas. Não salva nem modifica o arquivo de entrada.
