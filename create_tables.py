#!/usr/bin/env python3
"""
Script para criar tabelas no Supabase via API
"""

import requests
import json
from config import Config

def create_tables():
    """Cria as tabelas necessárias no Supabase"""
    
    # SQL para criar a tabela members
    sql_commands = [
        """
        CREATE TABLE IF NOT EXISTS members (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            commander_name VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(20),
            photo_filename VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_members_commander_name ON members(commander_name);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_members_created_at ON members(created_at);
        """,
        """
        ALTER TABLE members ENABLE ROW LEVEL SECURITY;
        """,
        """
        CREATE POLICY IF NOT EXISTS "Allow all operations for anonymous users" ON members
            FOR ALL USING (true);
        """,
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """,
        """
        DROP TRIGGER IF EXISTS update_members_updated_at ON members;
        CREATE TRIGGER update_members_updated_at 
            BEFORE UPDATE ON members 
            FOR EACH ROW 
            EXECUTE FUNCTION update_updated_at_column();
        """
    ]
    
    print("🔧 Criando tabelas no Supabase...")
    print(f"🌐 URL: {Config.SUPABASE_URL}")
    print("-" * 50)
    
    # URL para executar SQL no Supabase
    url = f"{Config.SUPABASE_URL}/rest/v1/rpc/exec_sql"
    
    headers = {
        "apikey": Config.SUPABASE_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Executar cada comando SQL
    for i, sql in enumerate(sql_commands, 1):
        print(f"📝 Executando comando {i}/{len(sql_commands)}...")
        
        try:
            # Tentar via RPC primeiro
            payload = {"sql": sql.strip()}
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code in [200, 201]:
                print(f"✅ Comando {i} executado com sucesso!")
            else:
                print(f"⚠️ Comando {i} - Status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro no comando {i}: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Testando a tabela criada...")
    
    # Testar se a tabela foi criada
    test_url = f"{Config.SUPABASE_URL}/rest/v1/members?select=*&limit=1"
    test_headers = {
        "apikey": Config.SUPABASE_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_KEY}"
    }
    
    try:
        response = requests.get(test_url, headers=test_headers, timeout=10)
        if response.status_code == 200:
            print("✅ Tabela 'members' criada e acessível!")
            data = response.json()
            print(f"📊 Registros existentes: {len(data)}")
            return True
        else:
            print(f"❌ Erro ao acessar tabela: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar tabela: {str(e)}")
        return False

def create_sample_data():
    """Cria dados de exemplo"""
    print("\n🎯 Criando dados de exemplo...")
    
    sample_members = [
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
    
    url = f"{Config.SUPABASE_URL}/rest/v1/members"
    headers = {
        "apikey": Config.SUPABASE_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    created_count = 0
    for member in sample_members:
        try:
            response = requests.post(url, headers=headers, json=member, timeout=10)
            if response.status_code in [200, 201]:
                print(f"✅ Criado: {member['name']}")
                created_count += 1
            else:
                print(f"⚠️ Erro ao criar {member['name']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao criar {member['name']}: {str(e)}")
    
    print(f"\n📊 Total criado: {created_count}/{len(sample_members)} membros")
    return created_count > 0

def main():
    """Função principal"""
    print("🚀 Configurando Supabase para gnS (Genius)")
    print("=" * 50)
    
    # Criar tabelas
    if create_tables():
        print("\n🎉 Tabelas criadas com sucesso!")
        
        # Criar dados de exemplo
        if create_sample_data():
            print("\n✅ SUCESSO TOTAL!")
            print("\n📋 Próximos passos:")
            print("1. A aplicação agora usará Supabase automaticamente")
            print("2. Faça deploy da aplicação")
            print("3. Acesse o admin em /admin/login")
            print("4. Credenciais: admin / gns2025!")
        else:
            print("\n⚠️ Tabelas criadas, mas erro nos dados de exemplo")
    else:
        print("\n❌ FALHA na criação das tabelas!")
        print("\n🔧 Soluções alternativas:")
        print("1. Acesse https://supabase.com/dashboard")
        print("2. Vá em 'SQL Editor'")
        print("3. Execute o conteúdo do arquivo 'supabase_schema.sql'")

if __name__ == "__main__":
    main()
