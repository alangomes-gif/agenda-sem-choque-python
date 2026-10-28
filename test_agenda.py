import unittest
from agenda import analisar

def evento(nome, inicio, fim):
    return dict(nome=nome, inicio='2026-11-02T'+inicio, fim='2026-11-02T'+fim)

class AgendaTest(unittest.TestCase):
    def test_sobreposicao_parcial(self):
        r=analisar([evento('A','09:00','10:00'),evento('B','09:30','11:00')])
        self.assertEqual(r,[{'eventos':['A','B'],'inicio_conflito':'2026-11-02T09:30','fim_conflito':'2026-11-02T10:00'}])
    def test_limites_encostados(self):
        self.assertEqual(analisar([evento('A','09:00','10:00'),evento('B','10:00','11:00')]),[])
    def test_contencao_e_entrada_fora_de_ordem(self):
        r=analisar([evento('C','10:00','11:00'),evento('B','09:30','10:30'),evento('A','09:00','12:00')])
        self.assertEqual(len(r),3)
    def test_validacao(self):
        for dados in [None,[evento('A','10:00','09:00')],[evento('A','09:00','10:00')]*2,[dict(nome='x',inicio='2026-02-30T09:00',fim='2026-03-01T10:00')]]:
            with self.assertRaises(ValueError): analisar(dados)
    def test_vazio(self): self.assertEqual(analisar([]),[])

if __name__=='__main__': unittest.main()
