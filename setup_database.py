#!/usr/bin/env python3
"""
Setup completo do banco de dados Supabase
"""

import requests
import json

# Configurações diretas
SUPABASE_URL = "https://orupwiygpnzibophlwpe.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ydXB3aXlncG56aWJvcGhsd3BlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTE2ODk0MiwiZXhwIjoyMDY0NzQ0OTQyfQ.if3LMxtMx5apkX5PVcUKUihCk8XmiBD9hoUQVvmMnW8"

def execute_sql(sql_command):
    """Executa comando SQL no Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/query"
    
    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {"query": sql_command}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

def create_members_table():
    """Cria a tabela members"""
    print("📝 Criando tabela 'members'...")
    
    sql = """
    CREATE TABLE IF NOT EXISTS members (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        commander_name VARCHAR(255) NOT NULL UNIQUE,
        phone VARCHAR(20),
        photo_filename VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    status, response = execute_sql(sql)
    if status in [200, 201]:
        print("✅ Tabela 'members' criada!")
        return True
    else:
        print(f"❌ Erro ao criar tabela: {status} - {response}")
        return False

def create_indexes():
    """Cria índices"""
    print("📝 Criando índices...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_members_commander_name ON members(commander_name);",
        "CREATE INDEX IF NOT EXISTS idx_members_created_at ON members(created_at);"
    ]
    
    for sql in indexes:
        status, response = execute_sql(sql)
        if status in [200, 201]:
            print("✅ Índice criado!")
        else:
            print(f"⚠️ Índice: {status} - {response}")

def setup_rls():
    """Configura Row Level Security"""
    print("📝 Configurando RLS...")
    
    rls_commands = [
        "ALTER TABLE members ENABLE ROW LEVEL SECURITY;",
        """CREATE POLICY IF NOT EXISTS "Allow all operations" ON members FOR ALL USING (true);"""
    ]
    
    for sql in rls_commands:
        status, response = execute_sql(sql)
        if status in [200, 201]:
            print("✅ RLS configurado!")
        else:
            print(f"⚠️ RLS: {status} - {response}")

def create_trigger():
    """Cria trigger para updated_at"""
    print("📝 Criando trigger...")
    
    trigger_sql = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    
    DROP TRIGGER IF EXISTS update_members_updated_at ON members;
    CREATE TRIGGER update_members_updated_at 
        BEFORE UPDATE ON members 
        FOR EACH ROW 
        EXECUTE FUNCTION update_updated_at_column();
    """
    
    status, response = execute_sql(trigger_sql)
    if status in [200, 201]:
        print("✅ Trigger criado!")
    else:
        print(f"⚠️ Trigger: {status} - {response}")

def test_table():
    """Testa se a tabela está funcionando"""
    print("🧪 Testando tabela...")
    
    url = f"{SUPABASE_URL}/rest/v1/members?select=*&limit=1"
    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tabela funcionando! Registros: {len(data)}")
            return True
        else:
            print(f"❌ Erro no teste: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

def create_sample_data():
    """Cria dados de exemplo"""
    print("📝 Criando dados de exemplo...")
    
    sample_data = [
        {
            "name": "João Silva",
            "commander_name": "JoaoCommander", 
            "phone": "(11) 99999-1234"
        },
        {
            "name": "Maria Santos",
            "commander_name": "MariaBattler",
            "phone": "(21) 98888-5678"
        },
        {
            "name": "Pedro Oliveira", 
            "commander_name": "PedroWarrior",
            "phone": None
        }
    ]
    
    url = f"{SUPABASE_URL}/rest/v1/members"
    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    created = 0
    for member in sample_data:
        try:
            response = requests.post(url, headers=headers, json=member, timeout=10)
            if response.status_code in [200, 201]:
                print(f"✅ Criado: {member['name']}")
                created += 1
            else:
                print(f"⚠️ {member['name']}: {response.status_code}")
        except Exception as e:
            print(f"❌ {member['name']}: {str(e)}")
    
    print(f"📊 Criados: {created}/{len(sample_data)} membros")
    return created > 0

def main():
    """Função principal"""
    print("🚀 CONFIGURANDO SUPABASE PARA gnS (GENIUS)")
    print("=" * 60)
    print(f"🌐 URL: {SUPABASE_URL}")
    print(f"🔑 Service Role Key: {SERVICE_ROLE_KEY[:30]}...")
    print("=" * 60)
    
    steps = [
        ("Criando tabela", create_members_table),
        ("Criando índices", create_indexes), 
        ("Configurando RLS", setup_rls),
        ("Criando trigger", create_trigger),
        ("Testando tabela", test_table),
        ("Criando dados exemplo", create_sample_data)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        try:
            if step_func():
                success_count += 1
        except Exception as e:
            print(f"❌ Erro em '{step_name}': {str(e)}")
    
    print("\n" + "=" * 60)
    if success_count >= 4:  # Pelo menos tabela, teste e dados
        print("🎉 SUCESSO! Supabase configurado!")
        print("\n✅ Próximos passos:")
        print("1. A aplicação agora usará Supabase automaticamente")
        print("2. Faça deploy no Railway/Render/Heroku")
        print("3. Acesse /admin/login com: admin / gns2025!")
        print("4. Teste o cadastro de novos membros")
    else:
        print("❌ FALHA na configuração!")
        print(f"Sucessos: {success_count}/{len(steps)}")
        print("\n🔧 Tente:")
        print("1. Verificar se o projeto Supabase está ativo")
        print("2. Confirmar a service_role key")
        print("3. Executar o script novamente")

if __name__ == "__main__":
    main()
