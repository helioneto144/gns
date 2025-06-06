# Configuração de Produção - gnS (Genius)

## ⚠️ IMPORTANTE: Configuração de Segurança

### 1. Variáveis de Ambiente Obrigatórias

Antes de fazer deploy, configure estas variáveis de ambiente:

```bash
# Segurança
SECRET_KEY=sua-chave-secreta-super-forte-aqui
ADMIN_USERNAME=seu-usuario-admin
ADMIN_PASSWORD=sua-senha-super-forte

# Supabase (obrigatório para produção)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-do-supabase

# Flask
FLASK_ENV=production
```

### 2. Configuração do Supabase

#### Passo 1: Criar Projeto
1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Anote a URL e a chave da API

#### Passo 2: Executar Schema
Execute este SQL no SQL Editor do Supabase:

```sql
-- Create the members table for gnS (Genius) member directory
CREATE TABLE IF NOT EXISTS members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    commander_name VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    photo_filename VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_members_commander_name ON members(commander_name);
CREATE INDEX IF NOT EXISTS idx_members_created_at ON members(created_at);

-- Enable Row Level Security
ALTER TABLE members ENABLE ROW LEVEL SECURITY;

-- Create policy for public access (ajuste conforme necessário)
CREATE POLICY "Allow all operations for anonymous users" ON members
    FOR ALL USING (true);

-- Create update trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_members_updated_at 
    BEFORE UPDATE ON members 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. Configuração de Deploy

#### Heroku
```bash
# Instalar Heroku CLI
# Criar app
heroku create gns-member-directory

# Configurar variáveis
heroku config:set SECRET_KEY=sua-chave-secreta
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=sua-senha-forte
heroku config:set SUPABASE_URL=https://seu-projeto.supabase.co
heroku config:set SUPABASE_KEY=sua-chave-publica
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

#### Railway
1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente no dashboard
3. Deploy automático

#### Vercel
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Configurar variáveis no dashboard
```

### 4. Segurança em Produção

#### Credenciais de Admin
- **NUNCA** use as credenciais padrão em produção
- Use senhas fortes (mínimo 12 caracteres)
- Considere usar 2FA se disponível

#### Exemplo de credenciais seguras:
```bash
ADMIN_USERNAME=admin_gns_2025
ADMIN_PASSWORD=GnS@2025!SecurePass#123
```

#### Configuração do Supabase
- Configure RLS (Row Level Security) adequadamente
- Limite permissões da chave pública
- Use políticas específicas para diferentes operações

### 5. Funcionalidades por Ambiente

#### Desenvolvimento (JSON)
- ✅ Funciona sem Supabase
- ✅ Dados locais em `members.json`
- ✅ Backup local funcional
- ⚠️ Não escalável

#### Produção (Supabase)
- ✅ Banco de dados PostgreSQL
- ✅ Escalabilidade automática
- ✅ Backup automático do Supabase
- ✅ Performance otimizada
- ✅ Sincronização em tempo real

### 6. Migração de Dados

Se você tem dados no JSON local e quer migrar para Supabase:

```python
# Script de migração (execute localmente)
from database import Database
import json

# Carregar dados do JSON
with open('members.json', 'r') as f:
    json_data = json.load(f)

# Configurar Supabase nas variáveis de ambiente
# Depois executar a migração
db = Database()  # Agora vai usar Supabase

for member in json_data:
    try:
        db.create_member(
            name=member['name'],
            commander_name=member['commander_name'],
            phone=member.get('phone'),
            photo_filename=member.get('photo_filename')
        )
        print(f"Migrated: {member['name']}")
    except Exception as e:
        print(f"Error migrating {member['name']}: {e}")
```

### 7. Monitoramento

#### Logs
- Configure logs centralizados
- Monitore tentativas de login no admin
- Acompanhe erros de banco de dados

#### Backup
- Supabase faz backup automático
- Configure backup adicional se necessário
- Teste restauração periodicamente

### 8. Checklist de Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] Credenciais de admin alteradas
- [ ] Supabase configurado e testado
- [ ] Schema SQL executado
- [ ] Testes locais realizados
- [ ] Deploy realizado
- [ ] Funcionalidades testadas em produção
- [ ] Backup testado
- [ ] Logs configurados

### 9. Troubleshooting

#### Erro de Conexão Supabase
```
Error: Failed to connect to Supabase
```
**Solução:** Verifique SUPABASE_URL e SUPABASE_KEY

#### Erro de Autenticação Admin
```
Error: Admin login failed
```
**Solução:** Verifique ADMIN_USERNAME e ADMIN_PASSWORD

#### Fallback para JSON
Se Supabase falhar, a aplicação automaticamente usa JSON local como fallback.

### 10. Contato

Para problemas de configuração:
- Verifique logs da aplicação
- Teste conexão com Supabase
- Valide variáveis de ambiente
- Consulte documentação do Supabase
