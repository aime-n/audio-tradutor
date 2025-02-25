```markdown
# Transcrição e Tradução de Áudio com Streamlit

Esta aplicação permite que o usuário envie um arquivo de áudio em inglês, realize a transcrição completa do áudio utilizando o modelo Whisper e traduza o resultado para o português. Todas as interações na interface são apresentadas em português.

## Recursos

- **Upload de Áudio**: Arraste e solte um arquivo de áudio ou clique para procurar (formatos suportados: WAV, MP3, M4A).
- **Transcrição Completa**: O áudio é dividido em blocos de 30 segundos para garantir a transcrição completa, utilizando configurações aprimoradas (beam search, temperatura zero) para melhorar a precisão.
- **Tradução Automática**: A transcrição em inglês é traduzida automaticamente para o português usando o `googletrans`.
- **Interface em Português**: Todas as mensagens e botões são exibidos em português para facilitar o uso.

## Pré-Requisitos

- **Python 3.7+**
- **Bibliotecas Python**:
  - streamlit
  - whisper
  - librosa
  - numpy
  - googletrans==4.0.0rc1 (ou versão compatível)

> **Observação**: Caso seu áudio não esteja no formato WAV, o `librosa` é utilizado para carregar o arquivo sem depender do `ffmpeg`.

## Instalação

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/aime-n/audio-tradutor.git
   cd audio-tradutor
   ```

2. **Crie e Ative um Ambiente Virtual (Opcional, mas Recomendado):**

   ```bash
   python -m venv venv
   # Ativação no Linux/Mac:
   source venv/bin/activate
   # Ativação no Windows:
   .\venv\Scripts\activate
   ```

3. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração de Chaves (Opcional):**

   Se você estiver utilizando APIs que exigem chave (por exemplo, para o OpenAI), armazene a chave em variáveis de ambiente ou use os "Secrets" do Streamlit Cloud. Certifique-se de não commitar suas chaves sensíveis no repositório.

## Uso

1. **Inicie a Aplicação:**

   ```bash
   streamlit run app.py
   ```

2. **Acesse a Interface:**

   Abra o navegador na URL fornecida pelo Streamlit e siga as instruções:
   - Arraste e solte um arquivo de áudio ou clique para procurar.
   - Aguarde o processamento para visualizar a transcrição em inglês e a tradução para o português.

## Implantação Segura

Para implantar sua aplicação sem expor chaves sensíveis:
- **Variáveis de Ambiente:** Configure suas chaves (ex: `OPENAI_API_KEY`) em variáveis de ambiente.
- **Secrets do Streamlit Cloud:** Utilize a funcionalidade de "Secrets" do Streamlit Cloud para gerenciar suas chaves de forma segura.
- **.env e .gitignore:** Se usar um arquivo `.env`, lembre-se de adicioná-lo ao `.gitignore` para não ser commitado.

## Licença

Este projeto está licenciado sob a licença MIT.

## Contato

Em caso de dúvidas ou sugestões, entre em contato:
- Email: [aime.nobrega@gmail.com](mailto:aime.nobrega@gmail.com)
```