# MemorySight
MemorySight é uma solução de instrumentação dinâmica baseada em Frida, projetada para extrair segredos diretamente da memória de processos de aplicativos.

Diferente de scanners estáticos que analisam apenas o código-fonte, o MemorySight observa o que o aplicativo está processando agora. Ele caça padrões de dados sensíveis (PII, Credenciais, Infraestrutura) que muitas vezes estão protegidos no disco, mas expostos em texto claro na Heap durante a execução.

# Por que MemorySight?
* Agnóstico a Framework: Funciona com Flutter, React Native, Java/Kotlin Nativo e C++.
* Deep Memory Inspection: Varredura em tempo real de segmentos de memória rw- (leitura/escrita).
* Dashboard Centralizado: Exfiltração automática de achados para uma interface Web limpa (Porta 9526).
* Anti-Spam Logic: Sistema de filtragem integrado para evitar notificações repetidas do mesmo endereço de memória.

## Guia Rápido

1 - Dependências
```bash
pip install frida-tools
```
2 - Dispositivo: Certifique-se de que o frida-server está rodando no celular e visível via USB.

## Execução
1 - Edite o $0.py com o PACKAGE_NAME do seu alvo.

2 - Inicie o motor de busca:
```bash
python3 $0.py
```
3 - Acesse o Dashboard: http://localhost:9526

# Personalização de Busca (scanner.js)
O MemorySight utiliza assinaturas Hex ASCII para localizar dados. Você pode expandir o DICTIONARY para qualquer alvo:

```javascript
const DICTIONARY = {
    "FINANCEIRO": {
        "Cartao_Credito": "34 35 32 31", // Início de cartões (ex: 4521)
        "Saldo_Conta": "22 62 61 6c 61 6e 63 65 22", // "balance"
    },
    "PRIVACIDADE": {
        "Telefone": "28 31 31 29 20 39", // (11) 9...
    }
};
```

# Pendente
* Busca por Regex (Patterns)
* Busca por string direta (UTF-8)

# Warning
Este projeto deve ser utilizado estritamente para testes de invasão autorizados e auditorias de segurança. O autor não se responsabiliza pelo uso indevido da ferramenta em sistemas de terceiros.




