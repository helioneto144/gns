# 🗄️ Configuração do Supabase - gnS (Genius)

## ⚡ Setup Rápido

### 1. **Acesse o Supabase Dashboard**
- URL: https://supabase.com/dashboard
- Faça login e acesse o projeto: `orupwiygpnzibophlwpe`

### 2. **Execute o SQL**
Vá em **SQL Editor** e execute este código:

```sql
-- Criar tabela members
CREATE TABLE IF NOT EXISTS members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    commander_name VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    photo_filename VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_members_commander_name ON members(commander_name);
CREATE INDEX IF NOT EXISTS idx_members_created_at ON members(created_at);

-- Configurar RLS
ALTER TABLE members ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações
CREATE POLICY IF NOT EXISTS "Allow all operations" ON members
    FOR ALL USING (true);

-- Função para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para updated_at
DROP TRIGGER IF EXISTS update_members_updated_at ON members;
CREATE TRIGGER update_members_updated_at 
    BEFORE UPDATE ON members 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Inserir dados de exemplo
INSERT INTO members (name, commander_name, phone) VALUES
('João Silva', 'JoaoCommander', '(11) 99999-1234'),
('Maria Santos', 'MariaBattler', '(21) 98888-5678'),
('Pedro Oliveira', 'PedroWarrior', NULL)
ON CONFLICT (commander_name) DO NOTHING;
```

### 3. **Verificar se funcionou**
Execute esta consulta para testar:

```sql
SELECT * FROM members;
```

Deve retornar os 3 membros de exemplo.

## 🔑 Configuração das Chaves

### **Chaves Configuradas:**
- **URL**: `https://orupwiygpnzibophlwpe.supabase.co`
- **Service Role Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ydXB3aXlncG56aWJvcGhsd3BlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTE2ODk0MiwiZXhwIjoyMDY0NzQ0OTQyfQ.if3LMxtMx5apkX5PVcUKUihCk8XmiBD9hoUQVvmMnW8`

### **Para Deploy:**
Configure estas variáveis de ambiente:

```bash
SUPABASE_URL=https://orupwiygpnzibophlwpe.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ydXB3aXlncG56aWJvcGhsd3BlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTE2ODk0MiwiZXhwIjoyMDY0NzQ0OTQyfQ.if3LMxtMx5apkX5PVcUKUihCk8XmiBD9hoUQVvmMnW8
```

## 🚀 Como a Aplicação Funciona

### **Modo Automático:**
1. **Com Supabase**: Se as variáveis estão configuradas, usa PostgreSQL
2. **Sem Supabase**: Automaticamente usa JSON local como fallback

### **Desenvolvimento Local:**
```bash
# Sem configurar Supabase
python app.py
# ✅ Funciona com JSON local

# Com Supabase configurado
export SUPABASE_URL=https://orupwiygpnzibophlwpe.supabase.co
export SUPABASE_KEY=sua-chave
python app.py
# ✅ Funciona com PostgreSQL
```

### **Deploy em Produção:**
1. Configure as variáveis de ambiente no Railway/Render
2. A aplicação detecta automaticamente e usa Supabase
3. Todas as funcionalidades ficam disponíveis

## ✅ Funcionalidades Garantidas

### **Com ou Sem Supabase:**
- ✅ Cadastro de membros
- ✅ Upload de fotos
- ✅ Diretório visual
- ✅ Busca avançada
- ✅ Painel admin protegido
- ✅ Sistema de backup
- ✅ Integração WhatsApp

### **Vantagens do Supabase:**
- 🚀 Performance superior
- 📊 Escalabilidade automática
- 💾 Backup automático
- 🔄 Sincronização em tempo real
- 📈 Analytics integrado

## 🔧 Troubleshooting

### **Se o Supabase não funcionar:**
- A aplicação automaticamente usa JSON local
- Todas as funcionalidades continuam funcionando
- Você pode configurar o Supabase depois

### **Para forçar uso do JSON:**
```bash
# Não configure as variáveis SUPABASE_*
python app.py
# Sempre usará JSON local
```

### **Para testar Supabase:**
```bash
# Configure as variáveis
export SUPABASE_URL=https://orupwiygpnzibophlwpe.supabase.co
export SUPABASE_KEY=sua-chave
python app.py
# Logs mostrarão "Connected to Supabase database"
```

## 📋 Checklist de Setup

- [ ] Acessar dashboard do Supabase
- [ ] Executar SQL no SQL Editor
- [ ] Verificar se tabela foi criada
- [ ] Testar consulta SELECT
- [ ] Configurar variáveis no deploy
- [ ] Testar aplicação em produção

## 🎯 Resultado Final

Após configurar o Supabase:
- ✅ **Banco PostgreSQL** robusto e escalável
- ✅ **Backup automático** pelo Supabase
- ✅ **Performance otimizada** para produção
- ✅ **Fallback automático** para JSON se necessário
- ✅ **Deploy garantido** em qualquer plataforma

**A aplicação funciona 100% com ou sem Supabase!** 🎉
