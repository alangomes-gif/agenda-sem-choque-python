"""Detecta sobreposição de compromissos em um JSON local."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def analisar(dados):
    if not isinstance(dados, list):
        raise ValueError('A agenda deve ser uma lista.')
    eventos = []
    ids = set()
    for n, item in enumerate(dados, 1):
        if not isinstance(item, dict):
            raise ValueError(f'Evento {n}: objeto esperado.')
        nome = item.get('nome')
        if not isinstance(nome, str) or not nome.strip() or nome in ids:
            raise ValueError(f'Evento {n}: nome vazio ou repetido.')
        ids.add(nome)
        datas = []
        for campo in ('inicio', 'fim'):
            valor = item.get(campo)
            if not isinstance(valor, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', valor):
                raise ValueError(f'Evento {n}: {campo} deve usar AAAA-MM-DDTHH:MM.')
            try:
                datas.append(datetime.strptime(valor, '%Y-%m-%dT%H:%M'))
            except ValueError:
                raise ValueError(f'Evento {n}: data inválida.') from None
        inicio, fim = datas
        if fim <= inicio:
            raise ValueError(f'Evento {n}: fim deve ser posterior ao início.')
        eventos.append((inicio, fim, nome))
    eventos.sort()
    conflitos = []
    for i, (inicio, fim, nome) in enumerate(eventos):
        for inicio2, fim2, nome2 in eventos[i + 1:]:
            if inicio2 >= fim:
                break
            conflitos.append({'eventos': [nome, nome2],
                              'inicio_conflito': max(inicio, inicio2).isoformat(timespec='minutes'),
                              'fim_conflito': min(fim, fim2).isoformat(timespec='minutes')})
    return conflitos


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('arquivo', type=Path)
    args = p.parse_args()
    try:
        conflitos = analisar(json.loads(args.arquivo.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError) as e:
        p.error(str(e))
    print(json.dumps({'conflitos': conflitos, 'total': len(conflitos)}, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
