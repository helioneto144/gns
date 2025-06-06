# gnS (Genius) - Diretório de Membros

Uma aplicação web bonita e funcional para servir como diretório de membros do gnS (Genius), facilitando a identificação de quem é quem tanto no jogo quanto no WhatsApp.

## Funcionalidades

- ✅ **Cadastro de Membros** com informações essenciais
- ✅ **Upload de Fotos** (armazenamento local, não URLs)
- ✅ **Diretório Visual** com galeria de membros
- ✅ **Interface Responsiva** em Português
- ✅ **Integração WhatsApp** para contato direto
- ✅ **Busca e Filtros** para encontrar membros
- ✅ **Design Moderno** com animações suaves

## Informações Coletadas

### Obrigatórias
- **Nome** - Nome completo do membro
- **Nome do Comandante** - Nome de usuário no jogo (único)

### Opcionais
- **Foto** - Foto de perfil (JPG, PNG, GIF, WEBP - máx. 16MB)
- **Telefone** - Número para contato via WhatsApp

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Upload**: Pillow para processamento de imagens
- **Styling**: CSS customizado com gradientes e animações

## Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

Execute o script SQL no Supabase:

```sql
-- Copie e execute o conteúdo de supabase_schema.sql
```

### 3. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## Estrutura do Projeto

```
gns/
├── app.py                 # Aplicação Flask principal
├── config.py              # Configurações
├── database.py            # Operações do banco de dados
├── requirements.txt       # Dependências Python
├── supabase_schema.sql    # Schema do banco de dados
├── .env                   # Variáveis de ambiente
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página de cadastro
│   └── directory.html    # Diretório de membros
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos customizados
│   ├── js/
│   │   └── main.js       # JavaScript principal
│   └── uploads/          # Fotos dos membros
└── README.md             # Este arquivo
```

## Configuração do Supabase

1. Acesse o [Supabase](https://supabase.com)
2. Crie um novo projeto ou use o existente
3. Execute o script `supabase_schema.sql` no SQL Editor
4. As credenciais já estão configuradas em `config.py`

## Deployment

### Para GitHub Pages (Estático)

Como esta é uma aplicação Flask (dinâmica), ela não pode ser hospedada diretamente no GitHub Pages. Para deployment, considere:

1. **Heroku** (Recomendado)
2. **Vercel**
3. **Railway**
4. **PythonAnywhere**

### Preparação para Deploy

1. Configure as variáveis de ambiente no serviço escolhido
2. Certifique-se de que `gunicorn` está nas dependências
3. Configure o arquivo `Procfile` se necessário

## Uso

### Cadastro
1. Acesse a página inicial
2. Preencha o formulário com suas informações
3. Faça upload de uma foto (opcional)
4. Clique em "Cadastrar-se"
5. Será redirecionado automaticamente para o diretório

### Diretório
- Visualize todos os membros cadastrados
- Use a busca para encontrar membros específicos
- Filtre por membros com foto ou WhatsApp
- Clique no botão WhatsApp para contato direto

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é de uso interno do gnS (Genius).

## Suporte

Para dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.
