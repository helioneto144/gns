# Guia de Deploy - gnS (Genius) Member Directory

## Opções de Deploy

### 1. Heroku (Recomendado)

#### Pré-requisitos
- Conta no Heroku
- Heroku CLI instalado
- Git configurado

#### Passos para Deploy

1. **Preparar o repositório**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Criar aplicação no Heroku**
```bash
heroku create gns-member-directory
```

3. **Configurar variáveis de ambiente**
```bash
heroku config:set SECRET_KEY=sua-chave-secreta-super-segura
heroku config:set FLASK_ENV=production
```

4. **Deploy**
```bash
git push heroku main
```

5. **Abrir aplicação**
```bash
heroku open
```

### 2. Railway

1. Conecte seu repositório GitHub ao Railway
2. Configure as variáveis de ambiente:
   - `SECRET_KEY`: sua chave secreta
   - `FLASK_ENV`: production
3. Deploy automático será feito

### 3. Vercel

1. Instale Vercel CLI: `npm i -g vercel`
2. Execute: `vercel`
3. Configure as variáveis de ambiente no dashboard

### 4. PythonAnywhere

1. Faça upload dos arquivos
2. Configure um Web App Python
3. Configure o WSGI file para apontar para `app:app`

## Configuração do Banco de Dados (Supabase)

### 1. Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Anote a URL e a chave da API

### 2. Executar Schema SQL

1. Vá para SQL Editor no Supabase
2. Execute o conteúdo do arquivo `supabase_schema.sql`

### 3. Configurar Aplicação

1. Atualize `config.py` com suas credenciais do Supabase
2. Ou configure como variáveis de ambiente:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

### 4. Migrar do JSON para Supabase

Para migrar da versão de desenvolvimento (JSON) para produção (Supabase):

1. Descomente as linhas do Supabase em `database.py`
2. Comente as linhas do JSON
3. Teste localmente
4. Faça deploy

## Variáveis de Ambiente Necessárias

```env
SECRET_KEY=sua-chave-secreta-muito-segura
FLASK_ENV=production
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-do-supabase
```

## Checklist Pré-Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados Supabase configurado
- [ ] Schema SQL executado
- [ ] Testes locais realizados
- [ ] .gitignore configurado
- [ ] Arquivos sensíveis não commitados

## Pós-Deploy

1. **Teste todas as funcionalidades**
   - Cadastro de membros
   - Upload de fotos
   - Visualização do diretório
   - Busca e filtros

2. **Configure domínio personalizado** (opcional)

3. **Configure SSL** (geralmente automático)

4. **Monitore logs** para erros

## Troubleshooting

### Erro de Upload de Arquivos
- Verifique se o diretório `static/uploads` existe
- Configure permissões adequadas

### Erro de Banco de Dados
- Verifique credenciais do Supabase
- Confirme que o schema foi executado
- Teste conexão local

### Erro 500
- Verifique logs da aplicação
- Confirme variáveis de ambiente
- Teste localmente primeiro

## Backup

### Dados
- Supabase faz backup automático
- Para backup manual, use a API do Supabase

### Fotos
- Configure backup automático do diretório uploads
- Considere usar storage do Supabase para fotos

## Monitoramento

- Configure alertas no Heroku/Railway
- Monitore uso de recursos
- Acompanhe logs de erro

## Atualizações

1. Teste mudanças localmente
2. Commit e push para repositório
3. Deploy automático (se configurado)
4. Teste em produção
5. Rollback se necessário
