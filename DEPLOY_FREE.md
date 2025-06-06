# 🚀 Deploy Gratuito - gnS (Genius)

## 📋 Opções de Hospedagem Gratuita

### 1. **Railway** (Recomendado) ⭐
- ✅ **500 horas/mês grátis**
- ✅ **Deploy automático do GitHub**
- ✅ **Suporte Python/Flask nativo**
- ✅ **Banco PostgreSQL incluído**

#### Como fazer deploy no Railway:
1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório `helioneto144/gns`
5. Configure as variáveis de ambiente:
   ```
   SECRET_KEY=sua-chave-secreta-forte
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=sua-senha-forte
   FLASK_ENV=production
   ```
6. Deploy automático! 🎉

### 2. **Render** (Alternativa)
- ✅ **750 horas/mês grátis**
- ✅ **Deploy automático**
- ✅ **SSL gratuito**

#### Como fazer deploy no Render:
1. Acesse [render.com](https://render.com)
2. Conecte com GitHub
3. "New" → "Web Service"
4. Conecte o repositório `helioneto144/gns`
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Adicione variáveis de ambiente
7. Deploy! 🚀

### 3. **Vercel** (Para Frontend + Serverless)
- ✅ **Ilimitado para projetos pessoais**
- ✅ **Deploy instantâneo**
- ⚠️ **Requer adaptação para serverless**

### 4. **Heroku** (Limitado)
- ⚠️ **550 horas/mês grátis**
- ✅ **Muito fácil de usar**
- ⚠️ **Dorme após 30min sem uso**

## 🗄️ Banco de Dados Gratuito

### **Supabase** (Recomendado)
1. Acesse [supabase.com](https://supabase.com)
2. Crie conta gratuita
3. "New Project"
4. Anote a **URL** e **API Key**
5. Vá em "SQL Editor"
6. Execute o script do arquivo `supabase_schema.sql`

### Configuração no Deploy:
```bash
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-aqui
```

## 🔧 Configuração Rápida

### **Variáveis de Ambiente Essenciais:**
```bash
# Segurança (OBRIGATÓRIO)
SECRET_KEY=gns-2025-super-secret-key-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=MinhaSenh@Forte123!

# Banco de Dados (Supabase)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Flask
FLASK_ENV=production
```

## 🎯 Deploy em 5 Minutos

### **Opção 1: Railway (Mais Fácil)**
1. ✅ Código já está no GitHub
2. ✅ Acesse railway.app
3. ✅ "Deploy from GitHub" → selecione `helioneto144/gns`
4. ✅ Adicione as variáveis de ambiente
5. ✅ Pronto! URL automática gerada

### **Opção 2: Render**
1. ✅ Acesse render.com
2. ✅ "New Web Service" → GitHub → `helioneto144/gns`
3. ✅ Build: `pip install -r requirements.txt`
4. ✅ Start: `gunicorn app:app`
5. ✅ Adicione variáveis de ambiente
6. ✅ Deploy automático!

## 📱 Funcionalidades Garantidas

### ✅ **Sem Supabase (Modo Desenvolvimento)**
- Funciona com JSON local
- Todas as funcionalidades ativas
- Admin protegido
- Upload de fotos
- Busca e filtros

### ✅ **Com Supabase (Modo Produção)**
- Banco PostgreSQL robusto
- Escalabilidade automática
- Backup automático
- Performance otimizada

## 🔒 Segurança

### **Credenciais Padrão (ALTERE!):**
- **Usuário**: admin
- **Senha**: gns2025!

### **Para Produção:**
```bash
ADMIN_USERNAME=seu_usuario_admin
ADMIN_PASSWORD=SuaSenhaForte123!@#
```

## 🌐 URLs de Acesso

Após o deploy, você terá:
- **App Principal**: `https://seu-app.railway.app`
- **Cadastro**: `https://seu-app.railway.app/`
- **Diretório**: `https://seu-app.railway.app/directory`
- **Admin**: `https://seu-app.railway.app/admin/login`
- **Busca**: `https://seu-app.railway.app/search`

## 🆘 Troubleshooting

### **Erro de Build:**
```bash
# Certifique-se que requirements.txt está correto
pip install -r requirements.txt
```

### **Erro de Variáveis:**
- Verifique se todas as variáveis estão configuradas
- SECRET_KEY é obrigatória
- ADMIN_PASSWORD deve ser forte

### **Erro de Banco:**
- Se Supabase não funcionar, app usa JSON automaticamente
- Verifique URL e KEY do Supabase

## 📞 Suporte

### **Links Úteis:**
- **Repositório**: https://github.com/helioneto144/gns
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Supabase**: https://supabase.com

### **Documentação:**
- `README.md` - Guia completo
- `production_setup.md` - Setup detalhado
- `FEATURES.md` - Lista de funcionalidades

## 🎉 Resultado Final

Após o deploy você terá:
- ✅ **Aplicação web completa** funcionando
- ✅ **Diretório de membros** com fotos
- ✅ **Sistema de busca** avançado
- ✅ **Painel administrativo** protegido
- ✅ **Backup automático** de dados
- ✅ **Interface responsiva** em português
- ✅ **Integração WhatsApp** direta

**Tudo funcionando 100% gratuito!** 🚀
